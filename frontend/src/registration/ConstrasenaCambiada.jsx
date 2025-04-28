import React from 'react';
import BaseLayout from '../components/BaseLayout';

import { Link } from 'react-router-dom';

const ContrasenaCambiada = () => {
  return (
    <div className="container py-5">
      <h2>Contraseña restablecida</h2>
      <p>
        Tu contraseña ha sido cambiada exitosamente. Ya puedes{''}
        <Link to="/login">iniciar sesión</Link>.
      </p>
    </div>
  );
};

export default ContrasenaCambiada;
