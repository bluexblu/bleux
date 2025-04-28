import React from 'react';
import baselayout from './baselayout';
import { Link } from 'react-router-dom';

const PagoCancelado = () => {
    return (
        <div className="container text-center mt-5">
            <h2>El pago fue cancelado</h2>
            <p>Lo sentimos, el pago no se completó. Puedes intentar nuevamente.</p>
            <Link to="/carrito" className="btn btn-primary">Volver al carrito</Link>
        </div>
    );
}

export default PagoCancelado;
