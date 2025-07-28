import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0', // Required for Docker to expose the server
    port: 3000, // Set Vite to run on port 3000
    hmr: {
      host: 'localhost', // Ensure HMR connects to localhost
      protocol: 'ws',    // Use WebSocket for HMR
    },
    watch: {
      usePolling: true, // Enable polling for file changes
      interval: 1000,   // Check every 1 second
    },
      optimizeDeps: {
      exclude: ['lucide-react'],
    },
  }
})
