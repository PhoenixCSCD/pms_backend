from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


def send_password_reset_email(user):
    token = default_token_generator.make_token(user)

    print(f'{settings.PASSWORD_RESET_URL}?email={user.email}&token={token}')
    send_mail(
        subject='Account Confirmation',
        message='',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
        html_message=render_to_string('account_created.html', {
            'reset_url': f'{settings.PASSWORD_RESET_URL}?email={user.email}&token={token}'
        })
    )
