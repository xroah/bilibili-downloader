import React from "react"
import { Provider } from "react-redux"
import store from "../store"

export default function App() {
    return (
        <Provider store={store}>
            <div>
                bilibili downloader
            </div>
        </Provider>
    )
}