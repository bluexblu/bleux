from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from inventario.views import MyTokenObtainPairView
from inventario.views import register_user, login_view
from django.contrib.auth import views as auth_views
from inventario import views

urlpatterns = [
    path('admin/', admin.site.urls),
    

    # Vistas principales
    path('', views.index, name='index'),  # Página de inicio
    path('producto/<int:pk>/', views.producto_detail, name='producto_detail'),
    path('peliculas/', views.peliculas_view, name='peliculas'),
    path('series/', views.series_view, name='series'),
    path('comics/', views.comics_view, name='comics'),

    # Endpoints extra
    path('usuarios/', views.usuarios_list, name='usuarios_list'),
    path('transacciones/', views.transacciones_list, name='transacciones_list'),
    path('resenas/<int:producto_id>/', views.resenas_producto, name='resenas_producto'),
    path('deseos/<int:usuario_id>/', views.lista_deseos, name='lista_deseos'),

    # Endpoints adicionales
    path('catalogo/', views.catalogo, name='catalogo'),
    path('usuarios/', views.usuarios, name='usuarios'),
    path('suscripcion/', views.suscripcion, name='suscripcion'),
    path('planes/', views.planes, name='planes'),
    path('metodos-pago/', views.metodos_pago, name='metodos_pago'),
    path('historial/', views.historial_suscripcion, name='historial_suscripcion'),
    path('pago/', views.pago_paypal, name='pago_paypal'),
    path('paypal/', include('paypal.standard.ipn.urls')),      
    
    # Rutas de autenticación y token
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),  # Usando tu vista personalizada
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # renovar token
    path('register_user/', register_user, name='register_user'),

    # Rutas de recuperación de contraseña
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('login/', views.login_view, name='login'),
    path('carrito/', views.carrito_view, name='carrito'),
    path('pedidos/', views.pedidos_view, name='pedidos'),
    path('devoluciones/', views.devoluciones_view, name='devoluciones'),
    path('registro/', views.registro_view, name='registro'),
    path('logout/', views.logout_view, name='logout'),

    # PagosPayPal
    path('pago/exito/', views.pago_exito, name='pago_exito'),
    path('pago/cancelado/', views.pago_cancelado, name='pago_cancelado'),
    path('paypal/ipn/', views.paypal_ipn, name='paypal_ipn'),
    path('procesar_pago/', views.procesar_pago, name='procesar_pago'),
    path('confirmacion_pago/', views.confirmacion_pago, name='confirmacion_pago'),
    path('cancelar_pago/', views.cancelar_pago, name='cancelar_pago'),
    path('pedido/<int:pedido_id>/pdf/', views.generar_pdf_pedido, name='generar_pdf_pedido'),
    path('procesar-pedido/', views.procesar_pedido, name='procesar_pedido'),


]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
