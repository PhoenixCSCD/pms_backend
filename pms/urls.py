from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from pms.schema import schema
from pms.core.views import upload_file

urlpatterns = [
    path('graphql/', csrf_exempt(GraphQLView.as_view(schema=schema, graphiql=True))),
    path('upload-file/', upload_file),
]
