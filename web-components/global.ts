declare global {
  interface Window {
    isIPythonEmbed: boolean;
    arLocal: boolean;
    reportProps?: any;
    Alpine: any;
    $testResources: any;
    errorHandler: any;
  }
}

export {};
