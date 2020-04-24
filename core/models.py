import uuid

from django.contrib.auth import get_user_model
from django.db import models
from authentication.models import User


class Branch(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(get_user_model(), related_name='branches')
