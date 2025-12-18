from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta

def send_weekly_notifications():
    users = User.objects.filter(is_active=True)
    for user in users:
        send_mail(
            'Your Weekly Training Update',
            'Here are your training notes for the week...',
            'from@example.com',
            [user.email],
            fail_silently=False,
        )