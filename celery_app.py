from celery import Celery
from run import app


def make_celery(flask_app):
    my_celery_app = Celery(
        app.name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    my_celery_app.conf.update(app.config)

    class ContextTask(my_celery_app.Task):
        abstract = True

        def __call__(self, *args, **kwargs):
            with flask_app.app_context():
                return self.run(*args, **kwargs)

    my_celery_app.Task = ContextTask

    return my_celery_app


celery_app = make_celery(app)
