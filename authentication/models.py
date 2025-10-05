from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import pyotp


class User(AbstractUser):
    """Extended User model with 2FA support"""
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    
    # 2FA Fields
    two_factor_enabled = models.BooleanField(default=False)
    two_factor_secret = models.CharField(max_length=32, blank=True, null=True)
    
    # Google OAuth
    google_id = models.CharField(max_length=255, blank=True, null=True, unique=True)
    
    # Login tracking
    login_attempts = models.IntegerField(default=0)
    last_login_attempt = models.DateTimeField(null=True, blank=True)
    account_locked_until = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return self.email
    
    def generate_2fa_secret(self):
        """Generate a new 2FA secret"""
        if not self.two_factor_secret:
            self.two_factor_secret = pyotp.random_base32()
            self.save()
        return self.two_factor_secret
    
    def verify_2fa_token(self, token):
        """Verify 2FA token"""
        if not self.two_factor_enabled or not self.two_factor_secret:
            return False
        totp = pyotp.TOTP(self.two_factor_secret)
        return totp.verify(token, valid_window=1)
    
    def is_account_locked(self):
        """Check if account is currently locked"""
        if self.account_locked_until:
            if timezone.now() < self.account_locked_until:
                return True
            else:
                # Unlock account if lock period has expired
                self.account_locked_until = None
                self.login_attempts = 0
                self.save()
        return False
    
    def increment_login_attempts(self):
        """Increment failed login attempts and lock if needed"""
        self.login_attempts += 1
        self.last_login_attempt = timezone.now()
        
        # Lock account after 3 failed attempts for 30 minutes
        if self.login_attempts >= 3:
            self.account_locked_until = timezone.now() + timezone.timedelta(minutes=30)
        
        self.save()
    
    def reset_login_attempts(self):
        """Reset login attempts after successful login"""
        self.login_attempts = 0
        self.last_login_attempt = None
        self.account_locked_until = None
        self.save()


class LoginHistory(models.Model):
    """Track user login history"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='login_history')
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    login_time = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'login_history'
        verbose_name = 'Login History'
        verbose_name_plural = 'Login Histories'
        ordering = ['-login_time']
    
    def __str__(self):
        return f"{self.user.email} - {self.login_time}"
