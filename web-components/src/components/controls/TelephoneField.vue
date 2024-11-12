<script setup lang="ts">
import { computed } from 'vue'

const p = defineProps<{
  name: string
  label?: string
  initial?: string
  required?: boolean
}>()

const validation = computed(() => (p.required ? 'required' : ''))
</script>

<template>
  <form-kit
    type="tel"
    :label="label || name"
    :name="name"
    :value="initial"
    :validation="validation"
    validation-visibility="live"
    data-cy="text-field"
    outer-class="flex-1"
  />
</template>
