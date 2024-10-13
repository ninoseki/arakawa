import { ARClipboard } from '../shared/ARClipboard'
import './src/polyfills'
import './src/styles/base.scss'
import './src/styles/tailwind.css'
import './src/styles/templates-base.scss'
// JS Polyfills
import 'whatwg-fetch'

// Window objects
window.errorHandler = window.errorHandler || {}

export { ARClipboard as DPClipboard }
