<script lang="ts">
    import { setLinguiContext } from "lingui-for-svelte"
    import { i18n } from "./i18n"
    import { createGameRoot, setGameRootContext } from "./gameRoot"
    import GameCanvas from "./GameCanvas.svelte"
    import Hud from "./ui/Hud.svelte"

    const gameRoot = createGameRoot()
    setGameRootContext(gameRoot)

    setLinguiContext(i18n)
</script>

<div class="stack">
    <GameCanvas></GameCanvas>

    {#if gameRoot.pixiManager.initialized}
        <Hud></Hud>
    {/if}
</div>
