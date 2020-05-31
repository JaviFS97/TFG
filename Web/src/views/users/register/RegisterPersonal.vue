<template>
    <v-row justify="center">
        <v-card class="form-card" flat>
                            
            <v-app-bar color="primary" dark>
                <v-row justify="center">
                    <h1>Personal info</h1> 
                </v-row>
            </v-app-bar>                    

            <v-card-text>
                <v-text-field label="Nick" 
                    outlined prepend-inner-icon="mdi-pound"
                    v-model="personalForm.nick"
                    :error-messages="nickError"
                    @blur="$v.personalForm.nick.$touch()">
                </v-text-field>
                <v-text-field label="Name" 
                    outlined prepend-inner-icon="mdi-format-text"
                    v-model="personalForm.name"
                    :error-messages="nameError"
                    @blur="$v.personalForm.name.$touch()">
                </v-text-field>
                <v-text-field label="Last Name" 
                    outlined prepend-inner-icon="mdi-format-text"
                    v-model="personalForm.lastName"
                    :error-messages="lastNameError"
                    @blur="$v.personalForm.lastName.$touch()">
                </v-text-field>
                <v-select label="Country" 
                    :items="countriesNames" 
                    @change="countrySelected"
                    prepend-inner-icon="mdi-map-marker-outline" 
                    dense 
                    outlined
                    v-model="personalForm.country"
                    :error-messages="countryError"
                    @blur="$v.personalForm.country.$touch()"                    
                    >
                </v-select>

            </v-card-text>

            <v-card-actions>            
                <v-row justify="center">
                    <v-btn @click="beforeView()" color="secondary" class="ma-4 form-btn" >
                        BEFORE 
                    </v-btn>                        
                    <v-btn @click="registerPersonalUser()" color="secondary" class="ma-4 form-btn" >
                        Register
                    </v-btn>      
                </v-row>                                    
            </v-card-actions>

        </v-card>
    </v-row>
  
</template>


<script>
    // Data
    import countries from '../../../data/countries.js'

    // Vuelidate
    import {required, maxLength} from 'vuelidate/lib/validators'

    // Personalized validator that check spaces and accents.
    const accentAndSpacesValidator = (value) => /^(?! )(?!.* {2})[a-zA-ZáéíóúÁÉÍÓÚüÜñÑ ]+$/.test(value)    

    export default {

        data() {
            return {
                countriesNames: [],
                personalForm: {
                    nick: '',
                    name: '',
                    lastName: '',
                    country: '',
                },
            }
        },

        created() {
            for (let country of countries){
                this.countriesNames.push( country.name );
            }
        },

        methods: {
            countrySelected(country){
                this.country = country.name

            },

            /**
             * Throw events to parents.
             */
            registerPersonalUser() {
                if (this.$v.personalForm.$invalid){
                    this.$v.personalForm.$touch()
                }else {
                    this.$emit('registerPersonal', this.personalForm);
                }                
            },            
            beforeView() {
                this.$emit('beforeViewChield');
            },

        },
        
        validations: {
            personalForm: {
                nick: {
                    required,      
                    maxLength: maxLength(20)    
                },
                name: {
                    required,
                    accentAndSpacesValidator,
                    maxLength: maxLength(20)
                },
                lastName: {
                    required,
                    accentAndSpacesValidator,
                    maxLength: maxLength(30)
                },
                country: {
                    required,
                }
            },
        },

        computed: {
            /**
             * Validations for personalForm fields 
             */  
            nickError() {
                let error = []
                if (!this.$v.personalForm.nick.$dirty){ return error}
                else {
                    if (!this.$v.personalForm.nick.required){ error.push("Nick required.")}
                    if (!this.$v.personalForm.nick.maxLength){ error.push("Max length 20.")}
                    return error
                }
            },
            nameError() {
                let error = []
                if (!this.$v.personalForm.name.$dirty){ return error}
                else {
                    if (!this.$v.personalForm.name.required){ error.push("Name required.")}
                    if (!this.$v.personalForm.name.maxLength){ error.push("Max length 20.")}
                    if (!this.$v.personalForm.name.accentAndSpacesValidator){ error.push("Alphabet characters only.")}
                    return error
                }
            },
            lastNameError() {
                let error = []
                if (!this.$v.personalForm.lastName.$dirty){ return error}
                else {
                    if (!this.$v.personalForm.lastName.required){ error.push("Last name required.")}
                    if (!this.$v.personalForm.lastName.maxLength){ error.push("Max length 20.")}
                    if (!this.$v.personalForm.lastName.accentAndSpacesValidator){ error.push("Alphabet characters only.")}
                    return error
                }
            },    
            countryError() {
                let error = []
                if (!this.$v.personalForm.country.$dirty){ return error}
                else {
                    if (!this.$v.personalForm.country.required){ error.push("Country required.")}

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
    }
</style>
