import uuid

from django.db import models

#
# class Manufacturer(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4)
#     name = models.CharField(max_length=100)
#
#
# class Drug(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4)
#     name = models.CharField(max_length=200)
#     price = models.DecimalField(max_digits=19, decimal_places=2)
#
#
# class Supplier(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4)
#     name = models.CharField(max_length=100)
#     email = models.CharField(max_length=320)
#     drugs = models.ManyToManyField(Drug)
