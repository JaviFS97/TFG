v-<template>
    <v-tabs fixed-tabs class="mt-2"> 
        <v-tab>
            <v-icon left>mdi-account</v-icon>
            INFO
        </v-tab>

        <v-tab-item>
            <v-card flat> 
                <v-row v-if='isLoading' justify="center" class="mt-10"> 
                    <v-progress-circular
                        :size="75"
                        color="primary"
                        indeterminate>
                    </v-progress-circular>
                </v-row>    
                <v-card-text v-else>
                    <ul class="mt-5">
                        <li> <b>Name of garaje:</b> {{selectedRent.title}} </li>
                        <li v-if="selectedRent.approvedByOwner"> <b>Approved by owner:</b> <b style="color: green;"> {{selectedRent.approvedByOwner}}</b> </li>
                        <li v-else> <b>Approved by owner:</b> <b style="color: red;"> {{selectedRent.approvedByOwner}}</b> </li>
                        <li> <b>Owner nick:</b> {{user.nick}} </li>
                        <li> <b>Owner name:</b> {{user.name}}, {{user.lastName}} </li>
                        <li> <b>Dates:</b> {{selectedRent.dates}} </li>
                        <li> <b>Time </b> {{selectedRent.startHour}} - {{selectedRent.endHour}}</li>
                        <li> <b>Coordenates: </b> </li>
                    </ul>

                    <MapGaraje :organization="selectedRent"></MapGaraje>

                </v-card-text>
            </v-card>            
        </v-tab-item>



    </v-tabs>        

</template>

<script>
    // Components
    import MapGaraje from '../../../components/maps/MapGaraje'

    // Models
    import PersonalUser from '../../../models/user/personalUser'

    export default {
        props: ['selectedRent'],

        components: {MapGaraje},

        data() {
            return {
                user: {},
                isLoading: true,
            }
        },

        async created() {
            let personalUser = new PersonalUser({
                nick: undefined,
                name: undefined,
                lastName: undefined,
                country: undefined,
            })
            await personalUser.getPersonalUserByUID(this.selectedRent.uidOwner).then (userData => {
                this.user.name = userData.name
                this.user.lastName = userData.lastName
                this.user.nick = userData.nick

            })
            this.sleep(2000).then(() => { this.isLoading = false })
        },

        methods: {
            /** Simulates a response wait from the backend
             * @param {Number} ms time to sleep.
             * @return {Promise}
             */
            sleep(ms) {
                return new Promise(resolve => setTimeout(resolve, ms));
            }  
        }
  
    }
</script>