from django.shortcuts import render, redirect
from trade_hub.models import Trade, UserItem, Item, TradeItem
from django.contrib.auth.decorators import login_required
import math

# Create your views here.

def trade_hub(request):
    trades = Trade.objects.filter(status=Trade.NEW)

    context = {
        'trades': trades
    }
    return render(request, 'trade_hub/trade_hub.html', context=context)


@login_required(login_url='login')
def create_trade_offer(request):

    if request.method == 'POST':
        profile = request.user.profile
        user_items_chosen = request.POST.getlist('user_items')
        second_party_items_chosen = request.POST.getlist('second_party_items')

        if not user_items_chosen or not second_party_items_chosen:
            print("You must select items from both sides to proceed")
            return redirect('create-trade-offer')

        trade = Trade.objects.create(creator=profile)

        for user_item_id in user_items_chosen:
            user_item = UserItem.objects.get(id=user_item_id)
            TradeItem.objects.create(trade=trade, user_item=user_item, user=profile)

        for item_id in second_party_items_chosen:
            item = Item.objects.get(id=item_id)
            TradeItem.objects.create(trade=trade, item=item)

        return redirect('trade-hub')
    else:
        user_items = UserItem.objects.all()
        items = Item.objects.all()
        additional_blocks_user_items = range(6 - (user_items.count() % 6))
        additional_blocks_items = range(6 - (items.count() % 6))


    context = {
        'user_items': user_items,
        'items': items,
        'additional_blocks_user_items': additional_blocks_user_items,
        'additional_blocks_items': additional_blocks_items,
    }
    return render(request, 'trade_hub/trade_offer.html', context=context)


@login_required(login_url='login')
def history(request):

    return render(request, 'history.html')


