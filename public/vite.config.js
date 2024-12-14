import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  base: '',  // Ensures relative paths for assets in index.html
  plugins: [react()],
  build: {
    outDir: 'dist',  // Output folder
    target: 'esnext',  // Use modern JavaScript for better performance
    chunkSizeWarningLimit: 500,  // Warn if any chunk exceeds 500KB
    rollupOptions: {
      output: {
        // Place all JavaScript entry files in the "js" folder with a hash for cache busting
        entryFileNames: 'js/[name]-[hash].js',
        // Place dynamically split JavaScript chunks in the "js" folder
        chunkFileNames: 'js/[name]-[hash].js',
        // Place CSS assets in the "css" folder with a hash for cache busting
        assetFileNames: 'css/[name]-[hash][extname]',
        
        // Manual chunking to separate dependencies from application code
        manualChunks(id) {
          if (id.includes('node_modules')) {
            return id.toString().split('node_modules/')[1].split('/')[0].toString();
          }
        },
      },
    },
  },
})
