<script setup lang="ts">
import { defineAsyncComponent } from 'vue'

import BlockWrapper from '@/components/layout/BlockWrapper.vue'
import type { BlockFigureProps } from '@/data-model/blocks'

const Formula = defineAsyncComponent(() => import('./Formula.vue'))
defineProps<{
  content: string
  figure: BlockFigureProps
  singleBlockEmbed?: boolean
}>()
</script>

<template>
  <block-wrapper :figure="figure" :single-block-embed="singleBlockEmbed">
    <formula :content="content"></formula>
  </block-wrapper>
</template>
