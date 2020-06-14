import uuid

from django.db import models
from django.db.models import Sum
from django.utils import timezone

from pms.core.models import Drug, User


class Stock(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE)
    lot_number = models.CharField(max_length=100)
    expiry_date = models.DateField()
    quantity = models.IntegerField(default=0)

    @classmethod
    def get_stock_level(cls, drug_id, lot_number=None, include_expired=False):
        if lot_number:
            if include_expired:
                try:
                    return cls.objects.get(
                        drug_id=drug_id,
                        lot_number=lot_number
                    ).quantity
                except Stock.DoesNotExist:
                    return 0
            else:
                try:
                    return cls.objects.get(
                        drug_id=drug_id,
                        lot_number=lot_number,
                        expiry_date__gt=timezone.now()
                    ).quantity
                except Stock.DoesNotExist:
                    return 0
        else:
            if include_expired:
                return cls.objects.filter(drug_id=drug_id).aggregate(Sum('quantity'))['quantity__sum'] or 0
            else:
                return cls.objects.filter(
                    drug_id=drug_id,
                    expiry_date__gt=timezone.now()
                ).aggregate(Sum('quantity'))['quantity__sum'] or 0

    @classmethod
    def dispense(cls, drug_id, quantity):
        stocks = cls.objects.select_for_update().filter(
            drug_id=drug_id,
            expiry_date__gt=timezone.now()
        ).order_by('expiry_date')

        if cls.get_stock_level(drug_id) < quantity:
            raise Exception("Stock level is low.")

        i = 0
        for _index, stock in enumerate(stocks):
            if stock.quantity > quantity:
                stock.quantity -= quantity
                quantity = 0
            else:
                quantity -= stocks[i].quantity
                stock.quantity = 0
            stock.save()
            i += 1

    @classmethod
    def adjust_stock(cls, drug_id, lot_number, quantity, expiry_date=None):
        stock, _created = cls.objects.select_for_update().get_or_create(
            drug_id=drug_id,
            lot_number=lot_number,
            defaults={'expiry_date': expiry_date}
        )
        if cls.get_stock_level(drug_id=drug_id, lot_number=lot_number) + quantity < 0:
            raise Exception('Stock Level is low!')

        stock.quantity += quantity
        stock.save()

    @classmethod
    def get_drug_lot_numbers(cls, drug_id, include_expired=False):
        if include_expired:
            return cls.objects.values_list('lot_number', flat=True).filter(drug_id=drug_id)
        else:
            return cls.objects.values_list('lot_number', flat=True).filter(drug_id=drug_id, expiry_date__gt=timezone.now())


class Supply(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    supply_date = models.DateField()
    supplier = models.CharField(max_length=250)
    vat = models.DecimalField(max_digits=19, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=19, decimal_places=2, default=0)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE)
    sub_total = models.DecimalField(max_digits=19, decimal_places=2, default=0)
    grand_total = models.DecimalField(max_digits=19, decimal_places=2, default=0)
    freight_charge = models.DecimalField(max_digits=19, decimal_places=2, default=0)


class SupplyLine(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    supply = models.ForeignKey(Supply, on_delete=models.CASCADE, related_name='supply_lines')

    drug = models.ForeignKey(Drug, on_delete=models.CASCADE)
    expiry_date = models.DateField()
    quantity = models.IntegerField()
    lot_number = models.CharField(max_length=100)
    cost_price = models.DecimalField(max_digits=19, decimal_places=2)


class StockAdjustment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    timestamp = models.DateTimeField()
    reason = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class StockAdjustmentLine(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    stock_adjustment = models.ForeignKey(StockAdjustment, on_delete=models.CASCADE)

    drug = models.ForeignKey(Drug, on_delete=models.CASCADE)
    lot_number = models.CharField(max_length=100)
    quantity = models.IntegerField()
