import time
from .base import celery
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@celery.task(bind=True, queue="add")
def add_together(self, a, b):
    for i in range(1, 10):
        time.sleep(i)
        logger.warning(i)
        self.update_state(state='PROGRESS', meta={'current': i})
    return a + b
