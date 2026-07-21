<script lang="ts">
    import { onMount } from "svelte"
    import type { GameRoot } from "./gameRoot"

    let { gameRoot }: { gameRoot: GameRoot } = $props()

    onMount(() => {
        const target = document.getElementById("app")!
        target.appendChild(gameRoot.pixiManager.canvas)

        return () => {
            gameRoot.pixiManager.destroy()
        }
    })
</script>
