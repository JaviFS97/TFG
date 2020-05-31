<template>

    <v-dialog 
        v-model="visibleForm" 
        persistent 
        max-width="600">
            <v-card>
                <v-container>

                    <v-row justify="center">
                        <v-card-title v-if="modifyingVehicule" class="headline">
                            Modify vehicule.
                        </v-card-title>
                        <v-card-title v-else class="headline">
                            Add vehicule.
                        </v-card-title>
                    </v-row>

                    <v-row justify="center">
                        <v-card-text>
                            <v-container>

                                <v-row>
                                    <v-col xs="12" >
                                        <v-text-field
                                            v-model="vehiculeForm.plate"
                                            :disabled="modifyingVehicule"
                                            label="License Plate"
                                            prepend-inner-icon="mdi-boom-gate-up"
                                            outlined>
                                        </v-text-field>
                                    </v-col>
                                    <v-col cols="6">
                                        <v-text-field
                                            v-model="vehiculeForm.name"
                                            label="Vehicule Name"
                                            prepend-inner-icon="mdi-format-text"
                                            outlined>
                                        </v-text-field>
                                    </v-col>
                                </v-row>

                                <!-- Type -->
                                <v-row>
                                    <v-col cols="4">
                                        <v-select
                                            v-model="vehiculeForm.type"
                                            label="Type"
                                            :items="typesVehicules" 
                                            dense 
                                            outlined
                                            prepend-inner-icon="mdi-train-car">
                                        </v-select>
                                    </v-col>
                                    <v-col cols="4">
                                        <v-text-field
                                            v-model="vehiculeForm.brand"
                                            label="Brand"
                                            prepend-inner-icon="mdi-car-multiple"
                                            outlined>
                                        </v-text-field>
                                    </v-col>
                                    <v-col cols="4">
                                        <v-text-field
                                            v-model="vehiculeForm.model"
                                            label="Model"
                                            prepend-inner-icon="mdi-engine"
                                            outlined>
                                        </v-text-field>
                                    </v-col>                                                                        
                                </v-row>

                                <!-- Dimensions -->
                                <v-row>
                                    <v-col cols="4">
                                        <v-text-field
                                            v-model="vehiculeForm.height"
                                            label="Height"
                                            prepend-inner-icon="mdi-arrow-collapse-vertical"
                                            outlined>
                                        </v-text-field>
                                    </v-col>
                                    <v-col cols="4">
                                        <v-text-field
                                            v-model="vehiculeForm.width"
                                            label="Width"
                                            prepend-inner-icon="mdi-arrow-collapse-horizontal"
                                            outlined>
                                        </v-text-field>
                                    </v-col>
                                    <v-col cols="4">
                                        <v-text-field
                                            v-model="vehiculeForm.depth"
                                            label="Depth"
                                            prepend-inner-icon="mdi-arrow-collapse-all"
                                            outlined>
                                        </v-text-field>
                                    </v-col>                                                                        
                                </v-row>                            
                            </v-container>
                        </v-card-text>
                    </v-row>

                    <v-row justify="center">
                        <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn color="red darken-1" text @click="disabledForm">Close</v-btn>
                        <v-btn v-if="modifyingVehicule" color="blue darken-1" text @click="saveVehicule">Modify</v-btn>
                        <v-btn v-else color="blue darken-1" text @click="saveVehicule">Save</v-btn>
                        </v-card-actions>
                    </v-row>
                </v-container>
                
            </v-card>

    </v-dialog>
  
</template>

<script>
    // Models
    import Vehicule from '../../models/vehicule/vehicule'

    // Data
    import types from '../../data/vehicules/types'

    // Vuex
    import { mapActions } from 'vuex'

    export default {
        props: ['visibleForm', 'vehiculeToModify'],

        data() {
            return {
                typesVehicules: [],
                modifyingVehicule: false,
                vehiculeForm: {
                    plate: '',
                    name: '',
                    type: '',
                    brand: '',
                    model: '',
                    height: '',
                    width: '',
                    depth: '',
                }
            }
        },

        created() {
            for (let type of types){
                this.typesVehicules.push( type.name );
            }

            console.log(this.vehiculeToModify)
            if (this.vehiculeToModify){
                this.vehiculeForm.plate =  this.vehiculeToModify.plate
                this.vehiculeForm.name =  this.vehiculeToModify.name
                this.vehiculeForm.type =  this.vehiculeToModify.type
                this.vehiculeForm.brand =  this.vehiculeToModify.brand
                this.vehiculeForm.model =  this.vehiculeToModify.model
                this.vehiculeForm.height =  this.vehiculeToModify.height
                this.vehiculeForm.width =  this.vehiculeToModify.width
                this.vehiculeForm.depth =  this.vehiculeToModify.depth

                this.modifyingVehicule = true
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
            /**
             * Throw events to parents.
             */
            disabledForm(){
                this.$emit('disabledForm');
            },

            /**
             * Throw events to parents.
             */
            async saveVehicule(){
                console.log('save')

                let vehicule = new Vehicule(this.vehiculeForm.plate,
                                            this.vehiculeForm.name,
                                            this.vehiculeForm.type,
                                            this.vehiculeForm.brand,
                                            this.vehiculeForm.model,
                                            this.vehiculeForm.height,
                                            this.vehiculeForm.width,
                                            this.vehiculeForm.depth)

                await this.userLogged.saveVehicule(vehicule)
                    .then(res => {
                        if (this.vehiculeToModify){
                            this.showNotificationSuccess({msg: 'Vehicule modified', timeout:4000, axisY: 'top', axisX: 'center'})    
                        }else{
                            this.showNotificationSuccess({msg: 'Vehicule added', timeout:4000, axisY: 'top', axisX: 'center'})
                        }
                        
                        this.$emit('saveVehicule', vehicule);                        
                    })
                    .catch(error => {
                        this.showNotificationError({msg: 'Vehicule plate already exists', timeout:4000, axisY: 'top', axisX: 'center'})
                    })
            },

            
        }

        
    }
</script>