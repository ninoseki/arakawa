import Folium from '@/components/blocks/Folium.vue'

import iframeContent from '../assets/folium.html?raw'
import { makeTemplate } from '../utils'

export default {
  title: 'Folium',
  component: Folium,
}

export const Primary = makeTemplate(Folium)

Primary.args = {
  singleBlockEmbed: false,
  iframeContent,
}
