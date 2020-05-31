<template>
    <v-container>
        <v-row v-if="userType=='organizationUser'">
            <v-col cols="6">
                <v-row justify="center" >
                    <h2 id="title-chart">Garaje status</h2>
                    <canvas id="planet-chart"></canvas>
                </v-row>
                
            </v-col>
                
            <v-col cols="6">
                <v-timeline dense>
                    <v-timeline-item v-for="timeLine in timeLines" :key="timeLine"
                        color="green lighten-2"
                        small
                    >
                    <v-card class="elevation-2">
                        <v-card-title class="headline primary">

                            <h4 v-if="timeLine.status == 'Leave'" class="ml-4" style="color:white;">
                                Leave garaje
                            </h4>
                            <h4 v-if="timeLine.status == 'Enter'" class="ml-4" style="color:white;">
                                Enter garaje
                            </h4>                            
                            <h4 v-if="timeLine.status == 'Error'" class="ml-4" style="color:white;">
                                Does not belong to the garage
                            </h4>                             
                        </v-card-title>
                        <v-container>
                            <v-row>                            
                                <v-col cols="6">                               
                                    <b>Date:</b> {{timeLine.date }}
                                    
                                </v-col>
                                <v-col cols="6">
                                    <img :src="timeLine.plateURL " height="100%" width="100%">
                                </v-col>    
                            </v-row>
                        </v-container>
                        
                            
                        
                        
                    </v-card>
                    </v-timeline-item>
                </v-timeline>
            </v-col>
        </v-row>
    </v-container>

</template>

<script>
    // Vuex
    import { mapMutations } from 'vuex'

    // Chartjs
   import Chart from 'chart.js'; 

    export default {
        created(){
            this.setTopBarName('Dashboard')
            this.getTimeLines()

            const ctx = document.getElementById('planet-chart');
            const myChart = new Chart(ctx, {
            type: '',
            data: [],
            options: {},
            });
        },

        data() {
            return {
                timeLines: [],
                planetChartData:  {
                    type: 'pie',
                    data: {
                        labels: ['Free', 'Occuped'],
                        datasets: [
                        {
                            label: 'Number of Moons',
                            data: [4, 8],
                            backgroundColor: [
                                'rgba(77, 175, 124, 1)', // Blue
                                'rgba(236, 100, 75, 1)',
                            ],
                            borderColor: [
                                '#36495d',
                                '#36495d',      
                            ],
                            borderWidth: 3
                        },
                        ]
                    },
                    options: {
                        responsive: true,
                    }
                }
            }
        },

        computed:{
			/**
			 * Determine if a user is logged in the app.
			 */
			userLogged(){
				return this.$store.state.session.user
            },

            userType() {
                return this.$store.state.session.userType
            }
            

        },

        mounted() {
            this.createChart('planet-chart', this.planetChartData);
        },


        methods: {
            ...mapMutations('core', ['setTopBarName']),

            async getTimeLines() {
                await this.userLogged.getTimeLines().then( timeLines => {
                    for (const timeLine of timeLines){
                        // let personalUser = new PersonalUser({
                        //     nick: undefined,
                        //     name: undefined,
                        //     lastName: undefined,
                        //     country: undefined,
                        // })
                        // personalUser.getPersonalUserByUID(user.uid).then( userInfo => {
                        //     this.usersList.push({name: userInfo.name, uid: user.uid, parkingSpaces: user.parkingSpaces})
                        // })

                        this.timeLines.push({date: this.timeConverter(timeLine.date.seconds), plateURL: timeLine.plateURL, status: timeLine.status})
                    }

                })
            },


            timeConverter(unixtimestamp){
                var months_arr = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
                var date = new Date(unixtimestamp*1000);
                var year = date.getFullYear();
                var month = months_arr[date.getMonth()];
                var day = date.getDate();
                var hours = date.getHours();
                var minutes = "0" + date.getMinutes();
                var seconds = "0" + date.getSeconds();
                var convdataTime = month+'-'+day+'-'+year+' '+hours + ':' + minutes.substr(-2) + ':' + seconds.substr(-2);
                return convdataTime
            },


            createChart(chartId, chartData) {
                const ctx = document.getElementById(chartId);
                const myChart = new Chart(ctx, {
                    type: chartData.type,
                    data: chartData.data,
                    options: chartData.options,
                });
            }
        }
    
    }
</script>


<style >
    #planet-chart{
        position: fixed;
        top: 35%;
        left: 7%;
    }
    #title-chart{
        position: fixed;
        top: 30%;
    }
</style>