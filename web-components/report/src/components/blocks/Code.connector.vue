<script setup lang="ts">
import { BlockFigureProps } from "../../data-model/blocks";
import BlockWrapper from "../layout/BlockWrapper.vue";
import CodeBlock from "./Code.vue";

const p = defineProps<{
  code: string;
  language: string;
  figure: BlockFigureProps;
  singleBlockEmbed?: boolean;
}>();
const childProps = { code: p.code, language: p.language };
</script>

<template>
  <block-wrapper :figure="p.figure" :single-block-embed="singleBlockEmbed">
    <code-block v-bind="childProps" class="w-full"></code-block>
  </block-wrapper>
</template>
