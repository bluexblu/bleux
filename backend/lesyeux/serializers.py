from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from lesyeux.inventario.models import Usuario, Producto, ListaDeseos, Resena, Suscripcion, Transaccion,  Carrito,Pedido, ItemPedido

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'  # Usar el campo email como identificador en lugar del username

    def validate(self, attrs):
        # Obtener email y contraseña del request
        email = attrs.get("email")
        password = attrs.get("password")

        # Verificar si el usuario existe y si las credenciales son correctas
        user = authenticate(request=self.context.get("request"), email=email, password=password)

        if user is None:
            raise serializers.ValidationError("Credenciales inválidas")

        # Obtener el token de acceso y el token de actualización
        refresh = self.get_token(user)

        # Retornar los tokens y la información del usuario
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user_id": user.id,
            "email": user.email,
        }

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        # Verifica si el correo ya está registrado en la base de datos
        if Usuario.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este correo ya está registrado.")
        return value

    def create(self, validated_data):
        # Lógica para crear un usuario, si es necesario
        # Podrías agregar aquí la creación del código de verificación, si corresponde
        user = Usuario.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            nombre=validated_data['nombre']
        )
        return user
    
# Serializador para el modelo Producto
class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

# Serializador para el modelo ListaDeseos
class ListaDeseosSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer()  # Para incluir la información del producto en la lista de deseos
    usuario = UsuarioSerializer()   # Para incluir la información del usuario

    class Meta:
        model = ListaDeseos
        fields = '__all__'

# Serializador para el modelo Resena
class ResenaSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer()  # Información del producto reseñado
    usuario = UsuarioSerializer()   # Información del usuario que hizo la reseña

    class Meta:
        model = Resena
        fields = '__all__'

# Serializador para el modelo Transaccion
class TransaccionSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer()  # Información del producto en la transacción
    usuario = UsuarioSerializer()   # Información del usuario que hizo la transacción

    class Meta:
        model = Transaccion
        fields = '__all__'

# Serializador para el modelo Carrito
class CarritoSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer()  # Información del producto en el carrito
    usuario = UsuarioSerializer()   # Información del usuario

    total = serializers.SerializerMethodField()  # Campo para el total

    class Meta:
        model = Carrito
        fields = '__all__'

    def get_total(self, obj):
        # Asume que hay un método `get_total()` en el modelo Carrito
        if obj.tipo == 'compra':
            return obj.producto.precio_compra * obj.cantidad
        return obj.producto.precio_alquiler * obj.cantidad
    
# Serializador para el modelo Pedido
class PedidoSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer()  # Información del usuario que hizo el pedido
    items = serializers.SerializerMethodField()  # Campo para obtener los items del pedido

    class Meta:
        model = Pedido
        fields = '__all__'

    def get_items(self, obj):
        # Obtén los items asociados al pedido
        items = ItemPedido.objects.filter(pedido=obj)
        return ItemPedidoSerializer(items, many=True).data

# Serializador para el modelo ItemPedido
class ItemPedidoSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer()  # Información del producto del item
    total = serializers.SerializerMethodField()  # Campo para obtener el subtotal

    class Meta:
        model = ItemPedido
        fields = '__all__'

    def get_total(self, obj):
        # Calcula el total basado en la cantidad y el precio unitario
        return obj.producto.precio_compra * obj.cantidad if obj.tipo == 'compra' else obj.producto.precio_alquiler * obj.cantidad
    
class TransaccionResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    message = serializers.CharField()


class SuscripcionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suscripcion
        fields = '__all__'


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

