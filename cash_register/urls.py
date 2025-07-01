from django.urls import path
from . import views

urlpatterns = [
    path('open', views.open_cash_register_view, name='open-cash-register'),
    path('close/<int:cash_register_pk>/', views.close_cash_register_view, name='close-cash-register'),
    path('cash-registers/', views.cash_register_list_view, name='cash-register-list'),
    path('cash-register/detail/<int:pk>/', views.cash_register_detail_view, name='cash-register-detail'),
    path('cash-register/movement/add/', views.cash_movement_create, name='cash-movement-create'),
]
