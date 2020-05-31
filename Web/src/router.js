import Vue from 'vue'
import Router from 'vue-router'

// Firebase
import {auth} from '@/firebase'

// Vuex
import store from '@/store'

// Views.
import VehiculeCore from './views/vehicule/Vehicule-core.vue'
import Dashboard from './views/dashboard/Dashboard.vue'
import Register from './views/users/register/Register.vue'
import Login from './views/users/Login.vue'
import emailVerification from './views/users/actions/emailVerification.vue'
import actionController from './views/users/actions/actionController.vue'
import GarajeCore from './views/garaje/Garaje-core.vue'
import ManageCore from './views/manageGaraje/Manage-core.vue'

Vue.use(Router)

const router = new Router({
    mode: 'history',
    base: process.env.BASE_URL,
    routes: [
        {
            path: '/',
            meta: {
                userRedirection: true,
            }
        },
        {
            path: '/register',
            name: 'register',
            component: Register,
        },               
        {
            path: '/login',
            name: 'login',
            component: Login
        },
        {
            path: '/actionController',
            name: 'actionController',
            component: actionController
        },
        {
            path: '/emailVerification',
            name: 'emailVerification',
            component: emailVerification
        },
        {
            path: '/dashboard',
            name: 'dashboard',
            component: Dashboard,
            meta: {
                userIsAuthenticated: true,
            }
        },
        {
            path: '/vehicules',
            name: 'vehicules',
            component: VehiculeCore,
            meta: {
                userIsAuthenticated: true,
                isPersonalUser: true
            }
        },
        {
            path: '/garaje',
            name: 'garaje',
            component: GarajeCore,
            meta: {
                userIsAuthenticated: true,
                isPersonalUser: true
            }
        },
        {
            path: '/ManageOrganization',
            name: 'ManageCore',
            component: ManageCore,
            meta: {
                userIsAuthenticated: true,
                isOrganizationUser: true
            }
        },        
    ]
})



/** Navigation guards => are primarily used to guard navigations either by redirecting it or canceling it. */

router.beforeEach((to, from, next) => {    
    /**
     * userIsAuthenticated guard. 
     * The urls, that have this guard, will check if the user is logged in app to access the url.
     */
    if(to.matched.some( record => record.meta.userIsAuthenticated)){
        let user = auth.currentUser
        
        if(user){
            // If user has not email verified.
            if(user.providerData[0].providerId == 'password' && !user.emailVerified){
                next( {name:'emailVerification'})
            }
            else{
                next()
            }    
        }else{
            next({name:'login'})
        }

    }
    /**
     * userRedirection guard.
     * Check if a user is login or not to redirect them from '/' to the correct view.
     */
    else if(to.matched.some( record => record.meta.userRedirection)){
        let user = auth.currentUser
        if(user){
            next({name:'dashboard'})
        }else{
            next({name:'login'})
        }

    } else{
        next()
    }

    /**
     * isPersonalUser guard.
     * To protect routes of personalUser
     */
    if(to.matched.some( record => record.meta.isPersonalUser)){
        if(store.state.session.userType == 'personalUser'){
            next()
        }else{
            next({name:'dashboard'})
        }
    }

    /**
     * isOrganizationUser guard.
     * To protect routes of organizationUser
     */
    else if(to.matched.some( record => record.meta.isOrganizationUser)){
        if(store.state.session.userType == 'organizationUser'){
            next()
        }else{
            next({name:'dashboard'})
        }
    }

  })


export default router