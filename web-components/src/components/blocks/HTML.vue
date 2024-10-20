<script setup lang="ts">
import iframeResize from 'iframe-resizer/js/iframeResizer'
import contentWindowJs from 'iframe-resizer/js/iframeResizer.contentWindow.js?raw'
import { v4 as uuid4 } from 'uuid'
import { computed, type ComputedRef, onMounted } from 'vue'

import type { BlockFigureProps } from '@/data-model/blocks'

import userIframeCss from '../../styles/user-iframe.css?inline'
import BlockWrapper from '../layout/BlockWrapper.vue'

const p = defineProps<{
  html: string
  sandbox?: string
  figure: BlockFigureProps
  singleBlockEmbed?: boolean
}>()

const iframeId = `iframe_${uuid4()}`

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
            <script>${contentWindowJs}<\/script>
            <div class="doc-root">${p.html}</div>
        </body>
        </html>
    `
})

onMounted(() => {
  iframeResize({ checkOrigin: false, warningTimeout: 10000 }, `#${iframeId}`)
})
</script>

<template>
  <block-wrapper :figure="p.figure" :single-block-embed="singleBlockEmbed">
    <iframe
      :srcdoc="iframeDoc"
      :sandbox="p.sandbox || ''"
      :id="iframeId"
      width="100%"
      data-cy="block-user-iframe"
    ></iframe>
  </block-wrapper>
</template>
