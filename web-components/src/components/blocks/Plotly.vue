<script setup lang="ts">
import Plotly from 'plotly.js-dist-min'
import { v4 as uuid4 } from 'uuid'
import { onMounted } from 'vue'

const p = defineProps<{
  plotJson: any
  responsive: boolean
  singleBlockEmbed?: boolean
}>()
const divId = `plotly_${uuid4()}`

const makeResponsive = (json: any) => {
  /**
   * make the plot respond to the dimensions of its container
   * if the responsive property is set
   */
  const { layout } = json
  if (layout) {
    delete layout.autosize
    delete layout.width
    if (p.singleBlockEmbed) {
      delete layout.height
    }
  }
}

const addPlotToDom = async () => {
  /**
   * mount a Plotly plot to the block element
   */
  if (p.responsive) {
    makeResponsive(p.plotJson)
  }
  Plotly.newPlot(divId, {
    data: p.plotJson.data,
    layout: {
      ...PLOTLY_LAYOUT_DEFAULTS,
      ...p.plotJson.layout,
      autosize: p.responsive,
    },
    config: PLOTLY_CONFIG,
    frames: p.plotJson.frames || undefined,
  })
}

onMounted(() => {
  addPlotToDom()
})
</script>

<script lang="ts">
const PLOTLY_CONFIG: any = {
  displaylogo: false,
  responsive: true,
}

const PLOTLY_LAYOUT_DEFAULTS = {
  modebar: {
    orientation: 'v',
  },
}
</script>

<template>
  <div
    data-cy="block-plotly"
    :class="[
      'bg-white flex justify-center',
      { 'w-full': responsive, 'h-iframe': singleBlockEmbed },
    ]"
  >
    <div :id="divId" class="w-full"></div>
  </div>
</template>
