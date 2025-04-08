from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('producto/<int:pk>/', views.producto_detail, name='producto_detail'),
    path('producto/nuevo/', views.producto_create, name='producto_create'),
    path('producto/<int:pk>/editar/', views.producto_edit, name='producto_edit'),
]
