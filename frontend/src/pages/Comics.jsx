import React, { useState, useEffect } from 'react';

const Comics = () => {
    const [comics, setComics] = useState([]);
    
    // Simulando la obtención de datos desde un backend (puedes adaptarlo a tu API)
    useEffect(() => {
        // Aquí deberías hacer la llamada a tu backend o API para obtener los comics
        // Este es solo un ejemplo de cómo podrías tener los datos.
        const fetchComics = async () => {
            // Fetch de ejemplo, reemplázalo con tu API real
            const response = await fetch('/api/comics');
            const data = await response.json();
            setComics(data);
        };
        
        fetchComics();
    }, []);
    
    return (
        <div className="my-5">
            <h1 className="mb-4">Comics</h1>

            <div className="row row-cols-1 row-cols-md-3 g-4">
                {comics.length > 0 ? (
                    comics.map((comic) => (
                        <div className="col" key={comic.id}>
                            <div className="card h-100 shadow-sm">
                                {/* Asegúrate de que la imagen exista antes de renderizarla */}
                                <img
                                    src={comic.imagen || "/images/default.jpg"}
                                    className="card-img-top"
                                    alt={comic.titulo}
                                />
                                <div className="card-body">
                                    <h5 className="card-title">{comic.titulo}</h5>
                                    <p className="card-text">{comic.descripcion.length > 20 ? `${comic.descripcion.substring(0, 20)}...` : comic.descripcion}</p>
                                </div>
                                <div className="card-footer d-flex justify-content-between align-items-center">
                                    <span className="text-muted">S/{comic.precio}</span>
                                    <a href={`/producto_detail/${comic.id}`} className="btn btn-sm btn-outline-primary">Ver más</a>
                                </div>
                            </div>
                        </div>
                    ))
                ) : (
                    <div className="col">
                        <p className="text-muted">No hay cómics disponibles por ahora.</p>
                    </div>
                )}
            </div>
        </div>
    );
}

export default Comics;
