<script setup lang="ts">
import hljs from 'highlight.js'
import { Marked } from 'marked'
import { markedHighlight } from 'marked-highlight'
import { computed } from 'vue'

import BlockWrapper from '@/components/layout/BlockWrapper.vue'
import type { BlockFigureProps } from '@/data-model/blocks'

const marked = new Marked(
  markedHighlight({
    highlight(code, lang) {
      const language = hljs.getLanguage(lang) ? lang : 'plaintext'
      return hljs.highlight(code, { language }).value
    },
  }),
)

const p = defineProps<{
  content: string
  isLightProse: boolean
  figure: BlockFigureProps
  singleBlockEmbed?: boolean
}>()
const md = computed(() => marked.parse(p.content))
</script>

<template>
  <block-wrapper :figure="p.figure" :single-block-embed="singleBlockEmbed">
    <div
      :class="['w-full overflow-y-hidden', { dark: p.isLightProse }]"
      data-cy="block-markdown"
    >
      <div
        class="w-full prose font-ar-prose dark:prose-invert text-container"
        v-html="md"
      ></div>
    </div>
  </block-wrapper>
</template>

<style scoped>
.text-container :deep(pre) {
  background: #f6f6f6 !important;
}

.dark :deep(code) {
  /* hack - TW prose disabling doesn't seem to work in invert mode, so this ensures
     non-highlighted code isn't affected by the prose-invert class */
  color: black;
}
</style>
