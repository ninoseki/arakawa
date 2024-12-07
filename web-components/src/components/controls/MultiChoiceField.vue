<script setup lang="ts">
import { computed } from 'vue'

const p = defineProps<{
  initial: string[]
  options: string[]
  label?: string
  required?: boolean
  validation?: string
  help?: string
  name: string
}>()

const validation = computed(() => {
  const values = [p.required ? 'required' : undefined, p.validation].filter(
    (i): i is Exclude<typeof i, undefined> => i !== undefined,
  )
  return values.join('|')
})

const multiSelectProps = {
  closeOnSelect: false,
  clearOnSelect: false,
  preserveSearch: true,
  placeholder: '',
  preselectFirst: false,
  searchable: false,
}
</script>

<template>
  <div class="mb-6" data-cy="multi-select-field">
    <form-kit
      type="multiSelectField"
      :label="label || name"
      :multiSelectProps="multiSelectProps"
      :name="name"
      :help="help"
      :validation="validation"
      validation-visibility="live"
      :tags="initial"
      :options="options"
    />
  </div>
</template>
