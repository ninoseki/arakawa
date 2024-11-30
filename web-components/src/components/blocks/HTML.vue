<script setup lang="ts">
import childIframeResizerJs from '@iframe-resizer/child/index.umd.js?raw'
import IframeResizer from '@iframe-resizer/vue/sfc'
import { computed, type ComputedRef } from 'vue'

import type { BlockFigureProps } from '@/data-model/blocks'

import userIframeCss from '../../styles/user-iframe.css?inline'
import BlockWrapper from '../layout/BlockWrapper.vue'

const p = defineProps<{
  html: string
  sandbox?: string
  figure: BlockFigureProps
  singleBlockEmbed?: boolean
}>()

const iframeDoc: ComputedRef<string> = computed(() => {
  /**
   * Inject some base CSS into the iframe, alongside the JS needed to
   * make the iframe resizer work
   */
  return `
        <!DOCTYPE html>
        <html>
        <body>
          <style>${userIframeCss}</style>
          <script>${childIframeResizerJs}<\/script>
          <div class="doc-root">${p.html}</div>
        </body>
        </html>
    `
})
</script>

<template>
  <block-wrapper :figure="p.figure" :single-block-embed="singleBlockEmbed">
    <iframe-resizer
      license="GPLv3"
      :srcdoc="iframeDoc"
      :sandbox="p.sandbox || ''"
      width="100%"
      data-cy="block-user-iframe"
    ></iframe-resizer>
  </block-wrapper>
</template>

<style scoped>
iframe {
  width: 100%;
  height: 100vh;
}
</style>
