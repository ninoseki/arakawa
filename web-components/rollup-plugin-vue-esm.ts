/**
 * Plugin that copies vue ES modules from node_modules/ to dist/
 * for access by template HTML files
 */

import fs from 'fs'
import path from 'path'

const VUE_DEV_FNAME = 'vue.esm-browser.js'
const VUE_PROD_FNAME = 'vue.esm-browser.prod.js'

export default () => ({
  name: 'rollup-plugin-vue-esm',
  buildEnd: async () => {
    const vuePath = path.resolve(__dirname, './node_modules/vue/dist')
    const distPath = path.resolve(__dirname, './dist')
    const prodVueFile = path.resolve(distPath, VUE_PROD_FNAME)

    if (fs.existsSync(prodVueFile)) {
      // Don't copy over files if they already exist
      return
    }

    if (!fs.existsSync(distPath)) {
      await fs.promises.mkdir(distPath)
    }

    await Promise.all([
      fs.promises.copyFile(
        path.resolve(vuePath, VUE_DEV_FNAME),
        path.resolve(distPath, VUE_DEV_FNAME),
      ),
      fs.promises.copyFile(path.resolve(vuePath, VUE_PROD_FNAME), prodVueFile),
    ])
  },
})
