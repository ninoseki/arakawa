<script setup lang="ts">
/**
 * Centres block and adds caption below if necessary
 */
import { type BlockFigureProps } from '@/data-model/blocks'

defineProps<{
  figure?: BlockFigureProps
  singleBlockEmbed?: boolean
  showOverflow?: boolean
}>()
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
    <div v-if="figure?.caption" class="text-sm text-ar-light-gray italic text-justify">
      <b>{{ figure.captionType }} {{ figure.count }}</b>
      {{ figure.caption }}
    </div>
  </div>
</template>
