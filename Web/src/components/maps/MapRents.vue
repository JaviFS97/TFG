<template>
    <v-container>
        <div>
            <script type="application/javascript" src='https://api.tiles.mapbox.com/mapbox-gl-js/v1.4.0/mapbox-gl.js'></script>
            <link href='https://api.tiles.mapbox.com/mapbox-gl-js/v1.4.0/mapbox-gl.css' rel='stylesheet' />
            
            <div id='map'></div>         
        </div>        
        <div class="bottoms">
            <v-row justify="center">                        
                <v-btn color="red darken-1" text @click="cancelForm">Cancel</v-btn>
                <v-btn color="green darken-1" text @click="confirmForm">Next</v-btn>
            </v-row>
        </div>        
    </v-container>

</template>


<script>
    import mapboxgl from 'mapbox-gl'

    var map = null
    window.rentPID = []

    export default {
        props: ['rents'],

        data() {
            return {
                listOID: [],
                pid: true
            }
        },

        computed:{
			/**
			 * Determine if a user is logged in the app.
			 */
			userLogged(){
				return this.$store.state.session.user
            }

        },        

        async mounted() {

            mapboxgl.accessToken = 'pk.eyJ1IjoicHJ1ZWJhMSIsImEiOiJjazFpNm1kNDAwMzJhM2ltbmRwcXJxbzUyIn0.xp_6hLfEEPqJsPfQA4pmNg';
            map = new mapboxgl.Map({
                container: 'map', 
                style: 'mapbox://styles/mapbox/streets-v11', 
                zoom: 1 
            });
            
            this.addControlToMap()
            
            for (const rent of this.rents){
                if (!this.itsMyPublish(rent.uidOwner)){
                    const popup = this.creatingPopup(rent)
                    const coordenates = [rent.coordenateLNG, rent.coordenateLAT]
                    this.garajeDoor = new mapboxgl.Marker().setLngLat(coordenates).setPopup(popup).addTo(map)
                }
            }
        },

        methods: {
            creatingPopup(rent){
                console.log(rent)
                // create the popup
                var popup = new mapboxgl.Popup({ offset: 25 }).setText(
                    name + "'s garaje is here."
                );

                const description = 
                    `
                    <div> 
                        <b> ${rent.pid} publish</b> 
                        <hr> 
                        <button type="button"
                            onclick=" window.rentPID.push( ${rent.pid});

                                    "> Follow</button>
                        <hr>  
                    </div>
                    `



                popup.setHTML(description)

                // create DOM element for the marker
                var el = document.createElement('div');
                return popup
            },

            addControlToMap(){
                map.addControl(
                    new mapboxgl.GeolocateControl({
                        positionOptions: {
                            enableHighAccuracy: true
                        },
                        trackUserLocation: true
                    }),
                );

                // Add zoom and rotation controls to the map.
                map.addControl(new mapboxgl.NavigationControl());
            },

            itsMyPublish(rentUidOwner){
                return rentUidOwner == this.userLogged.uid
            },

            /**
             * Throw events to parents.
             */
            confirmForm(){
                for (const rent of this.rents){
                    if (rent.pid == window.rentPID){
                        this.$emit('selectedParking', rent);
                    }
                }

            }, 

            /**
             * Throw events to parents.
             */
            cancelForm(){
                this.$emit('closeForm');
            }, 
        },

    }

</script>


<style scoped>
    #map { 

        position: absolute; 
        right: 40px; 
        top: 100px; 
        width: 90%; 
        height: 300px; 
    }

    .bottoms {
        position: relative;
        top: 400px;
    }
</style>

