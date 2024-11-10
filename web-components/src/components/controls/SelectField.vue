<script setup lang="ts">
defineProps<{
  name: string
  options: string[]
  initial?: string
  label?: string
  required?: boolean
}>()
</script>

<template>
  <span data-cy="select-field">
    <form-kit
      type="select"
      :label="label || name"
      :name="name"
      :options="options"
      :value="initial"
      data-cy="select-field"
    />
  </span>
</template>
