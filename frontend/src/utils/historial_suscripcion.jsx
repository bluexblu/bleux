import React from 'react';
import baselayout from './baselayout';

const HistorialSuscripciones = () => {
  const suscripciones = [
    {
      fecha: '10/03/2025',
      plan: 'Estándar',
      metodoPago: 'Visa',
      monto: '$10',
      estado: 'Activo',
    },
    {
      fecha: '10/02/2025',
      plan: 'Básico',
      metodoPago: 'PayPal',
      monto: '$5',
      estado: 'Vencido',
    },
  ];

  return (
    <div className="container mt-5">
      <div className="card shadow p-4 rounded-3">
        <h3 className="text-center mb-4">Historial de Suscripciones</h3>
        <div className="table-responsive">
          <table className="table table-bordered table-hover table-striped align-middle text-center">
            <thead className="table-dark">
              <tr>
                <th>Fecha</th>
                <th>Plan</th>
                <th>Método de pago</th>
                <th>Monto</th>
                <th>Estado</th>
              </tr>
            </thead>
            <tbody>
              {suscripciones.map((suscripcion, index) => (
                <tr key={index}>
                  <td>{suscripcion.fecha}</td>
                  <td>{suscripcion.plan}</td>
                  <td>{suscripcion.metodoPago}</td>
                  <td>{suscripcion.monto}</td>
                  <td>
                    <span
                      className={`badge ${suscripcion.estado === 'Activo' ? 'bg-success' : 'bg-secondary'}`}
                    >
                      {suscripcion.estado}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default HistorialSuscripciones;
