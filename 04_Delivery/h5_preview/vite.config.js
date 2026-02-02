import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: [
      { find: '@', replacement: path.resolve(__dirname, 'src') },
      { find: /^\/visuals/, replacement: path.resolve(__dirname, '../../02_Visuals/assets') },
      { find: /^\/tts/, replacement: path.resolve(__dirname, '../../03_Scripts/tts') },
    ]
  },
  server: {
    fs: {
      // Allow serving files from one level up to the project root
      allow: ['..', '../../']
    }
  }
})
