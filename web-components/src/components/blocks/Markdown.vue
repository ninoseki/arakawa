<script setup lang="ts">
import hljs from 'highlight.js'
import { Marked } from 'marked'
import { markedHighlight } from 'marked-highlight'
import { computed } from 'vue'

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
}>()
const md = computed(() => marked.parse(p.content))
</script>

<template>
  <div v-html="md"></div>
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
