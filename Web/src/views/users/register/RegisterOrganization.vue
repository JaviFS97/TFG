<template>
    <v-row justify="center">
        <v-card class="form-card" flat>
                            
            <v-app-bar color="primary" dark>
                <v-row justify="center">
                    <h1>Org. info</h1> 
                </v-row>
            </v-app-bar>                    

            <v-card-text>
                <v-text-field label="Organization name" 
                    outlined
                    prepend-inner-icon="mdi-format-text"
                    v-model="organizationForm.name"
                    :error-messages="nameError"
                    @blur="$v.organizationForm.name.$touch()">
                </v-text-field>
                <v-text-field label="Parking spaces" 
                    outlined 
                    prepend-inner-icon="mdi-boom-gate-up"
                    v-model="organizationForm.parkingSpaces"
                    :error-messages="parkingSpacesError"
                    @blur="$v.organizationForm.parkingSpaces.$touch()">
                </v-text-field>
                <Map @updatedMarkerFromMap="updatedMarker"></Map>     
            </v-card-text>          

            <v-card-actions id="v-card-actions">            
                <v-row justify="center">
                    <v-btn @click="beforeView()" color="secondary" class="ma-4 form-btn" >
                        BEFORE 
                    </v-btn>                        
                    <v-btn @click="registerOrganizationUser()" color="secondary" class="ma-4 form-btn" >
                        Register
                    </v-btn>      
                </v-row>                                    
            </v-card-actions>

        </v-card>
    </v-row>
  
</template>


<script>
/* eslint-disable */ 
    import {required, maxLength, numeric} from 'vuelidate/lib/validators'
    // Personalized validator that check spaces and accents.
    const accentAndSpacesValidator = (value) => /^(?! )(?!.* {2})[a-zA-ZáéíóúÁÉÍÓÚüÜñÑ ]+$/.test(value)    

    import Map from '../../../components/maps/MapRegister'

    export default {
        components: {
            Map
        },

        data() {
            return {
                organizationForm: {
                    name: '',
                    parkingSpaces: '',
                    garajeDoorCoordenates: '',
                },
            }
        },

        methods: {
            /**
             * Throw events to parents.
             */
            beforeView() {                
                this.$emit('beforeViewChield');
            },
            registerOrganizationUser() {
                if (this.$v.organizationForm.$invalid){
                    this.$v.organizationForm.$touch()
                }else {
                    this.$emit('registerOrganization', this.organizationForm);
                }   
            },

            /**
             * Events of childs.
             */
            updatedMarker(garajeDoor) {
                this.organizationForm.garajeDoorCoordenates = garajeDoor._lngLat
            }
        },

        validations: {
            organizationForm: {
                name: {
                    required,
                    accentAndSpacesValidator,
                    maxLength: maxLength(30)
                },
                parkingSpaces: {
                    required,
                    numeric
                },
            },
        },

        computed: {
            /**
             * Validations for organizationForm fields 
             */  
            nameError() {
                let error = []
                if (!this.$v.organizationForm.name.$dirty){ return error}
                else {
                    if (!this.$v.organizationForm.name.required){ error.push("Name required.")}
                    if (!this.$v.organizationForm.name.maxLength){ error.push("Max length 30.")}
                    if (!this.$v.organizationForm.name.accentAndSpacesValidator){ error.push("Alphabet characters only.")}
                    return error
                }
            },      
            parkingSpacesError() {
                let error = []
                if (!this.$v.organizationForm.parkingSpaces.$dirty){ return error}
                else {
                    if (!this.$v.organizationForm.parkingSpaces.required){ error.push("Parking spaces required.")}
                    if (!this.$v.organizationForm.parkingSpaces.numeric){ error.push("Numbers only")}
                    return error
                }
            },           
        }



    }
</script>


<style>
    .form-btn{
        width: 25%;
        max-width: 150px;
        min-width: 75px;
    }

    .form-card{
        width: 80%;
        min-width: 250px;
        height: 80%;
        min-height: 600px;
    }

    #v-card-actions{
        margin-top: 350px;
    }
</style>
