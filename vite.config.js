import { defineConfig } from 'vite'
import { resolve } from 'path'

export default defineConfig({
  base: '/static/',
  build: {
    outDir: resolve('./core/static/'),
    assetsDir: '',
    manifest: true,
    minify: 'esbuild',
    cssMinify: true,
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
          if (/\.(woff2?|eot|ttf|otf)$/.test(name ?? '')) {
            return 'fonts/[name][extname]';
          }
          return '[name]-[hash][extname]';
        },
      },
    },
    cssCodeSplit: true,
    sourcemap: false,
    target: 'es2015',
    chunkSizeWarningLimit: 500,
    reportCompressedSize: true
  },
  server: {
    host: '0.0.0.0',
    port: 3000,
    open: false,
    origin: 'http://node:3000',
    watch: {
      usePolling: true,
      disableGlobbing: false,
    },
    fs: {
      strict: false,
      allow: ['..']
    }
  },
  resolve: {
    alias: {
      '@': resolve(__dirname, './'),
      '~bootstrap-icons': resolve(__dirname, 'node_modules/bootstrap-icons')
    }
  },
  publicDir: resolve(__dirname, 'public')
}) 