<script setup lang="ts">
import { ref } from 'vue'

import BlockWrapper from '@/components/layout/BlockWrapper.vue'
import type { BlockFigureProps } from '@/data-model/blocks'

import Folium from './Folium.vue'

const p = defineProps<{
  fetchAssetData: any
  figure: BlockFigureProps
  singleBlockEmbed?: boolean
}>()
const iframeContent = ref<string | null>(null)

;(async () => {
  iframeContent.value = await p.fetchAssetData()
})()
</script>

<template>
  <block-wrapper :figure="figure" :single-block-embed="singleBlockEmbed">
    <folium
      v-if="iframeContent"
      :iframe-content="iframeContent"
      :single-block-embed="singleBlockEmbed"
    />
  </block-wrapper>
</template>
