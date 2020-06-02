from graphene_subscriptions.events import SubscriptionEvent

from pms.inventory.models import Stock

STOCK_LEVEL_CHANGE = 'stock_level_change'


def dispatch_stock_level_change(drug_id):
    event = SubscriptionEvent(
        operation=STOCK_LEVEL_CHANGE,
        instance=drug_id
    )
    event.send()
