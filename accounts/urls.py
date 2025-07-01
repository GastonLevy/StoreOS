from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('supplier/', supplier_list, name='supplier-list'),
    path('supplier/create/', supplier_create, name='supplier-create'),
    path('supplier/<int:pk>/edit/', supplier_update, name='supplier-update'),
    path('supplier/<int:pk>/', supplier_detail, name='supplier-detail'),
    path('supplier/<int:pk>/delete/', supplier_delete, name='supplier-delete'),

    path('supplier/<int:supplier_id>/entrypack/create/', entrypack_create, name='entrypack-create'),
    path('supplier/entry-pack/<int:entry_pack_id>/', entry_pack_detail, name='entry-pack-detail'),
    path('supplier/entry-pack/update/<int:pk>/', entry_pack_update, name='entry-pack-update'),
    path('supplier/entry-pack/delete/<int:pk>/', entry_pack_delete, name='entry-pack-delete'),

    path('supplier/supplier-entry/create/', create_supplier_entry, name='supplier-entry-create'),
    path('supplier/supplier-entry/<int:pk>/delete/<int:entry_pack_id>/', supplier_entry_delete_confirm, name='supplier-entry-delete'),

    path('account/', account_list, name='account-list'),
    path('account/<int:pk>/', account_detail, name='account-detail'),
    path('account/create/', account_create, name='account-create'),
    path('account/<int:pk>/edit/', account_update, name='account-update'),
    path('account/<int:pk>/delete/', account_delete, name='account-delete'),

    path('account/debt/create/', create_debt, name='debt-create'),
    path('account/debt/update/<int:pk>/', debt_update, name='debt-update'),
    path('account/debt/delete/<int:pk>/', debt_delete, name='debt-delete'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
