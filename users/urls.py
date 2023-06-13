
from django.urls import path
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView, PasswordResetDoneView

from . import views

urlpatterns = [
    path('profile/', views.profile, name="profile"),
    path('history/', views.history, name="history"),
    path('update-inventory/', views.update_inventory, name="update-inventory"),


    path('login/', views.login_user, name="login"),
    path('register/', views.register_user, name="register"),
    path('logout/', views.logout_user, name="logout"),

    path('reset_password/', PasswordResetView.as_view(template_name="reset_password.html"), name='reset-password'),
    path('reset_password_sent/', PasswordResetDoneView.as_view(template_name='reset_password_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='reset.html'), name='password_reset_confirm'),
    path('reset_password_complete/', PasswordResetCompleteView.as_view(template_name='reset_password_complete.html'), name='password_reset_complete'),
]
