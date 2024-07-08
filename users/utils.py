from trade_hub.models import Item, Trade, UserItem
from django.db.models import Q


def generate_random_inventory(profile):
    items = Item.objects.order_by('?')[:5]

    [UserItem.objects.create(item=item, user=profile) for item in items]
