<script setup lang="ts">
defineProps<{
  name: string
  initial: string
  type: string
}>()
</script>

<template>
  <form-kit type="hidden" :name="name" :value="initial" />
</template>
