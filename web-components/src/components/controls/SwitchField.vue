<script setup lang="ts">
defineProps<{
  initial: boolean
  name: string
  label?: string
  help?: string
}>()
</script>

<template>
  <!--
         TODO - formkit checkbox sets its validation to `required` regardless of validation settings,
         if it is the sole parent element of a component. Hacky solution for now is to wrap the component in `span`s.
     -->
  <span>
    <form-kit
      type="checkbox"
      :value="initial"
      :label="label || name"
      :name="name"
      :help="help"
      data-cy="switch-field"
    />
  </span>
</template>

<style>
:root {
  --fk-font-weight-option: bold !important;
}
</style>
