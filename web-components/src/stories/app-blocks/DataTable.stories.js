import DataTable from '@/components/blocks/DataTable/DataTable.vue'

import { makeTemplate } from '../utils'

export default {
  title: 'DataTable',
  component: DataTable,
}

export const Primary = makeTemplate(DataTable)

Primary.args = {
  cells: 600,
  deferLoad: false,
  downloadLocal: async () => ({}),
  getCsvText: async () => ({}),
  refId: '1e3104e2-1e7f-4750-ae97-4c354041df29',
  data: [...Array(100).keys()].map(n => ({
    A: n,
    B: `foo ${n}`,
    C: n % 2 === 0,
    D: Math.random(),
    E: Math.random() > 0.5 ? 'foo' : 'bar',
    F: new Date(),
  })),
  schema: [
    { name: 'A', type: 'integer' },
    { name: 'B', type: 'string' },
    { name: 'C', type: 'boolean' },
    { name: 'D', type: 'double' },
    { name: 'E', type: 'category' },
    { name: 'F', type: 'timestamp' },
  ],
  previewMode: false,
  singleBlockEmbed: false,
}
