import requests
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


def _send_email(subject, body, recipient_list, is_html_body=False):
    data = {
               'from': 'PMS <mailgun@sandboxb04b0169e10041ce896d9c8bf84f4406.mailgun.org>',
               'to': recipient_list,
               'subject': subject,
           }
    if is_html_body:
        data['html'] = body
    else:
        data['text'] = body

    return requests.post(
        url="https://api.mailgun.net/v3/sandboxb04b0169e10041ce896d9c8bf84f4406.mailgun.org/messages",
        auth=('api', settings.MAILGUN_API_KEY),
        data=data
    )


def send_password_reset_email(user):
    token = default_token_generator.make_token(user)

    print(f'{settings.PASSWORD_RESET_URL}?email={user.email}&token={token}')
    _send_email(
        subject='Account Confirmation',
        recipient_list=[user.email],
        is_html_body=True,
        body=render_to_string('account_created.html', {
            'reset_url': f'{settings.PASSWORD_RESET_URL}?email={user.email}&token={token}'
        })
    )
