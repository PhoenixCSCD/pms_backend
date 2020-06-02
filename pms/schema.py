import graphene


import pms.authentication.schema as authentication_schema
import pms.core.schema as core_schema
import pms.dispensary.schema as dispensary_schema
import pms.inventory.schema as inventory_schema


class RootQuery(authentication_schema.Query, core_schema.Query, dispensary_schema.Query, inventory_schema.Query):
    pass


class RootMutation(authentication_schema.Mutation, core_schema.Mutation, dispensary_schema.Mutation, inventory_schema.Mutation):
    pass


class RootSubscription(inventory_schema.Subscription):
    pass


# noinspection PyTypeChecker
schema = graphene.Schema(query=RootQuery, mutation=RootMutation, subscription=RootSubscription)
