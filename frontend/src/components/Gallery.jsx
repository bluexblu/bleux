import React from 'react';
import onepiece from '../assets/images/one-piece.jpg';
import akira from '../assets/images/akira.jpg';
import berserk from '../assets/images/berserk.jpg';
import thelastofus from '../assets/images/the-last-of-us.jpg';



const Gallery = () => {
  return (
    <div>
      <div className="image-background-container">
        <img src={thelastofus} alt="Imagen de fondo" className="image-background" />
      </div>

      {/* Galería de fotos estáticas */}
      <div className="content">
        <h4 className="mb-3">Galería</h4>
        <div className="container mt-4">
          <div className="row">
            <div className="col-2 d-flex justify-content-start mb-3">
              <div className="card shadow-sm border-0" style={{ width: '100%', maxWidth: '222px', height: '350px', overflow: 'hidden' }}>
                <img src={onepiece} alt="Imagen de fondo" className="img-fluid rounded" style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
              </div>
            </div>

            <div className="col-2 d-flex justify-content-center mb-3">
              <div className="card shadow-sm border-0" style={{ width: '100%', maxWidth: '222px', height: '350px', overflow: 'hidden' }}>
                <img src={akira} alt="Imagen de fondo" className="img-fluid rounded" style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
              </div>
            </div>

            <div className="col-2 d-flex justify-content-end mb-3">
              <div className="card shadow-sm border-0" style={{ width: '100%', maxWidth: '222px', height: '350px', overflow: 'hidden' }}>
                <img src={berserk} alt="Imagen de fondo" className="img-fluid rounded" style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
              </div>
            </div>

            {/* Continúa con el resto de las imágenes aquí de la misma forma */}

          </div>
        </div>
      </div>
    </div>
  );
};

export default Gallery;
