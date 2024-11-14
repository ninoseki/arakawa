import HiddenField from '@/components/controls/HiddenField.vue'

import { makeTemplate } from '../utils'

export default {
  title: 'Controls/HiddenField',
  component: HiddenField,
}

export const Primary = makeTemplate(HiddenField)

Primary.args = {
  name: 'Hidden field',
  initial: 'Dummy',
}
