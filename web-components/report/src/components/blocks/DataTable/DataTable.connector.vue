<script setup lang="ts">
import {
  BlockFigureProps,
  DatasetResponse,
  ExportType,
} from "../../../data-model/blocks";
import { useRootStore } from "../../../data-model/root-store";
import BlockWrapper from "../../layout/BlockWrapper.vue";
import { storeToRefs } from "pinia";
import { defineAsyncComponent, ref } from "vue";

const DataTableBlock = defineAsyncComponent(() => import("./DataTable.vue"));

const p = defineProps<{
  streamContents: () => Promise<DatasetResponse>;
  deferLoad: boolean;
  cells: number;
  refId: string;
  getCsvText: () => Promise<string>;
  downloadLocal: (type: ExportType) => Promise<void>;
  downloadRemote: (type: ExportType) => Promise<void>;
  figure: BlockFigureProps;
  singleBlockEmbed?: boolean;
}>();

const rootStore = useRootStore();
const { singleBlockEmbed } = storeToRefs(rootStore);
const previewMode = ref(p.deferLoad);
const dsData = ref([]);
const dsSchema = ref({});

const getResultData = async () => {
  /**
   * Fetch dataset content and schema
   */
  try {
    const successfulDownload: any = await p.streamContents();
    if (successfulDownload) {
      // TODO - containsBigInt
      const { schema, data } = successfulDownload;
      dsData.value = dsData.value.concat(data);
      dsSchema.value = schema;
    }
  } catch (e) {
    console.error("An error occurred downloading your dataset data: " + e);
  }
};

if (!p.deferLoad) {
  getResultData();
}

const handleLoadFull = async () => {
  await getResultData();
  if (dsData.value.length) {
    previewMode.value = false;
  }
};
</script>

<template>
  <block-wrapper :figure="p.figure" :single-block-embed="singleBlockEmbed">
    <data-table-block
      :singleBlockEmbed="!!singleBlockEmbed"
      :data="dsData"
      :cells="p.cells"
      :schema="dsSchema"
      :previewMode="previewMode"
      :getCsvText="p.getCsvText"
      :downloadLocal="p.downloadLocal"
      :downloadRemote="p.downloadRemote"
      :refId="p.refId"
      @load-full="handleLoadFull"
    />
  </block-wrapper>
</template>
