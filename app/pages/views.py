from flask import current_app as app
from flask import render_template

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
