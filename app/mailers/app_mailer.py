from .base_mail import BaseMail


class AppMailer(BaseMail):

    def __init__(self):
        self.from_email = 'default-from-email'
