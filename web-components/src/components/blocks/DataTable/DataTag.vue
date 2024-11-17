<script setup lang="ts">
import { formatNumber } from './shared'

defineProps<{
  value: string | number
  unit: string
  icon?: string
}>()
</script>

<template>
  <div
    class="px-2.5 py-0.5 mr-0 flex items-center inline-flex items-center md:rounded text-xs font-medium leading-4 bg-gray-200 text-gray-700"
  >
    <div>
      <i :class="`pr-2 fa ${icon}`"></i>
    </div>
    <div>
      <span>{{ formatNumber(+value) }}</span>
      <span className="hidden lg:inline">{{ ' ' }}{{ unit }}</span>
    </div>
  </div>
</template>
