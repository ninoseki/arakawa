<script setup lang="ts">
defineProps<{ iframeContent: string; singleBlockEmbed?: boolean }>()
const IFRAME_HEIGHT = '35rem'
</script>

<template>
  <div
    :style="{ height: IFRAME_HEIGHT }"
    :class="['flex justify-center w-full', { 'h-iframe': singleBlockEmbed }]"
    data-cy="block-iframe"
  >
    <iframe
      :style="{ border: 'none !important' }"
      :class="['w-full', { 'h-iframe': singleBlockEmbed }]"
      :srcdoc="iframeContent"
      sandbox="allow-scripts"
    ></iframe>
  </div>
</template>
