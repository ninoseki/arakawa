import "./src/styles/base.scss";
import "./src/styles/templates-base.scss";
import "./src/styles/tailwind.css";
import { ARClipboard } from "../shared/ARClipboard";

// JS Polyfills
import "whatwg-fetch";
import "./src/polyfills";

import "htmx.org/dist/htmx";

// Window objects
window.errorHandler = window.errorHandler || {};

export { ARClipboard as DPClipboard };
