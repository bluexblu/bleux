import React from 'react';

const NotificacionImportante = ({ usuario, mensaje }) => {
  return (
    <div className="container py-5">
      <h2>Notificación Importante</h2>
      <p>Hola {usuario.email},</p>
      <p>Tenemos un mensaje importante para ti:</p>
      <p>{mensaje}</p>
      <p>Gracias por estar con nosotros.</p>
    </div>
  );
};

export default NotificacionImportante;
