<script setup lang="ts">
import childIframeResizerJs from '@iframe-resizer/child/index.umd.js?raw'
import IframeResizer from '@iframe-resizer/vue/sfc'
import { computed, type ComputedRef, onMounted } from 'vue'

const p = defineProps<{ iframeContent: string; singleBlockEmbed?: boolean }>()

// Unescape script tags when embedding
const iframeDoc: ComputedRef<string> = computed(() => {
  return p.iframeContent.replace(
    '<body>',
    `<body><script>${childIframeResizerJs}<\/script>`,
  )
})

onMounted(() => {
  iframeResize({ checkOrigin: false, warningTimeout: 10000 }, `#${iframeId}`)
})
</script>

<template>
  <iframe-resizer
    :style="{ border: 'none !important' }"
    :class="['w-full', { 'h-iframe': singleBlockEmbed }]"
    :srcdoc="iframeDoc"
    sandbox="allow-scripts"
  ></iframe-resizer>
</template>
