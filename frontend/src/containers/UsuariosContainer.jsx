// UsuariosContainer.jsx
import React, { useEffect, useState } from 'react';
import { fetchUsuarios } from '../api/api';
import Usuarios from '../components/Usuarios';  // Asegúrate de importar bien

const UsuariosContainer = () => {
  const [usuarios, setUsuarios] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchUsuarios()
      .then((data) => {
        setUsuarios(data);
        setLoading(false);
      })
      .catch((err) => {
        setError('Error al cargar los usuarios');
        setLoading(false);
      });
  }, []);

  if (loading) return <div>Cargando usuarios...</div>;
  if (error) return <div style={{ color: 'red' }}>{error}</div>;

  return <Usuarios usuarios={usuarios} />;
};

export default UsuariosContainer;
