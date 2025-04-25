from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

class UsuarioManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El email es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # encripta la contraseña
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class Usuario(AbstractBaseUser, PermissionsMixin):
    codigo_verificacion = models.CharField(max_length=100, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True)
    nombre = models.CharField(max_length=100)
    fecha_registro = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre']

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'usuarios'
 
class Producto(models.Model):
    tipo = models.CharField(max_length=50)
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2)
    precio_alquiler = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    stock = models.IntegerField(blank=True, null=True)
    fecha_publicacion = models.DateField(blank=True, null=True)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    
    def __str__(self):
        return self.titulo
    
    def save(self, *args, **kwargs):
            if self.stock < 0:
                raise ValueError("El stock no puede ser negativo.")
            super().save(*args, **kwargs)
    class Meta:
        db_table = 'productos'

class ListaDeseos(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, blank=True, null=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = 'lista_deseos'

class Resena(models.Model): 
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, blank=True, null=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, blank=True, null=True)
    calificacion = models.IntegerField(blank=True, null=True)
    comentario = models.TextField(blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'resenas'

class Transaccion(models.Model): 
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, blank=True, null=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, blank=True, null=True)
    tipo_transaccion = models.CharField(max_length=10)
    fecha = models.DateTimeField(blank=True, null=True)
    precio_pagado = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        if not self.fecha:
            self.fecha = timezone.now()  # Establecer la fecha automáticamente si no se pasa
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'transacciones'

class Carrito(models.Model):
    TIPO_CHOICES = [
        ('compra', 'Compra'),
        ('alquiler', 'Alquiler'),
    ]
    
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    cantidad = models.PositiveIntegerField(default=1)

    def save(self, *args, **kwargs):
        if self.tipo == 'compra' and self.producto.stock < self.cantidad:
            raise ValueError(f"No hay suficiente stock para comprar {self.cantidad} unidades de {self.producto.titulo}.")
        if self.tipo == 'alquiler' and self.producto.stock < self.cantidad:
            raise ValueError(f"No hay suficiente stock para alquilar {self.cantidad} unidades de {self.producto.titulo}.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.usuario.nombre} - {self.producto.titulo} ({self.tipo})'

    def get_total(self):
        if self.tipo == 'compra':
            return self.producto.precio_compra * self.cantidad
        else:
            return self.producto.precio_alquiler * self.cantidad

class Pedido(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Pedido #{self.id} de {self.usuario.nombre}"

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='items', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    tipo = models.CharField(max_length=10, choices=[('compra', 'Compra'), ('alquiler', 'Alquiler')])

    def precio_unitario(self):
        if self.tipo == 'compra':
            return self.producto.precio_compra
        elif self.tipo == 'alquiler' and self.producto.precio_alquiler:
            return self.producto.precio_alquiler
        return 0

    def subtotal(self):
        return self.cantidad * self.precio_unitario()

    def __str__(self):
        return f"Producto: {self.producto.titulo}, Tipo: {self.tipo}, Cantidad: {self.cantidad}"

    class Meta:
        db_table = 'item_pedido'
