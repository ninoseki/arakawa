import SVG from '../../components/blocks/SVG.vue'
import svgData from '../assets/svg.b64?raw'
import { makeTemplate } from '../utils'

export default {
  title: 'SVG',
  component: SVG,
}

export const Primary = makeTemplate(SVG)

Primary.args = {
  src: `data:image/svg+xml;base64,${svgData}`,
  responsive: true,
}
