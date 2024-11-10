<script setup lang="ts">
import { computed, type ComputedRef } from 'vue'

const p = defineProps<{
  initial: string[]
  label?: string
  required?: boolean
  name: string
}>()

const validation: ComputedRef = computed(() =>
  p.required ? [['+required']] : [],
)

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
      :multiSelectProps="multiSelectProps"
      validation-visibility="live"
      :tags="p.initial"
      :options="p.initial"
    />
  </div>
</template>
