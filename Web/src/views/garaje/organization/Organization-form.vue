<template>
    <v-row justify="center">
        <v-dialog v-model="enableOrganizationForm" persistent max-width="900" >

        <v-card height="700">
            <v-container>
                <v-row justify="center">
                    <v-card-title class="headline">ADD ORGANIZATION</v-card-title>
                </v-row>

                <v-row>

                    <v-tabs fixed-tabs class="mt-2"> 
                        <v-tab>
                            <v-icon left>mdi-format-list-bulleted</v-icon>
                            LIST
                        </v-tab>
                        <v-tab>
                            <v-icon left>mdi-map-search</v-icon>
                            MAP
                        </v-tab>
   
                        <v-tab-item>
                            <v-container> 
                                <v-card flat>
                                    <v-card-title>
                                        List of Organizations
                                        <v-spacer></v-spacer>
                                        <v-text-field
                                            v-model="search"
                                            append-icon="mdi-magnify"
                                            label="Search"
                                            single-line
                                            hide-details
                                        ></v-text-field>                                    
                                    </v-card-title>

                                    <v-data-table
                                        :loading="loadingListOrganizations" loading-text="Loading... Please wait"
                                        :headers="headers"
                                        :items="organizations"
                                        :search="search">                                            
                                            <template v-slot:item.action="{ item }">
                                                <v-icon v-if="!item.status" @click="followOrganization(item)"> mdi-plus-circle-outline </v-icon>
                                                <v-icon v-else class="ml-12" @click="unfollowOrganization(item)"> mdi-minus-circle-outline </v-icon>
                                            </template>
                                    </v-data-table>

                                    <v-card-actions>
                                        <v-row justify="center">                        
                                            <v-btn color="red darken-1" text @click="disableOrganizationForm">Cancel</v-btn>
                                            <v-btn color="green darken-1" text @click="confirmOrganizationForm">Confirm</v-btn>
                                        </v-row>
                                        
                                    </v-card-actions>

                                </v-card>
                            </v-container>


                        </v-tab-item>
                        <v-tab-item>
                            <v-container>
                                <v-row justify="center">
                                    <v-col cols="10">
                                        <MapGarajes :organizations="organizations" @followOIDFromMap="followOIDFromMap" @closeForm="disableOrganizationForm"></MapGarajes>
                                    </v-col>
                                </v-row>
                            </v-container>
    
                        </v-tab-item>
 
                    </v-tabs>
                </v-row>

            </v-container>
                   
        </v-card>
        </v-dialog>
    </v-row>
</template>

<script>

    // Models
    import organizationUserList from '../../../models/userList/organizationUserList'

    // Components
    import MapGarajes from '../../../components/maps/MapGarajes'

    // Vuex
    import { mapMutations, mapActions } from 'vuex'    

    export default {
        props: ['enableOrganizationForm'],

        components: {MapGarajes},

        data () {
            return {
                loadingListOrganizations: true,
                search: '',
                headers: [
                    {
                        text: 'Name',
                        align: 'left',
                        value: 'name',
                    },
                    {   
                        text: 'Free spaces', 
                        value: 'freeSpaces',
                        align: 'center',
                    },
                    {   text: 'Actions',
                        value: 'action',
                        sortable: false,
                        align: 'center',
                    },
                ],
                organizations: [
            //         {
            //             name: 'Frozen Yogurt',
            //             freeSpaces: 159,
            //             status: false
            //         },
            //         {
            //             name: 'Ice cream sandwich',
            //             freeSpaces: 232,
            //             status: false                        
            //         },
            //         {
            //             name: 'Eclair',
            //             freeSpaces: 500,
            //             status: false                        
            //         },
                ],
            }
        },

        created() {
            this.getAllOrganizationsList()
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

            disableOrganizationForm() {
                this.$emit('disableOrganizationForm')
            },

            async confirmOrganizationForm(){
                const listOrganizationsToRequest = []
                for (const org of this.organizations){
                    if (org.status){
                        listOrganizationsToRequest.push(org)
                    }
                }
                await this.userLogged.requestInvitation(listOrganizationsToRequest).then( () => {
                    this.showNotificationSuccess({msg: 'The requests were sent.', timeout:4000, axisY: 'top', axisX: 'center'}) 
                    this.$emit('disableOrganizationForm', true)
                }).catch( () => {
                    this.showNotificationError({msg: 'An error ocurred during sending requests.', timeout:4000, axisY: 'top', axisX: 'center'})
                    this.$emit('disableOrganizationForm', false)
                })
                
            },

            followOrganization(item) {
                let itemIndex = this.organizations.indexOf(item)
                console.log(itemIndex)
                this.organizations[itemIndex].status = true
            },

            unfollowOrganization(item) {
                let itemIndex = this.organizations.indexOf(item)
                console.log(itemIndex)
                this.organizations[itemIndex].status = false
            },

            async getAllOrganizationsList(){
                const organizationList = new organizationUserList()
                const orgList = await organizationList.getOrganizationList()
                const userOrganizations = await this.userLogged.getOrganizations()
                this.loadingListOrganizations = true
                await this.sleep(1500)

                let userOrganizationsOID = []
                for (const org of userOrganizations){
                    userOrganizationsOID.push(org.oid)
                }

                for (const org of orgList){
                    if (!userOrganizationsOID.includes(org.oid)){
                        this.organizations.push({oid: org.oid, name: org.name, status: false})
                    }
                }      

                this.loadingListOrganizations = false
            },

            followOIDFromMap(oidList){
                for (const oid of oidList){
                    for (const organization of this.organizations){
                        if (organization.oid == oid) {
                            organization.status = true
                            break
                        }
                    }
                }
                this.confirmOrganizationForm()
                
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