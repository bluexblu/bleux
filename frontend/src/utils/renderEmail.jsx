import React from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
import ConfirmacionCompra from '../components/ConfirmacionCompra';
import NotificacionImportante from '../components/NotificacionImportante';
import RecordatorioVencimiento from '../components/RecordatorioVencimiento';
import RecuperacionContrasena from '../components/RecuperacionContrasena';
import VerificacionCuenta from '../components/VerificacionCuenta';

// Función para renderizar cualquier componente de React a HTML
export const renderEmail = (component, props) => {
  return renderToStaticMarkup(React.createElement(component, props));
};

// Ejemplo: Usar con ConfirmacionCompra
const confirmarCompraHTML = renderEmail(ConfirmacionCompra, {
  usuario: { email: 'correo@ejemplo.com' },
  compra: { producto: 'Película', precio: '10$', fecha: '27/04/2025' }
});

console.log(confirmarCompraHTML);  // HTML generado

// Puedes hacer lo mismo para otros componentes
const notificacionHTML = renderEmail(NotificacionImportante, {
  usuario: { email: 'correo@ejemplo.com' },
  mensaje: 'Tu cuenta está actualizada.'
});

// Ahora `notificacionHTML` tiene el HTML listo para enviar

export { confirmarCompraHTML, notificacionHTML };