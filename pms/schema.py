import graphene


import pms.authentication.schema as authentication_schema
import pms.core.schema as core_schema


class RootQuery(authentication_schema.Query, core_schema.Query):
    pass


class RootMutation(authentication_schema.Mutation, core_schema.Mutation):
    pass


# noinspection PyTypeChecker
schema = graphene.Schema(query=RootQuery, mutation=RootMutation)
