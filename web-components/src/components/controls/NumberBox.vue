<script setup lang="ts">
import { computed, type ComputedRef } from 'vue'

const p = defineProps<{
  name: string
  label?: string
  initial?: number
  required?: boolean
}>()

const validation: ComputedRef = computed(() =>
  p.required ? [['+required']] : [],
)
</script>

<template>
  <form-kit
    type="number"
    :label="label || name"
    :name="name"
    :value="initial"
    :validation="validation"
    step="any"
    validation-visibility="live"
    outer-class="flex-1"
    data-cy="number-field"
  />
</template>
