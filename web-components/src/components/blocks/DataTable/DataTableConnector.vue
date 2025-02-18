<script setup lang="ts">
import { storeToRefs } from 'pinia'
import { defineAsyncComponent, ref } from 'vue'

import BlockWrapper from '@/components/layout/BlockWrapper.vue'
import type {
  BlockFigureProps,
  DatasetResponse,
  ExportType,
} from '@/data-model/blocks'
import { useRootStore } from '@/data-model/root-store'

const DataTableBlock = defineAsyncComponent(() => import('./DataTable.vue'))

const p = defineProps<{
  streamContents: () => Promise<DatasetResponse>
  deferLoad: boolean
  cells: number
  refId: string
  getCsvText: () => Promise<string>
  downloadLocal: (type: ExportType) => Promise<void>
  figure: BlockFigureProps
  singleBlockEmbed?: boolean
}>()

const rootStore = useRootStore()
const { singleBlockEmbed: storedSingleBlockEmbed } = storeToRefs(rootStore)
const previewMode = ref(p.deferLoad)
const dsData = ref([])
const dsSchema = ref({})

const getResultData = async () => {
  /**
   * Fetch dataset content and schema
   */
  try {
    const successfulDownload: any = await p.streamContents()
    if (successfulDownload) {
      // TODO - containsBigInt
      const { schema, data } = successfulDownload
      dsData.value = dsData.value.concat(data)
      dsSchema.value = schema
    }
  } catch (e) {
    console.error('An error occurred downloading your dataset data: ' + e)
  }
}

if (!p.deferLoad) {
  getResultData()
}

const handleLoadFull = async () => {
  await getResultData()
  if (dsData.value.length) {
    previewMode.value = false
  }
}
</script>

<template>
  <block-wrapper
    :figure="figure"
    :single-block-embed="singleBlockEmbed || storedSingleBlockEmbed"
  >
    <data-table-block
      :singleBlockEmbed="!!singleBlockEmbed"
      :data="dsData"
      :cells="cells"
      :schema="dsSchema"
      :previewMode="previewMode"
      :getCsvText="getCsvText"
      :downloadLocal="downloadLocal"
      :refId="refId"
      @load-full="handleLoadFull"
    />
  </block-wrapper>
</template>
