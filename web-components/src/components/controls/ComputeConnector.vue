<script setup lang="ts">
/**
 * Use a connector here so we can separate the data model from the Vue component in testing.
 * Also possible to pass the individual store properties from the data model class via `Compute.componentProps`,
 * but this would remove re-rendering on `store.children` change.
 */
import type { BlockFigureProps } from '@/data-model/blocks'

import BlockWrapper from '../layout/BlockWrapper.vue'
import ComputeBlock from './Compute.vue'

const p = defineProps<{
  children: any
  prompt: string
  label: string
  figure: BlockFigureProps
  subtitle?: string
  action?: string
  method: string
}>()
</script>

<template>
  <block-wrapper :figure="p.figure" :show-overflow="true">
    <compute-block
      :children="children"
      :subtitle="p.subtitle"
      :label="p.label"
      :prompt="p.prompt"
      :action="p.action"
      :method="p.method"
    />
  </block-wrapper>
</template>
