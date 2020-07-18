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


class VerifyPasswordResetToken(graphene.Mutation):
    class Arguments:
        user_id = graphene.UUID(required=True)
        token = graphene.String(required=True)

    valid = graphene.Boolean()

    @staticmethod
    def mutate(_root, _info, user_id, token):
        try:
            user = User.objects.get(id=user_id)
            return VerifyPasswordResetToken(valid=default_token_generator.check_token(user, token))
        except User.DoesNotExist:
            return VerifyPasswordResetToken(valid=False)


class Query(graphene.ObjectType):
    me = graphene.Field(UserType)
    has_permission = graphene.Boolean(permission=graphene.String())
    email_exists = graphene.Boolean(email=graphene.String())

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


class Mutation(graphene.ObjectType):
    obtain_token = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    revoke_token = graphql_jwt.Revoke.Field()
    verify_password_reset_token = VerifyPasswordResetToken.Field()
