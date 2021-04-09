from django.urls import path
from . import views

urlpatterns = [
    path('add_to_favourities/<int:id>/', views.cart_add, name='cart_add'),
    path('item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('clear/', views.cart_clear, name='cart_clear'),
    path('favorities/', views.cart_detail, name='favorities'),
]
