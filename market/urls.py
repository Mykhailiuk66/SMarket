
from django.urls import path
from . import views

urlpatterns = [
    path('market/', views.market, name="market"),
    path('delist-item/<str:pk>', views.delist_item, name="delist-item"),
]
