import React from 'react';

const RecuperacionContraseña = ({ usuario, link }) => {
  return (
    <div className="container py-5">
      <h2>Recuperación de Contraseña</h2>
      <p>Hola {usuario.email},</p>
      <p>Para restablecer tu contraseña, haz clic en el siguiente enlace:</p>
      <p><a href={link}>Restablecer Contraseña</a></p>
      <p>Si no solicitaste este cambio, ignora este mensaje.</p>
    </div>
  );
};

export default RecuperacionContraseña;
