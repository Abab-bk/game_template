import { Application, Container, Ticker, type ApplicationOptions } from "pixi.js"

export class PixiManager {
    readonly app: Application
    canvas!: HTMLCanvasElement
    stage!: Container
    ticker!: Ticker

    constructor() {
        this.app = new Application()
    }

    async init(options?: Partial<ApplicationOptions>): Promise<void> {
        await this.app.init({
            resizeTo: window,
            background: 0x0a0a14,
            ...options,
        })

        this.canvas = this.app.canvas as HTMLCanvasElement
        this.stage = this.app.stage
        this.ticker = this.app.ticker
    }

    destroy() {
        this.app.destroy()
    }
}
