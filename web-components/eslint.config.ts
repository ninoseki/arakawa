import pluginVitest from '@vitest/eslint-plugin'
import { defineConfigWithVueTs, vueTsConfigs } from '@vue/eslint-config-typescript'
import skipFormatting from 'eslint-config-prettier/flat'
import pluginOxlint from 'eslint-plugin-oxlint'
import simpleImportSort from 'eslint-plugin-simple-import-sort'
import storybook from 'eslint-plugin-storybook'
import pluginVue from 'eslint-plugin-vue'

const mode = process.env.NODE_ENV === 'production' ? 'error' : 'warn'

export default defineConfigWithVueTs(
  {
    name: 'app/files-to-lint',
    files: ['**/*.{ts,mts,tsx,vue}'],
  },
  {
    name: 'app/files-to-ignore',
    ignores: ['**/dist/**', '**/dist-ssr/**', '**/coverage/**', '**/storybook-static/**'],
  },
  ...pluginVue.configs['flat/essential'],
  vueTsConfigs.recommended,
  ...storybook.configs['flat/recommended'],
  {
    ignores: ['!.storybook'],
  },
  {
    ...pluginVitest.configs.recommended,
    files: ['src/**/__tests__/*'],
  },
  ...pluginOxlint.buildFromOxlintConfigFile('.oxlintrc.json'),
  skipFormatting,
  {
    plugins: {
      'simple-import-sort': simpleImportSort,
    },
    rules: {
      'simple-import-sort/imports': mode,
      'simple-import-sort/exports': mode,
      'no-console': 'warn',
      'no-debugger': 'warn',
      '@typescript-eslint/no-explicit-any': 'warn',
      'vue/multi-word-component-names': [
        'error',
        {
          ignores: [
            'Alert',
            'Attachment',
            'Bokeh',
            'Code',
            'Compute',
            'Divider',
            'Embed',
            'Folium',
            'Formula',
            'Group',
            'Header',
            'Markdown',
            'Media',
            'Modal.ce',
            'Plotapi',
            'Plotly',
            'SearchQuery.ce',
            'Sigma',
            'Table.ce',
            'Text',
            'Toggle',
            'Vega',
          ],
        },
      ],
    },
  },
)
