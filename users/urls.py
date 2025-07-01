from django.urls import path, reverse_lazy
from .views import login_view, register_view, logout_view, home_view, cambiar_password
from django.contrib.auth.views import PasswordChangeView

urlpatterns = [
    path('', home_view, name='home'),
    path('login/', login_view, name='login'),
    #path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('change_password/', cambiar_password, name='password_change'),
]