<script setup lang="ts">
import 'vue-multiselect/dist/vue-multiselect.min.css'

import Sigma from 'sigma'
import { onMounted, ref } from 'vue'
import MultiSelect from 'vue-multiselect'

const p = defineProps<{
  data: unknown
  layoutSettings: unknown
  height: number
  width: number
}>()

interface State {
  hoveredNode?: string
  hoveredNeighbors?: Set<string>
  selectedNode?: string
  suggestions?: Set<string>
}

import Graph from 'graphology'
import forceAtlas2 from 'graphology-layout-forceatlas2'
import seedrandom from 'seedrandom'

type RNGFunction = () => number

const createRng = (): RNGFunction => {
  return seedrandom('arakawa')
}

const isValidNumber = (value: unknown): boolean => {
  return typeof value === 'number' && !isNaN(value)
}

const updateLayout = (graph: Graph) => {
  const positions = forceAtlas2(graph, {
    iterations: 100,
    settings: p.layoutSettings as any,
  })

  for (const { node } of graph.nodeEntries()) {
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    graph.updateNodeAttribute(node, 'x', _ => positions[node].x)
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    graph.updateNodeAttribute(node, 'y', _ => positions[node].y)
  }

  return graph
}

const buildGraph = (data: any, rng: RNGFunction): Graph => {
  const graph = Graph.from(data)

  // Rectifications
  graph.updateEachNodeAttributes((key, attr) => {
    // Random position for nodes without positions
    if (!isValidNumber(attr.x)) attr.x = rng()
    if (!isValidNumber(attr.y)) attr.y = rng()

    return attr
  })

  return updateLayout(graph)
}

const graph = buildGraph(p.data, createRng())
const graphTitle = `${graph.multi ? 'Multi ' : ''}${
  graph.type === 'undirected' ? 'Undirected' : 'Directed'
} Graph`

const labels = graph
  .nodes()
  .map(n => graph.getNodeAttribute(n, 'label'))
  .filter(label => label !== undefined)

const container = ref<HTMLElement>()
const sigma = ref<Sigma>()

const state: State = {}
const searchQuery = ref('')

const onReset = () => {
  if (sigma.value) {
    state.hoveredNeighbors = undefined
    state.hoveredNode = undefined
    state.selectedNode = undefined
    state.suggestions = undefined
    sigma.value.refresh()

    const camera = sigma.value.getCamera()
    camera.animatedReset()
  }
}

const onSearch = () => {
  if (!sigma.value) {
    return
  }

  if (
    searchQuery.value === '' ||
    searchQuery.value === undefined ||
    searchQuery.value === null
  ) {
    onReset()
  }

  const lowerCased = searchQuery.value.toLowerCase()
  const suggestions = graph
    .nodes()
    .map(n => ({ id: n, label: graph.getNodeAttribute(n, 'label') }))
    .filter(({ label }) => label.toLowerCase().includes(lowerCased))

  if (suggestions.length === 1 && suggestions[0].label === searchQuery.value) {
    state.selectedNode = suggestions[0].id
    state.suggestions = undefined

    const nodePosition = sigma.value.getNodeDisplayData(state.selectedNode)
    if (nodePosition) {
      sigma.value.getCamera().animate(nodePosition, {
        duration: 500,
      })
    }
  } else {
    state.selectedNode = undefined
    state.suggestions = new Set(suggestions.map(s => s.id))
  }

  sigma.value.refresh()
}

onMounted(() => {
  if (container.value) {
    sigma.value = new Sigma(graph, container.value, {
      allowInvalidContainer: true,
      autoCenter: true,
      autoRescale: true,
    })

    sigma.value.setSetting('nodeReducer', (node: string, data: any) => {
      const res = { ...data }

      if (state.hoveredNeighbors?.has(node) && state.hoveredNode !== node) {
        res.label = ''
        res.color = '#f6f6f6'
      }

      if (state.selectedNode === node) {
        res.highlighted = true
      } else if (state.suggestions?.has(node)) {
        res.label = ''
        res.color = '#f6f6f6'
      }

      return res
    })

    sigma.value.setSetting('edgeReducer', (edge: string, data: any) => {
      const res = { ...data }

      if (state.hoveredNode && !graph.hasExtremity(edge, state.hoveredNode)) {
        res.hidden = true
      }

      if (
        state.suggestions &&
        (!state.suggestions.has(graph.source(edge)) ||
          !state.suggestions.has(graph.target(edge)))
      ) {
        res.hidden = true
      }

      return res
    })

    const setHoveredNode = (node?: string) => {
      if (node) {
        state.hoveredNode = node
        state.hoveredNeighbors = new Set(graph.neighbors(node))
      } else {
        state.hoveredNode = undefined
        state.hoveredNeighbors = undefined
      }
      sigma.value?.refresh()
    }

    sigma.value.on('clickNode', ({ node }) => {
      setHoveredNode(node)
    })
    sigma.value.on('clickStage', () => {
      setHoveredNode(undefined)
    })
  }
})
</script>

<template>
  <div class="w-full grid grid-cols-12 gap-1">
    <div class="col-span-10 flex items-center justify-center">
      <div
        id="sigma-container"
        class="rounded-md border border-gray-300"
        :style="{ height: `${p.height}px`, width: `${p.width}px` }"
        ref="container"
      ></div>
    </div>
    <div class="col-span-2">
      <p class="py-2">
        <span>{{ graphTitle }}</span>
        <br />
        <span class="text-sm text-ar-light-gray"> {{ graph.order }} nodes</span>
        <br />
        <span class="text-sm text-ar-light-gray"> {{ graph.size }} edges </span>
      </p>
      <div class="py-2">
        <multi-select
          v-model="searchQuery"
          placeholder="Search"
          :options="labels"
          class="text-sm font-medium text-gray-700"
          @change="onSearch"
          @select="onSearch"
          @close="onSearch"
        />
      </div>
      <div class="py-2">
        <ar-button
          class="bg-gray-500 hover:bg-gray-400 text-white rounded px-4 py-2"
          @click="onReset"
          >Reset</ar-button
        >
      </div>
    </div>
  </div>
</template>
