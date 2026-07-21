import { mount } from "svelte"
import "./app.css"
import App from "./App.svelte"
import { createGameRoot } from "./gameRoot"

const gameRoot = await createGameRoot()

const app = mount(App, {
    target: document.getElementById("app")!,
    props: { gameRoot },
})

export default app
