/* eslint-disable */

const defaultTheme = require("tailwindcss/defaultTheme");
const { colors: fontFamily } = defaultTheme;
const plugin = require("tailwindcss/plugin");

module.exports = {
    darkMode: "class",
    theme: {
        fontFamily: {
            ...fontFamily,
            "ar-prose": "var(--ar-font-family)",
        },
        extend: {
            colors: {
                "ar-accent-light": "var(--ar-accent-secondary-color)",
                "ar-accent": "var(--ar-accent-color)",
                "ar-accent-text": "var(--ar-accent-text)",
                "ar-background": "var(--ar-bg-color)",
                "ar-light-gray": "var(--ar-light-gray)",
                "ar-dark-gray": "var(--ar-dark-gray)",
            },
            typography: {
                DEFAULT: {
                    // Disable prose being applied to code elements
                    css: {
                        pre: false,
                        code: false,
                        "pre code": false,
                        "code::before": false,
                        "code::after": false,
                        p: {
                            "text-align": "var(--ar-text-align)",
                            hyphens: "auto",
                        },
                        li: {
                            "text-align": "var(--ar-text-align)",
                            hyphens: "auto",
                        },
                    },
                },
            },
            fontFamily: {
                sans: ["Inter", ...defaultTheme.fontFamily.sans],
            },
            width: {
                80: "20rem",
                96: "24rem",
            },
            flex: {
                fixed: "0 0 auto",
                "fixed-64": "0 0 16rem",
                full: "0 0 100%",
                "initial-grow": "1 0 0",
                "initial-80": "0 1 20rem",
            },
            gridTemplateColumns: {
                fit: "repeat(auto-fit, minmax(0, 1fr))",
            },
            gridTemplateRows: {
                fit: "repeat(auto-fit, minmax(auto, auto))",
            },
        },
        fontSize: {
            xs: "0.75rem",
            sm: "0.875rem",
            base: "1rem",
            lg: "1.125rem",
            xl: "1.25rem",
            "2xl": "1.5rem",
            "3xl": "1.875rem",
            "4xl": "2.25rem",
            "5xl": "3rem",
            "6xl": "4rem",
        },
    },
    variants: {
        extend: {
            backgroundColor: ["active", "odd"],
            textColor: ["active"],
            display: ["group-hover"],
            opacity: ["disabled"],
            cursor: ["disabled"],
        },
        opacity: ["responsive", "hover", "focus", "disabled"],
    },
    plugins: [
        require("@tailwindcss/forms"),
        require("@tailwindcss/typography"),
        require("@tailwindcss/aspect-ratio"),
        require("@formkit/themes/tailwindcss"),

        plugin(function ({ matchUtilities }) {
            // If we have this in a template:
            //   <svg class="stroke-width-[1.25]">
            //
            // then we want tailwind to produce CSS like this:
            // .stroke-width-\[1.25\] > svg {
            //    stroke-width: 1.25
            // }
            //
            // This is used with nested <svg> elements to override the
            // `stroke-width` attribute on the inner <svg>.
            matchUtilities(
                {
                    "stroke-width": (value) => ({
                        ["> svg"]: {
                            "stroke-width": value,
                        },
                    }),
                },
                { values: { "\\d+(\\.\\d+)?": true } }
            );
        }),
    ],
    content: [],
    safelist: [
        { pattern: /grid-cols-.*/ },
        { pattern: /grid-rows-.*/ },
        { pattern: /grid-flow-.*/ },
        "max-w-screen-xl",
        "max-w-3xl",
        "max-w-full",
        "max-w-none",
    ],
};
