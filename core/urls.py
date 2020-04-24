from django.urls import path
from .views import get_image_kit_signature

urlpatterns = [
    path('image-kit-signature/', get_image_kit_signature)
]
