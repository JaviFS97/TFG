<template>
    <div>

    </div>
</template>

<script>
    // Firebase 
    import { auth } from '@/firebase'

    // Vuex
    import { mapActions } from 'vuex'

    export default {
        data(){
            return {
                oobCode: '',    // A unique code used to identify and verify an application.
            }
        },

        created(){
            // Based on => https://firebase.google.com/docs/auth/custom-email-handler
            this.validate()
        },
        methods: {
            ...mapActions('snackbar', ['showNotificationSuccess', 'showNotificationError']),

            async validate(){

                let mode = this.$route.query.mode
                this.oobCode = this.$route.query.oobCode

                switch(mode){
                    case 'verifyEmail':

                        try{
                            // Validating user.
                            await auth.applyActionCode(this.oobCode)
                            await auth.currentUser.reload()

                            this.showNotificationSuccess({msg: 'Activation successful!!', timeout:4000, axisY: 'top', axisX: 'center'})
                            this.$router.push( {name:'dashboard'} )

                        }catch(error){
                            this.showNotificationError({msg: 'Activation failed!!', timeout:4000, axisY: 'top', axisX: 'center'})
                            this.$router.push( {name:'emailVerification'} )
                        }
                        break

                    case 'resetPassword':                     
                        // TODO
                        // this.$store.commit('mostrarOcupado',{
                        //     titulo: "Comprobando validacion",
                        //     mensaje: "Estamos comprobando los datos para la validacion del codigo de cambio de contraseña..."
                        // })
                        // try{
                        //     this.email = await auth.verifyPasswordResetCode(this.oobCode)
                        //     this.$store.commit('mostrarNotificacionInformacion', "Ingresa una nueva contraseña para " + this.email, 4000)      

                        // }catch(error){
                        //     this.$store.commit('mostrarNotificacionError', "Validación erronea del codigo de cambio de contraseña, intentelo más tarde.", 4000)   
                        // }
                        // this.$store.commit('ocultarOcupado')
                        // break

                }
            },
        }
    
    }
</script>