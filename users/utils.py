from trade_hub.models import Item, Trade, UserItem
from django.db.models import Q


def generate_random_inventory(profile):
    profile.creator.filter(Q(status=Trade.NEW) | Q(status=Trade.REVIEWING)).delete()
    profile.useritem_set.all().update(user=None)

    items = Item.objects.order_by('?')[:10]

    [UserItem.objects.create(item=item, user=profile) for item in items]
