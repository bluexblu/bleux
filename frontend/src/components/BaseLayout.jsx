import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Outlet } from 'react-router-dom';

const BaseLayout = () => {
    const navigate = useNavigate();  // Hook para navegar

    const handleNavigation = (path) => {
        navigate(path);  // Función que maneja la navegación
    };

    return (
        <div>
            {/* Navbar */}
            <nav className="navbar navbar-expand-lg navbar-dark">
                <div className="container-fluid">
                    <a className="navbar-brand pe-4 me-4 border-end border-light" href="/">lesyeux</a>
                    <button className="navbar-toggler" type="button" data-bs-toggle="collapse"
                        data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false"
                        aria-label="Toggle navigation">
                        <span className="navbar-toggler-icon"></span>
                    </button>
                    <div className="collapse navbar-collapse" id="navbarNav">
                        <ul className="navbar-nav me-auto gap-2">
                            <li className="nav-item dropdown">
                                <button
                                    className="nav-link dropdown-toggle btn btn-link"
                                    onClick={() => handleNavigation('/catalogo')}
                                    aria-expanded="false"
                                >
                                    Catálogo
                                </button>
                                <ul className="dropdown-menu dropdown-menu-dark">
                                    <li><button className="dropdown-item" onClick={() => handleNavigation('/peliculas')}>Películas</button></li>
                                    <li><button className="dropdown-item" onClick={() => handleNavigation('/series')}>Series</button></li>
                                    <li><button className="dropdown-item" onClick={() => handleNavigation('/comics')}>Cómics</button></li>
                                </ul>
                            </li>
                            <li className="nav-item">
                                <button className="nav-link btn btn-link" onClick={() => handleNavigation('/carrito')}>Carrito</button>
                            </li>
                            <li className="nav-item dropdown">
                                <button
                                    className="nav-link dropdown-toggle btn btn-link"
                                    onClick={() => handleNavigation('/usuarios')}
                                    aria-expanded="false"
                                >
                                    Usuarios
                                </button>
                                <ul className="dropdown-menu dropdown-menu-dark">
                                    <li><button className="dropdown-item" onClick={() => handleNavigation('/usuarios')}>Usuarios</button></li>
                                </ul>
                            </li>
                            <li className="nav-item dropdown">
                                <button
                                    className="nav-link dropdown-toggle btn btn-link"
                                    onClick={() => handleNavigation('/suscripcion')}
                                    aria-expanded="false"
                                >
                                    Suscripción
                                </button>
                                <ul className="dropdown-menu dropdown-menu-dark">
                                    <li><button className="dropdown-item" onClick={() => handleNavigation('/planes')}>Planes</button></li>
                                    <li><button className="dropdown-item" onClick={() => handleNavigation('/metodos_pago')}>Métodos de Pago</button></li>
                                </ul>
                            </li>
                        </ul>

                        {/* Sesion // Autenticacion */}
                        <ul className="navbar-nav gap-2">
                            <li className="nav-item dropdown">
                                <button
                                    className="btn btn-outline-light dropdown-toggle"
                                    onClick={(e) => e.preventDefault()}
                                    id="cuentaDropdown"
                                >
                                    Mi cuenta
                                </button>
                                <ul className="dropdown-menu dropdown-menu-end dropdown-menu-dark" aria-labelledby="cuentaDropdown">
                                    <li><button className="dropdown-item" onClick={() => handleNavigation('/login')}>Ingresar</button></li>
                                    <li><button className="dropdown-item" onClick={() => handleNavigation('/registro')}>Regístrate</button></li>
                                </ul>
                            </li>
                        </ul>
                    </div>
                </div>
            </nav>

            {/* Aquí se renderiza el contenido específico de cada página */}
            <main className="container">
                <Outlet /> {/* Aquí es donde se renderizan las rutas hijas */}
            </main>

            {/* Footer */}
            <footer className="text-center py-4">
                <p>&copy; 2025 lesyeux. Todos los derechos reservados.</p>
            </footer>
        </div>
    );
};

export default BaseLayout;
