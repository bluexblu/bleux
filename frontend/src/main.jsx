// index.js o main.jsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';  // Si tienes archivos de estilos globales

const root = ReactDOM.createRoot(document.getElementById('root'));  // Crear el root
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
