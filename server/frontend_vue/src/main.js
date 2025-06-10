import 'devextreme/dist/css/dx.common.css'
import 'devexpress-gantt/dist/dx-gantt.css'
import './themes/generated/theme.base.css'
import './themes/generated/theme.additional.css'
import config from "devextreme/core/config"
import { locale, loadMessages } from "devextreme/localization"
import koMessages from "./locales/ko.json"
import { createApp }  from 'vue'
import router from './router'

import App from './App'
import appInfo from './app-info'
import appConfig from './app-config'

config(appConfig)
loadMessages(koMessages)
locale(navigator.language)

const app = createApp(App)
app.use(router)
app.config.globalProperties.$appInfo = appInfo
app.mount('#app')
