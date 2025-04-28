import React from 'react';
import { Link } from 'react-router-dom';

const Series = ({ series }) => {
  return (
    <div className="my-5">
      <h1 className="mb-4">Series</h1>

      <div className="row row-cols-1 row-cols-md-3 g-4">
        {series.length > 0 ? (
          series.map((serie) => (
            <div className="col" key={serie.id}>
              <div className="card h-100 shadow-sm">
                <img
                  src={serie.imagen || 'https://via.placeholder.com/150'}
                  className="card-img-top"
                  alt={serie.titulo}
                />
                <div className="card-body">
                  <h5 className="card-title">{serie.titulo}</h5>
                  <p className="card-text">
                    {serie.descripcion.length > 20
                      ? `${serie.descripcion.substring(0, 20)}...`
                      : serie.descripcion}
                  </p>
                </div>
                <div className="card-footer d-flex justify-content-between align-items-center">
                  <span className="text-muted">S/{serie.precio}</span>
                  <Link to={`/producto_detail/${serie.id}`} className="btn btn-sm btn-outline-primary">
                    Ver más
                  </Link>
                </div>
              </div>
            </div>
          ))
        ) : (
          <div className="col">
            <p className="text-muted">No hay series disponibles por ahora.</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Series;
