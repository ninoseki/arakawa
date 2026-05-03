import { fileURLToPath, URL } from 'node:url'

import tailwindcss from '@tailwindcss/postcss'
import vue from '@vitejs/plugin-vue'

/** @type {import('vite').UserConfig} */
export const baseConfig = {
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
      // Vite 8's rolldown-based resolver doesn't honor the `browser` subpath map
      // (`{"./sfc": "iframe-resizer.vue"}`) in `@iframe-resizer/vue/package.json`,
      // so map the SFC entry explicitly.
      '@iframe-resizer/vue/sfc': '@iframe-resizer/vue/iframe-resizer.vue',
    },
  },
  css: {
    postcss: {
      plugins: [tailwindcss()],
    },
  },
  plugins: [
    vue({
      template: {
        compilerOptions: {
          isCustomElement: (tag) => ['x'].some((ce) => tag.startsWith(`${ce}-`)),
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
