from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from pms.schema import schema
from pms.core.views import upload_image

urlpatterns = [
    path('graphql/', csrf_exempt(GraphQLView.as_view(schema=schema, graphiql=True))),
    path('upload-image/', upload_image),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
