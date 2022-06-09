from django.shortcuts import render

# Create your views here.

def trade_hub(request):

    return render(request, 'trade_hub.html')


def create_trade_offer(request):

    return render(request, 'trade_offer.html')


def history(request):

    return render(request, 'history.html')


def profile(request):

    return render(request, 'profile.html')


def login_user(request):
    action = "Sign In"


    context = {
        'action': action
    }
    return render(request, 'login_register.html', context=context)



def register_user(request):
    action = "Sign Up"


    context = {
        'action': action
    }
    return render(request, 'login_register.html', context=context)
    