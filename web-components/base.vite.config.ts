import { fileURLToPath, URL } from 'node:url'

import vue from '@vitejs/plugin-vue'
import tailwindcss from 'tailwindcss'

/** @type {import('vite').UserConfig} */
export const baseConfig = {
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
}
