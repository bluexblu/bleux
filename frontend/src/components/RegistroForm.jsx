import React, { useState } from 'react';
import { registrarUsuario } from '../api/api.jsx'; // Importa tu servicio

const RegistroForm = () => {
  const [formData, setFormData] = useState({
    nombre: '',
    email: '',
    password: '',
  });

  const [errors, setErrors] = useState({
    nombre: '',
    email: '',
    password: '',
    nonFieldErrors: ''
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await registrarUsuario(formData);
      console.log('Usuario registrado:', response);
      // Puedes redirigir o mostrar un mensaje aquí si quieres
    } catch (error) {
      // Manejar errores de validación desde la API
      if (error.response && error.response.data) {
        const backendErrors = error.response.data; // Error que llega del backend
        setErrors({
          nombre: backendErrors.nombre || '',
          email: backendErrors.email || '',
          password: backendErrors.password || '',
          nonFieldErrors: backendErrors.nonFieldErrors || ''
        });
      } else {
        console.error('Error registrando usuario:', error);
      }
    }
  };

  return (
    <div className="container mt-5" style={{ maxWidth: '400px' }}>
      <div className="card shadow p-4 rounded-3">
        <h3 className="text-center mb-4">Formulario de Registro</h3>
        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <label htmlFor="nombre" className="form-label">Nombre</label>
            <input
              type="text"
              id="nombre"
              name="nombre"
              className="form-control"
              required
              value={formData.nombre}
              onChange={handleChange}
            />
            {errors.nombre && <div className="text-danger">{errors.nombre}</div>}
          </div>

          <div className="mb-3">
            <label htmlFor="email" className="form-label">Email</label>
            <input
              type="email"
              id="email"
              name="email"
              className="form-control"
              required
              value={formData.email}
              onChange={handleChange}
            />
            {errors.email && <div className="text-danger">{errors.email}</div>}
          </div>

          <div className="mb-3">
            <label htmlFor="password" className="form-label">Contraseña</label>
            <input
              type="password"
              id="password"
              name="password"
              className="form-control"
              required
              value={formData.password}
              onChange={handleChange}
            />
            {errors.password && <div className="text-danger">{errors.password}</div>}
          </div>

          {errors.nonFieldErrors && (
            <div className="alert alert-danger">{errors.nonFieldErrors}</div>
          )}

          <button type="submit" className="btn btn-primary w-100">Registrarse</button>
        </form>

        <div className="mt-3 text-center">
          <small>
            ¿Olvidaste tu contraseña?{' '}
            <a href="/password-reset" className="btn-recuperar">Recupérala aquí</a>
          </small>
        </div>
      </div>
    </div>
  );
};

export default RegistroForm;
