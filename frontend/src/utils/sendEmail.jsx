import nodemailer from 'nodemailer';
import { renderEmail } from './renderEmail';  // Importar la función de renderizado de los componentes React
import ConfirmacionCompra from '../components/ConfirmacionCompra';

// Configuración de Nodemailer con Mailtrap
const transporter = nodemailer.createTransport({
  host: 'sandbox.smtp.mailtrap.io',  // Mailtrap SMTP server
  port: 587,
  auth: {
    user: '3f7a88aa17cfcc',  // Usa el usuario de Mailtrap
    pass: '3241d99384e58d' // Usa la contraseña de Mailtrap
  }
});

// Función para enviar el correo
export const sendEmail = async (to, subject, htmlContent) => {
  try {
    const info = await transporter.sendMail({
      from: '"lesyeux" <no-reply@tucorreo.com>',  // El correo desde el que se enviará
      to,  // Dirección de destino
      subject,  // Asunto
      html: htmlContent  // El HTML generado desde React
    });

    console.log('Correo enviado:', info.messageId);
  } catch (error) {
    console.error('Error al enviar el correo:', error);
  }
};

// Ejemplo de cómo usar la función
const confirmarCompraHTML = renderEmail(ConfirmacionCompra, {
  usuario: { email: 'correo@ejemplo.com' },
  compra: { producto: 'Película', precio: '10$', fecha: '27/04/2025' }
});

sendEmail('correo@ejemplo.com', 'Confirmación de Compra', confirmarCompraHTML);