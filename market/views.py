from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from trade_hub.models import UserItem, ItemExterior, ItemQuality
from .models import MarketItem
from .utils import handle_buy_form, handle_sell_form


@login_required(login_url='login')
def market(request):
    profile = request.user.profile

    if request.method == 'POST':
        if 'sell-form' in request.POST:
            handle_sell_form(request)
        elif 'buy-form' in request.POST:
            handle_buy_form(request)
            
        return redirect('market')

    form_inputs = {}
    exteriors = ItemExterior.objects.all()
    qualities = ItemQuality.objects.all()
    user_market_items_new = MarketItem.objects.filter(user_item__user=profile, status=MarketItem.NEW)
    user_items = UserItem.objects.filter(user=profile).exclude(id__in=user_market_items_new.values_list('user_item__id', flat=True))
    
    items_fot_sale = MarketItem.objects.filter(status=MarketItem.NEW).exclude(seller=profile)
    if request.GET.get('exteriors-select'):
        exteriors_select = request.GET.getlist('exteriors-select')
        items_fot_sale = items_fot_sale.filter(user_item__item__exterior__id__in=exteriors_select)
        form_inputs['exteriors_select'] = exteriors_select
    if request.GET.get('qualities-select'):
        qualities_select = request.GET.getlist('qualities-select')
        items_fot_sale = items_fot_sale.filter(user_item__item__quality__id__in=qualities_select)
        form_inputs['qualities_select'] = qualities_select
    if request.GET.get('stattrak'):
        items_fot_sale = items_fot_sale.filter(user_item__item__stattrak=True)
        form_inputs['stattrak'] = True

    context = {
        'exteriors': exteriors,
        'qualities': qualities,
        'user_items': user_items,
        'form_inputs': form_inputs,
        'items_fot_sale': items_fot_sale,
    }
    return render(request, 'market/market.html', context=context)


@login_required(login_url='login')
def delist_item(request, pk):
    market_item = MarketItem.objects.get(id=pk)

    if market_item.status == MarketItem.NEW:
        market_item.status = MarketItem.CANCELED
        market_item.save()

    return redirect('history')