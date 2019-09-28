import time

from celery import group
from celery import chain
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


@celery.task(bind=True, queue="ball")
def scheduled_task(self, **kwargs):
    time_stamp = kwargs.get('time_stamp')
    logger.info('This scheduled at {}')
    return [time_stamp]


@celery.task(bind=True, queue="cat")
def parent_task(self, **kwargs):
    items_count = kwargs.get('items_count', 5)
    logger.info('items_count = '.format(items_count))
    l = ()
    for i in range(1, items_count+1):
        ct = child_task.s(i)
        l = l + (ct,)
    res = chain(l)()
    return res


@celery.task(bind=True, queue="cat")
def child_task(self, item):
    if not item:
        raise Exception('No item found')
    logger.info('item = {}'.format(item))
    return [item]


@celery.task(bind=True, queue="cat")
def parent_final_task(self, **kwargs):

    return ['i']
