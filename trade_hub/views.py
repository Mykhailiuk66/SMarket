from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from trade_hub.models import Trade, UserItem, Item
from .utils import handle_guarantor_acceptance, handle_second_party_acceptance, handle_trade_offer_creation


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
        messages.error(request, 'Access denied')
        return redirect('trade-hub')

    context = {
        'trades': trades,
    }
    return render(request, 'trade_hub/guarantor_hub.html', context=context)


@login_required(login_url='login')
def create_trade_offer(request):
    if request.method == 'POST':
        handle_trade_offer_creation(request)
        return redirect('trade-hub')

    profile = request.user.profile
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
        handle_guarantor_acceptance(request, trade)
        return redirect('guarantor-hub')
    elif profile != trade.creator:
        handle_second_party_acceptance(request, trade)
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
        messages.info(request, 'Trade offer has been declined')
        return redirect('guarantor-hub')
    elif profile == trade.creator or profile == trade.second_party:
        trade.status = Trade.CANCELED
        messages.info(request, 'Trade offer has been canceled')
        trade.save()

    return redirect('history')


