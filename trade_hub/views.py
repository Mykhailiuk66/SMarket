from django.shortcuts import render

# Create your views here.

def trade_hub(request):

    return render(request, 'trade_hub.html')


def create_trade_offer(request):

    return render(request, 'trade_offer.html')


def history(request):

    return render(request, 'history.html')


