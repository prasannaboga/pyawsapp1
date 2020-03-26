import os
import boto3

from celery.signals import before_task_publish
from celery import Celery, Task
from flask import Flask


def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL'],
        task_track_started=True
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


flask_app = Flask(__name__)
flask_app.config.update(
    CELERY_BROKER_URL=os.environ['CELERY_BROKER_URL'],
    CELERY_RESULT_BACKEND=os.environ['CELERY_RESULT_BACKEND']
)

celery = make_celery(flask_app)
cloudwatch = boto3.client('cloudwatch')


class BaseTask(Task):
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print('On Failure - {}'.format(task_id))


@before_task_publish.connect()
def before_task_publish(**kwargs):
    print('--------------------------')
    # print('I m in before_task_publish')
    print(cloudwatch)
    response = cloudwatch.put_metric_data(
        MetricData=[
            {
                'MetricName': 'TASKS_COUNT',
                'Dimensions': [
                    {
                        'Name': 'task',
                        'Value': 'one'
                    }
                ],
                'Unit': 'None',
                'Value': 1
            },
        ],
        Namespace='CELERY/PYAWSAPP1'
    )
    print(response)
    print('--AFTER RESPONSE--')
