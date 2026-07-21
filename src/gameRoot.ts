import { PixiManager } from "./pixiManager"

export interface GameRoot {
    pixiManager: PixiManager
}

export async function createGameRoot(): Promise<GameRoot> {
    const pixiManager = new PixiManager()
    await pixiManager.init()

    return { pixiManager }
}
