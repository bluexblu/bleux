import React from 'react';
import baselayout from './baselayout';

const ProductoDetail = ({ item }) => {
    const handleAction = (action) => {
        // Aquí puedes agregar la lógica para manejar las acciones (comprar, alquilar, añadir a deseos)
        console.log(`${action} clicked`);
    };

    return (
        <div className="container py-5">
            <div className="row justify-content-center">
                <div className="col-md-8 col-lg-6">
                    <div className="card shadow-lg border-0 rounded-4 p-4">
                        <div className="card-body">
                            <h2 className="card-title text-center fw-bold mb-4">{item.titulo}</h2>

                            <ul className="list-group list-group-flush mb-4">
                                <li className="list-group-item"><strong>Tipo:</strong> {item.tipo}</li>
                                <li className="list-group-item"><strong>Descripción:</strong> {item.descripcion}</li>
                                <li className="list-group-item"><strong>Fecha de lanzamiento:</strong> {item.fecha_lanzamiento}</li>
                                <li className="list-group-item"><strong>Disponibilidad:</strong> {item.disponibilidad}</li>
                            </ul>

                            <div className="d-flex flex-column gap-2">
                                <button 
                                    type="button" 
                                    className="btn btn-primary rounded-pill"
                                    onClick={() => handleAction('comprar')}
                                >
                                    Comprar
                                </button>
                                <button 
                                    type="button" 
                                    className="btn btn-outline-secondary rounded-pill"
                                    onClick={() => handleAction('alquilar')}
                                >
                                    Alquilar
                                </button>
                                <button 
                                    type="button" 
                                    className="btn btn-outline-dark rounded-pill"
                                    onClick={() => handleAction('deseo')}
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

export default ProductoDetail;
