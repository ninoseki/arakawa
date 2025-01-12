import '@/styles/base.scss'
import '@/styles/report.scss'
import '@fortawesome/fontawesome-free/css/fontawesome.css'
import '@fortawesome/fontawesome-free/css/solid.css'
import 'highlight.js/styles/stackoverflow-light.css'

import { defaultConfig, plugin as formkitPlugin } from '@formkit/vue'
import { createPinia } from 'pinia'
import { createApp, defineCustomElement } from 'vue'

import TableBlock from '@/components/blocks/Table.ce.vue'
import { formkitConfig } from '@/components/controls/formkit'
import Report from '@/components/ReportContainer.vue'

import('./tailwind')

customElements.define('x-table-block', defineCustomElement(TableBlock))

window.addEventListener('DOMContentLoaded', () => {
  const { reportProps } = window
  const app = createApp(Report, reportProps)
  const pinia = createPinia()
  app.use(pinia)
  app.use(formkitPlugin, defaultConfig(formkitConfig))
  app.mount('#report')
  return app
})
