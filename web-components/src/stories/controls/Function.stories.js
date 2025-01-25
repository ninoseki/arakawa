import Compute from '@/components/controls/Compute.vue'

import * as b from '../../data-model/blocks'
import { makeTemplate } from '../utils'

export default {
  title: 'Controls/Compute',
  component: Compute,
}

export const Primary = makeTemplate(Compute)

Primary.args = {
  method: 'GET',
  label: 'Compute block',
  subtitle: 'Compute subtitle',
  prompt: 'Custom prompt',
  children: [
    new b.TemporalDateTimeField(
      {
        initial: '2023-01-05T15:27:00',
        name: 'DateTime',
      },
      {},
      { timeFormat: 'YYYY-MM-DDTHH:mm:ss', type: 'datetime-local' },
    ),
    new b.FileField(
      {
        name: 'File',
      },
      {},
    ),
    new b.TemporalTextBox(
      {
        name: 'Input',
      },
      {},
      { type: 'text' },
    ),
    new b.MultiChoiceField(
      {
        options: ['foo', 'bar', 'boo', 'far'],
        initial: ['foo'],
        name: 'MultiSelect',
      },
      {},
    ),
    new b.RangeField(
      {
        min: 0,
        max: 10,
        initial: 3,
        step: 1,
        name: 'Range',
      },
      {},
    ),
    new b.SelectField(
      {
        options: ['foo', 'bar', 'boo', 'far'],
        initial: 'foo',
        name: 'Select',
      },
      {},
    ),
    new b.SwitchField(
      {
        initial: false,
        name: 'Switch',
      },
      {},
    ),
    new b.TagsField(
      {
        options: ['foo', 'bar', 'boo', 'far'],
        initial: ['foo'],
        name: 'Tags',
      },
      {},
    ),
  ],
}
