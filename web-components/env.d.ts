/// <reference types="vite/client" />

// `@iframe-resizer/vue` exposes the SFC entry only via its `browser` field
// (`./sfc` → `iframe-resizer.vue`), which TypeScript doesn't resolve. Stub it
// as a Vue component so consumers can import it without ts-plugin(2307).
declare module '@iframe-resizer/vue/sfc' {
  import type { DefineComponent } from 'vue'
  const component: DefineComponent<Record<string, unknown>, object, unknown>
  export default component
}
