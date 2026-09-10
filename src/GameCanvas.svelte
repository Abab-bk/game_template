<script lang="ts">
    import type { Attachment } from "svelte/attachments"
    import { getGameRootContext } from "./gameRoot"

    const { pixiManager } = getGameRootContext()

    const setup: Attachment = (element) => {
        pixiManager.init().then(() => element.appendChild(pixiManager.canvas))

        return () => {
            pixiManager.destroy()
        }
    }
</script>

<div {@attach setup}></div>
