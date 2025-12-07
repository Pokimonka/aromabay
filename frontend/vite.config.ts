import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    strictPort: true,
    allowedHosts: [
      'aromabay.site',
      'localhost',
      '127.0.0.1',
      '213.171.12.94'
    ],
    proxy: {
      '/api': {
        target: 'https://aromabay.site',
        changeOrigin: true,
      },
    },
  },
})
