<template>
    <div>
        <v-row justify="center">
            Put a marker in your garaje door.
        </v-row>
        

    <div>
        <script type="application/javascript" src='https://api.tiles.mapbox.com/mapbox-gl-js/v1.4.0/mapbox-gl.js'></script>
        <link href='https://api.tiles.mapbox.com/mapbox-gl-js/v1.4.0/mapbox-gl.css' rel='stylesheet' />
        
        <div id='map' @click="updatedMarker"></div>
    </div>
        </div>
</template>


<script>
    import mapboxgl from 'mapbox-gl'

    var map = null

    export default {
        mounted() {
            mapboxgl.accessToken = 'pk.eyJ1IjoicHJ1ZWJhMSIsImEiOiJjazFpNm1kNDAwMzJhM2ltbmRwcXJxbzUyIn0.xp_6hLfEEPqJsPfQA4pmNg';
            map = new mapboxgl.Map({
                container: 'map', 
                style: 'mapbox://styles/mapbox/streets-v11', 
                center: [4.50, 40], 
                zoom: 0
            });  

            map.addControl(new mapboxgl.GeolocateControl({
                positionOptions: {
                    enableHighAccuracy: true
                },
                trackUserLocation: true
            }));
            
            /**
             * Listener to click event.
             * Only allows one marker in the map. 
             * If there is a marker in the map and user clicks in map => The first marker will be removed 
             * and the second one will be added.
             */
            map.on('click', function(event){
                if(!this.garajeDoor){                    
                    this.garajeDoor = new mapboxgl.Marker().setLngLat(event.lngLat).addTo(map)
                }else {
                    this.garajeDoor.remove()
                    this.garajeDoor = new mapboxgl.Marker().setLngLat(event.lngLat).addTo(map)
                }
            });  
        },

        methods: {
            /**
             * Throw events to parents.
             */
            updatedMarker(){
                this.$emit('updatedMarkerFromMap', map.garajeDoor);
            }, 
                   
        },

    }

</script>


<style>
    #map { 
        position:absolute; 
        top:275px; 
        bottom: 75px; 
        width:95%; 
    }
</style>

