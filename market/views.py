from decimal import Decimal
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from trade_hub.models import Trade, Item, UserItem, ItemExterior, ItemQuality
from .models import MarketItem

from .utils import revise_profile_discount

# Create your views here.

MARKET_FEE = 10

@login_required(login_url='login')
def market(request):
    profile = request.user.profile

    if request.method == 'POST':
        if 'sell-form' in request.POST:
            user_item_id = request.POST.get('user_items', None)
            price = float(request.POST.get('price', None))

            if price is None or price <= 0:
                messages.info(request, 'Price should be greater than 0')
                return redirect('market')
            if not user_item_id:
                messages.info(request, 'Please choose item')
                return redirect('market')
                

            user_item = UserItem.objects.get(id=user_item_id, user=profile) 

            item_in_trade = user_item.tradeitem_set.filter(Q(trade__status=Trade.NEW) | Q(trade__status=Trade.REVIEWING)).exists()
            if item_in_trade:
                messages.error(request, 'In order to put this item up for sale, it must not be in trade')
                return redirect('market')

            market_item = MarketItem.objects.create(user_item=user_item, price=price, seller=profile)

        elif 'buy-form' in request.POST:
            buy_items_ids = set(request.POST.getlist('items-for-sale'))
            buy_items = [MarketItem.objects.get(id=item_id) for item_id in buy_items_ids]

            total_value = sum([item.price for item in buy_items])
            total_value_with_disc = total_value - (Decimal(profile.discount/100)*total_value)

            if profile.balance < total_value_with_disc:
                messages.error(request, 'Insufficient Balance')
                return redirect('market')


            item_already_sold = False
            for market_item in buy_items:
                if market_item.status != MarketItem.NEW:
                    item_already_sold = True

                seller = market_item.user_item.user
                user_item = market_item.user_item

                seller.balance += Decimal(float(market_item.price) - (float(market_item.price) * MARKET_FEE / 100))
                user_item.user = profile

                profile.balance -= market_item.price - (Decimal(profile.discount/100)*market_item.price)
                profile.total_trade_amount += float(market_item.price)

                market_item.buyer = profile
                market_item.status = MarketItem.SOLD

                seller.save()
                user_item.save()
                profile.save()
                market_item.save()

            if item_already_sold:
                messages.error(request, 'Some items have already been sold')

            revise_profile_discount(profile)

        return redirect('market')
    else:
        form_inputs = {}
        exteriors = ItemExterior.objects.all()
        qualities = ItemQuality.objects.all()
        new_user_market_items = MarketItem.objects.filter(user_item__user=profile, status=MarketItem.NEW)
        user_items = UserItem.objects.filter(user=profile).exclude(id__in=new_user_market_items.values_list('user_item__id', flat=True))
        
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