import React, { useState } from 'react';
import { loginUser } from '../api/api.jsx'; // Importa el servicio correctamente
import BaseLayout from './BaseLayout'; // corrige: BaseLayout con mayúscula

const LoginForm = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });

  const [errors, setErrors] = useState({
    email: '',
    password: '',
    nonFieldErrors: ''
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Validaciones básicas
    if (!formData.email || !formData.password) {
      setErrors({
        email: formData.email ? '' : 'Este campo es obligatorio.',
        password: formData.password ? '' : 'Este campo es obligatorio.',
        nonFieldErrors: 'Por favor, revisa los campos.'
      });
      return;
    }

    try {
      const response = await loginUser(formData);

      // Guardar el token
      localStorage.setItem('token', response.token);
      localStorage.setItem('user', JSON.stringify(response.user));

      console.log('Login exitoso');
      window.location.href = '/'; // Redirige después del login
    } catch (error) {
      setErrors({
        email: '',
        password: '',
        nonFieldErrors: 'Credenciales inválidas. Inténtalo de nuevo.'
      });
    }
  };

  return (
    <BaseLayout>
      <div className="container mt-5" style={{ maxWidth: '400px' }}>
        <div className="card shadow p-4 rounded-3">
          <h3 className="text-center mb-4">Inicia sesión en LesYeux</h3>
          <form onSubmit={handleSubmit} noValidate>
            <div className="mb-3">
              <label htmlFor="email" className="form-label">Correo electrónico</label>
              <input
                type="email"
                id="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                className="form-control"
              />
              {errors.email && <div className="text-danger">{errors.email}</div>}
            </div>

            <div className="mb-3">
              <label htmlFor="password" className="form-label">Contraseña</label>
              <input
                type="password"
                id="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                className="form-control"
              />
              {errors.password && <div className="text-danger">{errors.password}</div>}
            </div>

            {errors.nonFieldErrors && (
              <div className="alert alert-danger">{errors.nonFieldErrors}</div>
            )}

            <button type="submit" className="btn btn-primary w-100">Ingresar</button>
          </form>

          <div className="mt-3 text-center">
            <small>¿No tienes cuenta? <a href="/registro">Regístrate</a></small>
          </div>
        </div>
      </div>
    </BaseLayout>
  );
};

export default LoginForm;
