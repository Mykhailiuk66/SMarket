
from django.urls import path
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView, PasswordResetDoneView

from . import views

urlpatterns = [
    path('', views.trade_hub, name="trade-hub"),
    path('trade-offer/', views.create_trade_offer, name="create-trade-offer"),
    path('history/', views.history, name="history"),

    path('reset_password/', PasswordResetView.as_view(template_name="reset_password.html"), name='reset-password'),
    path('reset_password_sent/', PasswordResetDoneView.as_view(template_name='reset_password_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='reset.html'), name='password_reset_confirm'),
    path('reset_password_complete/', PasswordResetCompleteView.as_view(template_name='reset_password_complete.html'), name='password_reset_complete'),
    
]
