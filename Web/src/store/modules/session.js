// Firebase libraries
import {db, auth} from '@/firebase'
import router from '@/router'

// Models
import personalUser from '../../models/user/personalUser'
import organizationUser from '../../models/user/organizationUser'

export default {
    namespaced: true,
    state: {
        user: null,
        userType: null,
    },
    mutations: {
        /**
         * Update the value of user state.
         * @param {*} state 
         * @param {Object} user can be personalUser or organizationUser
         */
        updateUser(state, user){
            state.user = user
        },

        /**
         * Update the value of user type state.
         * In updateUser I define the type of user because of the user variable already is a 
         * personalUser object or organizationUser object, but in firebase I can't obtain the
         * name of the object.
         * For this reason I have to add this property to know what type of variable I have in firebase.
         * @param {*} state 
         * @param {Object} userType can be personalUser or organizationUser
         */
        updateUserType(state, userType){
            state.userType = userType
        },
        
        
        /**
         * 
         * @param {*} state 
         * @param {Object} payload 
         */
        updateDataUser(state, payload){
            if(state.user){
                state.user.name = payload.name
                state.user.lastName = payload.lastName
                // To complete

            }
        }
    },
    actions: {
        /**
         * Every time a user login or reload the page, this method will be called to update the user state.
         * A user can be personal user or organization user, for this reason we need to know what type
         * of user is logged for create this type of object.
         * @param {*} context 
         * @param {String} authUID uid of the logged user.
         */
        async userIsLogged(context, authUID){
            try{
                // is personal user?
                let doc = await db.collection('users').doc(authUID).get()
                if (doc.exists){
                    let userDoc = doc.data()
                    let personalUserLogged = new personalUser({
                                        nick: userDoc.nick,
                                        name: userDoc.name,
                                        lastName: userDoc.lastName,
                                        country: userDoc.country,
                                    })
                    context.commit('updateUser', personalUserLogged)
                    context.commit('updateUserType', 'personalUser')
                } 
                // is organization user?
                else {
                    let doc = await db.collection('organizations').doc(authUID).get()
                    if (doc.exists){
                        let userDoc = doc.data()
                        let organizationUserLogged = new organizationUser({
                                                            name: userDoc.organizationName,
                                                            parkingSpaces: userDoc.parkingSpaces,
                                                            coordenates: {lat: userDoc.coordenateLAT, lng: userDoc.coordenateLNG},
                        })
                        context.commit('updateUser', organizationUserLogged)
                        context.commit('updateUserType', 'organizationUser')
                        

                    } else {
                        router.push( {name: 'register'})
                    }   
                }
            }catch(error){
                // TODO error
            }
        },

        /**
         * Deleted session in browser and set user estate to null.
         * @param {*} context 
         */
        signOut(context){
            console.log('sign out')
            // Delete session in browser.
            auth.signOut()
            context.commit('updateUser', null)
            context.commit('updateUserType', null)
        }

    }
}
