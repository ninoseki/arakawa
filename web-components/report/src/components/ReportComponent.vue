<script setup lang="ts">
import { Block, View } from "../data-model/blocks";
import { useRootStore } from "../data-model/root-store";
import { ReportProps } from "../data-model/types";
import NavBar from "./layout/NavBar.vue";
import { storeToRefs } from "pinia";
import { computed, ComputedRef } from "vue";

// Vue can't use a ts interface as props
// see https://github.com/vuejs/core/issues/4294
const p = defineProps<{
  isOrg: ReportProps["isOrg"];
  reportWidthClass: ReportProps["reportWidthClass"];
  mode: ReportProps["mode"];
  htmlHeader?: ReportProps["htmlHeader"];
  resetApp: () => void;
  report: View;
}>();

const rootStore = useRootStore();
const { singleBlockEmbed } = storeToRefs(rootStore);

/* Set up deserialised report object */

const { children, tabNumber, hasPages } = storeToRefs(p.report.store);

const pages: ComputedRef<Block[]> = computed(() =>
  hasPages.value ? children.value[0].children : [],
);

const pageLabels: ComputedRef<string[]> = computed(() =>
  pages.value.map((pa: Block, i: number) => pa.label || `Page ${i + 1}`),
);

const currentPage: ComputedRef<Block[]> = computed(() =>
  hasPages.value ? [pages.value[tabNumber.value]] : children.value,
);

const handlePageChange = (newPageNumber: number) =>
  p.report!.store.setTab(newPageNumber);

const { isIPythonEmbed } = window;
</script>

<template>
  <template v-if="p.report">
    <nav-bar
      v-if="hasPages || !(isIPythonEmbed || singleBlockEmbed)"
      :reset-app="p.resetApp"
      :labels="pageLabels"
      :page-number="tabNumber"
      :report-width-class="p.reportWidthClass"
      @page-change="handlePageChange"
    />
    <main
      :class="['w-full bg-ar-background mx-auto pb-4', p.reportWidthClass]"
      data-cy="report-component"
    >
      <div class="flex flex-col justify-end bg-ar-background">
        <div class="sm:flex block">
          <div class="flex-1 flex flex-col min-w-0">
            <div class="grow px-4">
              <component
                :is="child.component"
                v-for="child in currentPage"
                :key="child.refId"
                v-bind="child.componentProps"
                class="py-4"
              />
            </div>
          </div>
        </div>
      </div>
    </main>
  </template>
</template>
