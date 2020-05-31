<template>
    <div>
        <v-dialog v-model="enableAcceptForm" persistent max-width="900" >
            <v-card >
                <v-card-title class="headline">Add '{{ infoToAcceptForm.userName }}' to your organization</v-card-title>

                <v-card-text>Parking spaces occupied: {{ infoToAcceptForm.numberOccupiedParking }} of {{ infoToAcceptForm.totalParkingSpaces }} </v-card-text>
                <v-card-text>How many parking spaces do you want to associate to '{{ infoToAcceptForm.userName }}' ?</v-card-text>
                <v-slider
                    class="mx-10"
                    min="1"
                    :max="maxNumberOfParkingSpaces()"
                    v-model="parkingSpaces"
                    :thumb-size="24"
                    thumb-label="always"
                ></v-slider>


                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="red darken-1" text @click="disableAcceptForm">Cancel</v-btn>                    
                    <v-btn color="green darken-1" text @click="acceptUser">Finish</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>

        <v-dialog v-model="enableDenyForm" persistent max-width="600" >
            <v-card>
                <v-card-title class="headline">Do you want to DENY user request ?</v-card-title>
                <v-card-text>Press 'NO' to cancel. Press 'YES' to deny user request.</v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="red darken-1" text @click="disableDenyForm">No</v-btn>
                    <v-btn color="green darken-1" text @click="dialog = false">Yes</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
    </div>
    
</template>

<script>

    // Vuex
    import { mapMutations, mapActions} from 'vuex'    

    export default {
        props: ['enableAcceptForm', 'enableDenyForm', 'infoToAcceptForm'],
        data(){
            return {
                parkingSpaces: 0
            }
        },

        computed:{
			/**
			 * Determine if a user is logged in the app.
			 */
			userLogged(){
				return this.$store.state.session.user
            }

        },

        methods: {
            ...mapActions('snackbar', ['showNotificationSuccess', 'showNotificationError']),

            disableAcceptForm(acceptUserStatus){
                this.$emit('disableAcceptForm', acceptUserStatus)
            },

            disableDenyForm(){
                this.$emit('disableDenyForm')
            },

            maxNumberOfParkingSpaces(){
                return this.infoToAcceptForm.totalParkingSpaces - this.infoToAcceptForm.numberOccupiedParking
            },

            async acceptUser(){
                await this.userLogged.acceptUserRequest(this.infoToAcceptForm.uid, this.parkingSpaces).then( () => {
                    this.showNotificationSuccess({msg: 'User added to your organization.', timeout:4000, axisY: 'top', axisX: 'center'}) 
                    this.disableAcceptForm(true)
                }).catch( () => {
                    this.showNotificationError({msg: 'Error during adding user to your organization.', timeout:4000, axisY: 'top', axisX: 'center'}) 
                    this.disableAcceptForm(false)
                })

            }


        }
        
    }
</script>