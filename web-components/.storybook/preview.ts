import '@/styles/tailwind.css'
import '@/styles/report.scss'
import '@/styles/user-iframe.css'
import 'highlight.js/styles/stackoverflow-light.css'

import { defaultConfig, plugin as formkitPlugin } from '@formkit/vue'
import { type Preview, setup } from '@storybook/vue3'
import { createPinia } from 'pinia'
import { type App } from 'vue'

import { formkitConfig } from '@/components/controls/formkit'

const pinia = createPinia()

setup((app: App) => {
  app.use(pinia)
  app.use(formkitPlugin, defaultConfig(formkitConfig))
})

const preview: Preview = {
  parameters: {
    backgrounds: {
      default: 'light',
    },
    controls: {
      matchers: {
        color: /(background|color)$/i,
        date: /Date$/,
      },
    },
  },
}

export default preview
