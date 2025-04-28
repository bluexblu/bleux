import React from 'react';
import BaseLayout from './BaseLayout'; 
import { Link } from 'react-router-dom';

const CarritoVacio = () => {
    return (
        <div className="container text-center mt-5">
            <h2>Tu Carrito</h2>
            <p>No tienes productos en el carrito.</p>
            <p>
                Para ver tu carrito, por favor{' '}
                <Link to="/login" className="btn btn-link">inicia sesión</Link> o{' '}
                <Link to="/registro" className="btn btn-link">regístrate</Link>.
            </p>
        </div>
    );
}

export default CarritoVacio;
