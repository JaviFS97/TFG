<template>
    <v-container fill-height>
        <v-row justify="center">
            <v-col xs="10" md="8">
                <v-card elevation="10">                                    
                    <v-app-bar color="primary" dark>
                        <v-row justify="center">
                            <h1>Login</h1> 
                        </v-row>
                    </v-app-bar>                    

                    <v-card-text>
                        <v-text-field label="Email"
                            outlined prepend-inner-icon="mdi-at"
                            v-model="loginForm.email"
                            :error-messages="emailError"
                            @blur="$v.loginForm.email.$touch()">
                        </v-text-field>
                        <v-text-field label="Password" 
                            :type="showPassword ? 'text' : 'password'" 
                            outlined 
                            prepend-inner-icon="mdi-textbox-password" 
                            :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"  
                            @click:append="showPassword = !showPassword"
                            v-model="loginForm.password"
                            :error-messages="passwordError"
                            @blur="$v.loginForm.password.$touch()">
                        </v-text-field>
                    </v-card-text>

                    <v-card-actions>            
                        <v-row justify="center">
                            <v-btn :to="{name:'register'}" color="secondary" class="ma-4 form-btn" >
                                Sign up
                            </v-btn>                        
                            <v-btn @click="login()" :loading="loginButtonLoading"  color="secondary" class="ma-4 form-btn" >
                                Login
                            </v-btn>      
                        </v-row>                                    
                    </v-card-actions>
                </v-card>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
    // Vuelidate
    import {required, email} from 'vuelidate/lib/validators'

    // Models
    import User from '../../models/user/user'

    // Vuex
    import { mapActions, mapMutations } from 'vuex'

    export default {
        data(){
            return {
                showPassword: false,
                loginButtonLoading: false,
                loginForm: {
                    email: '',
                    password: ''
                }
            }
        },

        created(){
            this.setTopBarName('Sign In')
        },


        methods: {
            ...mapMutations('core', ['setTopBarName']),
            ...mapActions('snackbar', ['showNotificationSuccess', 'showNotificationError']),
            /**
             * Check the validity of the form and log in the user.
             */
            async login() {
                if (this.$v.loginForm.$invalid){
                    this.$v.loginForm.$touch()
                }else{
                    this.loginButtonLoading = true
                    await this.sleep(1000)
                    var user = new User(this.loginForm.email, this.loginForm.password)
                    await user.login()
                    .then(credentials => {
                        this.loginButtonLoading = false
                        this.$router.push({ name: 'dashboard' })  
                        this.showNotificationSuccess({msg: 'Successful login', timeout:4000, axisY: 'top', axisX: 'center'})
                    })
                    .catch(credentials => {
                        this.loginButtonLoading = false
                        switch(credentials.code){
                            case 'auth/invalid-email':
                            case 'auth/user-not-found':
                            case 'auth/wrong-password':
                                this.showNotificationError({msg: 'Password or user invalid', timeout:4000, axisY: 'top', axisX: 'center'})
                                break
                        }
                    })
                }     
            },
            /** Simulates a response wait from the backend
             * @param {Number} ms time to sleep.
             * @return {Promise}
             */
            sleep(ms) {
                return new Promise(resolve => setTimeout(resolve, ms));
            }
        },


        validations: {
            loginForm: {
                email: {
                    required,   
                    email       
                },
                password: {
                    required,
                }
            },
        },

        computed: {
            /**
             * Validations for loginForm fields 
             */  
            emailError() {
                let error = []
                
                if (!this.$v.loginForm.email.$dirty){ return error }
                else{
                    if (!this.$v.loginForm.email.required){ error.push("Email required.")}
                    if (!this.$v.loginForm.email.email){ error.push("Invalid email.")}
                    return error
                }

            },
            passwordError() {
                let error = []
                if (!this.$v.loginForm.password.$dirty){ return error}
                else{
                    if (!this.$v.loginForm.password.required){ error.push("Password required.")}
                    return error
                }

            },


        },        

    }
</script>