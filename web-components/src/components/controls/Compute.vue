<script setup lang="ts">
import { v4 as uuid4 } from 'uuid'

import { ControlsField } from '../../data-model/blocks'
import ErrorCallout from '../ErrorCallout.vue'

const p = defineProps<{
  onChange: (v: { name: string; value: any }) => void
  update: () => void
  children: ControlsField[]
  prompt: string
  label: string
  method: string
  subtitle?: string
  action?: string
  error?: string
}>()

const formId = uuid4()
</script>

<template>
  <div class="w-full">
    <div class="border shadow-sm bg-gray-50 rounded-md w-full">
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
            @change="onChange"
          />
        </div>
        <div
          class="bg-gray-50 px-4 py-3 sm:px-6 flex items-center justify-start"
        >
          <form-kit
            type="submit"
            :class="[
              'ml-auto inline-flex justify-center rounded-md border border-transparent bg-indigo-600 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 disabled:opacity-50',
            ]"
          >
            {{ p.prompt }}
          </form-kit>
        </div>
        <error-callout v-if="error" :error="error" />
      </form-kit>
    </div>
  </div>
</template>
