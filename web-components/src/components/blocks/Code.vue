<script setup lang="ts">
import 'highlight.js/lib/common'

import hljsVuePlugin from '@highlightjs/vue-plugin'
import { computed, onMounted, onUnmounted, ref } from 'vue'

import { ARClipboard } from '@/shared/ARClipboard'

const highlightjs = hljsVuePlugin.component

const p = defineProps<{ language: string; code: string }>()

const clip = ref<ARClipboard>()
const copyBtn = ref<HTMLButtonElement | null>(null)
const code = computed(() => p.code.trim())

onMounted(() => {
  if (copyBtn.value) {
    clip.value = new ARClipboard(copyBtn.value, {
      text: code.value,
    })
  }
})

onUnmounted(() => {
  clip.value?.destroy()
})
</script>

<template>
  <div class="relative">
    <button
      class="absolute top-2 right-2 text-gray-700 h-5 w-5 opacity-75"
      ref="copyBtn"
    >
      <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
        <title>Copy</title>
        <path d="M8 3a1 1 0 011-1h2a1 1 0 110 2H9a1 1 0 01-1-1z"></path>
        <path
          d="M6 3a2 2 0 00-2 2v11a2 2 0 002 2h8a2 2 0 002-2V5a2 2 0 00-2-2 3 3 0 01-3 3H9a3 3 0 01-3-3z"
        ></path>
      </svg>
    </button>
    <highlightjs :language="language" :code="code" data-cy="block-code" />
  </div>
</template>

<style scoped>
pre {
  @apply w-full;
}
</style>
