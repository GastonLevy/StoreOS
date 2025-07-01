from django.urls import path
from . import views

urlpatterns = [
    # Overview and category listing view
    path('', views.wiki_overview, name='wiki_overview'),
    path('category_list/', views.wiki_category_list, name='list_wiki_category'),

    # Categories: CRUD
    path('add/', views.add_wiki_category, name='add_wiki_category'),
    path('edit/<int:pk>/', views.edit_wiki_category, name='wiki_category_edit'),
    path('category/<int:category_id>/delete/', views.delete_wiki_category, name='wiki_category_delete'),
    path('wiki/category/<int:pk>/', views.wiki_category_detail, name='wiki_category_detail'),

    # Entries inside categories: CRUD
    path('category/<int:category_id>/create/', views.create_wiki_entry, name='wiki_entry_create'),
    path('category/<int:category_id>/entry/<int:entry_id>/edit/', views.edit_wiki_entry, name='wiki_entry_edit'),
    path('category/<int:category_id>/entry/<int:entry_id>/delete/', views.delete_wiki_entry, name='wiki_entry_delete'),

    # Entry detail and content
    path('wiki/entry/<int:entry_id>/', views.wiki_entry_content, name='wiki_entry_content'),
    path('entry/<int:entry_id>/', views.wiki_entry_detail, name='wiki_entry_detail'),
]
