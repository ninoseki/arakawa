import type { Component } from 'vue'

export const makeTemplate = (ArComponent: Component) => (args: any) => ({
  components: { ArComponent },
  setup() {
    return { args }
  },
  template: "<ar-component v-bind='args' />",
})
