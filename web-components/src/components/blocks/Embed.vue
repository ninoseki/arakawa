<script setup lang="ts">
import childIframeResizerJs from '@iframe-resizer/child/index.umd.js?raw'
import IframeResizer from '@iframe-resizer/vue/sfc'
import { computed, type ComputedRef } from 'vue'

import BlockWrapper from '@/components/layout/BlockWrapper.vue'
import type { BlockFigureProps } from '@/data-model/blocks'

const p = defineProps<{
  html: string
  isIframe: boolean
  figure: BlockFigureProps
  singleBlockEmbed?: boolean
}>()

// Unescape script tags when embedding
const decodedHtml: ComputedRef<string> = computed(() => {
  return p.html
    .replace('&lt;script&gt;', '<script>')
    .replace('&lt;&sol;script&gt;', '<\/script>')
})

const iframeDoc: ComputedRef<string> = computed(() => {
  /**
   * Inject the JS needed to make the iframe resizer work
   */
  return `
        <!DOCTYPE html>
        <html>
        <body>
          <script>${childIframeResizerJs}<\/script>
          ${decodedHtml.value}
        </body>
        </html>
    `
})
</script>

<template>
  <block-wrapper :figure="p.figure" :single-block-embed="singleBlockEmbed">
    <div
      v-if="isIframe"
      v-html="decodedHtml"
      class="flex justify-center items-center"
      data-cy="block-embed"
    ></div>
    <iframe-resizer
      v-else
      license="GPLv3"
      :srcdoc="iframeDoc"
      class="flex justify-center items-center"
    ></iframe-resizer>
  </block-wrapper>
</template>

<style scoped>
iframe {
  width: 100%;
  height: 100vh;
}
</style>
