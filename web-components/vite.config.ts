import { fileURLToPath, URL } from 'node:url'

import vue from '@vitejs/plugin-vue'
import path from 'path'
import copy from 'rollup-plugin-copy'
import tailwindcss from 'tailwindcss'
import { defineConfig, LibraryFormats } from 'vite'
import VueDevTools from 'vite-plugin-vue-devtools'

import vueESM from './rollup-plugin-vue-esm'

// https://vite.dev/config/
export default defineConfig(({ mode }) => ({
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  css: {
    postcss: {
      plugins: [
        tailwindcss({
          config: './tailwind.config.js',
        }),
      ],
    },
  },
  plugins: [
    VueDevTools(),
    vue({
      template: {
        compilerOptions: {
          isCustomElement: tag => ['x'].some(ce => tag.startsWith(`${ce}-`)),
        },
      },
    }),
  ],
  define: {
    // Bokeh 2.4 expects a global PACKAGE_VERSION to be defined
    PACKAGE_VERSION: JSON.stringify(process.env.npm_package_version),
    // Pinia expects the node `process` global to be defined but support for this
    // was removed in Vite 3
    'process.env.NODE_ENV': `"${process.env.NODE_ENV}"`,
  },
  build: {
    sourcemap: mode === 'development',
    // Enabled in order to split out report `tailwind.css` file
    cssCodeSplit: true,
    outDir: './dist/report/',
    lib: {
      entry: [path.resolve(__dirname, './src/index.ts')],
      formats: ['es'] as LibraryFormats[],
      fileName: '[name]',
    },
    rollupOptions: {
      output: {
        assetFileNames: '[name].[ext]',
        entryFileNames: '[name].[format].js',
        chunkFileNames: '[name].[hash].[format].js',
        paths: {
          vue:
            mode === 'development'
              ? '../vue.esm-browser.js'
              : '../vue.esm-browser.prod.js',
        },
      },
      external: ['vue'],
      plugins: [
        vueESM(),
        // Cast as `any` as there seems to be a type conflict between the rollup plugin and Vite's typed config (which uses rollup under the hood)
        copy({
          targets: [
            {
              src: './node_modules/@iframe-resizer/child/index.umd.js',
              dest: './dist/assets',
            },
          ],
          verbose: true,
        }),
      ],
    },
  },
}))
