<script setup lang="ts">
import { ref } from 'vue'

import BlockWrapper from '@/components/layout/BlockWrapper.vue'
import type { BlockFigureProps } from '@/data-model/blocks'

import SvgBlock from './SVG.vue'

const p = defineProps<{
  fetchAssetData: any
  responsive: boolean
  figure: BlockFigureProps
  singleBlockEmbed?: boolean
}>()

const plotSrc = ref<string | null>(null)

;(async () => {
  plotSrc.value = await p.fetchAssetData()
})()
</script>

<template>
  <block-wrapper :figure="figure" :single-block-embed="singleBlockEmbed">
    <svg-block
      v-if="plotSrc"
      :src="plotSrc"
      :responsive="responsive"
      :single-block-embed="singleBlockEmbed"
    />
  </block-wrapper>
</template>
