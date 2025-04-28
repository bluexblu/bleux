import React, { useState } from 'react';
import baselayout from './baselayout';

const CambiarContrasena = () => {
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (password !== confirmPassword) {
      alert('Las contraseñas no coinciden');
    } else {
      // Aquí agregarías la lógica para enviar la nueva contraseña al backend.
      console.log('Contraseña cambiada:', password);
    }
  };

  return (
    <div className="container py-5">
      <h2>Ingresa tu nueva contraseña</h2>
      <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <label htmlFor="password" className="form-label">
            Nueva Contraseña
          </label>
          <input
            type="password"
            className="form-control"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <div className="mb-3">
          <label htmlFor="confirmPassword" className="form-label">
            Confirmar Nueva Contraseña
          </label>
          <input
            type="password"
            className="form-control"
            id="confirmPassword"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit" className="btn btn-primary">
          Cambiar Contraseña
        </button>
      </form>
    </div>
  );
};

export default CambiarContrasena;
