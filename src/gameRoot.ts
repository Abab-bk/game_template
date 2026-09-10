import { createContext } from "svelte"
import { PixiManager } from "./pixiManager.svelte"

export const [getGameRootContext, setGameRootContext] = createContext<GameRoot>()

export type GameRoot = ReturnType<typeof createGameRoot>

export function createGameRoot() {
    const pixiManager = new PixiManager()

    return { pixiManager }
}
