from django.db import models

# Create your models here.

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.CharField(unique=True, max_length=100)
    password = models.TextField()
    fecha_registro = models.DateTimeField(blank=True, null=True)

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

    class Meta:
        db_table = 'transacciones'
