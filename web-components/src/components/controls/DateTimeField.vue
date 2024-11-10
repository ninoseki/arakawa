<script setup lang="ts">
import { computed, type ComputedRef } from 'vue'

const p = defineProps<{
  name: string
  type: string
  initial?: string
  label?: string
  required?: boolean
}>()

const validation: ComputedRef = computed(() =>
  p.required ? [['+required']] : [],
)
</script>

<template>
  <form-kit
    :type="type"
    :data-cy="`${p.type}-field`"
    :value="initial"
    :name="name"
    :label="label || name"
    :validation="validation"
    validation-visibility="live"
    step="1"
  />
</template>
