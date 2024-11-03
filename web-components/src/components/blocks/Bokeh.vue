<script setup lang="ts">
import * as Bokeh from '@bokeh/bokehjs'
import { v4 as uuid4 } from 'uuid'
import { onMounted, onUnmounted } from 'vue'

const docIds: any[] = []
const divId = uuid4()

const p = defineProps<{
  plotJson: any
  responsive: boolean
  singleBlockEmbed?: boolean
}>()

const makeResponsive = (json: any) => {
  /**
   * make the plot respond to the dimensions of its container
   * if the responsive property is set
   */
  // NOTE: I'm not sure this is the best way...
  const roots: any[] = json.doc.roots
  roots.forEach(r => {
    r.attributes.sizing_mode = p.singleBlockEmbed
      ? 'stretch_both'
      : 'stretch_width'
  })
}

const cleanupDoc = (doc: any, docTimestamp: string) => {
  /**
   * remove any global Documents by checking their uuids
   */
  if ((doc as any).uuid === docTimestamp) {
    doc.clear()
    const i = Bokeh.documents.indexOf(doc)
    if (i > -1) {
      Bokeh.documents.splice(i, 1)
    }
  }
}

const addPlotToDom = async () => {
  /**
   * mount a Bokeh plot to the block element
   */
  try {
    if (p.responsive) {
      // TODO: makeResponsive does not work with Bokeh v3+.
      makeResponsive(p.plotJson)
    }
    const plotViews = await Bokeh.embed.embed_item(p.plotJson as any, divId)
    // Generate uuids for Bokeh Documents so they can be referenced on dismount
    plotViews.roots.forEach((pv: any) => {
      const docId = uuid4()
      ;(pv.model.document as any).uuid = docId
      docIds.push(docId)
    })
  } catch (e) {
    console.error('An error occurred while rendering a Bokeh chart: ', e)
  }
}

onMounted(() => {
  addPlotToDom()
})

onUnmounted(() => {
  // cleanup -- https://github.com/bokeh/bokeh/issues/5355#issuecomment-423580351
  for (const doc of Bokeh.documents) {
    for (const docTimestamp of docIds) {
      cleanupDoc(doc, docTimestamp)
    }
  }
})
</script>

<template>
  <div
    data-cy="block-bokeh"
    :id="divId"
    :class="[
      'bk-root m-auto flex justify-center items-center w-full',
      { 'w-full': p.responsive, 'h-iframe': singleBlockEmbed },
    ]"
  />
</template>
