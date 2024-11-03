import replace from '@rollup/plugin-replace'
import type { StorybookConfig } from '@storybook/vue3-vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from 'tailwindcss'

const config: StorybookConfig = {
  stories: ['../src/**/*.mdx', '../src/**/*.stories.@(js|jsx|mjs|ts|tsx)'],
  addons: [
    '@storybook/addon-onboarding',
    '@storybook/addon-links',
    '@storybook/addon-essentials',
    '@chromatic-com/storybook',
    '@storybook/addon-interactions',
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
    config.plugins = config.plugins.filter(p => p.name !== 'vite:vue')
    config.plugins.push(
      vue({
        template: {
          compilerOptions: {
            isCustomElement: tag => tag.startsWith('x-'),
          },
        },
      }),
      replace({
        include: ['../node_modules/@bokeh/**/*.js'],
        values: {
          // shim jquery to window object for bokehjs
          jQuery: 'window.jQuery',
        },
        preventAssignment: false,
      }),
    )
    return config
  },
}
export default config
