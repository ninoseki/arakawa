<script setup lang="ts">
/* eslint-disable no-useless-escape */
import { BlockFigureProps } from "../../data-model/blocks";
import BlockWrapper from "../layout/BlockWrapper.vue";
import iframeResize from "iframe-resizer/js/iframeResizer";
import contentWindowJs from "iframe-resizer/js/iframeResizer.contentWindow.js?raw";
import { v4 as uuid4 } from "uuid";
import { computed, ComputedRef, onMounted } from "vue";

const p = defineProps<{
  html: string;
  isIframe: boolean;
  figure: BlockFigureProps;
  singleBlockEmbed?: boolean;
}>();
const iframeId = `iframe_${uuid4()}`;

// Unescape script tags when embedding
const decodedHtml: ComputedRef<string> = computed(() => {
  return p.html
    .replace("&lt;script&gt;", "<script>")
    .replace("&lt;&sol;script&gt;", "<\/script>");
});

const iframeDoc: ComputedRef<string> = computed(() => {
  /**
   * Inject the JS needed to make the iframe resizer work
   */
  return `
        <!DOCTYPE html>
        <html>
        <body>
            <script>${contentWindowJs}<\/script>
            ${decodedHtml.value}
        </body>
        </html>
    `;
});

onMounted(() => {
  iframeResize({ checkOrigin: false, warningTimeout: 10000 }, `#${iframeId}`);
});
</script>

<template>
  <block-wrapper :figure="p.figure" :single-block-embed="singleBlockEmbed">
    <div
      v-if="isIframe"
      v-html="decodedHtml"
      class="flex justify-center items-center"
      data-cy="block-embed"
    />
    <iframe
      v-else
      :id="iframeId"
      :srcdoc="iframeDoc"
      class="flex justify-center items-center"
    />
  </block-wrapper>
</template>
