<template>
    <v-container>
        <v-card :height="listenerHeight">

            <v-tabs fixed-tabs class="mt-2"> 
                <v-tab>
                    <v-icon left>mdi-account</v-icon>
                    USERS REQUEST
                </v-tab>
                <v-tab>
                    <v-icon left>mdi-timetable</v-icon>
                    MANAGE ORGANIZATION
                </v-tab>

                <v-tab-item>
                    <UserRequestList></UserRequestList>
                </v-tab-item>
                
                <v-tab-item>
                    <OrganizationList></OrganizationList>
                </v-tab-item>

            </v-tabs>   

        </v-card>

    </v-container>
</template>

<script>
    // Vuex
    import { mapMutations } from 'vuex'

    // Child components
    import UserRequestList from './usersRequest/UsersRequest-list'
    import OrganizationList from './organization/Organization-list'

    export default {
        components: {UserRequestList, OrganizationList},

        data() {
            return {
            }
        },
        
        computed: {
            listenerHeight(){
                return screen.height*0.77
            }
        },

        created(){
            this.setTopBarName('Manage Organization')
        },


        methods: {
            ...mapMutations('core', ['setTopBarName']),


        }
    
    }
</script>
