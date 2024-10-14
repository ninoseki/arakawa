import pluginVitest from '@vitest/eslint-plugin'
import skipFormatting from '@vue/eslint-config-prettier/skip-formatting'
import vueTsEslintConfig from '@vue/eslint-config-typescript'
import simpleImportSort from 'eslint-plugin-simple-import-sort'
import pluginVue from 'eslint-plugin-vue'

const mode = process.env.NODE_ENV === 'production' ? 'error' : 'warn'

export default [
  {
    name: 'app/files-to-lint',
    files: ['**/*.{ts,mts,tsx,vue}'],
  },
  {
    name: 'app/files-to-ignore',
    ignores: ['**/dist/**', '**/dist-ssr/**', '**/coverage/**'],
  },
  ...pluginVue.configs['flat/essential'],
  ...vueTsEslintConfig(),
  {
    ...pluginVitest.configs.recommended,
    files: ['src/**/__tests__/*'],
  },
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
            'Bokeh',
            'Code',
            'Compute',
            'Embed',
            'File',
            'Folium',
            'Formula',
            'Group',
            'Header',
            'Media',
            'Modal.ce',
            'Plotapi',
            'Plotly',
            'SearchQuery.ce',
            'Table.ce',
            'Text',
            'Toggle',
            'Vega',
          ],
        },
      ],
    },
  },
]
