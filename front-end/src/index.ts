import App from "./components/app.svelte"

const el = document.createElement("div")
const app = new App({
    target: el
})

el.classList.add("app")
document.body.appendChild(el)