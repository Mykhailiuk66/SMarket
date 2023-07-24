from django.contrib import messages
from django.db.models import Q
from django.db import transaction, DatabaseError
from trade_hub.models import Trade, UserItem
from decimal import Decimal

from users.models import Discount
from .models import MarketItem


def revise_profile_discount(profile):
    total_trade_amount = profile.total_trade_amount
    discount = Discount.objects.filter(min_trade_amount__lte=total_trade_amount).order_by('-min_trade_amount').first()

    profile.discount = discount.discount
    profile.save()


def handle_sell_form(request):
    profile = request.user.profile
    user_item_id = request.POST.get('user_items', None)
    price = float(request.POST.get('price', None))

    if price is None or price <= 0:
        messages.info(request, 'Price should be greater than 0')
        return
    if not user_item_id:
        messages.info(request, 'Please choose item')
        return
        
    user_item = UserItem.objects.get(id=user_item_id, user=profile) 

    item_in_trade = user_item.tradeitem_set.filter(Q(trade__status=Trade.NEW) | Q(trade__status=Trade.REVIEWING)).exists()
    if item_in_trade:
        messages.error(request, 'In order to put this item up for sale, it must not be in trade')
        return

    MarketItem.objects.create(user_item=user_item, price=price, seller=profile)
    messages.success(request, f'"{user_item.item.name}" has been put up for sale')


def handle_buy_form(request, market_fee=10):
    profile = request.user.profile
    buy_items_ids = set(request.POST.getlist('items-for-sale'))
    buy_items = [MarketItem.objects.get(id=item_id) for item_id in buy_items_ids]

    total_value = sum([item.price for item in buy_items])
    total_value_with_disc = total_value - (Decimal(profile.discount/100)*total_value)

    if profile.balance < total_value_with_disc:
        messages.error(request, 'Insufficient balance')
        return

    item_already_sold = False
    for market_item in buy_items:
        try:
            with transaction.atomic():
                if market_item.status != MarketItem.NEW:
                    item_already_sold = True
                    continue

                seller = market_item.user_item.user
                user_item = market_item.user_item

                seller.balance += Decimal(float(market_item.price) - (float(market_item.price) * market_fee / 100))
                user_item.user = profile

                profile.balance -= market_item.price - (Decimal(profile.discount/100)*market_item.price)
                profile.total_trade_amount += float(market_item.price)

                market_item.buyer = profile
                market_item.status = MarketItem.SOLD

                seller.save()
                user_item.save()
                profile.save()
                market_item.save()

                messages.success(request, f'"{market_item.user_item.item.name}" has been successfully purchased')
        except DatabaseError:
            item_already_sold = True
    if item_already_sold:
        messages.error(request, 'Some items have already been sold')

    revise_profile_discount(profile)