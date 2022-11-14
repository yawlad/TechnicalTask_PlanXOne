from config.settings import EMAIL_HOST_USER

from config.celery import app
from .models import User
from django.core.mail import send_mail


@app.task
def statistics_mail_send_task():

    for user in User.objects.all().filter(email__icontains='@', is_superuser=False):
        stats = user.get_statistics()
        send_mail(
            'Your Statistics for previous day',
            f'{stats}',
            f'{EMAIL_HOST_USER}',
            [f'{user.email}'],
            fail_silently=False
        )
