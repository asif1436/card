from django.urls import path

from .views import card_view, card_add, card_delete, ajax_call

urlpatterns = [
    path('', card_add, name="card_add"),
    path('card-view/', card_view, name="card_view"),
    path('card-delete/<int:id>/', card_delete, name='card_delete'),
    path('ajax-add/', ajax_call, name='add_card_by_ajax'),
]
