<script setup lang="ts">
defineProps<{
  content?: string
}>()
</script>

<template>
  <div
    v-if="content"
    class="my-8 flex items-center gap-4 before:h-px before:flex-1 before:bg-gray-300 before:content-[''] after:h-px after:flex-1 after:bg-gray-300 after:content-['']"
  >
    {{ content }}
  </div>
  <div class="my-8 h-px border-0 bg-gray-300" v-else></div>
</template>
