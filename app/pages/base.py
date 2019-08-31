import time

from flask import Blueprint, g
from flask import current_app as app

pages = Blueprint('pages', __name__, url_prefix='', template_folder='templates')


@pages.before_request
def before_request():
    g.request_start_time = time.time()
    g.request_time = lambda: "%.5fs" % (time.time() - g.request_start_time)
