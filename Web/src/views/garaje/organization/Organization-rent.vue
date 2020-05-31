<template>
    <v-card flat>
        <v-container>
            <v-row justify="center">
                <v-col cols="10">
                    <v-stepper v-model="step">
                        <v-stepper-header>
                            <v-stepper-step :complete="step > 1" step="1">Date</v-stepper-step>
                            <v-divider></v-divider>
                            <v-stepper-step :complete="step > 2" step="2">Start hour</v-stepper-step>
                            <v-divider></v-divider>
                            <v-stepper-step :complete="step > 3" step="3">End hour</v-stepper-step>
                        </v-stepper-header>

                        <v-stepper-items>
                            <v-stepper-content step="1">
                                <ul v-for="rent in rentList" :key="rent.udiRent" justify="center">
                                    <li v-if="rent.approvedByOwner" class="mb-2"> <b :style=" {color: rent.color }">Color</b>   | hours: [{{rent.startHour}} - {{rent.endHour}}]</li>
                                    <li v-else  class="mb-2"> <b :style=" {color: rent.color }">Color</b>   | hours: [{{rent.startHour}} - {{rent.endHour}}]  <v-btn small color="red" dark class="ml-5 mr-2" @click="denyRent(rent)">Deny</v-btn> <v-btn small color="green" dark @click="acceptRent(rent)">Accept</v-btn> </li>
                                    
                                </ul>
                                <v-row justify="center" class="mt-4">
                                    <v-date-picker
                                        v-model="form.selectedDates"
                                        multiple
                                        :event-color="date => date[9] % 2 ? 'red' : 'yellow'"
                                        :events="functionEvents"
                                        :min="today"
                                    ></v-date-picker>
                                </v-row>
                                <v-row justify="center" class="mt-6">
                                    <v-btn @click="step += 1" color="primary" :disabled="form.selectedDates.length == 0"> Next </v-btn>
                                </v-row>
                            </v-stepper-content>

                            <v-stepper-content step="2">
                                <v-row justify="center">
                                    <h2>Start:</h2>
                                </v-row>
                                <v-row justify="center">
                                    <v-time-picker v-model="form.start" landscape :max="form.end" format="24hr" :event-color="date => date[9] % 2 ? 'red' : 'yellow'" :events="functionEvents"></v-time-picker>
                                </v-row>
                                <v-row justify="center" class="mt-6">
                                    <v-btn @click="step -= 1" color="primary" class="mr-6"> Before </v-btn>
                                    <v-btn @click="step += 1" color="primary" :disabled="!form.start"> Next </v-btn>
                                </v-row>
                            </v-stepper-content>
                            <v-stepper-content step="3">
                                <v-row justify="center">
                                    <h2>End:</h2>
                                </v-row>
                                <v-row justify="center">
                                    <v-time-picker v-model="form.end" landscape :min="form.start" format="24hr"></v-time-picker>                                            
                                </v-row>
                                <v-row justify="center" class="mt-6">
                                    <v-btn @click="step -= 1" color="primary" class="mr-6"> Before </v-btn>
                                    <v-btn @click="publishRent" color="primary" :disabled="!form.end"> Publish </v-btn>
                                </v-row>
                            </v-stepper-content>   

                        </v-stepper-items>
                    </v-stepper>
                </v-col>
            </v-row>

        </v-container>
    </v-card>
</template>


<script>

    // Models
    import PersonalUser from '../../../models/user/personalUser'
    import RentGarajeSpace from '../../../models/rentGarajeSpace/rentGarajeSpace'
    
    // Vuex
    import { mapMutations, mapActions} from 'vuex'    

    export default {
        props: ['selectedOrganization'],  
        data() {
            return {
                step: 1,
                today: null,
                colors: ['#339933', '#003366', '#ff3300', '#33cccc', '#996633', '#ffcc66', '#ff66cc', '#993366', '#cc00cc', '#666699'],
                form: {
                    selectedDates: [],
                    start: null,
                    end: null,
                },
                rentList: []
            }
        },

        created() {
            this.currentDate()
            this.getRentsOfParking()
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

            functionEvents (date) {
                //console.log(this.selectedOrganization)
                this.selectedOrganization.usersRents = []

                for (const rent of this.rentList){
                    this.selectedOrganization.usersRents.push( {userUID: rent.uidRent, dates: rent.dates })
                }

                const [yearDate, monthDate, dayDate] = date.split('-')

                let userCount = 0
                for (const userRent of this.selectedOrganization.usersRents){
                    for (const userDate of userRent.dates){
                        const [year, month, day] = userDate.split('-')
                        if(dayDate == day && monthDate == month && yearDate == year){
                            return this.colors[userCount]
                        }
                    }
                    userCount += 1
                }
            },    

            currentDate() {
                var today = new Date();
                var dd = String(today.getDate()).padStart(2, '0');
                var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
                var yyyy = today.getFullYear();

                this.today = yyyy + '-' + mm + '-' + dd;
            },

            async publishRent(){
                await this.userLogged.publishRent(this.selectedOrganization.pid, this.form.selectedDates, this.form.start, this.form.end, this.selectedOrganization.coordenateLAT , this.selectedOrganization.coordenateLNG).then( () => {
                    this.showNotificationSuccess({msg: 'Published succesfull.', timeout:4000, axisY: 'top', axisX: 'center'}) 
                    this.step = 1
                }).catch( () => {
                    this.showNotificationError({msg: 'Error during publising.', timeout:4000, axisY: 'top', axisX: 'center'}) 
                })
            },

            async getRentsOfParking(){
                const rentGarajeSpace = new RentGarajeSpace()
                await rentGarajeSpace.getRentsOfParking(this.selectedOrganization.pid).then( rentList => {
                    let cont = 0
                    for (const rent of rentList){
                        this.rentList.push( {'uidRent': rent.uidRent, 'approvedByOwner': rent.approvedByOwner, 'dates': rent.dates, 'endHour': rent.endHour, 'startHour': rent.startHour, 'color': this.colors[cont], 'index': cont})
                        cont += 1
                    }
                })
            },

            async acceptRent(rent){
                const rentGarajeSpace = new RentGarajeSpace()
                await rentGarajeSpace.acceptRent(rent, this.selectedOrganization.pid)
                this.rentList.splice(rent.index,1)
                this.getRentsOfParking()
            },

            async denyRent(rent){
                const rentGarajeSpace = new RentGarajeSpace()
                await rentGarajeSpace.denyRent(rent, this.selectedOrganization.pid)
                this.rentList.splice(rent.index,1)
                this.getRentsOfParking()
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