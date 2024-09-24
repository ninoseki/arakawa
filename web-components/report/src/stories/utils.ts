import { Component as VueComponent } from "vue";

export const makeTemplate = (DpComponent: VueComponent) => (args: any) => ({
    components: { DpComponent },
    setup() {
        return { args };
    },
    template: "<ar-component v-bind='args' />",
});
