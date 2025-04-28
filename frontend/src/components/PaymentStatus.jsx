
import React, { useEffect, useState } from 'react';
import { getPaymentStatus } from '../src/api';  // Asegúrate de ajustar la ruta si es necesario

const PaymentStatus = ({ paymentId }) => {
  const [status, setStatus] = useState(null);

  useEffect(() => {
    const fetchStatus = async () => {
      const data = await getPaymentStatus(paymentId);
      setStatus(data.status);  // Asumiendo que el backend te devuelve un objeto con un campo 'status'
    };

    fetchStatus();
  }, [paymentId]);

  return (
    <div>
      <h3>Estado del pago</h3>
      <div>{status ? `Pago ${status}` : 'Cargando estado del pago...'}</div>
    </div>
  );
};

export default PaymentStatus;
