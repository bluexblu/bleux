import React from 'react';

const CarritoCompras = ({ carritoData, total }) => {
  return (
    <div>
      <h2>Tu Carrito</h2>

      {carritoData && carritoData.length > 0 ? (
        <div>
          <table className="table">
            <thead>
              <tr>
                <th>Producto</th>
                <th>Cantidad</th>
                <th>Precio Unitario</th>
                <th>Total</th>
              </tr>
            </thead>
            <tbody>
              {carritoData.map((data) => (
                <tr key={data.id}>
                  <td>{data.producto.titulo}</td>
                  <td>{data.cantidad}</td>
                  <td>${data.precio_unitario.toFixed(2)}</td>
                  <td>${data.total.toFixed(2)}</td>
                </tr>
              ))}
            </tbody>
          </table>

          <h3>Total de la compra: ${total.toFixed(2)}</h3>

          <button className="btn btn-primary">Pagar con PayPal</button>

          <button className="btn btn-secondary mt-3">Procesar Pedido</button>
        </div>
      ) : (
        <p>No tienes productos en el carrito.</p>
      )}
    </div>
  );
};

export default CarritoCompras;
