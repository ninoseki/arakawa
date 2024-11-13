<script setup lang="ts">
import { computed } from 'vue'

const p = defineProps<{
  name: string
  label?: string
  initial?: string
  required?: boolean
  type: string
  validation?: string
  help?: string
}>()

const typeToValidation = new Map<string, string>([
  ['url', 'url'],
  ['email', 'email'],
  ['search', 'search'],
  ['textarea', 'textarea'],
])

const validation = computed(() => {
  const values = [
    p.required ? 'required' : undefined,
    typeToValidation.get(p.type),
    p.validation,
  ].filter((i): i is Exclude<typeof i, undefined> => i !== undefined)
  return values.join('|')
})
</script>

<template>
  <form-kit
    :type="type"
    :label="label || name"
    :name="name"
    :value="initial"
    :validation="validation"
    :help="help"
    validation-visibility="live"
    outer-class="flex-1"
  />
</template>
