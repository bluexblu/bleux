import React from 'react';

const MetodosPago = () => {
  return (
    <div className="container mt-5" style={{ maxWidth: '500px' }}>
      <div className="card shadow p-4 rounded-3">
        <h3 className="text-center mb-4">Métodos de Pago</h3>
        <ul className="list-group">
          <li className="list-group-item">Tarjeta de crédito (Visa, MasterCard, American Express)</li>
          <li className="list-group-item">PayPal</li>
          <li className="list-group-item">Transferencia bancaria</li>
          <li className="list-group-item">Pago en efectivo (solo en puntos autorizados)</li>
        </ul>
      </div>
    </div>
  );
};

export default MetodosPago;