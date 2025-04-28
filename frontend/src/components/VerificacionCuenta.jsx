import React from 'react';

const VerificacionCuenta = ({ usuario, codigo }) => {
  return (
    <div className="container py-5">
      <h2>Hola {usuario.nombre}!</h2>
      <p>Gracias por registrarte. Tu código de verificación es:</p>
      <h3>{codigo}</h3>
      <p>¡Bienvenido a nuestra comunidad!</p>
    </div>
  );
};

export default VerificacionCuenta;
