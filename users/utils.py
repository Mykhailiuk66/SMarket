from trade_hub.models import Item, UserItem
from django.contrib import messages

def generate_random_inventory(request, profile):
    items = Item.objects.order_by('?')[:5]

    [UserItem.objects.create(item=item, user=profile) for item in items]

    messages.success(request, 'New items have been added to your inventory')
