import React, { useState } from 'react';
import axios from 'axios';  // Para hacer la petición a la API
import BaseLayout from './BaseLayout';  // Asegúrate de que tienes BaseLayout correctamente importado

const RecuperarContrasena = () => {
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();
    
    try {
      const response = await axios.post('http://localhost:8000/api/password-reset/', { email });
      setMessage(response.data.message);  // Mostrar el mensaje de éxito
      setError('');
    } catch (err) {
      setError(err.response?.data?.error || 'Error al enviar el correo de restablecimiento.');
      setMessage('');
    }
  };

  return (
    <BaseLayout>
      <div className="container py-5">
        <h2>Recuperar contraseña</h2>
        <p>Introduce tu correo electrónico para recibir instrucciones.</p>

        {message && <div className="alert alert-success">{message}</div>}
        {error && <div className="alert alert-danger">{error}</div>}

        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <label htmlFor="email" className="form-label">Correo electrónico</label>
            <input
              type="email"
              id="email"
              className="form-control"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <button type="submit" className="btn btn-primary">Enviar enlace</button>
        </form>
      </div>
    </BaseLayout>
  );
};

export default RecuperarContrasena;
