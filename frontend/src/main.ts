import './assets/main.css'
import 'primeicons/primeicons.css'

import App from './App.vue'
import Button from 'primevue/button'
import PrimeVue from 'primevue/config'
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(PrimeVue)

app.component('PrimeButton', Button)

app.mount('#app')
