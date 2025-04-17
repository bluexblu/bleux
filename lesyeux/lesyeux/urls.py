from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Vistas principales
    path('', views.index, name='index'),
    path('producto/<int:pk>/', views.producto_detail, name='producto_detail'),

    # Endpoints extra
    path('usuarios/', views.usuarios_list, name='usuarios_list'),
    path('transacciones/', views.transacciones_list, name='transacciones_list'),
    path('resenas/<int:producto_id>/', views.resenas_producto, name='resenas_producto'),
    path('deseos/<int:usuario_id>/', views.lista_deseos, name='lista_deseos'),

    #Endpoints creados part2
    path('catalogo/', views.catalogo, name='catalogo'),
    path('usuarios/', views.usuarios, name='usuarios'),
    path('index/', views.index, name='index'),
    path('suscripcion/', views.suscripcion, name='suscripcion'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
