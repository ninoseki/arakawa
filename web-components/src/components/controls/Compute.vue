<script setup lang="ts">
import { FormKitMessages } from '@formkit/vue'
import { v4 as uuid4 } from 'uuid'

import { ControlsField } from '@/data-model/blocks'

const p = defineProps<{
  children: ControlsField[]
  prompt: string
  label: string
  method: string
  subtitle?: string
  action?: string
}>()

const formId = uuid4()

const isControlField = (child: any) => {
  return child instanceof ControlsField
}
</script>

<template>
  <div class="border shadow-sm rounded-md w-full">
    <form-kit
      type="form"
      :id="formId"
      :action="action"
      :method="method"
      :actions="false"
    >
      <div class="px-4 py-5 sm:p-6">
        <div class="mb-6">
          <div v-if="label">
            <h3 class="text-lg font-medium leading-6 text-gray-900">
              {{ label }}
            </h3>
          </div>
          <div v-if="subtitle">
            <p class="mt-1 max-w-2xl text-sm text-gray-500">
              {{ subtitle }}
            </p>
          </div>
        </div>
        <component
          :is="child.component"
          v-for="child in children"
          v-bind="child.componentProps"
          :key="child.refId"
          :class="{ 'py-4': !isControlField(child) }"
        />
      </div>
      <div class="px-4 py-3 sm:px-6 items-center justify-start">
        <form-kit
          type="submit"
          :class="[
            'ml-auto inline-flex justify-center rounded-md border border-transparent bg-indigo-600 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 disabled:opacity-50',
          ]"
        >
          {{ p.prompt }}
        </form-kit>
        <div>
          <form-kit-messages />
        </div>
      </div>
    </form-kit>
  </div>
</template>
