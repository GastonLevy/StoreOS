from django.urls import path

from .views import (
    category_list,
    category_detail,
    category_create,
    category_update,
    category_delete,
)

from .views import (
    item_list,
    item_detail,
    item_create,
    item_update,
    item_delete,
    item_search,
)

urlpatterns = [
    path('categories/', category_list, name='category-list'),                # Listar todas las categorías
    path('categories/<int:pk>/', category_detail, name='category-detail'),   # Detalles de una categoría
    path('categories/create/', category_create, name='category-create'),     # Crear una nueva categoría
    path('categories/update/<int:pk>/', category_update, name='category-update'),  # Actualizar una categoría
    path('categories/delete/<int:pk>/', category_delete, name='category-delete'),  # Eliminar una categoría

    path('items/', item_list, name='item-list'),                # Listar todas las item
    path('items/<int:pk>/', item_detail, name='item-detail'),   # Detalles de una item
    path('items/create/', item_create, name='item-create'),     # Crear una nueva item
    path('items/update/<int:pk>/', item_update, name='item-update'),  # Actualizar una item
    path('items/delete/<int:pk>/', item_delete, name='item-delete'),  # Eliminar una item
    path('item/search/', item_search, name='item-search'), # Busca un item
]
