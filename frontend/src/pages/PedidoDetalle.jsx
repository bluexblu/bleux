import React from 'react';
import baselayout from './baselayout';

const PedidoDetalle = ({ pedido, items }) => {
  return (
    <div style={{ fontFamily: 'Arial, sans-serif', margin: '40px', backgroundColor: '#f8f9fa', color: '#333' }}>
      <h1 style={{ color: '#0056b3', borderBottom: '2px solid #0056b3', paddingBottom: '10px' }}>
        Pedido #{pedido.id}
      </h1>
      <p><strong>Fecha:</strong> {pedido.fecha}</p>
      <p><strong>Cliente:</strong> {pedido.usuario.nombre}</p>

      <h2 style={{ color: '#007acc', marginTop: '30px' }}>Items</h2>
      <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '15px' }}>
        <thead>
          <tr>
            <th style={{ border: '1px solid #cce5ff', padding: '10px', textAlign: 'left', backgroundColor: '#007acc', color: 'white' }}>Producto</th>
            <th style={{ border: '1px solid #cce5ff', padding: '10px', textAlign: 'left', backgroundColor: '#007acc', color: 'white' }}>Cantidad</th>
            <th style={{ border: '1px solid #cce5ff', padding: '10px', textAlign: 'left', backgroundColor: '#007acc', color: 'white' }}>Precio Unitario</th>
            <th style={{ border: '1px solid #cce5ff', padding: '10px', textAlign: 'left', backgroundColor: '#007acc', color: 'white' }}>Subtotal</th>
          </tr>
        </thead>
        <tbody>
          {items.map((item) => (
            <tr key={item.producto.id} style={{ backgroundColor: item.id % 2 === 0 ? '#e6f2ff' : '', ':hover': { backgroundColor: '#d0e9ff' } }}>
              <td style={{ border: '1px solid #cce5ff', padding: '10px', textAlign: 'left' }}>
                {item.producto.titulo}
              </td>
              <td style={{ border: '1px solid #cce5ff', padding: '10px', textAlign: 'left' }}>
                {item.cantidad}
              </td>
              <td style={{ border: '1px solid #cce5ff', padding: '10px', textAlign: 'left' }}>
                ${item.precio_unitario_display}
              </td>
              <td style={{ border: '1px solid #cce5ff', padding: '10px', textAlign: 'left' }}>
                ${item.subtotal}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default PedidoDetalle;
