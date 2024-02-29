import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

export default defineConfig({
  plugins: [vue()],
  build: {
    lib: {
      entry: 'src/main.js',
      name: 'Like',
      formats: ['es']
    },
    rollupOptions: {
      output: {
        globals: {
          vue: 'Vue'
        },
        dir: '../djangogramm/static/js/vue-bundle/',
        entryFileNames: 'bundle.js'
      }
    }
  },
  define: {
    'process.env': {}
  },
  resolve: {
    alias: {
      'vue': 'vue/dist/vue.esm-bundler.js'
    }
  }
});
