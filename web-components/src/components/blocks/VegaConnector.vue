<script setup lang="ts">
import { storeToRefs } from 'pinia'
import { defineAsyncComponent, ref } from 'vue'

import BlockWrapper from '@/components/layout/BlockWrapper.vue'
import type { BlockFigureProps } from '@/data-model/blocks'
import { useRootStore } from '@/data-model/root-store'

const VegaBlock = defineAsyncComponent(() => import('./Vega.vue'))

const rootStore = useRootStore()
const { singleBlockEmbed: storedSingleBlockEmbed } = storeToRefs(rootStore)

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
  <block-wrapper
    :figure="figure"
    :single-block-embed="singleBlockEmbed || storedSingleBlockEmbed"
  >
    <vega-block
      v-if="plotJson"
      :plot-json="plotJson"
      :responsive="responsive"
      :single-block-embed="singleBlockEmbed"
    ></vega-block>
  </block-wrapper>
</template>
