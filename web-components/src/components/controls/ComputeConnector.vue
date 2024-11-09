<script setup lang="ts">
/**
 * Use a connector here so we can separate the data model from the Vue component in testing.
 * Also possible to pass the individual store properties from the data model class via `Compute.componentProps`,
 * but this would remove re-rendering on `store.children` change.
 */
import { storeToRefs } from 'pinia'
import { ref } from 'vue'

import type { BlockFigureProps } from '@/data-model/blocks'

import { parseError } from '../../shared/shared'
import BlockWrapper from '../layout/BlockWrapper.vue'
import ComputeBlock from './Compute.vue'

const p = defineProps<{
  store: any
  prompt: string
  label: string
  figure: BlockFigureProps
  subtitle?: string
  action?: string
  method: string
}>()

const { children } = storeToRefs(p.store)

const error = ref<string | undefined>()

const onChange = (v: any) => {
  p.store.setField(v.name, v.value)
}

const update = async () => {
  try {
    error.value = undefined
  } catch (e) {
    error.value = parseError(e)
  }
}
</script>

<template>
  <block-wrapper :figure="p.figure" :show-overflow="true">
    <compute-block
      :on-change="onChange"
      :update="update"
      :children="children"
      :subtitle="p.subtitle"
      :label="p.label"
      :prompt="p.prompt"
      :action="p.action"
      :method="p.action"
      :error="error"
    />
  </block-wrapper>
</template>
