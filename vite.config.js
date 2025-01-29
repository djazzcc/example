import { defineConfig } from 'vite'
import { resolve } from 'path'

export default defineConfig({
  base: '/static/',
  build: {
    outDir: resolve('./core/static/'),
    assetsDir: '',
    manifest: true,
    rollupOptions: {
      input: {
        main: resolve('./core/assets/js/main.js'),
      },
      output: {
        chunkFileNames: 'js/[name]-[hash].js',
        entryFileNames: 'js/[name]-[hash].js',
        assetFileNames: ({name}) => {
          if (/\.(gif|jpe?g|png|svg)$/.test(name ?? '')){
            return 'img/[name]-[hash][extname]';
          }
          if (/\.css$/.test(name ?? '')) {
            return 'css/[name]-[hash][extname]';
          }
          return '[name]-[hash][extname]';
        },
      },
    },
  },
  server: {
    host: 'localhost',
    port: 5173,
    open: false,
    watch: {
      usePolling: true,
      disableGlobbing: false,
    },
  },
}) 