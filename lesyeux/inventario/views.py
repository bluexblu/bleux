from django import forms
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.shortcuts import render
from .models import Usuario, ListaDeseos
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.db import transaction
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.http import HttpResponse

from .models import Carrito, Producto, ListaDeseos  # Importa las clases necesarias
from inventario.models import Usuario, Producto, Transaccion, Resena, ListaDeseos, Carrito, Pedido, ItemPedido
from lesyeux.emails import enviar_correo_verificacion
from lesyeux.forms import RegistroForm
from lesyeux.serializers import MyTokenObtainPairSerializer
from lesyeux.forms import LoginForm

from paypal.standard.forms import PayPalPaymentsForm
from paypal.standard.ipn.models import PayPalIPN
from paypal.standard.ipn.signals import valid_ipn_received

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from django_ratelimit.decorators import ratelimit

import random
import string
import uuid

from django.shortcuts import render

def index(request):
    return render(request, 'index.html')


def producto_detail(request, pk):
    producto = get_object_or_404(Producto, pk=pk)

    if request.method == 'POST':
        accion = request.POST.get('accion')
        precio = producto.precio_compra if accion == 'comprar' else producto.precio_alquiler

        if precio and (producto.stock is None or producto.stock > 0):
            Transaccion.objects.create(
                usuario_id=1,  # Temporal
                producto=producto,
                tipo_transaccion=accion,
                precio_pagado=precio,
                fecha=timezone.now()
            )

            if producto.stock is not None:
                producto.stock -= 1
                producto.save()

        return redirect('catalogo')

    return render(request, 'detalle_item.html', {'item': producto})

# Listado de usuarios
def usuarios_list(request):
    usuarios = Usuario.objects.all()
    return render(request, 'usuarios.html', {'usuarios': usuarios})

# Listado de transacciones
def transacciones_list(request):
    transacciones = Transaccion.objects.select_related('usuario', 'producto').all()
    return render(request, 'transacciones.html', {'transacciones': transacciones})

# Reseñas por producto
def resenas_producto(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    resenas = Resena.objects.filter(producto=producto)
    return render(request, 'resenas.html', {'producto': producto, 'resenas': resenas})

# Lista de deseos por usuario
def lista_deseos(request, usuario_id):
    usuario = get_object_or_404(Usuario, pk=usuario_id)
    deseos = ListaDeseos.objects.select_related('producto').filter(usuario=usuario)
    return render(request, 'lista_deseos.html', {'usuario': usuario, 'deseos': deseos})

def catalogo(request):
   query = request.GET.get('q', '')
   productos = Producto.objects.filter(titulo__icontains=query) if query else Producto.objects.all()
   return render(request, 'catalogo.html', {'items': productos})

def usuarios(request):
    return render(request, 'usuarios.html')

def usuarios_list(request):
    usuarios = Usuario.objects.all().prefetch_related('listadeseos_set__producto')
    return render(request, 'usuarios_list.html', {'usuarios': usuarios})

def suscripcion(request):
    paypal_dict = {
        "business": "sb-xyemu38604524@business.example.com",
        "amount": "10.00",
        "item_name": "Suscripción Premium",
        "invoice": "unique-invoice-id-0001",
        "currency_code": "USD",
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return_url": request.build_absolute_uri('/gracias/'),
        "cancel_return": request.build_absolute_uri('/cancelado/'),
        "custom": "1",  # ID del usuario logueado
    }

    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'suscripcion.html', {'form': form})

def generar_codigo_verificacion():
    return ''.join(random.choices(string.digits, k=6))  # Un código de 6 dígitos.

# Función para enviar el correo
def correo_verificacion(email, codigo_verificacion):
    subject = 'Verificación de tu cuenta'
    message = f'Gracias por registrarte. Tu código de verificación es: {codigo_verificacion}. Verifica tu cuenta aquí: {settings.SITE_URL}/verificar/{codigo_verificacion}/'
    from_email = 'noreply@tudominio.com'
    
    send_mail(subject, message, from_email, [email])

# Carrito
def carrito_view(request):
    return render(request, 'carrito.html')

# Pedidos
def pedidos_view(request):
    return render(request, 'pedidos.html')

# Devoluciones
def devoluciones_view(request):
    return render(request, 'devoluciones.html')

# Registro (puedes adaptar esto según tu formulario)
def registro_view(request):
    return render(request, 'registro.html')

# Logout
def logout_view(request):
    logout(request)
    return redirect('login')

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')  # Redirige a la vista con el nombre 'index'
            else:
                form.add_error(None, 'Correo o contraseña incorrectos')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

# Si usas un modelo de usuario personalizado, reemplaza 'User' con 'get_user_model()'
def register_user(request):
    if request.method == "POST":
        nombre = request.POST.get('nombre')  # 👈 Capturamos el nombre
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not all([nombre, email, password]):
            return HttpResponse('Faltan datos.')

        # Crear usuario con nombre incluido
        user = User.objects.create_user(
            email=email,
            password=password,
            nombre=nombre  # 👈 Lo pasamos al manager
        )

        # Generar código de verificación
        codigo_verificacion = get_random_string(length=6, allowed_chars='0123456789')
        request.session['codigo_verificacion'] = codigo_verificacion

        correo_verificacion(user.email, codigo_verificacion)

        return HttpResponse('Usuario registrado y correo de verificación enviado.')
    return HttpResponse('Método no permitido.')


User = get_user_model()

def register_user(request):
    if request.method == "POST":
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not nombre or not email or not password:
            return HttpResponse("Todos los campos son obligatorios")

        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            nombre=nombre
        )

        codigo_verificacion = get_random_string(length=6, allowed_chars='0123456789')
        user.codigo_verificacion = codigo_verificacion
        user.save()

        request.session['codigo_verificacion'] = codigo_verificacion
        correo_verificacion(user.email, codigo_verificacion)

        return HttpResponse('Usuario registrado y correo de verificación enviado.')
    
    return render(request, 'index.html')


def index(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.codigo_verificacion = str(uuid.uuid4())
            usuario.is_active = False
            usuario.save()
            enviar_correo_verificacion(usuario, usuario.codigo_verificacion)
            return render(request, 'verificacion_enviada.html')
    else:
        form = RegistroForm()
    return render(request, 'index.html', {'form': form})

def enviar_correo_verificacion(usuario, codigo_verificacion):
    asunto = 'Verifica tu cuenta en LesYeux 👁️'
    mensaje = f"""
Hola {usuario.nombres},

¡Gracias por registrarte en LesYeux!

Para activar tu cuenta, por favor haz clic en el siguiente enlace de verificación:

{settings.SITE_URL}/verificar/{codigo_verificacion}/

Si no realizaste este registro, simplemente ignora este mensaje.

Atentamente,  
El equipo de LesYeux
"""

    send_mail(
        asunto,
        mensaje,
        settings.DEFAULT_FROM_EMAIL,
        [usuario.email],
        fail_silently=False,
    )

def clean_email(self):
    email = self.cleaned_data.get('email')
    if Usuario.objects.filter(email=email).exists():
        raise forms.ValidationError('Este correo ya está registrado.')
    return email

def pago_paypal(request):
    paypal_dict = {
        "business": "sb-xyemu38604524@business.example.com",  # Asegúrate de usar tu correo de PayPal
        "amount": "10.00",  # El monto a pagar
        "item_name": "Producto de ejemplo",  # El nombre del producto
        "invoice": "0001",  # Un identificador único para la compra
        "currency_code": "USD",  # El código de la moneda
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),  # La URL IPN de PayPal
        "return_url": request.build_absolute_uri('/pago-exitoso/'),  # URL de éxito
        "cancel_return": request.build_absolute_uri('/pago-cancelado/'),  # URL de cancelación
    }

    form = PayPalPaymentsForm(initial=paypal_dict)  # Crear el formulario de PayPal

    context = {"form": form}
    return render(request, "suscripcion.html", context)  # Renderiza el HTML con el formulario

def ipn_handler(sender, **kwargs):
    ipn_obj = sender  # El objeto IPN recibido

    if ipn_obj.payment_status == "Completed":  # Si el pago fue completado
        # Obtener el usuario y producto relacionados al pago
        usuario_id = ipn_obj.custom  # Aquí se asume que 'custom' contiene el ID del usuario
        producto_titulo = ipn_obj.item_name  # Aquí se asume que 'item_name' contiene el nombre del producto

        # Obtener el usuario y producto desde la base de datos
        try:
            usuario = Usuario.objects.get(id=usuario_id)
            producto = Producto.objects.get(titulo=producto_titulo)
        except Usuario.DoesNotExist or Producto.DoesNotExist:
            # Manejar error si el usuario o producto no existen
            print(f"Usuario o Producto no encontrado.")
            return

        # Crear una nueva transacción
        transaccion = Transaccion.objects.create(
            usuario=usuario,
            producto=producto,
            tipo_transaccion="Compra",  # O "Alquiler", dependiendo del tipo de transacción
            fecha=timezone.now(),
            precio_pagado=ipn_obj.mc_gross,  # Precio pagado en el IPN
        )
        transaccion.save()
        print(f"Pago guardado para {usuario.nombre} por {producto.titulo}")

    else:
        print(f"El pago no fue completado o hubo un error: {ipn_obj.payment_status}")

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

def test_login():
    user = authenticate(email='admin@admin.com', password='123456')
    print(user)

@ratelimit(key='ip', rate='5/m', block=True)
def my_password_reset_view(request):
    ...

def producto_detail(request, pk):
    producto = get_object_or_404(Producto, pk=pk)

    if request.method == 'POST':
        accion = request.POST.get('accion')

        if accion in ['agregar_compra', 'agregar_alquiler']:
            tipo = 'compra' if accion == 'agregar_compra' else 'alquiler'
            cantidad = 1  # puedes cambiarlo si luego agregas input para elegir cantidad

            if request.user.is_authenticated:
                Carrito.objects.create(
                    usuario=request.user,
                    producto=producto,
                    cantidad=cantidad,
                    tipo=tipo
                )
                messages.success(request, f'Producto añadido al carrito para {tipo}.')
            else:
                carrito = request.session.get('carrito', [])
                carrito.append({
                    'producto_id': producto.id,
                    'cantidad': cantidad,
                    'tipo': tipo
                })
                request.session['carrito'] = carrito
                messages.success(request, f'Producto guardado en el carrito para {tipo}. Inicia sesión para completar la compra.')

            return redirect('carrito')

        elif accion == 'deseos':
            if request.user.is_authenticated:
                ListaDeseos.objects.get_or_create(usuario=request.user, producto=producto)
                messages.success(request, 'Producto añadido a tu lista de deseos.')
            else:
                messages.warning(request, 'Debes iniciar sesión para guardar productos en tu lista de deseos.')
                return redirect('login')

    return render(request, 'producto_detail.html', {'producto': producto})


def carrito_view(request):
    carrito_data = []
    total = 0

    if request.user.is_authenticated:
        items = Carrito.objects.filter(usuario=request.user)
        for item in items:
            precio_unitario = item.producto.precio_compra if item.tipo == 'compra' else item.producto.precio_alquiler
            total_producto = precio_unitario * item.cantidad
            carrito_data.append({
                'producto': item.producto,
                'cantidad': item.cantidad,
                'precio_unitario': precio_unitario,
                'total': total_producto
            })
            total += total_producto

    else:
        carrito_sesion = request.session.get('carrito', [])
        for item in carrito_sesion:
            try:
                producto = Producto.objects.get(pk=item['producto_id'])
                precio_unitario = producto.precio_compra if item['tipo'] == 'compra' else producto.precio_alquiler
                total_producto = precio_unitario * item['cantidad']
                carrito_data.append({
                    'producto': producto,
                    'cantidad': item['cantidad'],
                    'precio_unitario': precio_unitario,
                    'total': total_producto
                })
                total += total_producto
            except Producto.DoesNotExist:
                continue

    return render(request, 'carrito.html', {'carrito_data': carrito_data, 'total': total})

@login_required
def agregar_a_lista_deseos(request, producto_id):
    producto = Producto.objects.get(id=producto_id)
    
    # Verifica si el producto ya está en la lista de deseos
    lista_deseos_item, created = ListaDeseos.objects.get_or_create(
        usuario=request.user, producto=producto
    )
    
    return redirect('lista_deseos')  # Redirige a la vista de lista de deseos

@login_required
def ver_lista_deseos(request):
    lista_deseos_items = ListaDeseos.objects.filter(usuario=request.user)

    return render(request, 'lista_deseos.html', {
        'lista_deseos_items': lista_deseos_items,
    })

@login_required
def pago_paypal(request):
    carrito_items = Carrito.objects.filter(usuario=request.user)
    total = sum(item.get_total() for item in carrito_items)

    # Aquí iría la integración con PayPal, pero para simplificar
    # se muestra solo el total de la compra.
    
    # Después de la compra exitosa, se puede crear una transacción.
    # Aquí es donde se manejarían las transacciones
    # y se eliminarían los productos del carrito.

    return render(request, 'pago_paypal.html', {'total': total})
  
@login_required
def procesar_pago(request):
    if request.method == 'POST':
        # Obtener los productos del carrito del usuario
        carrito_items = Carrito.objects.filter(usuario=request.user)

        if not carrito_items:
            return redirect('carrito')  # Si el carrito está vacío

        total = 0
        for item in carrito_items:
            precio = item.producto.precio_compra if item.tipo == 'compra' else item.producto.precio_alquiler
            total += precio * item.cantidad

        # Redirigir al template donde se genera el formulario de PayPal
        return render(request, 'pago_paypal.html', {'total': total})

    return redirect('carrito')

def pago_exito(request):
    messages.success(request, "¡Pago completado con éxito!")
    return redirect('index')  # Redirige al índice o a la página que prefieras

def pago_cancelado(request):
    messages.error(request, "El pago fue cancelado.")
    return redirect('carrito')  # Redirige al carrito

def paypal_ipn(request):
    # Aquí iría la lógica para procesar las IPN de PayPal
    return redirect('index')  # Redirige al índice después de procesar el IPN

@login_required
def confirmacion_pago(request):
    carrito_items = Carrito.objects.filter(usuario=request.user)

    if not carrito_items:
        return redirect('carrito')

    total = 0
    pedido = Pedido.objects.create(usuario=request.user, total=0)  # total se actualizará luego

    for item in carrito_items:
        precio_unitario = item.producto.precio_compra if item.tipo == 'compra' else item.producto.precio_alquiler
        subtotal = precio_unitario * item.cantidad
        total += subtotal

        ItemPedido.objects.create(
            pedido=pedido,
            producto=item.producto,
            cantidad=item.cantidad,
            tipo=item.tipo,
            precio_unitario=precio_unitario
        )

    pedido.total = total
    pedido.save()

    carrito_items.delete()  # Vaciar carrito

    return render(request, 'confirmacion_pago.html', {'pedido': pedido})

@login_required
def cancelar_pago(request):
    messages.error(request, "El pago fue cancelado.")
    return render(request, 'cancelar_pago.html')

def agregar_al_carrito(request, producto_id, cantidad, tipo):
    if request.user.is_authenticated:
        # Guardar en el modelo Carrito como ya haces
        ...
    else:
        carrito = request.session.get('carrito', [])
        carrito.append({
            'producto_id': producto_id,
            'cantidad': cantidad,
            'tipo': tipo
        })
        request.session['carrito'] = carrito
    return redirect('carrito')

@login_required
def mis_pedidos(request):
    pedidos = Pedido.objects.filter(usuario=request.user).order_by('-fecha')
    return render(request, 'mis_pedidos.html', {'pedidos': pedidos})

def render_to_pdf(template_src, context_dict):
    """
    Función para renderizar un PDF a partir de una plantilla HTML usando xhtml2pdf.
    """
    # Renderiza la plantilla HTML con el contexto proporcionado
    html_string = render_to_string(template_src, context_dict)
    
    # Crea una respuesta HTTP con el tipo de contenido como PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="pedido.pdf"'
    
    # Genera el PDF a partir del HTML
    pisa_status = pisa.CreatePDF(html_string, dest=response)
    
    # Verifica si hubo algún error al generar el PDF
    if pisa_status.err:
        return HttpResponse('Error generando el PDF')
    
    return response

def generar_pdf_pedido(request, pedido_id):
    """
    Vista para generar el PDF de un pedido.
    """
    # Obtiene el pedido por ID o 404 si no existe
    pedido = get_object_or_404(Pedido, pk=pedido_id)
    
    # Recupera los items asociados al pedido
    items = pedido.items.all()
    
    # Crea el contexto para la plantilla HTML
    contexto = {
        'pedido': pedido,
        'items': items,
    }
    
    # Llama a la función que genera el PDF y devuelve la respuesta
    return render_to_pdf('pedido_pdf.html', contexto)
@property
def precio_unitario_display(self):
    return self.precio_unitario()

@transaction.atomic
def procesar_pedido(request):
    usuario = request.user
    carrito = Carrito.objects.filter(usuario=usuario)

    if not carrito.exists():
        # Aquí puedes redirigir a un mensaje o página de "carrito vacío"
        return redirect('carrito_vacio') 

    total = sum(item.get_total() for item in carrito)

    pedido = Pedido.objects.create(usuario=usuario, total=total)

    for item in carrito:
        ItemPedido.objects.create(
            pedido=pedido,
            producto=item.producto,
            cantidad=item.cantidad,
            tipo=item.tipo
        )

    carrito.delete()  # Limpiar carrito después de procesar

    return redirect('generar_pdf_pedido', pedido_id=pedido.id)

def peliculas_view(request):
    peliculas = Producto.objects.filter(tipo__iexact='pelicula')
    return render(request, 'peliculas.html', {'peliculas': peliculas})

def series_view(request):
    series = Producto.objects.filter(tipo__iexact='serie')
    return render(request, 'series.html', {'series': series})

def comics_view(request):
    comics = Producto.objects.filter(tipo__iexact='comic')
    return render(request, 'comics.html', {'comics': comics})

def planes(request):
    return render(request, 'planes.html')

def metodos_pago(request):
    return render(request, 'metodos_pago.html')

def historial_suscripcion(request):
    return render(request, 'historial_suscripcion.html')


