import { fileURLToPath } from 'node:url'

import type { ConfigEnv } from 'vite'
import { configDefaults, defineConfig, mergeConfig } from 'vitest/config'

import viteConfig from './vite.config'

export default defineConfig((configEnv) =>
  mergeConfig(
    // `vite.config.ts` exports a config-factory function, so it must be invoked
    // before merging rather than merged directly
    viteConfig(configEnv as ConfigEnv),
    defineConfig({
      test: {
        environment: 'jsdom',
        exclude: [...configDefaults.exclude, 'e2e/**'],
        root: fileURLToPath(new URL('./', import.meta.url)),
      },
    }),
  ),
)
