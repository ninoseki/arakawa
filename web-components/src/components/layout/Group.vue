<script setup lang="ts">
import { storeToRefs } from 'pinia'
import { computed, type ComputedRef, type Ref } from 'vue'

import type { Block } from '@/data-model/blocks'
import { useRootStore } from '@/data-model/root-store'
import { VAlign } from '@/data-model/types'

const p = defineProps<{
  columns: number
  widths?: number[]
  store: any
  valign?: VAlign
}>()

const rootStore = useRootStore()
const { singleBlockEmbed } = storeToRefs(rootStore)
const { children }: { children: Ref<Block[]> } = storeToRefs(p.store)

const alignItems: ComputedRef<string> = computed(() => {
  switch (p.valign) {
    default:
    case VAlign.TOP:
      return 'start'
    case VAlign.CENTER:
      return 'center'
    case VAlign.BOTTOM:
      return 'end'
  }
})

const gridTemplateColumns: ComputedRef<string | undefined> = computed(() => {
  if (p.columns === 0) {
    return
  }

  return p.widths
    ? p.widths.map(w => `${w}fr`).join(' ')
    : `repeat(${p.columns}, minmax(0, 1fr))`
})
</script>

<template>
  <div
    :class="[
      'w-full sm:grid sm:gap-4',
      {
        'grid-flow-col grid-cols-fit': !columns,
        'py-4 px-1': !singleBlockEmbed,
      },
    ]"
    :style="{ gridTemplateColumns, alignItems }"
  >
    <component
      :is="child.component"
      v-for="child in children"
      v-bind="child.componentProps"
      :key="child.refId"
    />
  </div>
</template>
