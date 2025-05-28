/**
 * main.js
 *
 * Bootstraps Vuetify and other plugins then mounts the App`
 */

// Plugins
import { registerPlugins } from '@/plugins'

// Components
import App from './App.vue'
import CMMSApi from './services/CMMSApi'

// Composables
import { createApp } from 'vue'

const app = createApp(App)
app.provide('cmms_api', new CMMSApi('http://localhost:5000'))

registerPlugins(app)

app.mount('#app')
