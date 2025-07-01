from django.urls import path
from . import views

urlpatterns = [
    path('reception/list/', views.reception_list, name='reception-list'),
    path('receptions/<int:pk>/', views.reception_detail, name='reception-detail'),
    path('reception/create/', views.reception_create, name='reception-create'),
    
    # URL para editar una recepción existente
    #path('reception/edit/<int:id>/', views.reception_edit, name='reception-edit'),
    
    # URL para ver la lista de recepciones
    #path('reception/list/', views.reception_list, name='reception-list'),
]
