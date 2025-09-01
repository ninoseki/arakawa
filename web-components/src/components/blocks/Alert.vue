<script setup lang="ts">
import { computed } from 'vue'

import Markdown from '@/components/blocks/Markdown.vue'
import BlockWrapper from '@/components/layout/BlockWrapper.vue'
import type { BlockFigureProps } from '@/data-model/blocks'

const p = defineProps<{
  content: string
  isLightProse: boolean
  figure: BlockFigureProps
  singleBlockEmbed?: boolean
  border: boolean
  mode?: string
}>()

const modeClass = computed(() => {
  switch (p.mode?.toLowerCase()) {
    case 'info':
      return 'text-blue-800 bg-blue-50 dark:bg-gray-800 dark:text-blue-400'
    case 'warning':
      return 'text-yellow-800 bg-yellow-50 dark:bg-gray-800 dark:text-yellow-30'
    case 'danger':
      return 'text-red-800 bg-red-50 dark:bg-gray-800 dark:text-red-400'
    case 'success':
      return 'text-green-800 bg-green-50 dark:bg-gray-800 dark:text-green-400'
    case 'dark':
      return 'text-gray-800 bg-gray-50 dark:bg-gray-800 dark:text-gray-300'
    default:
      return ''
  }
})
</script>

<template>
  <block-wrapper :figure="figure" :single-block-embed="singleBlockEmbed">
    <div
      :class="['w-full overflow-y-hidden', { dark: isLightProse }]"
      data-cy="block-markdown"
    >
      <markdown
        class="w-full prose font-ar-prose dark:prose-invert text-container rounded-lg p-4 mb-4"
        :class="[{ border: border }, modeClass]"
        :content="content"
      ></markdown>
    </div>
  </block-wrapper>
</template>
