import Vue from 'vue'
import Vuex from 'vuex'

import core from './modules/core'
import session from './modules/session'
import snackbar from './modules/snackbar'

Vue.use(Vuex)

export default new Vuex.Store({
    namespaced: true,
    modules: {
        core,
        session,
        snackbar
    },
    state: {

    },
    mutations: {

    },
    actions: {

    }
})
