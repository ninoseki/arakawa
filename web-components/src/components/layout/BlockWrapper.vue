<script setup lang="ts">
/**
 * Centres block and adds caption below if necessary
 */
import { toRefs } from 'vue'

import { type BlockFigureProps } from '@/data-model/blocks'

const p = defineProps<{
  figure: BlockFigureProps
  singleBlockEmbed?: boolean
  showOverflow?: boolean
}>()

const { caption, count, captionType } = toRefs(p.figure)
</script>

<template>
  <div
    :class="[
      'w-full relative flex flex-col justify-start items-center',
      { 'h-iframe': singleBlockEmbed },
      // TODO - why does overflow-x-auto create auto-y overflow in `Compute` block?
      { 'overflow-x-auto': !showOverflow },
      { 'overflow-visible': showOverflow },
    ]"
  >
    <slot></slot>
    <div v-if="caption" class="text-sm text-ar-light-gray italic text-justify">
      <b>{{ captionType }} {{ count }}</b>
      {{ caption }}
    </div>
  </div>
</template>
