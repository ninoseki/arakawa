<script setup lang="ts">
import { ref } from 'vue'

import type { BlockFigureProps } from '@/data-model/blocks'

import BlockWrapper from '../layout/BlockWrapper.vue'

const p = defineProps<{
  fetchAssetData: any
  figure: BlockFigureProps
  singleBlockEmbed?: { type: boolean; default: false }
}>()
const html = ref<string | null>(null)

;(async () => {
  html.value = await p.fetchAssetData()
})()
</script>

<template>
  <block-wrapper :figure="p.figure" :single-block-embed="singleBlockEmbed">
    <x-table-block
      v-if="html"
      :html="html"
      :single-block-embed="singleBlockEmbed"
      class="w-full"
    />
  </block-wrapper>
</template>
