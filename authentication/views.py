from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model, authenticate
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .serializers import (
    UserSerializer, RegisterSerializer, LoginSerializer,
    TwoFactorSetupSerializer, TwoFactorVerifySerializer,
    PasswordChangeSerializer
)
from .models import LoginHistory
from .tasks import send_welcome_email, log_login_attempt

User = get_user_model()


def get_client_ip(request):
    """Get client IP address from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class RegisterView(generics.CreateAPIView):
    """User Registration API"""
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer
    
    @swagger_auto_schema(
        operation_description="Register a new user",
        responses={201: UserSerializer, 400: 'Bad Request'}
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Send welcome email asynchronously
        send_welcome_email.delay(user.id)
        
        return Response({
            'user': UserSerializer(user).data,
            'message': 'User registered successfully'
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    """User Login API"""
    permission_classes = (permissions.AllowAny,)
    
    @swagger_auto_schema(
        operation_description="User login",
        request_body=LoginSerializer,
        responses={200: 'Login successful', 400: 'Bad Request', 401: 'Unauthorized'}
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        
        try:
            user = User.objects.get(email=email)
            
            if user.is_account_locked():
                return Response({
                    'error': 'Account temporarily locked. Try again later.'
                }, status=status.HTTP_403_FORBIDDEN)
            
            user_auth = authenticate(request, username=email, password=password)
            
            if user_auth is None:
                user.increment_login_attempts()
                LoginHistory.objects.create(
                    user=user,
                    ip_address=get_client_ip(request),
                    user_agent=request.META.get('HTTP_USER_AGENT', ''),
                    success=False
                )
                log_login_attempt.delay(user.id, False, get_client_ip(request))
                
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
            
            user.reset_login_attempts()
            
            if user.two_factor_enabled:
                return Response({
                    'requires_2fa': True,
                    'user_id': user.id,
                    'message': 'Please provide 2FA token'
                }, status=status.HTTP_200_OK)
            
            refresh = RefreshToken.for_user(user)
            
            LoginHistory.objects.create(
                user=user,
                ip_address=get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                success=True
            )
            
            log_login_attempt.delay(user.id, True, get_client_ip(request))
            user.last_login = timezone.now()
            user.save()
            
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': UserSerializer(user).data,
                'requires_2fa': False
            }, status=status.HTTP_200_OK)
            
        except User.DoesNotExist:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class Setup2FAView(APIView):
    """Setup 2FA API"""
    permission_classes = (permissions.IsAuthenticated,)
    
    @swagger_auto_schema(operation_description="Setup Two-Factor Authentication")
    def get(self, request):
        user = request.user
        serializer = TwoFactorSetupSerializer()
        data = serializer.get_qr_code(user)
        return Response(data, status=status.HTTP_200_OK)


class Verify2FAView(APIView):
    """Verify 2FA Token API"""
    permission_classes = (permissions.AllowAny,)
    
    @swagger_auto_schema(
        operation_description="Verify 2FA token",
        request_body=TwoFactorVerifySerializer
    )
    def post(self, request):
        serializer = TwoFactorVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        token = serializer.validated_data['token']
        user_id = request.data.get('user_id')
        
        if not user_id:
            user = request.user
            if not user.is_authenticated:
                return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
            
            if user.verify_2fa_token(token):
                user.two_factor_enabled = True
                user.save()
                return Response({'message': '2FA enabled successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid 2FA token'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                user = User.objects.get(id=user_id)
                
                if user.verify_2fa_token(token):
                    refresh = RefreshToken.for_user(user)
                    
                    LoginHistory.objects.create(
                        user=user,
                        ip_address=get_client_ip(request),
                        user_agent=request.META.get('HTTP_USER_AGENT', ''),
                        success=True
                    )
                    
                    user.last_login = timezone.now()
                    user.save()
                    
                    return Response({
                        'access': str(refresh.access_token),
                        'refresh': str(refresh),
                        'user': UserSerializer(user).data
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'Invalid 2FA token'}, status=status.HTTP_400_BAD_REQUEST)
                    
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


class Disable2FAView(APIView):
    """Disable 2FA API"""
    permission_classes = (permissions.IsAuthenticated,)
    
    @swagger_auto_schema(operation_description="Disable Two-Factor Authentication")
    def post(self, request):
        user = request.user
        user.two_factor_enabled = False
        user.two_factor_secret = None
        user.save()
        return Response({'message': '2FA disabled successfully'}, status=status.HTTP_200_OK)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """User Profile API"""
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer
    
    def get_object(self):
        return self.request.user


class ChangePasswordView(APIView):
    """Change Password API"""
    permission_classes = (permissions.IsAuthenticated,)
    
    @swagger_auto_schema(
        operation_description="Change password",
        request_body=PasswordChangeSerializer
    )
    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        
        if not user.check_password(serializer.validated_data['old_password']):
            return Response({'error': 'Invalid old password'}, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)


class LogoutView(APIView):
    """Logout API"""
    permission_classes = (permissions.IsAuthenticated,)
    
    @swagger_auto_schema(operation_description="Logout user")
    def post(self, request):
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
