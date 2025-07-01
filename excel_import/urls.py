from django.urls import path
from .views import cargar_excel_view

urlpatterns = [
    path('cargar_excel/', cargar_excel_view, name='cargar_excel'),  # URL para cargar el archivo Excel
]
