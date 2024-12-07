<script setup lang="ts">
import { defineAsyncComponent, ref } from 'vue'

import BlockWrapper from '@/components/layout/BlockWrapper.vue'
import type { BlockFigureProps } from '@/data-model/blocks'

const PlotlyBlock = defineAsyncComponent(() => import('./Plotly.vue'))

const p = defineProps<{
  fetchAssetData: any
  responsive: boolean
  figure: BlockFigureProps
  singleBlockEmbed?: boolean
}>()

const plotJson = ref<any>(null)

;(async () => {
  plotJson.value = await p.fetchAssetData()
})()
</script>

<template>
  <block-wrapper :figure="figure" :single-block-embed="singleBlockEmbed">
    <plotly-block
      v-if="plotJson"
      :plot-json="plotJson"
      :responsive="responsive"
      :single-block-embed="singleBlockEmbed"
    />
  </block-wrapper>
</template>
