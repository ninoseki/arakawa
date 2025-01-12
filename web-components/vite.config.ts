import path from 'path'
import copy from 'rollup-plugin-copy'
import { defineConfig, LibraryFormats, mergeConfig } from 'vite'
import VueDevTools from 'vite-plugin-vue-devtools'

import { baseConfig } from './base.vite.config'
import vueESM from './rollup-plugin-vue-esm'

export default defineConfig(({ mode }) =>
  mergeConfig(baseConfig, {
    plugins: [VueDevTools()],
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
  }),
)
