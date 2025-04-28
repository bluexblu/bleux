// api.js
const API_URL = 'http://localhost:8000';

export const fetchUsuarios = async () => {
  const response = await fetch(`${API_URL}/usuarios/`);
  if (!response.ok) throw new Error('Error al cargar los usuarios');
  return response.json();
};

export const fetchTransacciones = async () => {
  const response = await fetch(`${API_URL}/transacciones/`);
  if (!response.ok) throw new Error('Error al cargar las transacciones');
  return response.json();
};

export const fetchResenasProducto = async (productoId) => {
  const response = await fetch(`${API_URL}/resenas_producto/${productoId}/`);
  if (!response.ok) throw new Error('Error al cargar las reseñas');
  return response.json();
};

  // Función para obtener lista de deseos de un usuario
  export const fetchListaDeseos = async (usuarioId) => {
    const response = await fetch(`${API_URL}/lista_deseos/${usuarioId}/`);
    if (!response.ok) throw new Error('Error al cargar la lista de deseos');
    return response.json();
  };

  export const registerUser = async (userData) => {
    try {
      const response = await fetch(`${API_URL}/api/registro/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
      });
  
      if (!response.ok) {
        throw new Error('Error al registrar usuario');
      }
  
      const data = await response.json();
      return data;
    } catch (error) {
      throw error;
    }
  };

  export const loginUser = async (loginData) => {
    try {
      const response = await fetch(`${API_URL}/api/login/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(loginData),
      });
  
      if (!response.ok) {
        throw new Error('Credenciales inválidas');
      }
  
      const data = await response.json();
      
      // Guardamos los tokens
      localStorage.setItem('access_token', data.access);
      localStorage.setItem('refresh_token', data.refresh);
  
      return data;
    } catch (error) {
      throw error;
    }
  };


  export const realizarAccionProducto = async (productoId, accion) => {
    const formData = new FormData();
    formData.append('accion', accion);
  
    const response = await fetch(`http://localhost:8000/productos/${productoId}/`, {
      method: 'POST',
      body: formData,
      headers: {
        'X-CSRFToken': getCookie('csrftoken'), // Asegúrate de que getCookie esté definido
      },
    });
  
    if (!response.ok) {
      throw new Error('Error al procesar la transacción');
    }
  
    return response.json();
  };

export const obtenerUsuarios = async () => {
  try {
    const response = await fetch('http://localhost:8000/usuarios/');
    const data = await response.json();
    return data.usuarios;
  } catch (err) {
    throw new Error('Error al cargar los usuarios.');
  }
};

export const obtenerProductos = async (query) => {
    try {
      const response = await fetch(`http://localhost:8000/catalogo/?q=${query}`);
      const data = await response.json();
      return data.items;
    } catch (err) {
      throw new Error('Error al cargar los productos.');
    }
  };

export const obtenerFormularioSuscripcion = async () => {
    try {
      const response = await fetch('http://localhost:8000/suscripcion/', {
        method: 'GET',
      });
      const data = await response.text();  // Asumimos que el backend devuelve el formulario HTML completo
      return data;
    } catch (err) {
      throw new Error('Error al cargar el formulario de PayPal.');
    }
  };

export const GenerarCodigoVerificacion = () => {
    const [codigo, setCodigo] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
  
    const obtenerCodigo = async () => {
      setLoading(true);
      setError('');
  
      try {
        const response = await fetch('http://localhost:8000/generar-codigo/');
        const data = await response.json();
        if (response.ok) {
          setCodigo(data.codigo_verificacion);
        } else {
          setError('Error al generar el código.');
        }
      } catch (err) {
        setError('Error al conectar con el servidor.');
      } finally {
        setLoading(false);
      }
    };
  
    return (
      <div>
        <h1>Generar Código de Verificación</h1>
        <button onClick={obtenerCodigo} disabled={loading}>
          {loading ? 'Cargando...' : 'Generar Código'}
        </button>
        {codigo && <p>Código de Verificación: {codigo}</p>}
        {error && <p style={{ color: 'red' }}>{error}</p>}
      </div>
    );
  };

  export const enviarCorreoVerificacion = async (email) => {
    try {
      const response = await fetch(`http://localhost:8000/enviar-correo/${email}/`);
      const data = await response.json();
      if (response.ok) {
        return data.mensaje;
      } else {
        throw new Error('Error al enviar el correo.');
      }
    } catch (err) {
      throw new Error('Error al conectar con el servidor.');
    }
  };

  export const obtenerCarrito = async () => {
    const response = await fetch(`${API_URL}/api/carrito/`);
    if (!response.ok) {
      throw new Error('Error al obtener el carrito');
    }
    return response.json();
  };

  export const obtenerPedidos = async () => {
    try {
      const token = localStorage.getItem('token');  // Obtener el token desde localStorage
      const response = await fetch('http://localhost:8000/api/pedidos', {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,  // Incluir el token en los encabezados para autenticación
        },
      });
  
      // Verificar si la respuesta fue exitosa
      if (!response.ok) {
        throw new Error('Error al obtener los pedidos');
      }
  
      return await response.json();  // Retornar los datos de los pedidos
    } catch (error) {
      throw new Error('Error al cargar los pedidos: ' + error.message);
    }
  }; 

  export const obtenerDevoluciones = async () => {
    try {
      const token = localStorage.getItem('token');  // Obtener el token desde localStorage
      const response = await fetch('http://localhost:8000/api/devoluciones', {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,  // Incluir el token en los encabezados para autenticación
        },
      });
  
      // Verificar si la respuesta fue exitosa
      if (!response.ok) {
        throw new Error('Error al obtener las devoluciones');
      }
  
      return await response.json();  // Retornar los datos de las devoluciones
    } catch (error) {
      throw new Error('Error al cargar las devoluciones: ' + error.message);
    }
  };

export const registrarUsuario = async (username, email, password) => {
    try {
      const response = await fetch('http://localhost:8000/api/registro/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, email, password }),
      });
  
      // Verificar si la respuesta es exitosa
      if (!response.ok) {
        throw new Error('Error al registrar el usuario');
      }
  
      return await response.json();  // Retornar la respuesta en formato JSON
    } catch (error) {
      throw new Error('Error al registrar el usuario: ' + error.message);
    }
  };

  export const logoutUsuario = async () => {
    try {
      const response = await fetch('http://localhost:8000/logout/', {
        method: 'POST',
        credentials: 'include',  // Importante para enviar cookies de sesión
      });
  
      if (!response.ok) {
        throw new Error('Error al cerrar sesión');
      }
    } catch (error) {
      throw new Error('Error al realizar el logout: ' + error.message);
    }
  };


export const logoutUser = () => {
  try {
    // Aquí simplemente eliminas el token guardado
    localStorage.removeItem('token'); 
    localStorage.removeItem('user'); 
    console.log('Sesión cerrada correctamente.');
  } catch (error) {
    console.error('Error cerrando sesión:', error);
    throw error;
  }
};
  export const loginUsuario = async (email, password) => {
    try {
      const response = await fetch('http://localhost:8000/login/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
        credentials: 'include',  // Mantener las cookies de sesión
      });
  
      const data = await response.json();
  
      if (!response.ok) {
        throw new Error(data.error || 'Correo o contraseña incorrectos');
      }
  
      return data;  // Devuelve la respuesta en caso de éxito
    } catch (error) {
      throw new Error('Error al intentar iniciar sesión: ' + error.message);
    }
  };

  export const validarEmail = async (email) => {
    try {
      const response = await fetch('http://localhost:8000/api/validar_email/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email }),
      });
  
      const data = await response.json();
  
      if (!response.ok) {
        throw new Error(data.error || 'Este correo ya está registrado');
      }
  
      return data;  // Retorna los datos si la respuesta es exitosa
    } catch (error) {
      throw new Error('Error al validar el correo: ' + error.message);
    }
  };

  export const obtenerFormularioPaypal = async () => {
    try {
      const response = await fetch('/pago-paypal/', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });
  
      if (!response.ok) {
        throw new Error('Error al cargar los datos de PayPal');
      }
  
      const data = await response.json();
      return data.form_html;  // Devuelve el HTML del formulario de PayPal
    } catch (error) {
      throw new Error('Error al procesar la solicitud: ' + error.message);
    }
  };

  export const confirmarPagoPaypal = async (paymentData) => {
    try {
      const response = await fetch('/paypal-ipn/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(paymentData),
      });
  
      if (!response.ok) {
        throw new Error('Error al procesar el pago');
      }
  
      const data = await response.json();
      return data;  // Devuelve la respuesta de la API
    } catch (error) {
      throw new Error('Error al enviar la solicitud: ' + error.message);
    }
  };

  export const getPaymentStatus = async (paymentId) => {
    try {
      const response = await fetch(`/api/payment-status/${paymentId}/`);
      const data = await response.json();
      return data;
    } catch (error) {
      console.error("Error al obtener el estado del pago", error);
    }
  };
  
  export const obtenerTokenJWT = async (email, password) => {
    try {
      const response = await fetch('http://localhost:8000/api/token/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: email,
          password: password,
        }),
      });
  
      if (!response.ok) {
        throw new Error('Error en la autenticación');
      }
  
      const data = await response.json();  // Obtiene la respuesta JSON
      console.log('Token JWT:', data.access);  // Muestra el token JWT
  
      // Guarda el token en el almacenamiento local
      localStorage.setItem('access_token', data.access);
      return data.access;  // Devuelve el token
    } catch (error) {
      console.error('Error al realizar la solicitud:', error);
      throw error;  // Lanza el error para manejarlo en el frontend
    }
  };

  export const autenticarUsuario = async (email, password) => {
    try {
      const response = await fetch('http://localhost:8000/api/login/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: email,
          password: password,
        }),
      });
  
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Error de autenticación');
      }
  
      const data = await response.json();  // Obtiene la respuesta JSON
      console.log('Usuario autenticado:', data);
      localStorage.setItem('access_token', data.access_token);  // Guarda el token
      return data.access_token;  // Devuelve el token para usarlo en el frontend
  
    } catch (error) {
      console.error('Error en la solicitud:', error);
      throw error;  // Lanza el error para ser manejado en el frontend
    }
  };

  export const solicitarRestablecimientoContraseña = async (email) => {
    try {
      const response = await fetch('http://localhost:8000/password-reset/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email }),
      });
  
      if (response.ok) {
        const data = await response.json();
        console.log('Mensaje de éxito:', data.message);  // Mostrar mensaje de éxito
        return data.message;
      } else if (response.status === 400) {
        const errorData = await response.json();
        throw new Error(errorData.error);
      } else if (response.status === 429) {
        throw new Error('Límite de peticiones alcanzado. Inténtalo de nuevo más tarde.');
      } else {
        throw new Error('Error inesperado en la solicitud');
      }
    } catch (error) {
      console.error('Error en la solicitud:', error);
      throw error;  // Lanzamos el error para ser manejado en el frontend
    }
  };  

  export const agregarProducto = async (accion, productoId, csrfToken) => {
    const data = new FormData();
    data.append('accion', accion);
  
    try {
      const response = await fetch(`/producto/${productoId}/`, {
        method: 'POST',
        headers: {
          'X-CSRFToken': csrfToken,  // Incluye el token CSRF en las cabeceras
        },
        body: data,
      });
  
      if (response.ok) {
        const message = await response.text();  // Obtener el mensaje de respuesta
        console.log(message);  // O mostrar un mensaje en la interfaz
        return message;  // Devolver el mensaje de éxito
      } else {
        const errorMessage = await response.text();
        throw new Error(errorMessage);  // Lanza el error para manejarlo en el frontend
      }
    } catch (error) {
      console.error('Error al agregar producto:', error);
      throw error;  // Lanza el error para manejarlo en el frontend
    }
  };

  export const agregarAListaDeseos = async (productoId, csrfToken) => {
    try {
      const response = await fetch(`/agregar-a-lista-deseos/${productoId}/`, {
        method: 'POST',
        headers: {
          'X-CSRFToken': csrfToken,  // Incluye el token CSRF en las cabeceras
        },
      });
  
      if (!response.ok) {
        throw new Error('No se pudo agregar el producto a la lista de deseos.');
      }
  
      const data = await response.json();
  
      return data;  // Devuelve los datos de la respuesta (por ejemplo, success)
    } catch (error) {
      console.error('Error al agregar a la lista de deseos:', error);
      throw new Error('Hubo un error al agregar el producto a la lista de deseos.');
    }
  };

  export const cargarListaDeseos = async (csrfToken) => {
    try {
        const response = await fetch('/ver-lista-deseos/', {
            method: 'GET',
            headers: {
                'X-CSRFToken': csrfToken,  // Incluye el token CSRF en las cabeceras
            }
        });

        if (!response.ok) {
            throw new Error('No se pudo cargar la lista de deseos.');
        }

        const data = await response.json();
        return data;  // Devuelve la respuesta con los datos de la lista de deseos
    } catch (error) {
        console.error('Error al cargar la lista de deseos:', error);
        throw new Error('Hubo un error al cargar la lista de deseos.');
    }
};

export const fetchProductos = async () => {
  const response = await fetch('http://localhost:8000/productos/');
  if (!response.ok) throw new Error('Error al cargar los productos');
  return response.json();
};

export const crearSuscripcion = async (suscripcionData) => {
  const response = await fetch(`${API_URL}/suscripcion/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(suscripcionData),
  });

  if (!response.ok) throw new Error('Error al crear la suscripción');
  return response.json();
};

