import type { StorybookConfig } from '@storybook/vue3-vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from 'tailwindcss'

const config: StorybookConfig = {
  stories: ['../src/**/*.mdx', '../src/**/*.stories.@(js|jsx|mjs|ts|tsx)'],
  addons: [
    '@storybook/addon-links',
    '@chromatic-com/storybook',
    '@storybook/addon-docs',
  ],
  framework: {
    name: '@storybook/vue3-vite',
    options: {},
  },
  async viteFinal(config) {
    config.css = {
      postcss: {
        plugins: [
          tailwindcss({
            config: './tailwind.config.js',
          }),
        ],
      },
    }
    config.plugins = (config.plugins || []).filter(
      p =>
        typeof p === 'object' &&
        p !== null &&
        'name' in p &&
        p.name !== 'vite:vue',
    )
    config.plugins.push(
      vue({
        template: {
          compilerOptions: {
            isCustomElement: tag => tag.startsWith('x-'),
          },
        },
      }),
    )
    return config
  },
}
export default config
