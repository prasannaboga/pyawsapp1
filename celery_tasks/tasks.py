import time
from .base import celery
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@celery.task(bind=True, queue="apple")
def add_together(self, a, b):
    for i in range(1, 5):
        time.sleep(i)
        logger.warning(i)
        self.update_state(state='PROGRESS', meta={'current': i})
    return a + b


@celery.task()
def default_queue_task(a):
    return a


@celery.task(bind=True, queue="apple")
def long_running(self, **kwargs):
    max_value = kwargs.get('max_value', 10)
    timer_value = kwargs.get('timer_value', 1)
    for i in range(1, max_value):
        logger.info('Current Loop - {}'.format(i))
        time.sleep(i * timer_value)

    return [max_value, timer_value]
