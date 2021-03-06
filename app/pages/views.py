import random
import time
from multiprocessing import Pool
from multiprocessing import cpu_count

import boto3
from flask import current_app as app
from flask import render_template, jsonify, request, g

from celery_tasks import tasks
from .base import pages


@pages.route('/')
@pages.route('/index')
def index():
    # Testing logging levels
    app.logger.warning('I AM WARNING***')
    app.logger.debug('I AM DEBUG***')
    app.logger.error('I AM ERROR***')
    app.logger.info('I AM INFO***')
    return render_template('index.html')


@pages.route('/trigger_tasks')
def trigger_tasks():
    max_value = request.args.get('max_value', 10, int)
    timer_value = request.args.get('timer_value', 1, int)

    tasks.long_running.s(max_value=max_value, timer_value=timer_value).apply_async()

    return jsonify({'max_value': max_value, 'timer_value': timer_value})


@pages.route('/page_one')
def page_one():
    app.logger.info('This is page one')
    return jsonify({'request_time': g.request_time()})


def f(x):
    return x * x


@pages.route('/page_two')
def page_two():
    app.logger.info('This is page two start')
    processes = cpu_count()
    pool = Pool(1000)
    x = pool.map(f, range(processes))
    app.logger.info('This is page two end')
    return jsonify({'request_time': g.request_time(), 'x': x})


@pages.route('/long_request')
def long_request():
    max_value = request.args.get('max_value', 10, int)
    timer_value = request.args.get('timer_value', 1, int)

    for i in range(1, max_value + 1):
        time.sleep(i * timer_value)
        app.logger.info('Loop - {}'.format(i))

    return jsonify(
        {'max_value': max_value,
         'timer_value': timer_value,
         'request_time': g.request_time()})


@pages.route('/custom-metrics-example1')
def custom_metrics_example1():
    cloudwatch = boto3.client('cloudwatch')
    task_names = ['one', 'two', 'three', 'four']
    task_name = random.choice(task_names)
    metric_data = [
        {
            'MetricName': 'TASKS_COUNT',
            'Dimensions': [
                {
                    'Name': 'task_name',
                    'Value': 'one'
                }
            ],
            'Unit': 'None',
            'Value': int(request.args.get('value', 1))
        },
    ]
    namespace = 'PYAWSAPP1/APPLICATION_TASKS'

    response = cloudwatch.put_metric_data(
        MetricData=metric_data,
        Namespace=namespace
    )

    return jsonify(response)
