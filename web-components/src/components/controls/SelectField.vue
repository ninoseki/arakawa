<script setup lang="ts">
import { computed } from 'vue'

const p = defineProps<{
  name: string
  options: string[]
  initial?: string
  label?: string
  required?: boolean
  validation?: string
  help?: string
}>()

const validation = computed(() => {
  const values = [p.required ? 'required' : undefined, p.validation].filter(
    (i): i is Exclude<typeof i, undefined> => i !== undefined,
  )
  return values.join('|')
})
</script>

<template>
  <span data-cy="select-field">
    <form-kit
      type="select"
      :label="label || name"
      :name="name"
      :options="options"
      :value="initial"
      :validation="validation"
      :help="help"
      data-cy="select-field"
    />
  </span>
</template>
