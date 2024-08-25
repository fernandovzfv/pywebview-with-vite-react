import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: '../gui',
    assetsDir: '',
    sourcemap: false,
    emptyOutDir: true,
  }
})
