<template>
    <span>
        <!-- Navigation to all devices except small devices -->
        <v-navigation-drawer 
            v-if="!isSmallDevice"
            v-model="visibleSideBar"
            app dark color="primary" 
            bottom
            :mini-variant.sync="visibleSideBar"
            permanent
            >

            <v-list-item two-line>
                <v-list-item-avatar color="white">
                    <v-img src='../../assets/core/SideBar/logo.jpg' height="34" contain/>
                </v-list-item-avatar>
                <v-list-item-title class="title">
                    SmartGaraje
                </v-list-item-title>
            </v-list-item>

            <v-divider class="mx-3 mb-3" />

            <v-list nav>
                <v-list-item v-for="optionMenu in optionsMenuToShowComputed" 
                            :key="optionMenu.title"
                            active-class="primary white--text"
                            :to="optionMenu.to"
                            @click="triggerClick(optionMenu.action)"
                            >
                    <v-list-item-icon>
                        <v-icon>{{ optionMenu.icono }}</v-icon>
                    </v-list-item-icon>

                    <v-list-item-content>
                        <v-list-item-title>{{ optionMenu.titulo }}</v-list-item-title>
                    </v-list-item-content>           
                
                </v-list-item>
            </v-list>
        </v-navigation-drawer>

        <!-- Navigation to small devices -->
        <v-navigation-drawer 
            v-else
            v-model="visibleSideBar"
            app dark color="primary" 
            bottom
            >

            <v-list-item two-line>
                <v-list-item-avatar color="white">
                    <v-img src='../../assets/core/SideBar/logo.jpg' height="34" contain/>
                </v-list-item-avatar>
                <v-list-item-title class="title">
                    SmartGaraje
                </v-list-item-title>
            </v-list-item>

            <v-divider class="mx-3 mb-3" />

            <v-list nav>
                <v-list-item v-for="optionMenu in optionsMenuToShowComputed" 
                            :key="optionMenu.title"
                            active-class="primary white--text"
                            :to="optionMenu.to"
                            @click="triggerClick(optionMenu.action)"
                            >
                    <v-list-item-icon>
                        <v-icon>{{ optionMenu.icono }}</v-icon>
                    </v-list-item-icon>

                    <v-list-item-content>
                        <v-list-item-title>{{ optionMenu.titulo }}</v-list-item-title>
                    </v-list-item-content>           
                
                </v-list-item>
            </v-list>
        </v-navigation-drawer>        
    </span>
</template>


<script>

    // Vuex
    import { mapMutations } from 'vuex'

    const enabledPersonalUser = 'Personal-User'
    const enabledOrganizationUser = 'Organization-User'
    const enabledBothUser = 'User'
    const disabledUser = 'No-User'


	export default {
		components: {
			
		},
		data(){
			return{
                isSmallDevice: true,
                optionsMenu: [
                    { 
                        titulo: 'Sign In', 
                        icono: 'mdi-arrow-right-bold-box', 
                        to: {name: 'login'},

                        activedUser: disabledUser, 
                        action: 'doNothing',                        
                    },
                    { 
                        titulo: 'Sign Up', 
                        icono: 'mdi-account-plus', 
                        to: {name: 'register'},

                        activedUser: disabledUser, 
                        action: 'doNothing',                        
                    },                    
                    { 
                        titulo: 'Dashboard', 
                        icono: 'mdi-view-dashboard', 
                        to: {name: 'dashboard'},

                        activedUser: enabledBothUser, 
                        action: 'doNothing',                        
                    },
                    { 
                        titulo: 'Vehicules', 
                        icono: 'mdi-car-multiple', 
                        to: {name: 'vehicules'} ,

                        activedUser: enabledPersonalUser,
                        action: 'doNothing',

                    },
                    { 
                        titulo: 'Garages', 
                        icono: 'mdi-home-city', 
                        to: {name: 'garaje'} ,

                        activedUser: enabledPersonalUser,
                        action: 'doNothing',

                    },
                    { 
                        titulo: 'Manage Org.', 
                        icono: 'mdi-account-supervisor', 
                        to: {name: 'ManageCore'} ,

                        activedUser: enabledOrganizationUser,
                        action: 'doNothing',

                    },                                           
                    { 
                        titulo: 'Sign Out', 
                        icono: 'mdi-arrow-left-bold-box', 

                        activedUser: enabledBothUser,
                        action: 'signOut'
                    },                    

                ],
			}
        },

        created () {
            // Add listener to event 'resize'.
            window.addEventListener('resize', this.onResize, { passive: true })
            this.onResize()
        },

        computed: {
            /**
             * Determine the state of visibleSideBar variable. 
             * I need setter because I use it in a v-model.
             */
            visibleSideBar: {
                get() {
                    return this.$store.state.core.visibleSideBar
                },
                set(value){
                    if(this.isSmallDevice){
                        this.setVisibleSideBar(value)
                    }
                }
            },

            /**
			 * Determine the user type and if a user is logged in app.
			 */
			userLogged(){
                let user = this.$store.state.session.user
                let userType = this.$store.state.session.userType
                if(!user){
                    return disabledUser
                }else{
                    if (userType == 'personalUser'){
                        return enabledPersonalUser
                    }
                    return enabledOrganizationUser
                }
            },

            optionsMenuToShowComputed() {
                return this.optionsMenuToShowMethod()
            }
        
        },
        methods: {
            ...mapMutations('core', ['setVisibleSideBar']),

            optionsMenuToShowMethod(){
                let optionsMenuEnabled = []
                for(let optionMenu of this.optionsMenu){
                    if (optionMenu.activedUser == this.userLogged){
                        optionsMenuEnabled.push(optionMenu)
                    }
                    else if (this.userLogged != disabledUser && optionMenu.activedUser == enabledBothUser){
                        optionsMenuEnabled.push(optionMenu)
                    }
                }
                return optionsMenuEnabled
            },

            triggerClick(action){
                this[action]()
            },

            doNothing(){},

            signOut(){
                this.$store.dispatch('session/signOut')
                this.$router.push({name:'login'})
            },

            onResize() {
                this.isSmallDevice = window.innerWidth < 600
            },


        }
	};
</script>
