import time

from celery import group
from celery import chain
from .base import celery, BaseTask
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
    items_count = kwargs.get('items_count')
    logger.info('items_count = '.format(items_count))
    child_task.s(items_count, 1).apply_async(countdown=10)
    return [items_count]


@celery.task(bind=True, queue="cat")
def child_task(self, items_count, i):
    logger.info('**i = '.format(i))
    if i >= items_count:
        logger.info('Inside if')
    else:
        j = i + 1
        child_task.s(items_count, j).apply_async(countdown=10)
    return [i]


@celery.task(bind=True, queue="cat")
def parent_final_task(self, **kwargs):
    return ['i']


@celery.task(base=BaseTask, bind=True, queue="cat")
def error_task(self):
    try:
        print(self.request.id)
        raise Exception('I m Exception')
        return self.request.id
    except Exception as ex:
        print(str(ex))
        raise ex


@celery.task(base=BaseTask, bind=True, queue="cat")
def sample_task_one(self):
    try:
        # time.sleep(5)
        logger.info('I m task - {}'.format(self.name))
        return self.request.id
    except Exception as ex:
        print(str(ex))
        raise ex
