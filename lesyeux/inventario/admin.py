from django.contrib import admin
from .models import Usuario, Producto, ListaDeseos, Resena, Transaccion

# Registrar los modelos
admin.site.register(Usuario)
admin.site.register(Producto)
admin.site.register(ListaDeseos)
admin.site.register(Resena)
admin.site.register(Transaccion)
