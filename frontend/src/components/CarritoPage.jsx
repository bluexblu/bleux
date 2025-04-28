import React, { useEffect, useState } from 'react';
import BaseLayout from './BaseLayout';
import CarritoVacio from './CarritoVacio';
import CarritoCompras from './CarritoCompras';
import { obtenerCarrito } from '../api/api.jsx';  // Función para obtener el carrito desde la API

const CarritoPage = () => {
  const [carritoData, setCarritoData] = useState([]);
  const [total, setTotal] = useState(0);

  useEffect(() => {
    // Llamada a la API para obtener los datos del carrito
    const fetchCarrito = async () => {
      try {
        const data = await obtenerCarrito(); // Llamada a la API que definimos en api.js
        setCarritoData(data);
        const nuevoTotal = data.reduce((acc, item) => acc + item.total, 0);
        setTotal(nuevoTotal);
      } catch (error) {
        console.error('Error al obtener el carrito:', error);
      }
    };

    fetchCarrito();
  }, []);

  return (
    <BaseLayout>
      <div className="container mt-5">
        {carritoData.length > 0 ? (
          <CarritoCompras carritoData={carritoData} total={total} />
        ) : (
          <CarritoVacio />
        )}
      </div>
    </BaseLayout>
  );
};

export default CarritoPage;
