<template>
    <div>
        <script type="application/javascript" src='https://api.tiles.mapbox.com/mapbox-gl-js/v1.4.0/mapbox-gl.js'></script>
        <link href='https://api.tiles.mapbox.com/mapbox-gl-js/v1.4.0/mapbox-gl.css' rel='stylesheet' />
        
        <!-- <div id='map' @click="updatedMarker"></div> -->
        <div id='map'></div>
    </div>
</template>


<script>
    import mapboxgl from 'mapbox-gl'

    var map = null

    export default {
        props: ['organization'],

        mounted() {
            mapboxgl.accessToken = 'pk.eyJ1IjoicHJ1ZWJhMSIsImEiOiJjazFpNm1kNDAwMzJhM2ltbmRwcXJxbzUyIn0.xp_6hLfEEPqJsPfQA4pmNg';
            map = new mapboxgl.Map({
                container: 'map', 
                style: 'mapbox://styles/mapbox/streets-v11', 
                center: this.organization.coordenates, 
                zoom: 9 
            });
            
            const popup = this.creatingPopup()
            this.garajeDoor = new mapboxgl.Marker().setLngLat(this.organization.coordenates).setPopup(popup).addTo(map)
            this.addControlToMap()
            
            /**
             * Listener to click event.
             * Only allows one marker in the map. 
             * If there is a marker in the map and user clicks in map => The first marker will be removed 
             * and the second one will be added.
             */
            map.on('click', function(event){
                if(!this.garajeDoor){                    
                    //this.garajeDoor = new mapboxgl.Marker().setLngLat(event.lngLat).addTo(map)
                }else {
                    // this.garajeDoor.remove()
                    // this.garajeDoor = new mapboxgl.Marker().setLngLat(event.lngLat).addTo(map)
                }
            });  
        },

        methods: {
            creatingPopup(){
                // create the popup
                var popup = new mapboxgl.Popup({ offset: 25 }).setText(
                    this.organization.name + "'s garaje is here."
                );
                
                // create DOM element for the marker
                var el = document.createElement('div');
                el.id = 'marker';
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
            }

        },

    }

</script>

<style scoped>
    #map { 
        width:95%; 
        height: 300px;
    }
</style>

