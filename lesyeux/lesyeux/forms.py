from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['tipo', 'titulo', 'descripcion', 'precio_compra', 'precio_alquiler', 'stock', 'fecha_publicacion']
        widgets = {
            'fecha_publicacion': forms.DateInput(attrs={'type': 'date'}),
        }
