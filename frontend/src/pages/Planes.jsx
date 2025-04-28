import React from 'react';

const Planes = () => {
  const businessEmail = "sb-xyemu38604524@business.example.com";
  const successUrl = "https://tusitio.com/confirmacion_pago"; // Aquí coloca la URL final
  const cancelUrl = "https://tusitio.com/cancelar_pago";      // Aquí coloca la URL de cancelación

  const planes = [
    {
      nombre: "Básico",
      precio: "5.00",
      descripcion: "Acceso limitado al contenido.",
      btnColor: "primary",
    },
    {
      nombre: "Estándar",
      precio: "10.00",
      descripcion: "Acceso completo y sin anuncios.",
      btnColor: "success",
    },
    {
      nombre: "Premium",
      precio: "15.00",
      descripcion: "Todo incluido + contenido exclusivo.",
      btnColor: "warning",
    },
  ];

  return (
    <div className="container mt-5" style={{ maxWidth: "600px" }}>
      <div className="card shadow p-4 rounded-3">
        <h3 className="text-center mb-4">Elige tu plan</h3>
        <div className="row">
          {planes.map((plan, index) => (
            <div className="col-md-4 mb-3" key={index}>
              <div className="card text-center">
                <div className="card-header">{plan.nombre}</div>
                <div className="card-body">
                  <h5 className="card-title">${plan.precio} / mes</h5>
                  <p className="card-text">{plan.descripcion}</p>
                  <form
                    action="https://www.sandbox.paypal.com/cgi-bin/webscr"
                    method="post"
                  >
                    <input type="hidden" name="cmd" value="_xclick" />
                    <input type="hidden" name="business" value={businessEmail} />
                    <input type="hidden" name="item_name" value={`Suscripción ${plan.nombre}`} />
                    <input type="hidden" name="amount" value={plan.precio} />
                    <input type="hidden" name="currency_code" value="USD" />
                    <input type="hidden" name="return" value={successUrl} />
                    <input type="hidden" name="cancel_return" value={cancelUrl} />
                    <button type="submit" className={`btn btn-outline-${plan.btnColor} w-100`}>
                      Seleccionar
                    </button>
                  </form>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Planes;
