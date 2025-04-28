import React from 'react';

const Usuarios = ({ usuarios }) => {
  return (
    <div className="container py-5">
      <div className="text-center mb-5">
        <h2 className="fw-bold">Usuarios Registrados</h2>
        <p className="text-muted">Explora a los usuarios registrados y sus listas de deseos.</p>
      </div>

      <div className="row justify-content-center">
        {usuarios.map((usuario) => (
          <div className="col-md-6 col-lg-4 mb-4" key={usuario.id}>
            <div className="card h-100 border-0 shadow rounded-4">
              <div className="card-body">
                <h5 className="card-title mb-1 fw-semibold">{usuario.nombre}</h5>

                <p className="card-text fw-medium mb-2">Lista de deseos:</p>
                <ul className="list-group list-group-flush">
                  {usuario.listadeseos && usuario.listadeseos.length > 0 ? (
                    usuario.listadeseos.map((deseo) => (
                      <li className="list-group-item" key={deseo.id}>
                        {deseo.producto.titulo}
                      </li>
                    ))
                  ) : (
                    <li className="list-group-item text-muted fst-italic">
                      No tiene productos en su lista de deseos.
                    </li>
                  )}
                </ul>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Usuarios;
