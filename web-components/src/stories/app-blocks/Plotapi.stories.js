import Plotapi from '../../components/blocks/Plotapi.vue'
import iframeContent from '../assets/plotapi.html?raw'
import { makeTemplate } from '../utils'

export default {
  title: 'Plotapi',
  component: Plotapi,
}

export const Primary = makeTemplate(Plotapi)

Primary.args = {
  iframeContent,
  singleBlockEmbed: false,
}
