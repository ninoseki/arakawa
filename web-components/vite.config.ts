import path from 'path'
import copy from 'rollup-plugin-copy'
import { defineConfig, LibraryFormats, mergeConfig } from 'vite'

import { baseConfig } from './base.vite.config'
import vueESM from './rollup-plugin-vue-esm'

export default defineConfig(({ mode }) =>
  mergeConfig(baseConfig, {
    plugins: [
      // ref. https://github.com/vuejs/devtools/issues/703
      // VueDevTools(),
    ],
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
          entryFileNames: '[name].js',
          chunkFileNames: '[name].[hash].js',
          paths: {
            vue: mode === 'development' ? '../vue.esm-browser.js' : '../vue.esm-browser.prod.js',
          },
        },
        external: ['vue'],
        plugins: [
          vueESM(),
          // Cast as `any` as there seems to be a type conflict between the rollup plugin and Vite's typed config (which uses rollup under the hood)
          copy({
            hook: 'writeBundle',
            targets: [
              {
                src: './node_modules/@iframe-resizer/child/index.umd.js',
                dest: './dist/assets',
              },
              {
                src: './node_modules/katex/dist/katex.min.css',
                dest: './dist/report',
                rename: 'katex.css',
              },
              {
                src: './node_modules/katex/dist/fonts',
                dest: './dist/report',
              },
            ],
            verbose: true,
          }),
        ],
      },
    },
  }),
)
