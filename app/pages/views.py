import time

from flask import current_app as app
from flask import render_template, jsonify, request, g

from .base import pages

from celery_tasks.tasks import long_running


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

    long_running.s(max_value=max_value, timer_value=timer_value).apply_async()

    return jsonify({'max_value': max_value, 'timer_value': timer_value})


@pages.route('/page_one')
def page_one():
    app.logger.info('This is page one')
    return jsonify({'request_time': g.request_time()})


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
