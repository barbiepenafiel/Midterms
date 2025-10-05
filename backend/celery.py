"""
Celery configuration for the backend project.
"""
import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

app = Celery('backend')

# Load configuration from Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks in all installed apps
app.autodiscover_tasks()

# Celery Beat Schedule (for periodic tasks)
app.conf.beat_schedule = {
    'cleanup-expired-sessions': {
        'task': 'authentication.tasks.cleanup_expired_sessions',
        'schedule': crontab(hour=2, minute=0),  # Run daily at 2 AM
    },
    'send-daily-report': {
        'task': 'portfolio.tasks.generate_daily_report',
        'schedule': crontab(hour=8, minute=0),  # Run daily at 8 AM
    },
}

@app.task(bind=True)
def debug_task(self):
    """Debug task for testing Celery"""
    print(f'Request: {self.request!r}')
