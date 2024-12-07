<script setup lang="ts">
import BlockWrapper from '@/components/layout/BlockWrapper.vue'
import type { BlockFigureProps } from '@/data-model/blocks'

defineProps<{
  heading: string
  value: string
  figure: BlockFigureProps
}>()
</script>

<template>
  <block-wrapper :figure="figure">
    <div
      data-cy="block-bignumber"
      class="bg-white overflow-hidden border border-gray-300 rounded-lg w-full"
    >
      <div class="px-4 py-5 sm:p-6">
        <dl>
          <dt class="text-base leading-6 font-normal text-gray-900 truncate">
            {{ heading }}
          </dt>
          <dd class="mt-1 text-4xl leading-9 font-semibold text-gray-900">
            {{ value }}
          </dd>
        </dl>
      </div>
    </div>
  </block-wrapper>
</template>
