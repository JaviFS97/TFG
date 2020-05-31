<template>
    <v-container> 
        <v-card flat>
            <v-card-title>
                User list containing your organization
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
                :loading="loadingMemberList" loading-text="Loading... Please wait"
                :headers="headers"
                :items="usersList"
                :search="search">                                            
                    <template v-slot:item.action="{ item }">
                        <v-btn color="red darken-1" text @click="denyRequest(item)"><v-icon>mdi-delete</v-icon></v-btn>                        
                        <v-btn color="grey darken-1" text @click="confirmRequest(item)"> <v-icon>mdi-pencil</v-icon> </v-btn>
                    </template>
            </v-data-table>
        </v-card>

        <!-- <UsersRequestForm 
            :enableAcceptForm="isEnableAcceptForm" 
            @disableAcceptForm="disableAcceptForm"
            :enableDenyForm="isEnableDenyForm" 
            @disableDenyForm="isEnableDenyForm=false"
            :infoToAcceptForm="infoToAcceptForm">
        </UsersRequestForm> -->
    </v-container>
</template>


<script>

    // Models
    import PersonalUser from '../../../models/user/personalUser'

    export default {
        data () {
            return {
                isEnableAcceptForm: false,
                isEnableDenyForm: false,
                infoToAcceptForm: {},
                loadingMemberList: true,
                search: '',
                headers: [
                    {
                        text: 'Name',
                        align: 'left',
                        value: 'name',
                    },
                    {
                        text: 'ParkingSpaces',
                        align: 'left',
                        value: 'parkingSpaces',
                    },
                    {   text: 'Actions',
                        value: 'action',
                        sortable: false,
                        align: 'center',
                    },
                ],
                usersList: [
                    // {
                    //     name: 'Frozen Yogurt',
                    // },
                    // {
                    //     name: 'Pepe',
                    // },
                ],
            }
        },

        created() {
            this.getMemberList()
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
            async getMemberList(){
                this.usersList = []
                this.loadingMemberList = true
                await this.sleep(1500) 
                await this.userLogged.getMembers().then( usersList => {
                    for (const user of usersList){
                        let personalUser = new PersonalUser({
                            nick: undefined,
                            name: undefined,
                            lastName: undefined,
                            country: undefined,
                        })
                        personalUser.getPersonalUserByUID(user.uid).then( userInfo => {
                            this.usersList.push({name: userInfo.name, uid: user.uid, parkingSpaces: user.parkingSpaces})
                        })
                    }
                })
                this.loadingMemberList = false
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