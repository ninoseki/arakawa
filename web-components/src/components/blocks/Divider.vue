<script setup lang="ts">
import BlockWrapper from '@/components/layout/BlockWrapper.vue'
import type { BlockFigureProps } from '@/data-model/blocks'

defineProps<{
  content?: string
  figure: BlockFigureProps
}>()
</script>

<template>
  <block-wrapper :figure="figure">
    <div
      v-if="content"
      class="w-full my-8 flex items-center gap-4 before:h-px before:flex-1 before:bg-gray-300 before:content-[''] after:h-px after:flex-1 after:bg-gray-300 after:content-['']"
    >
      {{ content }}
    </div>
    <hr class="w-full my-8 h-px border-0 bg-gray-300" v-else />
  </block-wrapper>
</template>
