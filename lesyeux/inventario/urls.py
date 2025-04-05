from django.urls import path
from . import views

urlpatterns = [
    path('', views.inventario, name='inventario'),  # Página principal de inventario
    path('producto/<int:producto_id>/', views.producto_detalle, name='producto_detalle'),  # Detalle de un producto
]
