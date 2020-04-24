import json

import graphene
import jwt
from django.conf import settings
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.models import Group
from graphene_django.types import DjangoObjectType

from authentication.models import User


class AuthDataType(DjangoObjectType):
    token = graphene.String()

    class Meta:
        model = User
        exclude = ('password',)


class Query(graphene.ObjectType):
    auth_data = graphene.Field(AuthDataType, email=graphene.String(), password=graphene.String())

    @staticmethod
    def resolve_auth_data(root, info, email, password):
        user = authenticate(email=email, password=password)
        if user is None:
            raise Exception('Invalid email or password')
        token = jwt.encode({'id': str(user.id)}, settings.SECRET_KEY)
        user.token = token
        return user
