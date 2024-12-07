<script setup lang="ts">
defineProps<{
  src: string
  responsive: boolean
  singleBlockEmbed?: boolean
}>()
</script>

<template>
  <img
    :src="src"
    data-cy="block-svg"
    loading="lazy"
    :class="[
      'mx-auto',
      {
        'w-full': responsive,
        'h-full': responsive && singleBlockEmbed,
        'max-w-none': !responsive, // Don't scale non-responsive SVGs like a normal image -- overwriting default browser `max-width: 100%`
        'absolute top-0 left-0': !responsive && singleBlockEmbed, // Prevent large embedded SVGs from being wrongly positioned in the iframe
      },
    ]"
  />
</template>
