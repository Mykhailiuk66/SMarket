
from django.urls import path
from . import views

urlpatterns = [
    path('', views.trade_hub, name="trade-hub"),
    path('trade-offer/', views.create_trade_offer, name="create-trade-offer"),
    path('guarantor_hub', views.guarantor_hub, name="guarantor-hub"),
    path('accept-trade/<str:pk>', views.accept_trade, name="accept-trade"),
    path('cancel-trade/<str:pk>', views.cancel_trade, name="cancel-trade"),

]
