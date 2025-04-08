from django.shortcuts import render, get_object_or_404, redirect
from .models import Producto, Transaccion
from .forms import ProductoForm
from django.utils import timezone

def index(request):
    query = request.GET.get('q', '')
    productos = Producto.objects.filter(titulo__icontains=query) if query else Producto.objects.all()
    return render(request, 'catalogo/index.html', {'items': productos})

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

    return render(request, 'catalogo/detalle_item.html', {'item': producto})

def producto_create(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ProductoForm()
    return render(request, 'catalogo/formulario_item.html', {'form': form})

def producto_edit(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('producto_detail', pk=pk)
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'catalogo/formulario_item.html', {'form': form})
