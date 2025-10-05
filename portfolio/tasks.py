from celery import shared_task
from django.contrib.auth import get_user_model

User = get_user_model()


@shared_task
def generate_daily_report():
    """Generate daily portfolio report"""
    user_count = User.objects.count()
    
    print(f"Daily Report: Total users: {user_count}")
    
    return f"Daily report generated: {user_count} users"
