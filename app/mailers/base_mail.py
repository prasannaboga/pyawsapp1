from flask_mail import Mail
from flask import current_app as app

mail = Mail()


class BaseMail(object):

    def __init__(self):
        pass

    def override_to_email(self, to_emails):
        if app.config['OVERRIDE_TO_EMAILS']:
            return app.config['OVERRIDE_TO_EMAILS']
        return to_emails

