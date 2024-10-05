import { defineAsyncComponent, defineCustomElement } from "vue";
import { toggleVisibility, onLoad } from "./src/template-utils";

const Modal = defineAsyncComponent(() => import("./src/Modal.ce.vue"));
const SearchQuery = defineAsyncComponent(
  () => import("./src/SearchQuery.ce.vue"),
);

customElements.define("ar-modal", defineCustomElement(Modal));
customElements.define("ar-search-query", defineCustomElement(SearchQuery));

const templateUtils = {
  toggleVisibility,
  onLoad,
};

export { templateUtils };
