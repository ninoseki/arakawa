// JS Polyfills
import 'whatwg-fetch'
import './styles/base.scss'
import './styles/report.scss'
import '@fortawesome/fontawesome-free/css/all.css'
import 'highlight.js/styles/stackoverflow-light.css'

import { defaultConfig, plugin as formkitPlugin } from '@formkit/vue'
import iframeResize from 'iframe-resizer/js/iframeResizer'
import { createPinia } from 'pinia'
import { createApp, defineCustomElement } from 'vue'

import TableBlock from './components/blocks/Table.ce.vue'
import { formkitConfig } from './components/controls/formkit'
import Report from './components/ReportContainer.vue'
import { ARClipboard } from './shared/ARClipboard'

// base
window.errorHandler = window.errorHandler || {}

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

export { ARClipboard, iframeResize, mountReport, parseElementProps }
