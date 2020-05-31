<template>
    <v-card class="mx-auto" max-width="344">
        <v-img class="imageBackGround"></v-img>

        <v-card-title>
            <v-container>
                <v-row justify="center">
                    <div> {{vehicule.name}} </div>
                </v-row>
                <v-row justify="center">
                    <span class="grey--text subtitle-1"> {{ vehicule.plate }} </span>
                </v-row>
            </v-container>
        </v-card-title>

        <v-card-actions>
            <v-row justify="center">
                <v-btn icon @click="showExpandCard = !showExpandCard">
                    <v-icon>{{ showExpandCard ? 'mdi-chevron-up' : 'mdi-chevron-down' }}</v-icon>
                </v-btn>
            </v-row>

        </v-card-actions>

        <v-expand-transition>
            <div v-show="showExpandCard">
                <v-divider></v-divider>
                <v-card-text>
                    <v-container>
                        <v-row>
                            Type: {{vehicule.type}}
                        </v-row>
                        <v-row>
                            Brand: {{vehicule.brand}}
                        </v-row>
                        <v-row>
                            Model: {{vehicule.model}}
                        </v-row>
                        <v-row class="mt-5" justify="center">
                            <v-col cols="6" justify="center">
                                <v-row justify="center">
                                    <v-btn color="error" @click="removeVehicule">
                                        Delete
                                    </v-btn>
                                </v-row>
                            </v-col>
                            <v-col cols="6">
                              <v-row justify="center">
                                    <v-btn color="primary" @click="modifyVehicule">
                                        Modify
                                    </v-btn>
                                </v-row>
                            </v-col>

                        </v-row>
                    </v-container>
                </v-card-text>
            </div>
        </v-expand-transition>

    </v-card>
</template>

<script>
    // Vuex
    import { mapActions } from 'vuex'

    export default {
        props: ['vehicule'],

        data: () => ({
            showExpandCard: false,
        }),

        computed:{
			/**
			 * Determine if a user is logged in the app.
			 */
			userLogged(){
				return this.$store.state.session.user
            },

        },
        
        methods: {
            ...mapActions('snackbar', ['showNotificationSuccess', 'showNotificationError']),
            
            removeVehicule() {
                this.userLogged.deleteVehicule(this.vehicule)
                .then(res => {                        
                    this.showNotificationSuccess({msg: 'Vehicule removed!!', timeout:4000, axisY: 'top', axisX: 'center'})    
                    this.$emit('deleteVehicule')                 
                    })
                    .catch(error => {
                        this.showNotificationError({msg: 'An error ocurred during deleting vehicule!!', timeout:4000, axisY: 'top', axisX: 'center'})
                    })
                
            },

            modifyVehicule() {
                this.$emit('modifyVehicule', this.vehicule);   
            }
        }
    }
</script>


<style lang="css">
    .imageBackGround{
        height: 200px;
        width: 344px;
        background: rgba(212,228,239,1);
        background: -moz-linear-gradient(45deg, rgba(212,228,239,1) 5%, rgba(186,210,227,1) 17%, rgba(77,135,177,1) 67%, rgba(57,122,168,1) 76%);
        background: -webkit-gradient(left bottom, right top, color-stop(5%, rgba(212,228,239,1)), color-stop(17%, rgba(186,210,227,1)), color-stop(67%, rgba(77,135,177,1)), color-stop(76%, rgba(57,122,168,1)));
        background: -webkit-linear-gradient(45deg, rgba(212,228,239,1) 5%, rgba(186,210,227,1) 17%, rgba(77,135,177,1) 67%, rgba(57,122,168,1) 76%);
        background: -o-linear-gradient(45deg, rgba(212,228,239,1) 5%, rgba(186,210,227,1) 17%, rgba(77,135,177,1) 67%, rgba(57,122,168,1) 76%);
        background: -ms-linear-gradient(45deg, rgba(212,228,239,1) 5%, rgba(186,210,227,1) 17%, rgba(77,135,177,1) 67%, rgba(57,122,168,1) 76%);
        background: linear-gradient(45deg, rgba(212,228,239,1) 5%, rgba(186,210,227,1) 17%, rgba(77,135,177,1) 67%, rgba(57,122,168,1) 76%);
        filter: progid:DXImageTransform.Microsoft.gradient( startColorstr='#d4e4ef', endColorstr='#397aa8', GradientType=1 );
    }
</style>