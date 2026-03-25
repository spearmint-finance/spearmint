import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    host: true,  // Bind to 0.0.0.0 for dev container port forwarding
    port: 5173,
    watch: {
      usePolling: true,  // Required for WSL2 where inotify is unreliable
      interval: 500,
    },
    headers: {
      'Cache-Control': 'no-store',  // Prevent browser from caching dev assets
    },
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
})

