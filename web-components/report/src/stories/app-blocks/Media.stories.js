import Media from '../../components/blocks/Media.vue'
import dpLogo from '../assets/dplogo.b64?raw'
import { makeTemplate } from '../utils'

export default {
  title: 'Media',
  component: Media,
}

export const Primary = makeTemplate(Media)

Primary.args = {
  src: `data:image/png;base64,${dpLogo}`,
  type: 'image/png',
}
