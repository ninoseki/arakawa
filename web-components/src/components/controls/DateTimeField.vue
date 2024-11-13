<script setup lang="ts">
import { computed } from 'vue'

const p = defineProps<{
  name: string
  type: string
  initial?: string
  label?: string
  help?: string
  validation?: string
  required?: boolean
}>()

const validation = computed(() => {
  const values = [p.required ? 'required' : undefined, p.validation].filter(
    (i): i is Exclude<typeof i, undefined> => i !== undefined,
  )
  return values.join('|')
})
</script>

<template>
  <form-kit
    :type="type"
    :data-cy="`${p.type}-field`"
    :value="initial"
    :name="name"
    :label="label || name"
    :validation="validation"
    :help="help"
    validation-visibility="live"
    step="1"
  />
</template>
