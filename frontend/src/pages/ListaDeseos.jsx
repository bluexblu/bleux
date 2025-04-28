import React, { useState, useEffect } from 'react';

const ListaDeseos = ({ usuarioId }) => {
  const [deseos, setDeseos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (usuarioId) {
      // Llamada a la API para obtener los elementos de la lista de deseos
      fetch(`/api/lista_deseos/`)  // Asegúrate de usar la URL correcta
        .then((response) => response.json())
        .then((data) => {
          setDeseos(data.lista_deseos_items || []);  // Aseguramos que sea un array
          setLoading(false);
        })
        .catch((err) => {
          console.error(err);
          setError('Error al cargar la lista de deseos.');
          setLoading(false);
        });
    }
  }, [usuarioId]);

  if (loading) return <div>Cargando tu lista de deseos...</div>;
  if (error) return <div style={{ color: 'red' }}>{error}</div>;
  if (deseos.length === 0) return <div>No tienes productos en tu lista de deseos.</div>;

  return (
    <div className="container py-4">
      <h3 className="fw-bold mb-4">Tu Lista de Deseos</h3>
      <div className="row">
        {deseos.map((deseo) => (
          <div key={deseo.id} className="col-md-4 mb-4">
            <div className="card h-100 shadow-sm border-0 rounded-4">
              {deseo.producto.imagen && (
                <img 
                  src={deseo.producto.imagen}
                  className="card-img-top rounded-top"
                  alt={deseo.producto.nombre}
                  style={{ objectFit: 'cover', height: '200px' }}
                />
              )}
              <div className="card-body d-flex flex-column justify-content-between">
                <h5 className="card-title">{deseo.producto.nombre}</h5>
                <p className="card-text text-success fw-semibold">S/ {deseo.producto.precio}</p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ListaDeseos;
