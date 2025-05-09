<script setup lang="ts">
import { ChevronDownIcon } from '@heroicons/vue/20/solid'
import { AdjustmentsHorizontalIcon } from '@heroicons/vue/24/outline'
import { computed, onMounted, onUnmounted, ref } from 'vue'

import type { ReportProps } from '@/data-model/types'

const p = defineProps<{
  labels: string[]
  pageNumber: number
  reportWidthClass: ReportProps['reportWidthClass']
}>()
const emit = defineEmits(['page-change'])

const showDropdown = ref(false)
const showPagesDropdown = ref(false)
const dropdownBtnEl = ref<HTMLElement>()

const hideDropdownOnClickAway = (e: MouseEvent) => {
  if (
    e.target instanceof Node &&
    dropdownBtnEl.value &&
    !dropdownBtnEl.value.contains(e.target)
  ) {
    showDropdown.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', hideDropdownOnClickAway)
})

onUnmounted(() => {
  document.removeEventListener('click', hideDropdownOnClickAway)
})

const showWidgets = !window.arLocal

const alwaysShowPagesDropdown = computed(() => p.labels.length > 6)

const dropdownMenuLinks = [
  { label: 'Documentation', href: 'https://ninoseki.github.io/arakawa/' },
]
</script>

<template>
  <nav
    :class="[
      // z-40 to be below modals and side bars on datapane.com
      'bg-white relative z-40',
      { 'border-b border-gray-100 sticky top-0': labels.length > 0 },
    ]"
  >
    <div class="mx-auto px-4" :class="reportWidthClass">
      <div class="flex h-16 justify-between">
        <div class="flex">
          <div
            class="hidden sm:ml-6 sm:flex sm:space-x-8"
            v-if="!alwaysShowPagesDropdown"
          >
            <a
              v-for="(label, idx) in labels"
              :key="idx"
              :data-cy="`page-${idx}`"
              :class="[
                'inline-flex items-center border-b-2 px-1 pt-1 text-sm font-medium cursor-pointer',
                {
                  'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700':
                    idx !== pageNumber,
                  'border-ar-accent text-gray-900': idx === pageNumber,
                },
              ]"
              @click="emit('page-change', idx)"
            >
              {{ label }}
            </a>
          </div>
          <!-- If there are > a certain number of pages, we don't hide the dropdown on larger screens -->
          <div
            v-if="labels.length > 0"
            class="ml-6 flex"
            :class="{ 'sm:hidden': !alwaysShowPagesDropdown }"
          >
            <a
              class="group cursor-pointer inline-flex items-center rounded-md bg-white text-base font-medium hover:text-gray-900 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 text-gray-500"
              @click="showPagesDropdown = !showPagesDropdown"
            >
              {{ labels.length }} pages
              <chevron-down-icon
                :class="[
                  'ml-2 h-5 w-5 group-hover:text-gray-500 text-gray-400',
                  {
                    'text-gray-600': showPagesDropdown,
                    'text-gray-400': !showPagesDropdown,
                  },
                ]"
              />
            </a>
          </div>
        </div>
        <div class="ml-6 flex items-center" v-if="showWidgets">
          <div class="relative">
            <button
              type="button"
              class="rounded-full bg-white p-1 text-gray-400 hover:text-gray-500 focus:outline-none"
              ref="dropdownBtnEl"
              @click="showDropdown = !showDropdown"
            >
              <adjustments-horizontal-icon
                class="h-7 w-7 hover:transform hover:rotate-180"
              />
            </button>
            <div
              v-if="showDropdown"
              class="absolute right-0 z-10 mt-2 w-56 origin-top-right divide-y divide-gray-100 rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none"
              role="menu"
              aria-orientation="vertical"
              aria-labelledby="user-menu-button"
              tabindex="-1"
            >
              <div class="py-1" role="none">
                <a
                  v-for="(item, idx) in dropdownMenuLinks"
                  tabindex="-1"
                  :key="idx"
                  :href="item.href"
                  target="_blank"
                  class="block px-4 py-2 text-sm text-gray-700 cursor-pointer hover:bg-gray-100 hover:text-gray-900"
                >
                  {{ item.label }}
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
      <!-- Always hide on larger viewports, unless we have > N pages -->
      <div
        v-if="showPagesDropdown"
        :class="{ 'sm:hidden': !alwaysShowPagesDropdown }"
      >
        <div class="space-y-1 pt-2 pb-3">
          <a
            v-for="(label, idx) in labels"
            :key="idx"
            :data-cy="`page-${idx}`"
            :class="[
              'cursor-pointer block border-l-4 py-2 pl-3 pr-4 text-base font-medium',
              {
                'border-transparent text-gray-500 hover:border-gray-300 hover:bg-gray-50 hover:text-gray-700':
                  idx !== pageNumber,
                'border-indigo-500 bg-indigo-50 text-indigo-700':
                  idx === pageNumber,
              },
            ]"
            @click="emit('page-change', idx)"
          >
            {{ label }}
          </a>
        </div>
      </div>
    </div>
  </nav>
</template>
