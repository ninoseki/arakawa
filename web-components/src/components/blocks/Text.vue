<script setup lang="ts">
import Markdown from '@/components/blocks/Markdown.vue'
import BlockWrapper from '@/components/layout/BlockWrapper.vue'
import type { BlockFigureProps } from '@/data-model/blocks'

defineProps<{
  content: string
  isLightProse: boolean
  figure: BlockFigureProps
  singleBlockEmbed?: boolean
}>()
</script>

<template>
  <block-wrapper :figure="figure" :single-block-embed="singleBlockEmbed">
    <div
      :class="['w-full overflow-y-hidden', { dark: isLightProse }]"
      data-cy="block-markdown"
    >
      <markdown
        class="w-full prose font-ar-prose dark:prose-invert text-container"
        :content="content"
      />
    </div>
  </block-wrapper>
</template>
