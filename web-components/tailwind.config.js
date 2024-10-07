/* eslint-disable */

const config = require("./base.tailwind.config");

config.content = [
  // Report renderer
  "./report/src/**/*.{vue,js,ts}",
  // Web components
  "./template-components/src/**/*.{vue,js,ts}",
];

module.exports = config;
