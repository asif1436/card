from django.urls import path

from .views import *

urlpatterns = [
    path('', card_add, name="card_add"),
    path('login/', user_login, name="login"),
    path('logout/', user_logout, name="user_logout"),
    path('verify-user/', verify_user_with_otp, name='verify_user'),
    path('card-view/', card_view, name="card_view"),
    path('card-delete/<int:id>/', card_delete, name='card_delete'),
    path('ajax-add/', ajax_call, name='add_card_by_ajax'),
    path('expiry-otp/', otp_expiry, name='expiry_otp'),
]

