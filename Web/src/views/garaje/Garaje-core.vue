<template>
    <v-container>
        <v-card :height="listenerHeight">

            <v-row  no-gutters style="height:100%;">

                <v-col cols="12" sm="4">
                    <GarajeList 
                        ref="list"
                        @enableOrganizationForm="isEnableOrganizationForm=true" 
                        @selectOrganization="selectOrganization"
                        @enableRentForm="isEnableRentForm=true"
                        @selectRent="selectRent">
                    </GarajeList>
                </v-col>

                <v-divider vertical></v-divider>
                
                <v-col v-if="!selectedOrganization && !selectedRent">
                    <v-slide-y-transition mode="out-in">
                    <v-container fill-height>
                        <v-row justify="center">
                            <img src="../../assets/illustrations/undraw_Choose_bwbs.svg" width="40%" height="50%" alt="">
                        </v-row>
                    </v-container>      
                    </v-slide-y-transition>              
                </v-col>
                <v-col v-if="selectedOrganization" transition="slide-x-transition">
                    <v-slide-y-transition mode="out-in">
			            <OrganizationInfo :selectedOrganization="selectedOrganization" :key="selectedOrganization.title + selectedOrganization.oid"></OrganizationInfo>                     
		            </v-slide-y-transition>
                </v-col> 
                <v-col v-if="selectedRent">
                    <v-slide-y-transition mode="out-in">
			            <RentInfo :selectedRent="selectedRent"></RentInfo>                
		            </v-slide-y-transition>
                                        
                </v-col> 

            </v-row>

        </v-card>


        <OrganizationForm :enableOrganizationForm="isEnableOrganizationForm" @disableOrganizationForm="disableOrganizationForm"></OrganizationForm>
        <RentForm :enableRentForm="isEnableRentForm" @disableRentForm="isEnableRentForm=false"></RentForm>

    </v-container>
</template>

<script>
    // Vuex
    import { mapMutations } from 'vuex'

    // Child componets
    import GarajeList from './Garaje-list'
    import OrganizationForm from './organization/Organization-form'
    import OrganizationInfo from './organization/Organization-info'
    import RentForm from './rent/Rent-form'
    import RentInfo from './rent/Rent-info'
    

    export default {
        components: {GarajeList, OrganizationForm, OrganizationInfo, RentForm, RentInfo},

        data() {
            return {
                isEnableOrganizationForm: false,
                isEnableRentForm: false,
                selectedOrganization: null,
                selectedRent: null,

            }
        },
        
        computed: {
            listenerHeight(){
                return screen.height*0.77
            }
        },

        created(){
            this.setTopBarName('Organizations')
        },


        methods: {
            ...mapMutations('core', ['setTopBarName']),

            /**
             * Event called by childs.
             */
            selectOrganization(garaje){
                this.selectedRent = null
                this.selectedOrganization = garaje
            },

            /**
             * Event called by childs.
             */
            selectRent(garaje){
                this.selectedOrganization = null
                this.selectedRent = garaje
            },

            /**
             * Event called by childs.
             */
            disableOrganizationForm(requestsSended){
                if (requestsSended) {
                    this.$refs.list.getAllOrganizationsList()
                }
                this.isEnableOrganizationForm = false
            }

        }
    
    }
</script>
