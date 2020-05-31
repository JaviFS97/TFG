import Vue from 'vue'
import App from './App.vue'

// External libraries 
import router from './router'
import store from './store'
import vuetify from './plugins/vuetify';
import Vuelidate from 'vuelidate'

// Firebase libraries
import {auth} from './firebase'

Vue.config.productionTip = false
Vue.use(Vuelidate)

// Singleton variable of vue instance.
let vue = null

/**
 * Every time a user login, logout or reload(F5) this observer it's called.
 * 
 * The recommended way to get the current user is by setting an observer on the Auth object.
 * By using an observer, you ensure that the Auth object isn't in an intermediate state (such as 
 * initialization) when you get the current user.
 * 
 * We can see the current sesson in browser: F12 + application/strorage
 */
auth.onAuthStateChanged(user => {
    console.log('AUTH observer is called in main.js', user)
    if(user) {
        store.dispatch('session/userIsLogged', user.uid)
        .then( () => {
            initVueInstance()
        });
    } else {
      store.dispatch('session/signOut')
      initVueInstance()
    }
});


// We need to do this for reload(F5) behaviour.
function initVueInstance(){
    if (!vue) {
        vue = new Vue({
            router,
            store,
            vuetify,
            Vuelidate,
            render: h => h(App)
          }).$mount('#app')
    }
}

