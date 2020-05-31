<template>
    <div>
        <v-snackbar 
            v-model="snackbarProperties.visible" 
            :color="snackbarProperties.color" 
            :timeout="snackbarProperties.timeout" 
            :top=" positionAxisY('top') "
            :bottom=" positionAxisY('bottom') "
            :left=" positionAxisX('left') "
            :center=" positionAxisX('center') "
            :right=" positionAxisX('right') "
            >
                {{snackbarProperties.msg}}            
            <v-btn dark text @click="closeNotification">
                Close
            </v-btn>
        </v-snackbar>
    </div>
</template>

<script>
    // Vuex
    import { mapMutations } from 'vuex'

    export default {
        computed: {
            snackbarProperties(){
                return this.$store.state.snackbar.snackbarProperties
            }
        },

        methods: {
            ...mapMutations('snackbar', ['hideNotification']),

            closeNotification(){
                this.hideNotification()
            },

            positionAxisY(position){
                return position == this.snackbarProperties.axisY
            },

            positionAxisX(position){
                return position == this.snackbarProperties.axisX
            },

        }
        
    }
</script>