import { defineConfig } from "vite"
import { svelte } from "@sveltejs/vite-plugin-svelte"
import tailwindcss from "@tailwindcss/vite"
import linguiMacro from "unplugin-lingui-macro/vite"
import linguiForSvelte from "lingui-for-svelte/unplugin/vite"

export default defineConfig({
    plugins: [tailwindcss(), linguiMacro(), linguiForSvelte(), svelte()],
})
