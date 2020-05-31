<template>
    <v-row justify="center">
        <v-dialog v-model="enableRentForm" persistent max-width="900" >
            <v-card height="700">
                <v-row justify="center">
                    <v-card-title class="headline">SELECT GARAGE TO RENT</v-card-title>
                </v-row>

                <v-container>
                    <v-row justify="center">
                        <v-col cols="10">
                            <!-- <MapRents :rents="rentsList" @followOIDFromMap="followOIDFromMap" @closeForm="disableRentForm"></MapRents> -->
                            <MapRents :rents="rentsList" @closeForm="disableRentForm" @selectedParking="selectedParking"></MapRents>
                        </v-col>
                    </v-row>
                </v-container>
            </v-card>
        </v-dialog>

        <v-dialog v-model="parkingIsSelected" persistent max-width="900">
            <v-card height="700">
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
                                        <v-row justify="center">
                                            RELLENAR CON INFO De cada color
                                        </v-row>
                                        <v-row justify="center">
                                            <v-date-picker
                                                v-model="form.selectedDates"
                                                multiple
                                                :allowed-dates="allowedDates"
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
                                            <v-time-picker v-model="form.start" landscape :min="form.start" :max="form.end" format="24hr" ></v-time-picker>
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
                                            <v-time-picker v-model="form.end" landscape :min="form.start" :max="form.end" format="24hr"></v-time-picker>                                            
                                        </v-row>
                                        <v-row justify="center" class="mt-6">
                                            <v-btn @click="step -= 1" color="primary" class="mr-6"> Before </v-btn>
                                            <v-btn @click="sendRentParking" color="primary" :disabled="!form.end" :loading="loadingsendRentParking"> Send </v-btn>
                                        </v-row>
                                    </v-stepper-content>   

                                </v-stepper-items>
                            </v-stepper>
                        </v-col>
                    </v-row>
                </v-container>                
            </v-card>
        </v-dialog>
    </v-row>
</template>

<script>

    // Models
    import rentGarajeSpace from '../../../models/rentGarajeSpace/rentGarajeSpace'

    // Components
    import MapRents from '../../../components/maps/MapRents'

    export default {
        components: {MapRents},

        props: ['enableRentForm'],

        data () {
            return {
                infoRent: null,
                dialog: true,
                loadingListRents: true,
                rentsList: [],
                parkingIsSelected: false,
                loadingsendRentParking: false,
                step: 1,
                today: null,
                form: {
                    selectedDates: [],
                    start: null,
                    end: null,
                },
            }
        },

        created() {
            this.getAllRentsList()
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
            disableRentForm() {
                this.$emit('disableRentForm')
            },

            async getAllRentsList(){
                const rentGaraje = new rentGarajeSpace()
                this.rentsList = await rentGaraje.getAllRent()
                this.loadingListRents = true
                await this.sleep(1500)
                this.loadingListRents = false
            },   

            selectedParking(rent){
                this.infoRent = rent
                this.form.start = rent.startHour
                this.form.end = rent.endHour
                this.disableRentForm()
                this.parkingIsSelected = true
            },     
            
            allowedDates(date) {
                const [yearDate, monthDate, dayDate] = date.split('-')
                for (const userDate of this.infoRent.dates){
                    const [year, month, day] = userDate.split('-')
                    if(dayDate == day && monthDate == month && yearDate == year){
                        return true
                    }                
                }
                return false
            },

            async sendRentParking() {
                const rentGaraje = new rentGarajeSpace()
                this.rentsList = await rentGaraje.addRentToparking(this.infoRent.pid, this.infoRent.uidOwner, this.userLogged.uid, this.form.selectedDates, this.form.start, this.form.end, this.infoRent.coordenateLAT, this.infoRent.coordenateLNG)
                this.loadingsendRentParking = true
                await this.sleep(1500)
                this.loadingsendRentParking = false
                this.parkingIsSelected = false
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