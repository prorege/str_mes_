import engine from 'store/src/store-engine'
import localStorage from 'store/storages/localStorage'
import pluginDefault from 'store/plugins/defaults'
import pluginExpire from 'store/plugins/expire'

const storages = [localStorage]
const plugins = [pluginDefault, pluginExpire]
const store = engine.createStore(storages, plugins)

export default store