import type { StorybookConfig } from '@storybook/vue3-vite'
import tailwindcss from '@tailwindcss/postcss'
import vue from '@vitejs/plugin-vue'

const config: StorybookConfig = {
  stories: ['../src/**/*.mdx', '../src/**/*.stories.@(js|jsx|mjs|ts|tsx)'],
  addons: ['@storybook/addon-links', '@chromatic-com/storybook', '@storybook/addon-docs'],
  framework: {
    name: '@storybook/vue3-vite',
    options: {},
  },
  async viteFinal(config) {
    config.css = {
      postcss: {
        plugins: [tailwindcss()],
      },
    }
    config.plugins = (config.plugins || []).filter(
      (p) => typeof p === 'object' && p !== null && 'name' in p && p.name !== 'vite:vue',
    )
    config.plugins.push(
      vue({
        template: {
          compilerOptions: {
            isCustomElement: (tag) => tag.startsWith('x-'),
          },
        },
      }),
    )
    return config
  },
}
export default config
