<script setup lang="ts">
import { BlockFigureProps } from "../../data-model/blocks";
import { useRootStore } from "../../data-model/root-store";
import BlockWrapper from "../layout/BlockWrapper.vue";
import Plotapi from "./Plotapi.vue";
import { storeToRefs } from "pinia";
import { ref } from "vue";

const p = defineProps<{
  fetchAssetData: any;
  figure: BlockFigureProps;
  singleBlockEmbed?: boolean;
}>();
const rootStore = useRootStore();
const { singleBlockEmbed } = storeToRefs(rootStore);
const iframeContent = ref<string | null>(null);

(async () => {
  iframeContent.value = await p.fetchAssetData();
})();
</script>

<template>
  <block-wrapper :figure="p.figure" :single-block-embed="singleBlockEmbed">
    <plotapi
      v-if="iframeContent"
      :iframe-content="iframeContent"
      :single-block-embed="!!singleBlockEmbed"
    />
  </block-wrapper>
</template>
