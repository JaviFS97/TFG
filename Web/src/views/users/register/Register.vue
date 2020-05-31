<template>
    <v-container fill-height>
        <v-row justify="center">
            <v-col xs="10" md="8">
                <v-stepper v-model="view" class="stepper" alt-labels>

                    <v-stepper-header>
                        <v-stepper-step :complete="view > 1" step="1">
                            Select your role.
                        </v-stepper-step>

                        <v-divider></v-divider>

                        <v-stepper-step step="2">
                            Register.
                        </v-stepper-step>
                    </v-stepper-header>
                    
                    <v-stepper-items>
                        <v-stepper-content step="1">
                            <v-row justify="center">
                                <v-card v-if="view == 1" class="form-card mb-4" flat>
                                                    
                                    <v-app-bar color="primary" dark>
                                        <v-row justify="center">
                                            <h1>Select your role.</h1> 
                                        </v-row>
                                    </v-app-bar>                    

                                    <v-card-text>
                                        <v-text-field label="Email"
                                            outlined prepend-inner-icon="mdi-at"
                                            v-model="generalForm.email"
                                            :error-messages="emailError"
                                            @blur="$v.generalForm.email.$touch()">
                                        </v-text-field>
                                        <v-text-field label="Password" 
                                            :type="showPassword ? 'text' : 'password'" 
                                            outlined 
                                            prepend-inner-icon="mdi-textbox-password" 
                                            :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"  
                                            @click:append="showPassword = !showPassword"
                                            v-model="generalForm.password"
                                            :error-messages="passwordError"
                                            @blur="$v.generalForm.password.$touch()"
                                            >
                                        </v-text-field>
                                        <v-text-field label="Repeat password" 
                                            :type="showPassword ? 'text' : 'password'" 
                                            outlined 
                                            prepend-inner-icon="mdi-lock-reset" 
                                            :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"  
                                            @click:append="showPassword = !showPassword"
                                            v-model="generalForm.repeatPassword"
                                            :error-messages="repeatPasswordError"
                                            @blur="$v.generalForm.repeatPassword.$touch()"                                            
                                            >
                                        </v-text-field>
                                    </v-card-text>

                                    <v-card-actions>
                                        <v-row justify="center">
                                            <v-radio-group v-model="generalForm.accountType" row :error-messages="accountTypeError" @blur="$v.generalForm.accountType.$touch()"  >                            
                                                <v-radio label="Personal" value="Personal" color="primary"></v-radio>
                                                <v-radio label="Organization" value="Organization" color="primary"></v-radio>
                                            </v-radio-group>
                                        </v-row>
                                    </v-card-actions>

                                    <v-card-actions>            
                                        <v-row justify="center">
                                            <v-btn :to="{name:'login'}" color="secondary" class="ma-4 form-btn" >
                                                Sign in 
                                            </v-btn>                        
                                            <v-btn @click="nextView()" color="secondary" class="ma-4 form-btn" >
                                                NEXT
                                            </v-btn>      
                                        </v-row>                                    
                                    </v-card-actions>

                                </v-card>
                            </v-row>
                        </v-stepper-content>

                        <v-stepper-content step="2">
                            <RegisterPersonal v-if=" view==2 && generalForm.accountType=='Personal'"
                                @beforeViewChield="beforeView"
                                @registerPersonal="register">
                            </RegisterPersonal>
                            <RegisterOrganization v-if=" view==2 && generalForm.accountType=='Organization'"
                                @beforeViewChield="beforeView"
                                @registerOrganization="register">
                            </RegisterOrganization>
                        </v-stepper-content>
                    </v-stepper-items>

                </v-stepper>
            </v-col>
        </v-row>  
    </v-container>
</template>


<script>
    // Components
    import RegisterPersonal from './RegisterPersonal'
    import RegisterOrganization from './RegisterOrganization'

    // Vuelidate
    import {required, email, minLength, maxLength, sameAs} from 'vuelidate/lib/validators'

    // Models
    import personalUser from '../../../models/user/personalUser'
    import organizationUser from '../../../models/user/organizationUser'

    // Vuex
    import { mapActions, mapMutations } from 'vuex'
        
    export default {
        components: {
            RegisterPersonal, 
            RegisterOrganization
        },
        data() {
            return {
                view: 1,
                showPassword: false,
                showPassword: false,
                generalForm: {
                    email: '',
                    password: '',
                    repeatPassword: '',
                    accountType: '',
                }
            }
        },

        created(){
            this.setTopBarName('Sign Up')
        },

        methods: {
            ...mapMutations('core', ['setTopBarName']),
            ...mapActions('snackbar', ['showNotificationSuccess', 'showNotificationError']),

            /**
             * Event called by childs.
             */
            nextView() {
                if (this.$v.generalForm.$invalid){
                    this.$v.generalForm.$touch()
                }else{
                    this.view++;
                }                
            },

            /**
             * Event called by childs.
             */
            beforeView() {
                this.view--;
            },

            async register(formData){               
                var credentials = null
                // Adding specific data to the appropiate user.
                switch(this.generalForm.accountType ){
                    case 'Personal':
                        var newPersonalUser = new personalUser({
                            email: this.generalForm.email,
                            password: this.generalForm.password,
                            nick: formData.nick,
                            name: formData.name,
                            lastName: formData.lastName,
                            country: formData.country
                        })
                        // Register personal user in Auth Firebase
                        credentials = await newPersonalUser.createUserAuth()

                        // Register personal user in Database Firebase
                        try{
                            await newPersonalUser.newPersonalUserInDatabase(credentials)
                            await newPersonalUser.sendEmailVerification()
                            this.$router.push({name: 'emailVerification'})
                            this.showNotificationSuccess({msg: 'Successful register', timeout:4000, axisY: 'top', axisX: 'center'})
                        }catch(error){
                             this.showNotificationError({msg: 'An error ocurred during register.', timeout:4000, axisY: 'top', axisX: 'center'})
                        }      

                        break

                    case 'Organization':
                        var newOrganizationUser = new organizationUser({
                            email: this.generalForm.email,
                            password: this.generalForm.password,
                            name: formData.name,
                            parkingSpaces: formData.parkingSpaces,
                            coordenates: formData.garajeDoorCoordenates,
                        })
                        // Register organization user in Auth Firebase
                        credentials = await newOrganizationUser.createUserAuth()
                        // Register organization user in Database Firebase
                        try{
                            await newOrganizationUser.newOrganizationUserInDatabase(credentials)
                            await newOrganizationUser.sendEmailVerification()
                            this.$router.push({ name: 'emailVerification'})
                            this.showNotificationSuccess({msg: 'Successful register', timeout:4000, axisY: 'top', axisX: 'center'})                      
                        }catch(error){
                            this.showNotificationError({msg: 'An error ocurred during register.', timeout:4000, axisY: 'top', axisX: 'center'})
                        }
                        
                        break   
                }

            }

        },

        validations: {
            generalForm: {
                email: {
                    required,   
                    email       
                },
                password: {
                    required,
                    minLength: minLength(6),
                    maxLength: maxLength(20)
                },
                repeatPassword: {
                    required,
                    sameAs: sameAs('password')
                },
                accountType: {
                    required,
                }
            },
        },

        computed: {
            /**
             * Validations for generalForm fields 
             */  
            emailError() {
                let error = []
                
                if (!this.$v.generalForm.email.$dirty){ return error }
                else{
                    if (!this.$v.generalForm.email.required){ error.push("Email required.")}
                    if (!this.$v.generalForm.email.email){ error.push("Invalid email.")}
                    return error
                }

            },
            passwordError() {
                let error = []
                if (!this.$v.generalForm.password.$dirty){ return error}
                else{
                    if (!this.$v.generalForm.password.required){ error.push("Password required.")}
                    if (!this.$v.generalForm.password.minLength){ error.push("Min length 6.")}
                    if (!this.$v.generalForm.password.maxLength){ error.push("Max length 20.")}
                    return error
                }

            },
            repeatPasswordError() {
                let error = []
                if (!this.$v.generalForm.password.$dirty){ return error}
                else{
                    if (!this.$v.generalForm.password.required){ error.push("Password required.")}
                    if (!this.$v.generalForm.repeatPassword.sameAs){ error.push("Passwords must match.")}
                    return error                    
                }

            },
            accountTypeError() {
                let error = []
                if (!this.$v.generalForm.accountType.$dirty){ return error}
                else{
                    if (!this.$v.generalForm.accountType.required){ error.push("Account type required.")}
                    return error                    
                }
            }


        },


    }
</script>


<style scoped > 

    .stepper{
        min-height: 700px;
    }


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
