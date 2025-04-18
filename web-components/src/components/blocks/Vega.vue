<script setup lang="ts">
import { v4 as uuid4 } from 'uuid'
import vegaEmbed, { type Result } from 'vega-embed'
import { onMounted, onUnmounted, ref, toRaw } from 'vue'

const p = defineProps<{
  plotJson: any
  responsive: boolean
  singleBlockEmbed?: boolean
}>()
const divId = `vega_${uuid4()}`

// Vega view object to be stored for cleanup on unmount
const vegaView = ref<Result | undefined>()

const makeResponsive = (json: any) => {
  /**
   * make the plot respond to the dimensions of its container
   * if the responsive property is set
   */
  json.width = 'container'
  if (p.singleBlockEmbed) {
    json.height = 'container'
  }
}

const adjustHeightFromBindings = () => {
  /**
   * Prevent the vega-bindings element from being cut off in single block embed mode
   */
  const plotEl: HTMLElement | null = document.getElementById(divId)
  const bindingEl: HTMLElement | null =
    plotEl && plotEl.querySelector<HTMLElement>('.vega-bindings')
  const canvasEl: HTMLElement | null = plotEl && plotEl.querySelector('canvas')
  if (canvasEl && bindingEl) {
    canvasEl.style.height = `${
      canvasEl.offsetHeight - bindingEl.offsetHeight
    }px`
  }
}

const addPlotToDom = async () => {
  /**
   * mount a Vega plot to the block element
   */
  try {
    if (p.responsive) {
      makeResponsive(p.plotJson)
    }
    const unwrapped = toRaw(p.plotJson)
    const view = await vegaEmbed(`#${divId}`, unwrapped, {
      mode: 'vega-lite',
      actions: false, // disable the altair action menu
    })
    vegaView.value = view
    if (p.singleBlockEmbed) {
      adjustHeightFromBindings()
    }
  } catch (e) {
    console.error('An error occurred while rendering an Altair chart: ', e)
  }
}

onMounted(() => {
  addPlotToDom()
})

onUnmounted(() => void vegaView.value?.finalize())
</script>

<template>
  <div
    :class="[
      'justify-center bg-white flex',
      { 'w-full': p.responsive, 'h-iframe': singleBlockEmbed },
    ]"
  >
    <!-- Vega bindings don't display correctly when setting `flex` directly on the vega element,
            so wrap it in a flex container and apply `dimensionClasses` twice -->
    <div
      :id="divId"
      :class="{ 'w-full': p.responsive, 'h-iframe': singleBlockEmbed }"
      data-cy="block-vega"
    ></div>
  </div>
</template>
