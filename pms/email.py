from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


def send_password_reset_email(user):
    domain = 'localhost:8080'
    token = default_token_generator.make_token(user)
    send_mail(
        subject="Account Confirmation",
        message='',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
        html_message=render_to_string('account_created.html', {
            'domain': domain,
            'user_id': user.id,
            'token': token
        })
    )
