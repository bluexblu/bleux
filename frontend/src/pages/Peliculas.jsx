import React from 'react';
import { Link } from 'react-router-dom';

const Peliculas = ({ peliculas }) => {
  return (
    <div className="my-5">
      <h1 className="mb-4">Películas</h1>

      <div className="row row-cols-1 row-cols-md-3 g-4">
        {peliculas.length > 0 ? (
          peliculas.map((pelicula) => (
            <div className="col" key={pelicula.id}>
              <div className="card h-100 shadow-sm">
                <img
                  src={pelicula.imagen || 'https://via.placeholder.com/150'}
                  className="card-img-top"
                  alt={pelicula.titulo}
                />
                <div className="card-body">
                  <h5 className="card-title">{pelicula.titulo}</h5>
                  <p className="card-text">
                    {pelicula.descripcion.length > 20
                      ? `${pelicula.descripcion.substring(0, 20)}...`
                      : pelicula.descripcion}
                  </p>
                </div>
                <div className="card-footer d-flex justify-content-between align-items-center">
                  <span className="text-muted">S/{pelicula.precio}</span>
                  <Link to={`/producto_detail/${pelicula.id}`} className="btn btn-sm btn-outline-primary">
                    Ver más
                  </Link>
                </div>
              </div>
            </div>
          ))
        ) : (
          <div className="col">
            <p className="text-muted">No hay películas disponibles por ahora.</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Peliculas;
