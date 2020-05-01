import graphene
import authentication.schema
import core.schema


class RootQuery(authentication.schema.Query, core.schema.Query):
    pass


class RootMutation(authentication.schema.Mutation, core.schema.Mutation):
    pass


# noinspection PyTypeChecker
schema = graphene.Schema(query=RootQuery, mutation=RootMutation)
