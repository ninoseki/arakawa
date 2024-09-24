declare global {
    interface Window {
        isIPythonEmbed: boolean;
        arLocal: boolean;
        reportProps?: any;
        arAppRunner: boolean;
        Alpine: any;
        $testResources: any;
        errorHandler: any;
    }
}

export {};
