import babelExtractor from "@lingui/cli/api/extractors/babel"
import { defineConfig } from "lingui-for-svelte/config"
import { svelteExtractor } from "lingui-for-svelte/extractor"

export default defineConfig({
    locales: ["zh-Hans", "en"],
    sourceLocale: "zh-Hans",
    catalogs: [
        {
            path: "<rootDir>/src/locales/{locale}/messages",
            include: ["src"],
        },
    ],
    extractors: [svelteExtractor, babelExtractor],
    macro: {
        corePackage: ["@lingui/core/macro", "#lingui-macro"],
    },
})
