<template>
    <v-container> 
        <v-card flat>
            <v-card-title>
                List of user's request
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
                :loading="loadingListRequest" loading-text="Loading... Please wait"
                :headers="headers"
                :items="usersRequest"
                :search="search">                                            
                    <template v-slot:item.action="{ item }">
                        <v-btn color="red darken-1" text @click="denyRequest(item)">DENY</v-btn>                        
                        <v-btn color="green darken-1" text @click="confirmRequest(item)">ACCEPT</v-btn>
                    </template>
            </v-data-table>
        </v-card>

        <UsersRequestForm 
            :enableAcceptForm="isEnableAcceptForm" 
            @disableAcceptForm="disableAcceptForm"
            :enableDenyForm="isEnableDenyForm" 
            @disableDenyForm="isEnableDenyForm=false"
            :infoToAcceptForm="infoToAcceptForm">
        </UsersRequestForm>
    </v-container>
</template>

<script>

    // Models
    import PersonalUser from '../../../models/user/personalUser'

    // Child components
    import UsersRequestForm from './UsersRequest-form'

    export default {
        components: {UsersRequestForm},
        data () {
            return {
                isEnableAcceptForm: false,
                isEnableDenyForm: false,
                infoToAcceptForm: {},
                loadingListRequest: true,
                search: '',
                headers: [
                    {
                        text: 'Name',
                        align: 'left',
                        value: 'name',
                    },
                    {   text: 'Actions',
                        value: 'action',
                        sortable: false,
                        align: 'center',
                    },
                ],
                usersRequest: [
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
            this.getRequestList()
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

            async confirmRequest(item) {
                let itemIndex = this.usersRequest.indexOf(item)
                console.log(itemIndex, this.usersRequest[itemIndex].name)

                const userName = this.usersRequest[itemIndex].name
                const uid = this.usersRequest[itemIndex].uid
                const numberOccupiedParking = await this.userLogged.getNumberOfOccupiedParkingSpaces()
                const totalParkingSpaces = this.userLogged.parkingSpaces

                this.infoToAcceptForm = { userName: userName, uid: uid, numberOccupiedParking: numberOccupiedParking, totalParkingSpaces: Number(totalParkingSpaces)}
                console.log(this.infoToAcceptForm)
                this.isEnableAcceptForm = true
                //this.usersRequest[itemIndex].status = true
            },

            denyRequest(item) {
                let itemIndex = this.usersRequest.indexOf(item)
                console.log(itemIndex)

                this.isEnableDenyForm = true
                //this.usersRequest[itemIndex].status = false
            },

            async getRequestList(){
                this.usersRequest = []
                this.loadingListRequest = true
                await this.sleep(1500) 
                await this.userLogged.getUsersRequest().then( usersRequest => {
                    for (const request of usersRequest){
                        let personalUser = new PersonalUser({
                            nick: undefined,
                            name: undefined,
                            lastName: undefined,
                            country: undefined,
                        })
                        personalUser.getPersonalUserByUID(request.uid).then( userInfo => {
                            this.usersRequest.push({name: userInfo.name, uid: request.uid})
                        })
                    }
                })
                this.loadingListRequest = false
            },

            /**
             * Event called by childs.
             */
            disableAcceptForm() {
                this.isEnableAcceptForm=false
                this.getRequestList()
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