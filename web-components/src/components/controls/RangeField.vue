<script setup lang="ts">
import { ref } from 'vue'

const p = defineProps<{
  name: string
  min: number
  max: number
  step: number
  initial?: number
  required?: boolean
  label?: string
}>()

// Hold value in state so that it can be shown in input prefix
const inputValue = ref(p.initial)
</script>

<template>
  <form-kit
    type="range"
    :label="label || name"
    :name="name"
    v-model="inputValue"
    :min="min"
    :max="max"
    :step="step"
    data-cy="range-field"
    outer-class="flex-1"
  >
    <template #prefix>
      <div class="pr-2">{{ inputValue }}</div>
    </template>
  </form-kit>
</template>
