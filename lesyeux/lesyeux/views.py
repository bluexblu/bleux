from django.shortcuts import render, get_object_or_404, redirect
from inventario.models import Producto, Transaccion
from django.utils import timezone

def index(request):
    query = request.GET.get('q', '')
    productos = Producto.objects.filter(titulo__icontains=query) if query else Producto.objects.all()
    return render(request, 'index.html', {'items': productos})

def producto_detail(request, pk):
    producto = get_object_or_404(Producto, pk=pk)

    if request.method == 'POST':
        accion = request.POST.get('accion')
        precio = producto.precio_compra if accion == 'comprar' else producto.precio_alquiler

        if precio:
            Transaccion.objects.create(
                usuario_id=1,  # Temporal: cambiar cuando uses autenticación real
                producto=producto,
                tipo_transaccion=accion,
                precio_pagado=precio,
                fecha=timezone.now()
            )

        return redirect('index')

    return render(request, 'detalle_item.html', {'item': producto})
