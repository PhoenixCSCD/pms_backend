from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from pms.schema import schema

urlpatterns = [
    path('graphql/', csrf_exempt(GraphQLView.as_view(schema=schema, graphiql=True))),
]
