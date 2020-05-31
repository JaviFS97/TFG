<template>
    <v-container>
        <v-row justify="center" class="mb-5">
            <h1>Your vehicules</h1>
        </v-row>

        <v-row v-if='loading' justify="center" class="mt-10"> 
            <v-progress-circular
                :size="75"
                color="primary"
                indeterminate>
            </v-progress-circular>
        </v-row>      

        <v-row v-else justify="center">
            <img v-if="listOfVehicules.length == 0" src="../../assets/illustrations/undraw_no_data_qbuo.svg" width="40%" height="50%" alt="">
            
            <!-- <v-col xs="12" sm="6" md="4" v-for="vehicule in vehicules" :key="vehicule.plate"> -->
            <v-col cols="10" sm="6" md="4" lg="3" xl="2" v-for="(vehicule, index) in listOfVehicules" :key="index">
                <VehiculeCard 
                    :vehicule='vehicule'
                    @deleteVehicule='removeVehiculeCard'
                    @modifyVehicule='modifyVehiculeCard'>
                </VehiculeCard>
            </v-col>
        </v-row>
        

        <v-row class="boton-flotante">
            <v-btn 
                @click="enableVehiculeForm"
                class="mx-8 mt-8"  
                fab 
                dark 
                color="primary">
                    <v-icon dark>mdi-plus</v-icon>
            </v-btn>          
        </v-row>
        
        <v-row v-if="visibleVehiculeForm">
            <VehiculeForm 
                :visibleForm='visibleVehiculeForm'
                :vehiculeToModify='vehiculeToModify'
                @saveVehicule='addVehiculeCard'
                @disabledForm='disableVehiculeForm'>
            </VehiculeForm>
        </v-row>

        
    </v-container>
</template>


<script>
    // Vuex
    import { mapMutations } from 'vuex'

    // Child componets
    import VehiculeCard from './Vehicule-card'
    import VehiculeForm from './Vehicule-form'

    export default {
        components: { VehiculeCard, VehiculeForm },

        data: () => ({
           i:0,
           visibleVehiculeForm: false,
           listOfVehicules: [],
           loading: true,
           vehiculeToModify: null
        }),

        computed:{
			/**
			 * Determine if a user is logged in the app.
			 */
			userLogged(){
				return this.$store.state.session.user
            },
            

        },
        
        async created(){
            this.setTopBarName('Vehicules')

            // Getting vehicules from database
            await this.sleep(1000)
            this.listenerVehicules()
        },

        methods: {
            ...mapMutations('core', ['setTopBarName']),

            enableVehiculeForm(){
                this.visibleVehiculeForm = true
            },
            
            /**
             * Event called by childs.
             */
            disableVehiculeForm(){
                this.visibleVehiculeForm = false
                this.vehiculeToModify = null
            },

            /**
             * Event called by childs.
             */
            addVehiculeCard(){
                this.listenerVehicules()
                this.disableVehiculeForm()
            },

            /**
             * Event called by childs.
             */
            removeVehiculeCard(){
                this.listenerVehicules()
            },

            /**
             * Event called by childs.
             */ 
            modifyVehiculeCard(vehicule){
                this.vehiculeToModify = vehicule
                this.enableVehiculeForm()
            },


            /**
             * listens to all the changes that hapen in the user's vehicules database.
             */
            async listenerVehicules(){
                this.loading = true
                this.listOfVehicules = await this.userLogged.listenerVehicules()
                this.loading = false
            },

            /** Simulates a response wait from the backend
             * @param {Number} ms time to sleep.
             * @return {Promise}
             */
            sleep(ms) {
                return new Promise(resolve => setTimeout(resolve, ms));
            }

        },
    }
</script>


<style>
    .boton-flotante {
        position:fixed;
        width:60px;
        height:60px;
        bottom:50px;
        right:60px;
    }
</style>