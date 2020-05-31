<template>
    <v-card flat>
        <v-card-title style="background-color:#164E77;"> <v-row justify="center"> <h4 style="color:white;"> Your Garages </h4> </v-row></v-card-title>

        <v-divider></v-divider>

        <v-list>
            <v-list-item @click="enableOrganizationForm">
                <v-list-item-icon><v-icon>mdi-plus-circle</v-icon></v-list-item-icon>
                <v-list-item-title>Add new Organization</v-list-item-title>
            </v-list-item>
            <v-list-item @click="enableRentForm">
                <v-list-item-icon><v-icon>mdi-plus-circle</v-icon></v-list-item-icon>
                <v-list-item-title>Rent a garaje</v-list-item-title>
            </v-list-item>

        </v-list>

        <v-divider></v-divider>

        <v-list two-line style=" width:100%; height:100%;">
            <v-subheader>Organizations</v-subheader>
            <v-list-group
                v-for="org in organizations"
                :key="org.oid"
                v-model="org.active"
                :disabled="org.requestStatus == 'SENT'"
                no-action
            >
                <template v-slot:activator>
                    <v-list-item-content>
                        <v-list-item-title v-text="org.name"></v-list-item-title>
                        <v-list-item-subtitle v-if="org.requestStatus == 'SENT'">Request is not accepted yet</v-list-item-subtitle>
                    </v-list-item-content>
                </template>

                <v-list-item
                    v-for="garaje in org.garajes"
                    :key="garaje.title"
                    @click="selectOrganization(garaje)">
                    <v-list-item-content>
                        <v-list-item-title v-text="garaje.title"></v-list-item-title>
                    </v-list-item-content>
                </v-list-item>
            </v-list-group>
        </v-list>

        <v-divider></v-divider>

        <v-list two-line style=" width:100%; height:100%;">
            <v-subheader>Rents</v-subheader>
            <v-list-group
                v-for="r in rents"
                :key="r.oid"
                v-model="r.active"
                :disabled="r.requestStatus == 'SENT'"
                no-action
            >
                <template v-slot:activator>
                    <v-list-item-content>
                        <v-list-item-title v-text="r.name"></v-list-item-title>
                        <v-list-item-subtitle v-if="r.requestStatus == 'SENT'">Request is not accepted yet</v-list-item-subtitle>
                    </v-list-item-content>
                </template>

                <v-list-item
                    v-for="rent in r.rents"
                    :key="rent.title"
                    @click="selectRent(rent)">
                    <v-list-item-content>
                        <v-list-item-title v-text="rent.title"></v-list-item-title>
                    </v-list-item-content>
                </v-list-item>
            </v-list-group>
        </v-list>

    </v-card>
</template>

<script>

    // Models
    import OrganizationUser from '../../models/user/organizationUser'
    import RentGarajeSpace from '../../models/rentGarajeSpace/rentGarajeSpace'

    export default {
        data () {
            return {
                organizations: [
                    // {                        
                    //     name: 'Test',
                    //     requestStatus: 'TRUE',
                    //     garajes: [
                    //         { title: 'List Item1' },
                    //         { title: 'List Item2' },
                    //     ],
                    // },
                ],
                rents: [

                ]
            }
        },   

        created() {
            this.getAllOrganizationsList()
            this.getAllRentList()
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
            enableOrganizationForm() {
                this.$emit('enableOrganizationForm')
            },

            enableRentForm() {
                this.$emit('enableRentForm')
            },

            selectOrganization(garaje){
                this.$emit('selectOrganization', garaje)
            },

            selectRent(garaje){
                this.$emit('selectRent', garaje)
            },

            async getAllOrganizationsList(){
                await this.userLogged.getOrganizations().then( organizations => {
                    this.organizations = []
                    for (let org of organizations){
                        let instanceOrg = new OrganizationUser({
                            email: undefined,
                            password: undefined,
                            name: undefined,
                            parkingSpaces: undefined,
                            coordenates: undefined,
                        })
                        instanceOrg.getOrganizationByOID(org.oid).then( orgByOID => {
                            let nameOrg = orgByOID.organizationName

                            this.userLogged.getParkingsOfOrganization(org.oid).then( parkings => {
                                let garajes = []
                                for (const park of parkings){
                                    garajes.push({'title': park.title, 'oid': org.oid, 'pid': park.pid, 'coordenateLAT': orgByOID.coordenateLAT, 'coordenateLNG': orgByOID.coordenateLNG})
                                }
                                return garajes
                            }).then( (garajes) => {
                                this.organizations.push({ 'oid': org.oid, 'name': nameOrg, 'requestStatus': org.requestStatus, 'garajes': garajes})
                            })
                        })
                    }
                })
            },  
            
            async getAllRentList() {
                await this.userLogged.getRentList().then( rents => {
                    this.rents = []
                    for(const rent1 of rents){
                        let cont = 1
                        const instaceRentGarajeSpace = new RentGarajeSpace()
                        instaceRentGarajeSpace.getMyRentByPID(rent1.pid, this.userLogged.uid).then( listOfRents => {
                            let rents = []
                            let cont = 1
                            for (const rent of listOfRents) {
                                rents.push({'title': 'Parking ' + cont, 'uidOwner': rent1.uidOwner, 'approvedByOwner': rent.approvedByOwner, 'coordenates': [rent.coordenateLNG, rent.coordenateLAT] , 'dates': rent.dates, 'endHour': rent.endHour, 'startHour': rent.startHour })
                                cont +=1
                            }
                            return rents
                        }).then( rents => {
                            this.rents.push({'pid': rent1.pid, 'name': 'Rent ' + cont, 'rents': rents})
                            cont += 1
                        })
                    }
                })
            }
        
        }
    }
</script>