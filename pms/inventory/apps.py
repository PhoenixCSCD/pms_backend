from django.apps import AppConfig


class InventoryConfig(AppConfig):
    name = 'pms.inventory'

    def ready(self):
        import pms.inventory.signals

