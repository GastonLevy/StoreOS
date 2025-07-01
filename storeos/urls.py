from django.contrib import admin
from django.urls import path, include
from . import views  # Import views, where error_view is located

# Redirect errors to the custom error view
handler404 = 'storeos.views.error_view'
handler403 = 'storeos.views.error_view'
handler500 = 'storeos.views.error_view'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('landing_page.urls')),  # Home
    path('users/', include('users.urls')),  # Users
    path('logs/', include('self_logs.urls')),  # Logs
    path('inventory/', include('inventory.urls')),  # Inventory
    path('checkout/', include('checkout.urls')),  # Cart and others
    path('suppliers/', include('accounts.urls')),  # Suppliers
    path('cash_register/', include('cash_register.urls')),  # Cash register
    path('receptions/', include('receptions.urls')),  # Receptions
    path('excel_import/', include('excel_import.urls')),  # Import
    path('wiki/', include('self_wiki.urls')),  # Wiki
    path('cyber_control/', include('cyber_control.urls')),  # Cyber control
    #path('restaurant/', include('restaurant.urls')),  # Restaurant
]
