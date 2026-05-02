<script setup lang="ts">
import katex from 'katex'
import { computed } from 'vue'

const p = defineProps<{ content: string }>()

const katexCssHref = new URL('./katex.css', import.meta.url).href

const rendered = computed(() => {
  try {
    return katex.renderToString(p.content)
  } catch (e) {
    console.error(`Error rendering formula: ${e}`)
    return ''
  }
})
</script>

<template>
  <Teleport to="head">
    <link rel="stylesheet" :href="katexCssHref" />
  </Teleport>
  <div
    data-cy="block-formula"
    class="w-full overflow-y-hidden bg-white flex justify-center"
    v-html="rendered"
  ></div>
</template>
