/* eslint-disable */

const defaultTheme = require('tailwindcss/defaultTheme')
const config = require('./base.tailwind.config')
const { colors: fontFamily } = defaultTheme

config.content = [
  './src/**/*.{vue,js,ts}',
  '../python-client/src/arakawa/resources/html_templates/*.html.j2',
]

module.exports = config
