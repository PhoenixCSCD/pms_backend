import datetime

import graphene
from django.db import transaction
from django.utils import timezone
from graphene_django import DjangoObjectType

from pms.dispensary.models import Sale, SaleLine
from pms.inventory.events import dispatch_stock_level_change
from pms.inventory.models import Stock


class SaleType(DjangoObjectType):
    class Meta:
        model = Sale


class SaleLineType(DjangoObjectType):
    class Meta:
        model = SaleLine


class SaleLineInputType(graphene.types.InputObjectType):
    drug_id = graphene.UUID(required=True)
    quantity = graphene.Decimal(required=True)
    selling_price = graphene.Decimal(required=True)
    id = graphene.UUID()  # for the sake of frontend


class RecordSale(graphene.Mutation):
    class Arguments:
        timestamp = graphene.DateTime(required=True)
        discount = graphene.Decimal(required=True)
        sale_lines = graphene.List(SaleLineInputType)

    sale = graphene.Field(SaleType)

    @staticmethod
    @transaction.atomic()
    def mutate(_root, _info, timestamp, discount, sale_lines):
        sale = Sale()
        sale.timestamp = timestamp
        sale.attendant_id = _info.context.user.id
        sale.discount = discount
        sale.sub_total = 0
        sale.save()

        for sale_line_input in sale_lines:
            sale_line = SaleLine()
            sale_line.sale_id = sale.id
            sale_line.drug_id = sale_line_input.drug_id
            sale_line.quantity = sale_line_input.quantity
            sale_line.selling_price = sale_line_input.selling_price
            sale_line.save()

            sale.sub_total += sale_line.quantity * sale_line.selling_price
            Stock.dispense(
                sale_line.drug_id,
                sale_line.quantity
            )
            dispatch_stock_level_change(sale_line.drug_id)
            print("Dispatch Call")
        sale.grand_total = sale.sub_total - sale.discount
        sale.save()

        return RecordSale(sale=sale)


class Mutation(graphene.ObjectType):
    record_sale = RecordSale.Field()


class Query(graphene.ObjectType):
    sales = graphene.List(SaleType)
    today_sales = graphene.List(SaleType)

    @staticmethod
    def resolve_sales(_root, _info):
        return Sale.objects.all()

    @staticmethod
    def resolve_today_sales(_root, _info):
        return Sale.objects.filter(timestamp__month=5)