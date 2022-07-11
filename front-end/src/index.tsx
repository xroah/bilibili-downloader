import React from "react"
import {createRoot} from "react-dom/client"
import App from "./views/App"

import "./styles/index.scss"

const el = document.createElement("div")
const root = createRoot(el)

root.render(<App/>)
document.body.appendChild(el)