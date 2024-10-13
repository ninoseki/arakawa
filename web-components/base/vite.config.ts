import path from 'path'
import tailwindcss from 'tailwindcss'
import { defineConfig } from 'vite'

import vueESM from '../shared/rollup-plugin-vue-esm'

module.exports = defineConfig(() => ({
  css: {
    postcss: {
      plugins: [
        tailwindcss({
          config: './tailwind.config.js',
        }),
      ],
    },
  },
  build: {
    outDir: './dist/base/',
    lib: {
      formats: ['es'],
      entry: '',
    },
    rollupOptions: {
      input: {
        index: path.resolve(__dirname, 'index.ts'),
      },
      output: {
        format: 'es',
        entryFileNames: '[name].[format].js',
        assetFileNames: '[name].[ext]',
      },
      plugins: [vueESM()],
    },
  },
}))
