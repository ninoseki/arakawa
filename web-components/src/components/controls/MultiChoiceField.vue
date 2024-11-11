<script setup lang="ts">
import { computed, type ComputedRef } from 'vue'

const p = defineProps<{
  initial: string[]
  options: string[]
  label?: string
  required?: boolean
  name: string
}>()

const validation: ComputedRef = computed(() =>
  p.required ? [['+required']] : [],
)

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
      :validation="validation"
      validation-visibility="live"
      :tags="p.initial"
      :options="options"
    />
  </div>
</template>
