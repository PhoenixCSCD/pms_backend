from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model


class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        auth = request.headers.get('Authorization')
        if auth is not None:
            prefix = 'Bearer'
            parts = auth.split(' ')

            if len(parts) != 2 or parts[0] != prefix:
                raise Exception("Improperly formed token")

            # request.user = get_user_model().objects.get(id=1)
        else:
            request.user = AnonymousUser()
        return self.get_response(request)
