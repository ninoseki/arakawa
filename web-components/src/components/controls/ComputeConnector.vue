<script setup lang="ts">
/**
 * Use a connector here so we can separate the data model from the Vue component in testing.
 * Also possible to pass the individual store properties from the data model class via `Compute.componentProps`,
 * but this would remove re-rendering on `store.children` change.
 */
import BlockWrapper from '@/components/layout/BlockWrapper.vue'
import type { BlockFigureProps } from '@/data-model/blocks'

import ComputeBlock from './Compute.vue'

defineProps<{
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
  <block-wrapper :figure="figure" :show-overflow="true">
    <compute-block
      :children="children"
      :subtitle="subtitle"
      :label="label"
      :prompt="prompt"
      :action="action"
      :method="method"
    />
  </block-wrapper>
</template>
