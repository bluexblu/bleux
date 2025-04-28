import 'bootstrap/dist/css/bootstrap.min.css';  // Debe estar al principio
import './index.css';  // Si tienes un archivo CSS personalizado
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
   <React.StrictMode>  // Comenta esta línea
  <App />
  </React.StrictMode>
);
