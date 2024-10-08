<script setup lang="ts">
import { ControlsField } from "../../data-model/blocks";
import { TriggerType } from "../../data-model/types";
import ErrorCallout from "../ErrorCallout.vue";
import LoadingSpinner from "../LoadingSpinner.vue";
import { getNode } from "@formkit/core";
import { v4 as uuid4 } from "uuid";
import { onMounted, onUnmounted, ref } from "vue";

const p = defineProps<{
  onChange: (v: { name: string; value: any }) => void;
  update: () => void;
  children: ControlsField[];
  prompt: string;
  label: string;
  functionId: string;
  trigger: TriggerType;
  loading: boolean;
  timer?: number;
  subtitle?: string;
  error?: string;
  immediate?: boolean;
}>();

// Disable function runs for local reports
const functionRunDisabled = window.arLocal;

const scheduleInterval = ref<ReturnType<typeof setInterval> | null>(null);
const formId = uuid4();

// Don't show the block if it has no children and isn't triggered on submit
const isVisible = p.trigger === TriggerType.SUBMIT || p.children.length;

const updateIfValid = () => {
  const node = getNode(formId);
  if (node?.context?.state.valid || !isVisible) {
    p.update();
  }
};

const setAutomaticFunctionUpdates = () => {
  /**
   * Set schedule and on-mount updates
   */
  if (functionRunDisabled) {
    return;
  }

  if (p.trigger === TriggerType.SCHEDULE && p.timer) {
    scheduleInterval.value = setInterval(updateIfValid, p.timer * 1000);
  } else if (p.trigger === TriggerType.MOUNT) {
    p.update();
  }

  // Run schedule if `immediate=True`
  if (p.trigger === TriggerType.SCHEDULE && p.immediate) {
    p.update();
  }
};

onMounted(() => {
  setAutomaticFunctionUpdates();
});

onUnmounted(() => {
  if (scheduleInterval.value) {
    clearInterval(scheduleInterval.value);
  }
});
</script>

<template>
  <div class="w-full" v-if="isVisible">
    <div class="border shadow-sm bg-gray-50 rounded-md w-full max-w-3xl">
      <form-kit
        type="form"
        :actions="false"
        :id="formId"
        #default="{ state: { valid } }"
        @submit="update"
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
          v-if="p.trigger === TriggerType.SUBMIT"
        >
          <div
            class="flex items-center justify-start bg-gray-200 p-2 rounded-md shadow"
            v-if="p.loading || functionRunDisabled"
          >
            <template v-if="p.loading">
              <loading-spinner />
              <div class="pl-1">Running function...</div>
            </template>
            <template v-else-if="functionRunDisabled">
              <i class="fa fa-info-circle" />
              <div class="pl-1">
                Function running is disabled for static reports
              </div>
            </template>
          </div>
          <button
            type="submit"
            :disabled="p.loading || !valid || functionRunDisabled"
            :class="[
              'ml-auto inline-flex justify-center rounded-md border border-transparent bg-indigo-600 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 disabled:opacity-50',
            ]"
          >
            {{ p.prompt }}
          </button>
        </div>
        <error-callout v-if="error" :error="error" />
      </form-kit>
    </div>
  </div>
</template>
