from django.shortcuts import render, get_object_or_404, redirect
from inventario.models import Usuario, Producto, Transaccion, Resena, ListaDeseos
from django.utils import timezone
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

def suscripcion(request):
    return render(request, 'suscripcion.html')
