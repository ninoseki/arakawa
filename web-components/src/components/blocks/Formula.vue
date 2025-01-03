<script setup lang="ts">
import katex from 'katex'

const p = defineProps<{ content: string }>()

const renderFormula = (node: any) => {
  try {
    katex.render(p.content, node)
  } catch (e) {
    console.error(`Error rendering formula: ${e}`)
  }
}

const formulaRef = (node: any) => {
  if (node) {
    renderFormula(node)
  }
}
</script>

<template>
  <link
    rel="stylesheet"
    href="https://cdn.jsdelivr.net/npm/katex@0.16.15/dist/katex.css"
    integrity="sha256-4aMlusw7NpNRNuQ50hS7anjdz2PU+g2PLD0FRjz8BsA="
    crossorigin="anonymous"
  />
  <div
    data-cy="block-formula"
    className="w-full overflow-y-hidden bg-white flex justify-center"
    :ref="formulaRef"
  ></div>
</template>
