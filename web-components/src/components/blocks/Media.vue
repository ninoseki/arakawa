<script setup lang="ts">
import BlockWrapper from '@/components/layout/BlockWrapper.vue'
import type { BlockFigureProps } from '@/data-model/blocks'

defineProps<{
  src: string
  type: string
  figure: BlockFigureProps
  singleBlockEmbed?: boolean
}>()
</script>

<template>
  <block-wrapper :figure="figure" :single-block-embed="singleBlockEmbed">
    <div class="w-full flex items-center justify-center" data-cy="block-media">
      <video
        v-if="type.startsWith('video')"
        controls
        :src="src"
        width="800"
      ></video>
      <audio
        v-else-if="type.startsWith('audio')"
        controls
        :src="src"
        class="w-full"
      ></audio>
      <img v-else :src="src" loading="lazy" class="mx-auto" />
    </div>
  </block-wrapper>
</template>
