import React from 'react';

const ConfirmacionCompra = ({ usuario, compra }) => {
  return (
    <div className="container py-5">
      <h2>Confirmación de Compra/Alquiler</h2>
      <p>Hola {usuario.email},</p>
      <p>Gracias por tu compra/alquiler. Los detalles de tu transacción son los siguientes:</p>
      <ul>
        <li><strong>Producto:</strong> {compra.producto}</li>
        <li><strong>Precio:</strong> {compra.precio}</li>
        <li><strong>Fecha de compra/alquiler:</strong> {compra.fecha}</li>
      </ul>
      <p>Si tienes alguna pregunta, no dudes en contactarnos.</p>
    </div>
  );
};

export default ConfirmacionCompra;
