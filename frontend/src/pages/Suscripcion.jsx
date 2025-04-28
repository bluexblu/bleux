import React, { useState } from 'react';
import { crearSuscripcion } from './api';  // Asegúrate de que la ruta sea correcta

const Suscripcion = () => {
  const [selectedPlan, setSelectedPlan] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (!selectedPlan) {
      setError('Por favor, selecciona un plan.');
      return;
    }

    setLoading(true);
    const suscripcionData = {
      plan: selectedPlan,
      monto: selectedPlan === 'Básico' ? 5.00 : selectedPlan === 'Estándar' ? 10.00 : 15.00,
      // Aquí puedes poner la fecha de inicio y fin, o calculándolas si es necesario
    };

    try {
      const response = await crearSuscripcion(suscripcionData);
      console.log('Suscripción creada:', response);
      // Aquí puedes hacer algo como redirigir o mostrar un mensaje de éxito
    } catch (err) {
      console.error('Error al crear suscripción:', err);
      setError('Hubo un error al crear la suscripción.');
    }
    setLoading(false);
  };

  return (
    <div className="container mt-5" style={{ maxWidth: '600px' }}>
      <div className="card shadow p-4 rounded-3">
        <h3 className="text-center mb-4">Elige tu plan</h3>
        <div className="row">
          {/* Plan Básico */}
          <div className="col-md-4 mb-3">
            <div className="card text-center">
              <div className="card-header">Básico</div>
              <div className="card-body">
                <h5 className="card-title">$5 / mes</h5>
                <p className="card-text">Acceso limitado al contenido.</p>
                <button 
                  onClick={() => setSelectedPlan('Básico')} 
                  className="btn btn-outline-primary w-100"
                >
                  Seleccionar
                </button>
              </div>
            </div>
          </div>

          {/* Plan Estándar */}
          <div className="col-md-4 mb-3">
            <div className="card text-center">
              <div className="card-header">Estándar</div>
              <div className="card-body">
                <h5 className="card-title">$10 / mes</h5>
                <p className="card-text">Acceso completo y sin anuncios.</p>
                <button 
                  onClick={() => setSelectedPlan('Estándar')} 
                  className="btn btn-outline-success w-100"
                >
                  Seleccionar
                </button>
              </div>
            </div>
          </div>

          {/* Plan Premium */}
          <div className="col-md-4 mb-3">
            <div className="card text-center">
              <div className="card-header">Premium</div>
              <div className="card-body">
                <h5 className="card-title">$15 / mes</h5>
                <p className="card-text">Todo incluido + contenido exclusivo.</p>
                <button 
                  onClick={() => setSelectedPlan('Premium')} 
                  className="btn btn-outline-warning w-100"
                >
                  Seleccionar
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Botón para confirmar suscripción */}
        {selectedPlan && (
          <button 
            onClick={handleSubmit} 
            className="btn btn-primary w-100 mt-4"
            disabled={loading}
          >
            {loading ? 'Procesando...' : 'Confirmar Suscripción'}
          </button>
        )}

        {error && <div className="alert alert-danger mt-3">{error}</div>}
      </div>
    </div>
  );
};

export default Suscripcion;
