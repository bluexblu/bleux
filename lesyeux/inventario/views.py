from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import Producto

# Vista para la página de inicio
def home(request):
    return render(request, 'home.html')

# Vista para la lista de productos
def productos(request):
    productos = Producto.objects.all()  # Obtiene todos los productos
    return render(request, 'productos.html', {'productos': productos})

# Vista para una página de detalles de un producto
def producto_detalle(request, producto_id):
    producto = Producto.objects.get(id=producto_id)
    return render(request, 'producto_detalle.html', {'producto': producto})
