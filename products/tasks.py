from celery import shared_task
from time import sleep
from django.core.mail import send_mail

@shared_task
def sleepy(duration):
    sleep(duration)
    return None
@shared_task
def send_email_task():
    sleepy(10)
    send_mail('Celery Task Worked',
    'This is proof the task is worked',
    'ffsdgd.com',
    ['dsfsfsf.com']
    )
    return None
