declare global {
  interface Window {
    isIPythonEmbed: boolean
    arLocal: boolean
    reportProps?: any
  }
}

export {}
