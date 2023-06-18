from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from trade_hub.models import Trade, UserItem, Item, TradeItem
from market.models import MarketItem

from .utils import get_items_to_trade

# Create your views here.

def trade_hub(request):
    trades = Trade.objects.filter(status=Trade.NEW)
    guarantor = request.user.groups.filter(name="guarantor").exists()

    context = {
        'trades': trades,
        'guarantor': guarantor,
    }
    return render(request, 'trade_hub/trade_hub.html', context=context)


@login_required(login_url='login')
def guarantor_hub(request):
    trades = Trade.objects.filter(status=Trade.REVIEWING)
    guarantor = request.user.groups.filter(name="guarantor").exists()
    
    if not guarantor:
        messages.error(request, 'Access Denied')
        return redirect('trade-hub')

    context = {
        'trades': trades,
    }
    return render(request, 'trade_hub/guarantor_hub.html', context=context)


@login_required(login_url='login')
def create_trade_offer(request):
    profile = request.user.profile

    if request.method == 'POST':
        user_items_chosen = request.POST.getlist('user_items')
        second_party_items_chosen = request.POST.getlist('second_party_items')

        if not user_items_chosen or not second_party_items_chosen:
            messages.error(request, 'You must select items from both sides to proceed')

            return redirect('create-trade-offer')

        trade = Trade.objects.create(creator=profile)

        for user_item_id in user_items_chosen:
            user_item = UserItem.objects.get(id=user_item_id)
            market_items = user_item.marketitem_set.filter(status=MarketItem.NEW)
            for market_item in market_items:
                market_item.status = MarketItem.CANCELED

            TradeItem.objects.create(trade=trade, user_item=user_item, user=profile)

        for item_id in second_party_items_chosen:
            item = Item.objects.get(id=item_id)
            TradeItem.objects.create(trade=trade, item=item)

        return redirect('trade-hub')
    else:
        user_items = UserItem.objects.filter(user=profile)
        items = Item.objects.all()


    context = {
        'user_items': user_items,
        'items': items,
    }
    return render(request, 'trade_hub/trade_offer.html', context=context)



@login_required(login_url='login')
def accept_trade(request, pk):
    user = request.user
    profile = user.profile
    trade = Trade.objects.get(id=pk)

     
    if user.groups.filter(name="guarantor").exists() and trade.creator != profile and trade.second_party != profile:
        if not trade.second_party:
            messages.error(request, 'Error')
            return redirect('trade-hub')
        
        creator = trade.creator
        second_party = trade.second_party
        trade_items = trade.tradeitem_set.all()
        for trade_item in trade_items:
            user_item = trade_item.user_item
            if user_item.user == creator:
                user_item.user = second_party
            else:
                user_item.user = creator 
            
            another_trade_items = TradeItem.objects.filter(user_item=user_item).exclude(id__in=trade_items.values_list('id', flat=True))
            for another_trade_item in another_trade_items:
                another_trade_item.trade.status = Trade.CANCELED
                another_trade_item.trade.save()

            user_item.save()
        
        trade.guarantor = profile
        trade.status = Trade.SUCCESS
        trade.save()
        return redirect('guarantor-hub')
    elif profile != trade.creator:
        trade.second_party = profile
        trade_items = trade.tradeitem_set.filter(user_item=None)
        
        user_trade_items = get_items_to_trade(trade_items, profile)
        if user_trade_items:
            for trade_item, user_item in zip(trade_items, user_trade_items):
                trade_item.user_item = user_item
                trade_item.user = profile
                trade_item.item = None
                trade_item.save()
            trade.status = Trade.REVIEWING
            trade.save()
        else:
            messages.error(request, "You don't have all the items requested for the trade")
            return redirect('trade-hub')
        
    return redirect('history')


@login_required(login_url='login')
def cancel_trade(request, pk):
    user = request.user
    profile = user.profile
    trade = Trade.objects.get(id=pk)

    if user.groups.filter(name="guarantor").exists():
        trade.guarantor = profile
        trade.status = Trade.DECLINED
        trade.save()
        return redirect('guarantor-hub')
    elif profile == trade.creator or profile == trade.second_party:
        trade.status = Trade.CANCELED
        trade.save()

    return redirect('history')


