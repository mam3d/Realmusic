import random
from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail
from django.dispatch import receiver
from django.template.loader import render_to_string


class Email:
    """ cache code based on user being logged in or not and sends email to specified email"""

    def __init__(self, email, user=None):
        self.email = email
        self.user = user

    def cache(self):
        code = random.randint(100000, 1000000)
        if self.user:
            data = {
                "current":self.user.email,
                "new":self.email,
                "code":code,
            }
            cache.set(self.user, data, 90)
        else:
            cache.set(self.email, code, 90)

        return self.email, self.user, code
                

    def send(self):
        email, user, code = self.cache()

        # if user currently has email,email will be sent to that email
        receiver_email = user.email if user and user.email else email

        html = render_to_string("email.html", {"code":code})    
        send_mail(
            subject = "realmusic email verification",
            message = str(code),
            from_email = settings.EMAIL_HOST_USER,
            recipient_list = [receiver_email],
            html_message = html,
        )
        return receiver_email
