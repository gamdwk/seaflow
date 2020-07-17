from ..main.exts import mail
from flask_mail import Message


def send_mail(subject, recipients, *args, **kwargs):
    message = Message(subject=subject, recipients=recipients, *args, **kwargs)
    mail.send(message)
