import path from 'path'
import { LibraryFormats, mergeConfig } from 'vite'
import { viteSingleFile } from 'vite-plugin-singlefile'

import { baseConfig } from './base.vite.config'

export default mergeConfig(baseConfig, {
  plugins: [viteSingleFile()],
  build: {
    outDir: './dist/local-report/',
    lib: {
      entry: [path.resolve(__dirname, './src/local-report.index.ts')],
      formats: ['es'] as LibraryFormats[],
      fileName: 'local-report',
      cssFileName: 'local-report',
    },
  },
})
