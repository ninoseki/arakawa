<script setup lang="ts">
import { ARClipboard } from "../../../../../shared/ARClipboard";
import { ExportType } from "../../../data-model/blocks";
import ArButton from "../../../shared/ARButton.vue";
import ArDropdown from "../../../shared/ARDropdown.vue";
import { Section } from "../../../shared/shared";
import DataTag from "./DataTag.vue";

const p = defineProps<{
  previewMode: boolean;
  queryOpen: boolean;
  rows: number;
  columns: number;
  cells: number;
  getCsvText: () => Promise<string>;
  downloadLocal: (type: ExportType) => Promise<void>;
  downloadRemote: (type: ExportType) => Promise<void>;
}>();

const emit = defineEmits(["toggle-query-open"]);

const withErrHandling = function (f: (...args: any) => any): any {
  return function (this: any, ...args: any[]) {
    return f.apply(this, args).catch((e: any) => {
      console.error(e);
    });
  };
};

const localActionSections: Section[] = [
  {
    title: "Current State",
    options: [
      {
        name: "Copy CSV to clipboard",
        onClick: async () => ARClipboard.copyOnce(await p.getCsvText()),
        id: "copy-clipboard",
      },
      {
        name: "Download CSV",
        onClick: withErrHandling(p.downloadLocal),
        id: "download-csv",
      },
    ],
  },
];

const remoteActionSections: Section[] = [
  {
    title: "Original Data",
    options: [
      {
        name: "Download CSV",
        onClick: withErrHandling(() => p.downloadRemote("CSV")),
        id: "download-original-csv",
      },
      {
        name: "Download Excel",
        onClick: withErrHandling(() => p.downloadRemote("EXCEL")),
        id: "download-original-excel",
      },
    ],
  },
];

const actionSections: Section[] = [
  ...localActionSections,
  ...(window.arLocal ? [] : remoteActionSections),
];
</script>

<template>
  <div class="bg-gray-100 py-2" data-cy="block-datatable">
    <div class="flex justify-between items-center flex-wrap">
      <div class="flex justify-end md:space-x-2 ml-2">
        <data-tag :value="p.rows" icon="fa-bars" unit="rows" />
        <data-tag :value="p.columns" icon="fa-columns" unit="columns" />
        <data-tag :value="p.cells" icon="fa-th-large" unit="cells" />
      </div>
      <div
        v-if="!p.previewMode"
        class="min-w-0 flex items-center pr-2 sm:divide-x flex-wrap"
      >
        <div class="pr-2 sm:flex hidden space-x-2">
          <ar-button
            @click="emit('toggle-query-open')"
            :icon="`fa ${p.queryOpen ? 'fa-caret-up' : 'fa-caret-down'}`"
            :disabled="p.previewMode"
            data-cy="btn-open-query"
            class="ar-btn-info"
          >
            Run SQL Query
          </ar-button>
        </div>
        <ar-dropdown name="Export" :sections="actionSections" />
      </div>
    </div>
  </div>
</template>
