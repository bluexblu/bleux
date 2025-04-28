// vite.config.js
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// vite.config.js
export default defineConfig({
  plugins: [react()],
  build: {
    outDir: '../backend/static',  // El directorio donde Django busca los archivos estáticos
    emptyOutDir: true,  // Limpiar la carpeta de salida antes de construir
  },
});