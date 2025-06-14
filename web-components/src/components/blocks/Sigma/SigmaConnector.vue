<script setup lang="ts">
import BlockWrapper from '@/components/layout/BlockWrapper.vue'
import type { BlockFigureProps } from '@/data-model/blocks'

import Sigma from './Sigma.vue'

defineProps<{
  data: unknown
  layoutSettings: unknown
  height: number
  width: number
  figure: BlockFigureProps
  singleBlockEmbed?: boolean
}>()
</script>

<template>
  <block-wrapper :figure="figure" :single-block-embed="singleBlockEmbed">
    <sigma
      :data="data"
      :layout-settings="layoutSettings"
      :height="height"
      :width="width"
    />
  </block-wrapper>
</template>
