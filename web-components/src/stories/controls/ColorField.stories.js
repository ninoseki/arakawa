import ColorField from '@/components/controls/ColorField.vue'

import { makeTemplate } from '../utils'

export default {
  title: 'Controls/ColorField',
  component: ColorField,
}

export const Primary = makeTemplate(ColorField)

Primary.args = {
  name: 'ColorField',
}
