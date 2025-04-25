from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import send_mail

def enviar_correo(destinatario, asunto, template, contexto):
    """
    Envía un correo usando un template HTML y un diccionario de contexto.
    """
    contenido_html = render_to_string(template, contexto)
    
    correo = EmailMessage(
        subject=asunto,
        body=contenido_html,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[destinatario],
    )
    correo.content_subtype = 'html'
    correo.send()


# Funciones específicas

def enviar_codigo_verificacion(user, codigo):
    enviar_correo(
        destinatario=user.email,
        asunto='Verificación de cuenta',
        template='emails/verificacion.html',
        contexto={'usuario': user, 'codigo': codigo}
    )

def enviar_recuperacion_contrasena(user, link):
    enviar_correo(
        destinatario=user.email,
        asunto='Recuperación de contraseña',
        template='emails/recuperacion.html',
        contexto={'usuario': user, 'link': link}
    )

def enviar_notificacion(user, mensaje):
    enviar_correo(
        destinatario=user.email,
        asunto='Notificación importante',
        template='emails/notificacion.html',
        contexto={'usuario': user, 'mensaje': mensaje}
    )

def enviar_confirmacion_compra(user, compra):
    enviar_correo(
        destinatario=user.email,
        asunto='Confirmación de compra/alquiler',
        template='emails/confirmacion.html',
        contexto={'usuario': user, 'compra': compra}
    )

def enviar_recordatorio(user, producto, dias_restantes):
    enviar_correo(
        destinatario=user.email,
        asunto='Recordatorio de vencimiento',
        template='emails/recordatorio.html',
        contexto={'usuario': user, 'producto': producto, 'dias': dias_restantes}
    )

def enviar_correo_verificacion(email, codigo_verificacion):
    asunto = "Verificación de correo"
    mensaje = f"Tu código de verificación es: {codigo_verificacion}"
    from_email = settings.DEFAULT_FROM_EMAIL
    send_mail(asunto, mensaje, from_email, [email])