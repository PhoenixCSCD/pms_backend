import graphene
import graphql_jwt
from graphene_django.types import DjangoObjectType

from pms.core.models import User


class AuthDataType(DjangoObjectType):
    token = graphene.String()

    class Meta:
        model = User
        exclude = ('password',)


class Query(graphene.ObjectType):
    pass


class Mutation(graphene.ObjectType):
    obtain_token = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    revoke_token = graphql_jwt.Revoke.Field()
