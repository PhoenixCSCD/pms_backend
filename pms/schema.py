import graphene
from authentication.schema import Query as AuthenticationQuery
from core.schema import Query as CoreQuery
from core.schema import Mutation as CoreMutation


class RootQuery(AuthenticationQuery, CoreQuery):
    pass


class RootMutation(CoreMutation):
    pass


schema = graphene.Schema(query=RootQuery, mutation=RootMutation)
