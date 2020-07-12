from celery_app import celery_app
from flask_mail import Message
from seaflow.exts import mail


@celery_app.task
def send_mail(subject, recipients, body):
    message = Message(subject=subject, recipients=recipients, body=body)
    mail.send(message)
