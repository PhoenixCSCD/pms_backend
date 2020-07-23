import graphene
import graphql_jwt
from django.contrib.auth.tokens import default_token_generator
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required

from pms.core.models import User
from pms.core.schema import UserType


class AuthDataType(DjangoObjectType):
    token = graphene.String()

    class Meta:
        model = User
        exclude = ('password',)


class ResetPassword(graphene.Mutation):
    class Arguments:
        email = graphene.String()
        token = graphene.String()
        password = graphene.String()

    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, _root, _info, email, token, password):
        user = User.objects.get(email=email)
        if default_token_generator.check_token(user, token):
            user.set_password(password)
            user.save()
        return cls(ok=True)


class Query(graphene.ObjectType):
    me = graphene.Field(UserType)
    has_permission = graphene.Boolean(permission=graphene.String())
    email_exists = graphene.Boolean(email=graphene.String())
    password_reset_token_is_valid = graphene.Boolean(email=graphene.String(), token=graphene.String())

    @staticmethod
    @login_required
    def resolve_me(_root, _info):
        return _info.context.user

    @staticmethod
    @login_required
    def resolve_has_permission(_root, _info, permission):
        return _info.context.user.has_perm(permission)

    @staticmethod
    def resolve_email_exists(_root, _info, email):
        return User.objects.filter(email=email).exists()

    @staticmethod
    def resolve_password_reset_token_is_valid(_root, _info, email, token):
        try:
            user = User.objects.get(email=email)
            return default_token_generator.check_token(user, token)

        except User.DoesNotExist:
            return False


class Mutation(graphene.ObjectType):
    obtain_token = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    revoke_token = graphql_jwt.Revoke.Field()
    reset_password = ResetPassword.Field()
