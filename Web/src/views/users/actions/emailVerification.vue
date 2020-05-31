<template>
    <v-container fill-height>
        <v-row justify="center">
            <v-col xs="10" md="8">
                <v-card min-width="280" elevation="10">

                    <v-app-bar color="primary" dark>
                        <v-row justify="center">
                            <h1>Confirm your email address.</h1> 
                        </v-row>
                    </v-app-bar>                    

                    <v-card-text>
                        <v-row justify="center">
                            <h3>We send a email to {{user.email}} </h3> 
                        </v-row>

                    </v-card-text>

                    <v-card-actions>   
                        <v-row justify="center">
                            <v-btn @click="resendEmail" color="secondary">Resend Email</v-btn>
                        </v-row>
                    </v-card-actions>   

                </v-card>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>

    // Firebase
    import {auth} from '@/firebase'

    // Vuex
    import { mapMutations, mapActions} from 'vuex'

    export default {
        created(){
            this.setTopBarName('Verificate Email')
        },

        computed:{
			/**
			 * Determine if a user is logged in the app.
			 */
			user(){
				return auth.currentUser
            },

		},

        methods: {
            ...mapMutations('core', ['setTopBarName']),
            ...mapActions('snackbar', ['showNotificationSuccess', 'showNotificationError']),

            async resendEmail(){
                await this.user.sendEmailVerification()
                    .then( () => {
                        this.showNotificationSuccess({msg: 'We send another message to your email.', timeout:4000, axisY: 'top', axisX: 'center'}) 
                    })
                    .catch( () => {
                        this.showNotificationError({msg: 'An error ocurred during sending another message to your email.', timeout:4000, axisY: 'top', axisX: 'center'})
                    })
            },
        }


    }
</script>