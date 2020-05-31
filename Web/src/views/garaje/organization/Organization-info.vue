v-<template>
    <v-tabs fixed-tabs class="mt-2"> 
        <v-tab>
            <v-icon left>mdi-account</v-icon>
            INFO
        </v-tab>
        <v-tab>
            <v-icon left>mdi-timetable</v-icon>
            RENT YOUR GARAJE
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
                        <li> <b>Name of garaje:</b> {{selectedOrganization.title}} </li>
                        <li> <b>Belongs to</b> {{organization.name}} <b>organization</b> </li>
                        <li> <b>Coordenates: </b> </li>
                    </ul>

                    <MapGaraje :organization="organization"></MapGaraje>

                </v-card-text>
            </v-card>
        </v-tab-item>
        <v-tab-item>
            <OrganizationRent :selectedOrganization="selectedOrganization"></OrganizationRent>
        </v-tab-item>
    </v-tabs>        

</template>


<script>

    // Components
    import MapGaraje from '../../../components/maps/MapGaraje'
    import OrganizationRent from "./Organization-rent"

    // Models
    import OrganizationUser from '../../../models/user/organizationUser'

    export default {
        props: ['selectedOrganization'],  

        components: {MapGaraje, OrganizationRent},

        data() {
            return {
                organization: {},
                isLoading: true,
            }
        },

        async created() {
            await this.getOrganizationInfo()
            this.sleep(2000).then(() => { this.isLoading = false })
            
        },

        methods: {

            async getOrganizationInfo(){
                let instanceOrg = new OrganizationUser({
                    email: undefined,
                    password: undefined,
                    name: undefined,
                    parkingSpaces: undefined,
                    coordenates: undefined,
                })
                await instanceOrg.getOrganizationByOID(this.selectedOrganization.oid).then( orgByOID => {

                    let org = {}
                    org.name = orgByOID.organizationName
                    org.coordenates = [orgByOID.coordenateLNG, orgByOID.coordenateLAT]
                    return org
                }).then( org => {
                    this.organization = org
                    
                })
  
            },      

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