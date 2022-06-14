from django.shortcuts import render, redirect
from users.forms import CustomUserCreationForm, CustomUserLoginForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q

from trade_hub.models import Trade
from market.models import MarketItem
from .utils import generate_random_inventory


@login_required(login_url='login')
def profile(request):
    profile = request.user.profile

    if request.method == 'POST':
        profile = request.user.profile
        trade_link = request.POST.get('trade-link')
        avatar_img = request.FILES.get('avatar-input')
        
        if avatar_img:
            profile.image = avatar_img
        if trade_link is not None:
            profile.trade_url = trade_link
        
        profile.save()

    context = {
        'profile': profile
    }
    return render(request, 'users/profile.html', context=context)


@login_required(login_url='login')
def history(request):
    profile = request.user.profile
    trades = Trade.objects.filter(Q(creator=profile) | Q(second_party=profile) | Q(guarantor=profile))
    market_items = MarketItem.objects.filter(Q(buyer=profile) | Q(seller=profile)).order_by('-created')

    context = {
        'trades': trades,
        'market_items': market_items,
    }
    return render(request, 'users/history.html', context=context)


@login_required(login_url='login')
def update_inventory(request):
    profile = request.user.profile
    
    generate_random_inventory(profile)

    return redirect(request.GET['next'] if 'next' in request.GET else 'profile')


def login_user(request):
    action = "Sign In"

    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == 'POST':
        form = CustomUserLoginForm(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            try:
                user = User.objects.get(username=username)
            except:
                print('User does not exists')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect(request.GET['next'] if 'next' in request.GET else 'trade-hub')
            else:
                print('Username OR password is incorrect')
        else:
            print('Username OR password is incorrect')
    else:
        form = CustomUserLoginForm()


    context = {
        'action': action,
        'form': form,
    }
    return render(request, 'users/login_register.html', context=context)


def logout_user(request):
    logout(request)

    return redirect('trade-hub')


def register_user(request):
    action = "Sign Up"

    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == 'POST':
        form = CustomUserCreationForm(data=request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            login(request, user)
            return redirect('trade-hub')
    else:
        form = CustomUserCreationForm()

    context = {
        'action': action,
        'form': form,
    }
    return render(request, 'users/login_register.html', context=context)
    