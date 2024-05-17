import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import axios from "axios";

const app = createApp(App)

const token = localStorage.getItem('user-token')
const name = localStorage.getItem('user-name')
if (token) {
    axios.defaults.headers.common['Authorization'] = token
    axios.defaults.headers.common['Name'] = name
}

app.use(router)

app.mount('#app')


