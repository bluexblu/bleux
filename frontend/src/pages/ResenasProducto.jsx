import React, { useState, useEffect } from 'react';
import { fetchResenasProducto } from '../api/api';  // Asegúrate que apunte bien a tu fetch

const ResenasProducto = ({ productoId }) => {
  const [resenas, setResenas] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (productoId) {
      fetchResenasProducto(productoId)
        .then((data) => {
          setResenas(data);  // Recuerda que ahora viene un array directamente
          setLoading(false);
        })
        .catch((err) => {
          setError('Error al cargar reseñas.');
          setLoading(false);
        });
    }
  }, [productoId]);

  if (loading) return <div>Cargando reseñas...</div>;
  if (error) return <div style={{ color: 'red' }}>{error}</div>;
  if (resenas.length === 0) return <div>No hay reseñas aún para este producto.</div>;

  return (
    <div className="container py-4">
      <h3 className="fw-bold mb-4">Reseñas del Producto</h3>
      {resenas.map((resena) => (
        <div key={resena.id} className="mb-4 p-3 border rounded-3 shadow-sm">
          <div className="d-flex justify-content-between align-items-center mb-2">
            <h5 className="fw-semibold mb-0">{resena.usuario.nombre}</h5>
            <div>
              {Array.from({ length: resena.calificacion }).map((_, i) => (
                <span key={i} style={{ color: '#ffc107', fontSize: '1.2rem' }}>★</span>
              ))}
              {Array.from({ length: 5 - resena.calificacion }).map((_, i) => (
                <span key={i} style={{ color: '#e4e5e9', fontSize: '1.2rem' }}>★</span>
              ))}
            </div>
          </div>
          <p className="mb-0 text-muted fst-italic">"{resena.comentario}"</p>
        </div>
      ))}
    </div>
  );
};

export default ResenasProducto;
