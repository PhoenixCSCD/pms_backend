from django.dispatch import receiver
from graphql_jwt.refresh_token.signals import refresh_token_rotated
from graphql_jwt.signals import token_refreshed


@receiver(token_refreshed)
def revoke_refresh_token(_sender, request, refresh_token, **_kwargs):
    refresh_token.revoke(request)
