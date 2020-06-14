from graphene_subscriptions.events import SubscriptionEvent

from pms.inventory.models import Stock

STOCK_LEVEL_CHANGE = 'stock_level_change'
LOT_STOCK_LEVEL_CHANGE = 'lot_stock_level_change'


def dispatch_stock_level_change(drug_id):
    event = SubscriptionEvent(
        operation=STOCK_LEVEL_CHANGE,
        instance={'drug_id': drug_id}
    )
    event.send()


def dispatch_lot_stock_level_change(drug_id, lot_number):
    event = SubscriptionEvent(
        operation=LOT_STOCK_LEVEL_CHANGE,
        instance={'drug_id': drug_id, 'lot_number': lot_number}
    )
    event.send()
    dispatch_stock_level_change(drug_id=drug_id)
