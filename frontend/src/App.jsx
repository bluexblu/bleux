// App.jsx
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import BaseLayout from './components/BaseLayout'; // Ajusta según la ubicación de tu componente
import Gallery from './components/Gallery'; // Asegúrate de que Home exista en la carpeta 'pages'
import Peliculas from './pages/Peliculas'; // Asegúrate de que Peliculas exista en la carpeta 'pages'
import Series from './pages/Series'; // Asegúrate de que Series exista en la carpeta 'pages'
import Comics from './pages/Comics'; // Asegúrate de que Comics exista en la carpeta 'pages'
import Usuarios from './pages/Usuarios'; // Asegúrate de que Usuarios exista en la carpeta 'pages'
import Planes from './pages/Planes'; // Asegúrate de que Planes exista en la carpeta 'pages'
import MetodosPago from './pages/MetodosPago'; // Asegúrate de que MetodosPago exista en la carpeta 'pages'
import LoginForm from './components/LoginForm'; // Asegúrate de que LoginForm exista en la carpeta 'components'
import RegistroForm from './components/RegistroForm'; // Asegúrate de que RegistroForm exista en la carpeta 'components'
import Carrito from './components/CarritoPage'; // Asegúrate de que Carrito exista en la carpeta 'components'

import 'bootstrap/dist/css/bootstrap.min.css';  // Importa Bootstrap si es necesario

const App = () => {
  return (
    <Router>
      <BaseLayout>
        <Routes>
          <Route path="/" element={<Gallery />} />
          <Route path="peliculas" element={<Peliculas />} />
          <Route path="series" element={<Series />} />
          <Route path="comics" element={<Comics />} />
          <Route path="usuarios" element={<Usuarios />} />
          <Route path="planes" element={<Planes />} />
          <Route path="metodos_pago" element={<MetodosPago />} />
          <Route path="login" element={<LoginForm />} />
          <Route path="registro" element={<RegistroForm />} />
          <Route path="carrito" element={<Carrito />} />
        </Routes>
      </BaseLayout>
    </Router>
  );
}

export default App;
