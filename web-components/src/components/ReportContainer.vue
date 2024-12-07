<script setup lang="ts">
import { storeToRefs } from 'pinia'
import { onMounted, ref } from 'vue'

import { isView } from '@/data-model/blocks'
import { useRootStore } from '@/data-model/root-store'
import type { AppData, ReportProps } from '@/data-model/types'
import { parseError } from '@/shared/shared'
import { setTheme } from '@/theme'

import ErrorCallout from './ErrorCallout.vue'
import ReportComponent from './ReportComponent.vue'

const p = defineProps<{
  isLightProse: ReportProps['isLightProse']
  reportWidthClass: ReportProps['reportWidthClass']
  mode: ReportProps['mode']
  id: ReportProps['id']
  htmlHeader: ReportProps['htmlHeader']
  appData: AppData
}>()

const rootStore = useRootStore()
const error = ref<string | undefined>()

const setApp = async () => {
  try {
    await rootStore.setReport(
      { isLightProse: p.isLightProse, mode: p.mode },
      p.appData,
    )
  } catch (e) {
    error.value = parseError(e)
    console.error(e)
  }
}

setApp()

const storeProps = storeToRefs(rootStore)
const { report } = storeProps

onMounted(() => {
  setTheme(p.isLightProse)
})
</script>

<template>
  <div id="html-header" v-html="htmlHeader"></div>
  <report-component
    v-if="isView(report) && !error"
    :report-width-class="reportWidthClass"
    :mode="mode"
    :report="report"
    :key="report.refId"
  />
  <error-callout v-if="error" :error="error" />
</template>
