import React from 'react';

const RecordatorioVencimiento = ({ usuario, producto, dias }) => {
  return (
    <div className="container py-5">
      <h2>Recordatorio de Vencimiento</h2>
      <p>Hola {usuario.email},</p>
      <p>Queremos recordarte que el siguiente producto está a punto de vencer:</p>
      <ul>
        <li><strong>Producto:</strong> {producto}</li>
        <li><strong>Días restantes:</strong> {dias} días</li>
      </ul>
      <p>No olvides renovarlo o devolverlo a tiempo.</p>
    </div>
  );
};

export default RecordatorioVencimiento;
