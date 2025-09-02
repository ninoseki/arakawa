// @ts-check
import pluginVitest from '@vitest/eslint-plugin'
import skipFormatting from '@vue/eslint-config-prettier/skip-formatting'
import vueTsEslintConfig from '@vue/eslint-config-typescript'
import simpleImportSort from 'eslint-plugin-simple-import-sort'
import storybook from 'eslint-plugin-storybook'
import pluginVue from 'eslint-plugin-vue'
import tseslint from 'typescript-eslint'

const mode = process.env.NODE_ENV === 'production' ? 'error' : 'warn'

export default tseslint.config(
  {
    name: 'app/files-to-lint',
    files: ['**/*.{ts,mts,tsx,vue}'],
  },
  {
    name: 'app/files-to-ignore',
    ignores: [
      '**/dist/**',
      '**/dist-ssr/**',
      '**/coverage/**',
      '**/storybook-static/**',
    ],
  },
  ...pluginVue.configs['flat/essential'],
  ...vueTsEslintConfig(),
  ...storybook.configs['flat/recommended'],
  {
    ignores: ['!.storybook'],
  },
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
            'Alert',
            'Attachment',
            'Bokeh',
            'Code',
            'Compute',
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
