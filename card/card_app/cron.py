from .models import OTP
from django.utils import timezone


def my_scheduled_job():
    active_otp = OTP.objects.filter(
        timestamp__lt=timezone.now() - timezone.timedelta(minutes=2),
        is_active=True)
    for at in active_otp:
        at.is_active = False
        at.save()