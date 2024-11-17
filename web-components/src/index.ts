import '@/styles/base.scss'
import '@/styles/report.scss'
import 'highlight.js/styles/stackoverflow-light.css'
import '@fortawesome/fontawesome-free/css/fontawesome.css'
import '@fortawesome/fontawesome-free/css/solid.css'

import { defaultConfig, plugin as formkitPlugin } from '@formkit/vue'
import iframeResize from 'iframe-resizer/js/iframeResizer'
import { createPinia } from 'pinia'
import { createApp, defineCustomElement } from 'vue'

import TableBlock from './components/blocks/Table.ce.vue'
import { formkitConfig } from './components/controls/formkit'
import Report from './components/ReportContainer.vue'

// report
import('./tailwind')

customElements.define('x-table-block', defineCustomElement(TableBlock))

const parseElementProps = (elId: string): any => {
  const propsEl = document.getElementById(elId)
  if (!propsEl || !propsEl.textContent) {
    throw new Error("Couldn't find props JSON element")
  }
  return JSON.parse(propsEl.textContent)
}

const mountReport = (props: any) => {
  const app = createApp(Report, props)
  const pinia = createPinia()
  app.use(pinia)
  app.use(formkitPlugin, defaultConfig(formkitConfig))
  app.mount('#report')
  return app
}

export { iframeResize, mountReport, parseElementProps }
