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
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.forms import PasswordResetForm
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from .models import Carrito, Producto, ListaDeseos  # Importa las clases necesarias
from lesyeux.inventario.models import Usuario, Producto, Transaccion, Resena, ListaDeseos, Carrito, Pedido, ItemPedido
from lesyeux.emails import enviar_correo_verificacion
from lesyeux.staticfiles.forms import RegistroForm
from lesyeux.serializers import MyTokenObtainPairSerializer, UsuarioSerializer, ProductoSerializer, ListaDeseosSerializer, ResenaSerializer, TransaccionSerializer, CarritoSerializer, PedidoSerializer, ItemPedidoSerializer, SuscripcionSerializer, LoginSerializer
from lesyeux.utils import correo_verificacion
from lesyeux.serializers import UsuarioSerializer
from paypal.standard.forms import PayPalPaymentsForm
from paypal.standard.ipn.models import PayPalIPN
from paypal.standard.ipn.signals import valid_ipn_received

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import viewsets

from django_ratelimit.decorators import ratelimit
from django.http import JsonResponse
import random
import string
import uuid
import json
from django.shortcuts import render
import os 



def frontend(request):
    return render(request, 'frontend/index.html') 

def index(request):
    index_path = os.path.join(settings.BASE_DIR.parent, 'frontend', 'build', 'index.html')
    with open(index_path, 'r', encoding='utf-8') as f:
        return HttpResponse(f.read())
    
class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

# Listado de usuarios
class UsuarioList(APIView):
    def get(self, request):
        usuarios = Usuario.objects.all()  # Obtén todos los usuarios de la base de datos
        serializer = UsuarioSerializer(usuarios, many=True)  # Serializa los usuarios
        return Response(serializer.data)
    
#Transacciones
class TransaccionViewSet(viewsets.ModelViewSet):
    queryset = Transaccion.objects.select_related('usuario', 'producto').all()
    serializer_class = TransaccionSerializer

#Resenas
@api_view(['GET'])
def resenas_producto(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    resenas = Resena.objects.filter(producto=producto)
    serializer = ResenaSerializer(resenas, many=True)
    return Response(serializer.data)

# Lista de deseos por usuario
def lista_deseos(request, usuario_id):
    usuario = get_object_or_404(Usuario, pk=usuario_id)
    
    # Obtener los productos deseados del usuario
    deseos = ListaDeseos.objects.select_related('producto').filter(usuario=usuario)
    
    # Usamos el serializador para convertir los deseos a un formato JSON
    serializer = ListaDeseosSerializer(deseos, many=True)

    # Crear la respuesta
    return JsonResponse({
        'usuario': usuario.nombre,
        'deseos': serializer.data  # Usamos el serializer para devolver los deseos formateados
    })

@api_view(['GET'])
def catalogo_api(request):
    query = request.GET.get('q', '')  # Filtrar productos por título si se pasa un parámetro 'q'
    productos = Producto.objects.filter(titulo__icontains=query) if query else Producto.objects.all()
    
    # Serializar los productos
    serializer = ProductoSerializer(productos, many=True)
    
    # Devolver los datos serializados como JSON
    return Response(serializer.data)

#Suscripcion
class SuscripcionView(APIView):
    def post(self, request):
        serializer = SuscripcionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def generar_codigo_verificacion(request):
    codigo = ''.join(random.choices(string.digits, k=6))
    return JsonResponse({'codigo_verificacion': codigo})

# Función para enviar el correo
def enviar_correo_verificacion(request, email):
    # Generar el código de verificación
    codigo_verificacion = generar_codigo_verificacion()

    # Enviar el correo
    subject = 'Verificación de tu cuenta'
    message = f'Gracias por registrarte. Tu código de verificación es: {codigo_verificacion}. Verifica tu cuenta aquí: {settings.SITE_URL}/verificar/{codigo_verificacion}/'
    from_email = 'noreply@tudominio.com'
    
    send_mail(subject, message, from_email, [email])

    # Retornar el código para efectos de confirmación en el frontend
    return JsonResponse({'mensaje': 'Correo enviado exitosamente', 'codigo_verificacion': codigo_verificacion})

#Carrito
def carrito_view(request):
    # Obtén el carrito desde la sesión o base de datos
    carrito = request.session.get('carrito', [])
    
    # Serializamos los datos del carrito
    carrito_serializado = CarritoSerializer(carrito, many=True)
    
    # Devolver los datos del carrito en formato JSON
    return JsonResponse(carrito_serializado.data, safe=False)

# Pedidos
def pedidos_view(request):
    # Obtener los pedidos del usuario logueado
    if request.user.is_authenticated:
        pedidos = Pedido.objects.filter(usuario=request.user)
    else:
        pedidos = []

    # Serializar los pedidos (esto depende de cómo quieras mostrar los datos)
    pedidos_data = list(pedidos.values('id', 'producto', 'cantidad', 'estado', 'fecha_pedido'))

    # Devolver los pedidos en formato JSON
    return JsonResponse(pedidos_data, safe=False)

#Registro 
@csrf_exempt
def registro_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            serializer = UsuarioSerializer(data=data)

            if serializer.is_valid():
                # Serializamos los datos antes de guardar el usuario
                user = serializer.save(password=make_password(data['password']))  # Si deseas encriptar la contraseña antes de guardar
                return JsonResponse({'message': 'Usuario registrado exitosamente'}, status=201)
            else:
                return JsonResponse({'error': serializer.errors}, status=400)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'message': 'Método no permitido'}, status=405)

# Logout
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            
            user = authenticate(request, email=email, password=password)

            if user is not None:
                # Generamos el JWT usando `RefreshToken`
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                    }
                }, status=status.HTTP_200_OK)

            return Response({
                'nonFieldErrors': ['Credenciales incorrectas']
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Verifica aun
@api_view(['POST'])
def register_user(request):
    if request.method == "POST":
        data = request.data
        
        # Validar si faltan campos
        if not data.get('nombre') or not data.get('email') or not data.get('password'):
            return Response({"error": "Todos los campos son obligatorios"}, status=status.HTTP_400_BAD_REQUEST)

        # Crear usuario
        usuario = get_user_model().objects.create_user(
            email=data['email'],
            password=data['password'],
            nombre=data['nombre']
        )

        # Generar código de verificación
        codigo_verificacion = get_random_string(length=6, allowed_chars='0123456789')
        usuario.codigo_verificacion = codigo_verificacion
        usuario.save()

        # Enviar correo de verificación
        send_mail(
            'Código de verificación',
            f'Tu código de verificación es: {codigo_verificacion}',
            'no-reply@tusitio.com',
            [usuario.email],
            fail_silently=False,
        )

        return Response({"message": "Usuario registrado y correo de verificación enviado."}, status=status.HTTP_201_CREATED)

    return Response({"error": "Método no permitido"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


########################################
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
    asunto = 'Verifica tu cuenta en LesYeux'
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
#####################################################################################
class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Crea el usuario
            return Response({"message": "Usuario registrado con éxito!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

    form = PayPalPaymentsForm(initial=paypal_dict)

    # Devuelve el formulario como HTML
    return JsonResponse({'form_html': str(form)})

@csrf_exempt
def ipn_handler(request):
    # Recibe los datos de la IPN enviados por PayPal
    ipn_obj = PayPalIPN(request.POST)
    
    # Verifica que la IPN es válida
    if ipn_obj.payment_status == "Completed":  # Si el pago fue completado
        # Obtener el usuario y producto relacionados al pago
        usuario_id = ipn_obj.custom  # Aquí se asume que 'custom' contiene el ID del usuario
        producto_titulo = ipn_obj.item_name  # Aquí se asume que 'item_name' contiene el nombre del producto

        try:
            # Obtener el usuario y producto desde la base de datos
            usuario = Usuario.objects.get(id=usuario_id)
            producto = Producto.objects.get(titulo=producto_titulo)
        except Usuario.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Usuario no encontrado.'}, status=400)
        except Producto.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Producto no encontrado.'}, status=400)

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

        return JsonResponse({'status': 'success', 'message': 'Transacción guardada.'})

    else:
        print(f"El pago no fue completado o hubo un error: {ipn_obj.payment_status}")
        return JsonResponse({'status': 'error', 'message': 'El pago no fue completado o hubo un error.'}, status=400)

import requests

def validate_ipn(ipn_obj):
    pay_pal_url = "https://www.paypal.com/cgi-bin/webscr"
    params = {
        "cmd": "_notify-validate",
        **ipn_obj.POST  # Datos que recibimos de PayPal
    }
    
    # Realizar la validación con PayPal
    response = requests.post(pay_pal_url, data=params)
    
    if response.text == "VERIFIED":
        # La IPN es válida
        return True
    else:
        # La IPN no es válida
        return False

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['POST'])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')
    
    # Autenticar al usuario
    user = authenticate(request, email=email, password=password)
    
    if user is not None:
        # Generar token JWT
        refresh = RefreshToken.for_user(user)
        return Response({
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
        })
    else:
        return Response({'error': 'Invalid credentials'}, status=400)

#Recuperacion de Contrasena
@csrf_exempt
@ratelimit(key='ip', rate='5/m', block=True)  # Limita a 5 peticiones por minuto por IP
@require_POST
def my_password_reset_view(request):
    email = request.POST.get('email')

    # Validar si el correo está registrado
    try:
        user = Usuario.objects.get(email=email)
    except Usuario.DoesNotExist:
        return JsonResponse({'error': 'Correo no registrado'}, status=400)

    # Crear formulario de reset de contraseña
    form = PasswordResetForm({'email': email})
    if form.is_valid():
        # Enviar correo de reset
        form.save(
            request=request,
            email_template_name='password_reset_email.html',
            subject_template_name='password_reset_subject.txt',
        )
        return JsonResponse({'message': 'Correo de restablecimiento enviado correctamente'}, status=200)
    else:
        return JsonResponse({'error': 'Error en el formulario de restablecimiento'}, status=400)

#Lista de Productos
@api_view(['GET', 'POST'])
def producto_detail(request, pk):
    producto = get_object_or_404(Producto, pk=pk)

    if request.method == 'GET':
        serializer = ProductoSerializer(producto)
        return JsonResponse(serializer.data)

    elif request.method == 'POST':
        accion = request.data.get('accion')

        if accion in ['agregar_compra', 'agregar_alquiler']:
            tipo = 'compra' if accion == 'agregar_compra' else 'alquiler'
            cantidad = 1  # Cambia esto si luego agregas un campo para seleccionar la cantidad

            if request.user.is_authenticated:
                Carrito.objects.create(
                    usuario=request.user,
                    producto=producto,
                    cantidad=cantidad,
                    tipo=tipo
                )
                return JsonResponse({'message': f'Producto añadido al carrito para {tipo}.'})
            else:
                carrito = request.session.get('carrito', [])
                carrito.append({
                    'producto_id': producto.id,
                    'cantidad': cantidad,
                    'tipo': tipo
                })
                request.session['carrito'] = carrito
                return JsonResponse({'message': f'Producto guardado en el carrito para {tipo}. Inicia sesión para completar la compra.'})

        elif accion == 'deseos':
            if request.user.is_authenticated:
                ListaDeseos.objects.get_or_create(usuario=request.user, producto=producto)
                return JsonResponse({'message': 'Producto añadido a tu lista de deseos.'})
            else:
                return JsonResponse({'error': 'Debes iniciar sesión para guardar productos en tu lista de deseos.'}, status=400)

    return JsonResponse({'error': 'Acción no válida'}, status=400)

# Lista de Deseos
@login_required
@api_view(['POST'])
def agregar_a_lista_deseos(request, producto_id):
    try:
        # Obtener el producto
        producto = Producto.objects.get(id=producto_id)

        # Verifica si el producto ya está en la lista de deseos
        lista_deseos_item, created = ListaDeseos.objects.get_or_create(
            usuario=request.user, producto=producto
        )

        # Si se crea un nuevo item en la lista de deseos, devolver una respuesta exitosa con el serializador
        if created:
            # Serializa el item de la lista de deseos para incluir en la respuesta
            serializer = ListaDeseosSerializer(lista_deseos_item)
            return Response({'success': True, 'message': 'Producto agregado a la lista de deseos.', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({'success': False, 'message': 'El producto ya está en tu lista de deseos.'}, status=status.HTTP_400_BAD_REQUEST)

    except Producto.DoesNotExist:
        return Response({'success': False, 'message': 'Producto no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
    
@login_required
@api_view(['GET'])
def ver_lista_deseos(request):
    # Obtener los items de la lista de deseos del usuario autenticado
    lista_deseos_items = ListaDeseos.objects.filter(usuario=request.user)

    # Serializar los items de la lista de deseos
    serializer = ListaDeseosSerializer(lista_deseos_items, many=True)

    # Devolver los datos serializados en la respuesta
    return Response({
        'success': True,
        'lista_deseos_items': serializer.data,
    })

#Pagos con Paypal
@api_view(['GET'])
@login_required
def pago_paypal(request):
    carrito_items = Carrito.objects.filter(usuario=request.user)
    carrito_serializado = CarritoSerializer(carrito_items, many=True)

    total = sum(item.get_total() for item in carrito_items)

    return Response({
        'success': True,
        'total': total,
        'carrito': carrito_serializado.data,  # Datos del carrito serializados
    })

def pago_exito(request):
    # Aquí se pueden agregar más lógica para manejar el éxito del pago, como crear transacciones, etc.
    messages.success(request, "¡Pago completado con éxito!")
    
    # Responde con un JSON que le indique al frontend que el pago fue exitoso y que debe redirigir.
    return JsonResponse({'success': True, 'redirect_url': '/'})  # Aquí puedes cambiar el URL de redirección

@api_view(['POST'])
@login_required
def procesar_pago(request):
    carrito_items = Carrito.objects.filter(usuario=request.user)

    if not carrito_items:
        return Response({'success': False, 'message': 'El carrito está vacío.'}, status=400)

    total = 0
    carrito_serializado = CarritoSerializer(carrito_items, many=True)

    # Calcular el total
    for item in carrito_items:
        precio = item.producto.precio_compra if item.tipo == 'compra' else item.producto.precio_alquiler
        total += precio * item.cantidad

    # Aquí iría la lógica para integrar con PayPal, por ejemplo, generar un enlace a la página de PayPal
    paypal_url = f"https://www.paypal.com/cgi-bin/webscr?cmd=_xclick&business=sb-xyemu38604524@business.example.com&amount={total}&currency_code=USD"

    return Response({
        'success': True,
        'paypal_url': paypal_url,
        'carrito': carrito_serializado.data,  # Enviamos los datos serializados del carrito
        'total': total
    })

@api_view(['POST'])
def paypal_ipn(request):
    # Lógica para procesar el IPN de PayPal.
    # Verifica el mensaje de IPN con PayPal y actualiza el estado de la transacción.

    # Una vez procesado el IPN, responder con un JSON
    return Response({
        'success': True,
        'redirect_url': '/index',  # Redirige al índice o página principal
    })

@api_view(['POST'])
def pago_cancelado(request):
    # Lógica adicional si lo deseas
    messages.error(request, "El pago fue cancelado.")
    
    # Responde con un JSON que indique al frontend que el pago fue cancelado y redirige al carrito
    return Response({
        'success': True,
        'redirect_url': '/carrito',  # Redirigir al carrito
    })

@api_view(['POST'])
@login_required
def confirmacion_pago(request):
    carrito_items = Carrito.objects.filter(usuario=request.user)

    if not carrito_items:
        return Response({'success': False, 'message': 'El carrito está vacío.'}, status=400)

    total = 0
    pedido = Pedido.objects.create(usuario=request.user, total=0)  # Total se actualizará luego

    for item in carrito_items:
        precio_unitario = item.producto.precio_compra if item.tipo == 'compra' else item.producto.precio_alquiler
        subtotal = precio_unitario * item.cantidad
        total += subtotal

        # Crear el item en el pedido
        ItemPedido.objects.create(
            pedido=pedido,
            producto=item.producto,
            cantidad=item.cantidad,
            tipo=item.tipo,
            precio_unitario=precio_unitario
        )

    # Actualizar el total del pedido
    pedido.total = total
    pedido.save()

    # Vaciar el carrito después de confirmar el pedido
    carrito_items.delete()

    # Serializar el pedido con sus items
    pedido_serializado = PedidoSerializer(pedido)

    # Enviar respuesta al frontend
    return Response({
        'success': True,
        'redirect_url': '/confirmacion-pago/',
        'pedido': pedido_serializado.data  # Incluimos el pedido serializado
    })

@api_view(['POST'])
def pago_exito(request):
    # Agregar más lógica si se desea (como crear una transacción en la base de datos)

    # Mensaje de éxito para el usuario
    messages.success(request, "¡Pago completado con éxito!")
    
    # Responde con un JSON que indique al frontend que el pago fue exitoso y que debe redirigir
    return Response({
        'success': True,
        'redirect_url': '/',  # Redirige a la página principal (puedes cambiar este URL)
    })



#Carrito
@api_view(['POST'])
@login_required
def agregar_al_carrito(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        producto_id = data.get('producto_id')
        cantidad = data.get('cantidad')
        tipo = data.get('tipo')

        if request.user.is_authenticated:
            # Guardar en el modelo Carrito para usuarios autenticados
            carrito_item, created = Carrito.objects.get_or_create(
                usuario=request.user,
                producto_id=producto_id,
                tipo=tipo
            )
            carrito_item.cantidad += cantidad  # Aumentar la cantidad si el producto ya está en el carrito
            carrito_item.save()
            
            # Serializar el carrito después de la adición
            carrito_data = Carrito.objects.filter(usuario=request.user)
            carrito_serializado = CarritoSerializer(carrito_data, many=True)
            success = True
            return Response({
                'success': success,
                'carrito': carrito_serializado.data  # Retornar el carrito actualizado
            })
        else:
            # Guardar en la sesión para usuarios no autenticados
            carrito = request.session.get('carrito', [])
            # Verifica si el producto ya existe en el carrito de sesión
            existing_item = next((item for item in carrito if item['producto_id'] == producto_id and item['tipo'] == tipo), None)
            if existing_item:
                existing_item['cantidad'] += cantidad  # Aumentar la cantidad si ya está en el carrito
            else:
                carrito.append({
                    'producto_id': producto_id,
                    'cantidad': cantidad,
                    'tipo': tipo
                })
            request.session['carrito'] = carrito
            success = True

            return JsonResponse({
                'success': success,
                'carrito': carrito  # Retornar el carrito actualizado de sesión
            })

    return JsonResponse({'success': False}, status=400)


@login_required
def mis_pedidos(request):
    # Obtener los pedidos del usuario actual y ordenarlos por fecha
    pedidos = Pedido.objects.filter(usuario=request.user).order_by('-fecha')

    # Convertir los pedidos a un formato que se pueda devolver como JSON
    pedidos_data = []
    for pedido in pedidos:
        pedidos_data.append({
            'id': pedido.id,
            'fecha': pedido.fecha.strftime('%Y-%m-%d %H:%M:%S'),
            'total': pedido.total,
            'estado': pedido.estado,
        })

    # Devolver los pedidos en formato JSON
    return JsonResponse({'pedidos': pedidos_data})

#PDF
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

@login_required
def generar_pdf_pedido(request, pedido_id):
    # Obtener el pedido desde la base de datos
    try:
        pedido = Pedido.objects.get(id=pedido_id, usuario=request.user)
    except Pedido.DoesNotExist:
        return HttpResponse('Pedido no encontrado o no autorizado')

    # Crear el contexto para pasar a la plantilla PDF
    context = {
        'pedido': pedido,
        'items': pedido.productos.all(),  # Asumiendo que tienes productos relacionados con el pedido
    }

    # Llamar a la función para generar el PDF
    return render_to_pdf('pedido_pdf.html', context)

@property
def precio_unitario_display(self):
    return f"${self.precio_unitario:.2f}"

def procesar_pedido(request):
    usuario = request.user
    carrito = Carrito.objects.filter(usuario=usuario)

    if not carrito.exists():
        return redirect('carrito_vacio')  # Si el carrito está vacío, redirige.

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

    return JsonResponse({'redirect': f'/generar_pdf_pedido/{pedido.id}/'})

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


