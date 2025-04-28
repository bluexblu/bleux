import React, { useState, useEffect } from 'react';
import { fetchProductos } from '../api/api'; // Asegúrate de importar correctamente la función

const Catalogo = () => {
  const [items, setItems] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // Obtener los productos desde la API al montar el componente
  useEffect(() => {
    fetchProductos()
      .then((data) => {
        setItems(data);  // Seteamos los productos que obtenemos de la API
        setLoading(false);
      })
      .catch((err) => {
        setError('Error al cargar los productos.');
        setLoading(false);
      });
  }, []);  // Solo se ejecuta una vez cuando el componente se monta

  const handleSearchChange = (event) => {
    setSearchQuery(event.target.value);
  };

  const filteredItems = items.filter(item =>
    item.titulo.toLowerCase().includes(searchQuery.toLowerCase())
  );

  if (loading) return <div>Cargando productos...</div>;
  if (error) return <div style={{ color: 'red' }}>{error}</div>;

  return (
    <main className="container py-5">
      <h2 className="text-center fw-bold mb-4">Explora el Catálogo</h2>

      {/* Formulario de búsqueda */}
      <div className="search-form mb-5 text-center">
        <input
          type="text"
          value={searchQuery}
          onChange={handleSearchChange}
          className="form-control w-50 rounded-pill shadow-sm"
          placeholder="Buscar cómic, película o serie..."
        />
      </div>

      {/* Catálogo */}
      <div className="row row-cols-1 row-cols-sm-2 row-cols-md-3 g-4">
        {filteredItems.length > 0 ? (
          filteredItems.map((item) => (
            <div className="col" key={item.id}>
              <div className="card h-100 border-0 shadow rounded-4 overflow-hidden">
                <img
                  src={item.imagen ? item.imagen.url : "/images/default.jpg"}
                  className="card-img-top object-fit-cover"
                  alt={item.titulo}
                  style={{ height: "250px" }}
                />
                <div className="card-body d-flex flex-column">
                  <h5 className="card-title fw-semibold">{item.titulo}</h5>
                  <p className="card-text text-muted small">
                    {item.descripcion.length > 20
                      ? `${item.descripcion.substring(0, 20)}...`
                      : item.descripcion}
                  </p>
                  <a
                    href={`/producto_detail/${item.id}`}
                    className="btn btn-dark mt-auto rounded-pill"
                  >
                    Ver detalles
                  </a>
                </div>
              </div>
            </div>
          ))
        ) : (
          <div className="col-12 text-center">
            <p className="text-muted">No se encontraron resultados.</p>
          </div>
        )}
      </div>
    </main>
  );
};

export default Catalogo;
