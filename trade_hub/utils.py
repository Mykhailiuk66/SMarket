from django.shortcuts import redirect
from django.contrib import messages
from django.db import transaction, DatabaseError

from trade_hub.models import Trade, UserItem, Item, TradeItem
from market.models import MarketItem


def get_items_to_trade(trade_items, profile):
    user_trade_items = []
    for trade_item in trade_items:
        items = profile.useritem_set.filter(item=trade_item.item)
        if items:
            for item in items:
                if item not in user_trade_items:
                    user_trade_items.append(item)
                    break
            else:
                return []
        else:
            return []
        
    return user_trade_items


def cancel_other_trades_with_item(user_item, trade_items):
    other_trade_items = TradeItem.objects.filter(user_item=user_item).exclude(id__in=trade_items.values_list('id', flat=True))
    for other_trade_item in other_trade_items:
        other_trade_item.trade.status = Trade.CANCELED
        other_trade_item.trade.save()


def handle_guarantor_acceptance(request, trade):
    profile = request.user.profile

    if not trade.second_party:
        messages.error(request, 'Error')
        return redirect('trade-hub')
    
    try:
        with transaction.atomic():
            creator = trade.creator
            second_party = trade.second_party
            trade_items = trade.tradeitem_set.all()
            for trade_item in trade_items:
                user_item = trade_item.user_item
                if user_item.user == creator:
                    user_item.user = second_party
                else:
                    user_item.user = creator 
                
                cancel_other_trades_with_item(user_item, trade_items)

                user_item.save()
            
            trade.guarantor = profile
            trade.status = Trade.SUCCESS
            trade.save()
        
        messages.success(request, 'Trade offer has been accepted')
    except DatabaseError:
        messages.error(request, 'An error occurred while processing the trade. Please try again.')


def handle_second_party_acceptance(request, trade):
    profile = request.user.profile
    trade.second_party = profile
    trade_items = trade.tradeitem_set.filter(user_item=None)
    
    user_trade_items = get_items_to_trade(trade_items, profile)
    if user_trade_items:
        try:
            with transaction.atomic():
                for trade_item, user_item in zip(trade_items, user_trade_items):
                    trade_item.user_item = user_item
                    trade_item.user = profile
                    trade_item.item = None
                    trade_item.save()
                trade.status = Trade.REVIEWING
                trade.save()
            messages.success(request, 'Trade offer has been accepted')
        except DatabaseError:
            messages.error(request, 'An error occurred while processing the trade. Please try again.')
    else:
        messages.error(request, "You don't have all the items requested for the trade")


def handle_trade_offer_creation(request):
    profile = request.user.profile
    user_items_chosen = request.POST.getlist('user_items')
    second_party_items_chosen = request.POST.getlist('second_party_items')

    if not user_items_chosen or not second_party_items_chosen:
        messages.error(request, 'You must select items from both sides to proceed')

        return redirect('create-trade-offer')

    try:
        with transaction.atomic():
            trade = Trade.objects.create(creator=profile)
            for user_item_id in user_items_chosen:
                user_item = UserItem.objects.get(id=user_item_id)
                market_items = user_item.marketitem_set.filter(status=MarketItem.NEW)
                for market_item in market_items:
                    market_item.status = MarketItem.CANCELED
                    market_item.save()

                TradeItem.objects.create(trade=trade, user_item=user_item, user=profile)

            for item_id in second_party_items_chosen:
                item = Item.objects.get(id=item_id)
                TradeItem.objects.create(trade=trade, item=item)
        
        messages.success(request, 'Trade offer has been created')
    except DatabaseError:
        messages.error(request, 'An error occurred while creating the trade offer. Please try again.')
