from django.urls import path
from . import views

urlpatterns = [
    # URL para crear o editar un dispositivo
    path('device/', views.create_or_edit_device, name='create_device'),  # Crear dispositivo
    path('device/<int:device_id>/', views.create_or_edit_device, name='edit_device'),  # Editar dispositivo
    path('devices/', views.device_list, name='device-list'),  # URL para la lista de dispositivos
    path('device/delete/<int:device_id>/', views.device_delete, name='delete_device'),

    path('usage_sessions/', views.usage_session_list, name='usage-session-list'),
    path('add_time/<int:device_id>/', views.add_usage_time, name='add-usage-time'),
    path('end_session/<int:device_id>/', views.end_session, name='end_session'),
    path('get_all_remaining_times/', views.get_all_remaining_times, name='get_all_remaining_times'),

    path('reports/usage/', views.usage_reports, name='usage_reports'),
]
