<script setup lang="ts">
import { CloudArrowUpIcon } from '@heroicons/vue/24/outline'
import { computed, ref } from 'vue'

const p = defineProps<{
  name: string
  label?: string
  help?: string
  validation?: string
  required?: boolean
  accept?: string
}>()

const validation = computed(() => {
  const values = [p.required ? 'required' : undefined, p.validation].filter(
    (i): i is Exclude<typeof i, undefined> => i !== undefined,
  )
  return values.join('|')
})

const hasFile = ref(false)

const id = `file_${p.name}`
</script>

<template>
  <form-kit
    type="file"
    :id="id"
    :label="label || name"
    name="parameter_files"
    :validation="validation"
    :help="help"
    :accept="accept"
    file-item-icon="fileDoc"
    file-remove-icon="trash"
    no-files-icon="fileDoc"
    validation-visibility="live"
    form="params-form"
  >
    <template #noFiles>
      <label
        class="flex w-full h-full items-center space-x-4 text-gray-500 hover:text-gray-700 formkit-no-files px-4 pt-3 pb-4 cursor-pointer"
        v-if="!hasFile"
        :for="id"
      >
        <cloud-arrow-up-icon class="w-6 h-6" />
        <div class="flex flex-col" data-cy="file-field">
          <span class="font-semibold text-sm">Upload a file</span
          ><span class="text-xs">Up to 25mb supported.</span>
        </div>
      </label>
    </template>
  </form-kit>
</template>
