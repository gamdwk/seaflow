from celery import Celery

from celeryconfig import broker_url

celery = Celery(__name__, broker=broker_url)


def register_celery(flask_app):
    celery.config_from_object('celeryconfig')

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with flask_app.app_context() as c:
                c.push()
                return self.run(*args, **kwargs)

    celery.Task = ContextTask


from .main import create_app
from config import DevelopmentConfig
app = create_app(DevelopmentConfig)
app.app_context().push()
@celery.task
def send_async_mail(subject, recipients, *args, **kwargs):
    from .helper import send_mail
    send_mail(subject=subject, recipients=recipients, *args, **kwargs)


from .main.exts import api
from .helper import *
from .auth import *
from .error import *
from .main import *
