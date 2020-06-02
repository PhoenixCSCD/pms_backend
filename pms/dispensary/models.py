import uuid

from django.db import models

from pms.core.models import User, Drug


class Sale(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    attendant = models.ForeignKey(User, on_delete=models.CASCADE)
    discount = models.DecimalField(max_digits=19, decimal_places=2, default=0)
    sub_total = models.DecimalField(max_digits=19, decimal_places=2, default=0)
    grand_total = models.DecimalField(max_digits=19, decimal_places=2, default=0)
    timestamp = models.DateTimeField()


class SaleLine(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name="sale_lines")
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    selling_price = models.DecimalField(max_digits=19, decimal_places=2, default=0)
