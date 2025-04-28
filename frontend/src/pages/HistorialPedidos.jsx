import React from 'react';
import baselayout from './baselayout';

const HistorialPedidos = ({ user, pedidos }) => {
  return (
    <div className="container">
      <h2>Historial de Pedidos de {user.nombre}</h2>

      {pedidos.length > 0 ? (
        <div className="list-group">
          {pedidos.map((pedido) => (
            <div className="list-group-item" key={pedido.id}>
              <h4>Pedido #{pedido.id} - {pedido.fecha}</h4>
              <p>Total: S/. {pedido.total}</p>

              <h5>Items:</h5>
              <ul>
                {pedido.items.map((item) => (
                  <li key={item.id}>
                    <strong>{item.producto.titulo}</strong> - {item.tipo} - x{item.cantidad} - S/. {item.subtotal}
                  </li>
                ))}
              </ul>

              <div className="d-flex justify-content-end">
                <a href={`/ver_detalle_pedido/${pedido.id}`} className="btn btn-info btn-sm">Ver Detalles</a>
                <a href={`/descargar_pdf_pedido/${pedido.id}`} className="btn btn-success btn-sm ml-2">Descargar PDF</a>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <p>No tienes pedidos aún. ¡Haz tu primera compra o alquiler!</p>
      )}
    </div>
  );
};

export default HistorialPedidos;
