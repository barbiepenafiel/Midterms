from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


@shared_task
def send_welcome_email(user_id):
    """Send welcome email to new user"""
    try:
        user = User.objects.get(id=user_id)
        subject = 'Welcome to Oursfolio Portfolio!'
        message = f"""
        Hi {user.first_name or user.username},
        
        Welcome to Oursfolio Portfolio!
        
        Thank you for registering. We're excited to have you on board.
        
        Best regards,
        The Oursfolio Team
        """
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        
        return f"Welcome email sent to {user.email}"
    except User.DoesNotExist:
        return f"User with id {user_id} does not exist"
    except Exception as e:
        return f"Error sending email: {str(e)}"


@shared_task
def log_login_attempt(user_id, success, ip_address):
    """Log login attempt asynchronously"""
    try:
        user = User.objects.get(id=user_id)
        status = "successful" if success else "failed"
        
        # You can add additional logging here (e.g., to external service)
        print(f"Login attempt for {user.email} from {ip_address}: {status}")
        
        return f"Logged {status} login attempt for user {user.email}"
    except User.DoesNotExist:
        return f"User with id {user_id} does not exist"


@shared_task
def cleanup_expired_sessions():
    """Clean up expired user sessions and locked accounts"""
    from django.utils import timezone
    
    # Unlock accounts where lock period has expired
    unlocked_count = User.objects.filter(
        account_locked_until__lt=timezone.now()
    ).update(
        account_locked_until=None,
        login_attempts=0
    )
    
    return f"Unlocked {unlocked_count} accounts"


@shared_task
def send_security_alert(user_id, alert_type, details):
    """Send security alert to user"""
    try:
        user = User.objects.get(id=user_id)
        
        subject = f'Security Alert: {alert_type}'
        message = f"""
        Hi {user.first_name or user.username},
        
        We detected unusual activity on your account:
        
        {details}
        
        If this wasn't you, please change your password immediately.
        
        Best regards,
        The Oursfolio Team
        """
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        
        return f"Security alert sent to {user.email}"
    except User.DoesNotExist:
        return f"User with id {user_id} does not exist"
    except Exception as e:
        return f"Error sending alert: {str(e)}"
