<script setup lang="ts">
import { storeToRefs } from 'pinia'
import { type Ref, ref } from 'vue'

import type { Block } from '@/data-model/blocks'

const p = defineProps<{ label?: string; store: any }>()
const isOpen = ref(false)
const { children }: { children: Ref<Block[]> } = storeToRefs(p.store)
</script>

<template>
  <div class="w-full bg-gray-100 p-2 rounded-md" data-cy="section-toggle">
    <div
      class="cursor-pointer px-2 w-full font-semibold flex items-center justify-start"
      @click="isOpen = !isOpen"
    >
      <div class="flex-1">
        {{ label || 'Toggle Section' }}
      </div>
      <div class="flex-initial ml-auto">
        <i
          :class="[
            'opacity-50 fa',
            { 'fa-chevron-up': isOpen, 'fa-chevron-down': !isOpen },
          ]"
        ></i>
      </div>
    </div>
    <div :class="['w-full pt-2 m-auto overflow-hidden', { hidden: !isOpen }]">
      <component
        :is="child.component"
        v-for="child in children"
        v-bind="child.componentProps"
        :key="child.refId"
      />
    </div>
  </div>
</template>
