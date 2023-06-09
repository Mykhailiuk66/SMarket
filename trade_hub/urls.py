
from django.urls import path
from . import views

urlpatterns = [
    path('', views.trade_hub, name="trade-hub"),
    path('trade-offer/', views.create_trade_offer, name="create-trade-offer"),
    path('login/', views.login_user, name="login"),
    path('register/', views.register_user, name="register"),
    path('history/', views.history, name="history"),
    path('profile/', views.profile, name="profile"),


]
