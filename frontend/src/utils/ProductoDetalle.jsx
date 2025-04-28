import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';

const ProductoDetalle = () => {
    const { id } = useParams(); // Captura el id de la URL
    const [producto, setProducto] = useState(null);

    const handleAction = async (action) => {
        try {
            const response = await axios.post(`http://localhost:8000/api/producto/${id}/`, { accion: action });
            console.log(response.data.message);
            alert(response.data.message);  // Mostrar mensaje de acción realizada
        } catch (error) {
            console.error('Error:', error);
            alert(error.response?.data?.error || 'Error al realizar la acción.');
        }
    };

    useEffect(() => {
        const fetchProducto = async () => {
            try {
                const response = await axios.get(`http://localhost:8000/api/producto/${id}/`);
                setProducto(response.data);
            } catch (error) {
                console.error('Error:', error);
            }
        };

        fetchProducto();
    }, [id]);

    if (!producto) return <div>Cargando producto...</div>;

    return (
        <div className="container py-5">
            <div className="row justify-content-center">
                <div className="col-md-8 col-lg-6">
                    <div className="card shadow-lg border-0 rounded-4 p-4">
                        <div className="card-body">
                            <h2 className="card-title text-center fw-bold mb-4">{producto.titulo}</h2>
                            <p className="text-center mb-4"><em>{producto.descripcion}</em></p>

                            <div className="text-center mb-4">
                                <img 
                                    src={producto.imagen} 
                                    className="img-fluid rounded" 
                                    alt={producto.titulo} 
                                    style={{ maxHeight: '400px' }}
                                />
                            </div>

                            <ul className="list-group list-group-flush mb-4">
                                <li className="list-group-item"><strong>Tipo:</strong> {producto.tipo}</li>
                                <li className="list-group-item"><strong>Precio de compra:</strong> S/ {producto.precio_compra}</li>
                                <li className="list-group-item"><strong>Precio de alquiler:</strong> S/ {producto.precio_alquiler}</li>
                                <li className="list-group-item"><strong>Stock disponible:</strong> {producto.stock}</li>
                                <li className="list-group-item"><strong>Fecha de publicación:</strong> {new Date(producto.fecha_publicacion).toLocaleDateString('es-PE', { day: '2-digit', month: 'short', year: 'numeric' })}</li>
                            </ul>

                            <div className="d-flex flex-column gap-2">
                                <button 
                                    type="button" 
                                    className="btn btn-primary rounded-pill"
                                    onClick={() => handleAction('agregar_compra')}
                                >
                                    Comprar
                                </button>
                                <button 
                                    type="button" 
                                    className="btn btn-outline-secondary rounded-pill"
                                    onClick={() => handleAction('agregar_alquiler')}
                                >
                                    Alquilar
                                </button>
                                <button 
                                    type="button" 
                                    className="btn btn-outline-dark rounded-pill"
                                    onClick={() => handleAction('deseos')}
                                >
                                    Añadir a lista de deseos
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default ProductoDetalle;
