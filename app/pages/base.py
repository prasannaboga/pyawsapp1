from flask import Blueprint


pages = Blueprint('pages', __name__, url_prefix='', template_folder='templates')
