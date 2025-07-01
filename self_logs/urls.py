from django.urls import path
from .views import action_log_list

urlpatterns = [
    path('action_logs/', action_log_list, name='action_log_list'),
]
