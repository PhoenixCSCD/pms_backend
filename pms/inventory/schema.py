import graphene
from django.db import transaction
from graphene_django.types import DjangoObjectType
from rx import Observable

from pms.core.models import Drug
from pms.inventory.events import STOCK_LEVEL_CHANGE
from pms.inventory.models import Supply, SupplyLine, Stock


class SupplyType(DjangoObjectType):
    class Meta:
        model = Supply


class SupplyLineType(DjangoObjectType):
    class Meta:
        model = SupplyLine


class SupplyLineInput(graphene.types.InputObjectType):
    drug_id = graphene.UUID(required=True)
    expiry_date = graphene.Date(required=True)
    quantity = graphene.Int(required=True)
    lot_number = graphene.String(required=True)
    cost_price = graphene.Decimal(required=True)


class RecordSupply(graphene.Mutation):
    class Arguments:
        supply_date = graphene.Date(required=True)
        supplier = graphene.String(required=True)
        vat = graphene.Decimal(required=True)
        discount = graphene.Decimal(required=True)
        freight_charge = graphene.Decimal(required=True)
        supply_lines = graphene.List(SupplyLineInput, required=True)

    supply = graphene.Field(SupplyType)

    @staticmethod
    @transaction.atomic()
    def mutate(_root, _info, supply_date, supplier, vat, discount, freight_charge, supply_lines):
        supply = Supply()
        supply.supply_date = supply_date
        supply.receiver_id = _info.context.user.id
        supply.supplier = supplier
        supply.vat = vat
        supply.discount = discount
        supply.freight_charge = freight_charge
        supply.sub_total = 0
        supply.save()

        for supply_line in supply_lines:
            supply_line1 = SupplyLine()
            supply_line1.supply_id = supply.id
            supply_line1.drug_id = supply_line.drug_id
            supply_line1.expiry_date = supply_line.expiry_date
            supply_line1.quantity = supply_line.quantity
            supply_line1.lot_number = supply_line.lot_number
            supply_line1.cost_price = supply_line.cost_price
            supply_line1.save()

            supply.sub_total += supply_line.cost_price * supply_line.quantity

            quantity_per_pack = Drug.objects.get(id=supply_line.drug_id).quantity_per_pack

            Stock.adjust_stock(
                supply_line.drug_id,
                supply_line.lot_number,
                supply_line.quantity * quantity_per_pack,
                supply_line.expiry_date
            )

        supply.grand_total = supply.sub_total + supply.vat + supply.freight_charge - supply.discount
        supply.save()

        return RecordSupply(supply=supply)




class Mutation(graphene.ObjectType):
    record_supply = RecordSupply.Field()


class Query(graphene.ObjectType):
    supplies = graphene.List(SupplyType)
    stock_level = graphene.Int(drug_id=graphene.UUID(required=True), lot_number=graphene.String())

    @staticmethod
    def resolve_supplies(_root, _info):
        return Supply.objects.all()

    @staticmethod
    def resolve_stock_level(_root, _info, drug_id, lot_number=None):
        return Stock.get_stock_level(drug_id, lot_number)


class Subscription(graphene.ObjectType):
    hello = graphene.String()
    stock_level = graphene.Int(drug_id=graphene.UUID(required=True))

    def resolve_hello(root, info):
        return Observable.interval(3000) \
            .map(lambda i: "hello world!")

    @staticmethod
    def resolve_stock_level(_root, _info, drug_id):

        return _root.filter(
            lambda event: event.operation == STOCK_LEVEL_CHANGE and event.instance == drug_id
        ).map(lambda event: Stock.get_stock_level(drug_id=drug_id))
