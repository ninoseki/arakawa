<script setup lang="ts">
import { computed } from 'vue'

const p = defineProps<{
  initial: string[]
  label?: string
  required?: boolean
  name: string
  validation?: string
  help?: string
}>()

const validation = computed(() => {
  const values = [p.required ? 'required' : undefined, p.validation].filter(
    (i): i is Exclude<typeof i, undefined> => i !== undefined,
  )
  return values.join('|')
})

const multiSelectProps = {
  taggable: true,
  placeholder: 'Search or add a tag',
}
</script>

<template>
  <div class="mb-6" data-cy="tags-field">
    <form-kit
      type="multiSelectField"
      :label="label || name"
      :name="name"
      :validation="validation"
      :help="help"
      :multiSelectProps="multiSelectProps"
      validation-visibility="live"
      :tags="initial"
      :options="initial"
    />
  </div>
</template>
