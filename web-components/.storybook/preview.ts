import '@/styles/tailwind.css'
import '@/styles/report.scss'
import '@/styles/user-iframe.css'
import 'highlight.js/styles/stackoverflow-light.css'

import { defaultConfig, plugin as formkitPlugin } from '@formkit/vue'
import { type Preview, setup } from '@storybook/vue3'
import { createPinia } from 'pinia'

import { formkitConfig } from '@/components/controls/formkit'

const pinia = createPinia()

setup(app => {
  app.use(formkitPlugin, defaultConfig(formkitConfig))
  app.use(pinia)
})

const preview: Preview = {
  parameters: {
    controls: {
      matchers: {
        color: /(background|color)$/i,
        date: /Date$/i,
      },
    },
  },
}

export default preview
