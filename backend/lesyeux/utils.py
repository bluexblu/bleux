# utils.py

from django.core.mail import send_mail
from django.conf import settings

def correo_verificacion(usuario_email, codigo_verificacion):
    """
    Función para enviar un correo de verificación al usuario con el código
    """
    asunto = "Código de Verificación"
    mensaje = f"Tu código de verificación es: {codigo_verificacion}"
    from_email = settings.DEFAULT_FROM_EMAIL  # Asumimos que usas settings.py para configurar el correo

    # Enviar correo
    send_mail(asunto, mensaje, from_email, [usuario_email])
