from flask import Flask

from .pages import pages


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('config')

    app.config['BUNDLE_ERRORS'] = True

    app.register_blueprint(pages)

    return app
