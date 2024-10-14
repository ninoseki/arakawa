<script setup lang="ts">
import { sql } from '@codemirror/lang-sql'
import { Extension } from '@codemirror/state'
import { EditorView } from '@codemirror/view'
import { basicSetup } from 'codemirror'
import { onMounted, ref } from 'vue'

import ArButton from '../../../shared/ARButton.vue'

const p = defineProps<{
  initialQuery: string
  errors?: string
}>()

const CM_OPTIONS = {
  theme: 'eclipse',
  mode: 'sql',
  lineNumbers: false,
  autoRefresh: true,
}

function editorFromTextArea(
  textarea: HTMLTextAreaElement,
  extensions?: Extension,
) {
  const view = new EditorView({ doc: textarea.value, extensions })
  textarea.parentNode!.insertBefore(view.dom, textarea)
  textarea.style.display = 'none'
  if (textarea.form)
    textarea.form.addEventListener('submit', () => {
      textarea.value = view.state.doc.toString()
    })
  return view
}

const emit = defineEmits(['query-change', 'run-query', 'clear-query'])
const cmEl = ref<HTMLTextAreaElement>()
const cmInstance = ref<EditorView>()

const emitQueryChange = (query: string) => void emit('query-change', query)

onMounted(() => {
  if (cmEl.value) {
    // Set up codemirror instance on mount
    cmInstance.value = editorFromTextArea(cmEl.value, [
      basicSetup,
      sql(),
      EditorView.updateListener.of(v => {
        emitQueryChange(v.state.doc.toString())
      }),
    ])
    emitQueryChange(cmInstance.value.state.doc.toString())
  } else {
    console.error("Couldn't find codemirror textarea element")
  }
})
</script>

<template>
  <div class="flex flex-col justify-start border-b border-gray-200">
    <div class="flex flex-col flex-fixed h-full">
      <textarea ref="cmEl" :value="p.initialQuery"></textarea>
      <div class="flex justify-start flex-fixed my-2 px-2">
        <ar-button
          @click="emit('run-query')"
          icon="fa fa-play"
          data-cy="btn-run-query"
          class="w-28 ar-btn-primary"
        >
          Run Query
        </ar-button>
        <ar-button
          @click="emit('clear-query')"
          icon="fa fa-undo"
          class="ml-2 w-28 ar-btn-secondary-gray"
          data-cy="btn-reset-data"
        >
          Reset Data
        </ar-button>
      </div>
    </div>
  </div>
  <div v-if="p.errors" class="w-full bg-red-100" data-cy="alasql-error-msg">
    {{ p.errors }}
  </div>
</template>
