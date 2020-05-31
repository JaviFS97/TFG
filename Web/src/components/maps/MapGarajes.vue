<template>
    <v-container>
        <div>
            <script type="application/javascript" src='https://api.tiles.mapbox.com/mapbox-gl-js/v1.4.0/mapbox-gl.js'></script>
            <link href='https://api.tiles.mapbox.com/mapbox-gl-js/v1.4.0/mapbox-gl.css' rel='stylesheet' />
            
            <div id='map'></div>         
        </div>        
        <div class="test">
            <v-row justify="center">                        
                <v-btn color="red darken-1" text @click="cancelForm">Cancel</v-btn>
                <v-btn color="green darken-1" text @click="confirmForm">Confirm</v-btn>
            </v-row>
        </div>
    </v-container>

</template>


<script>
    import mapboxgl from 'mapbox-gl'

    // Models
    import OrganizationUser from '../../models/user/organizationUser'

    var map = null
    window.followOID = []

    export default {
        props: ['organizations'],

        data() {
            return {
                listOID: []
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
            
            await this.getOrganizationsInfo()

        },

        methods: {
            creatingPopup(name, oid){
                // create the popup
                var popup = new mapboxgl.Popup({ offset: 25 }).setText(
                    name + "'s garaje is here."
                );

                const description = 
                    `
                    <div> 
                        <b> ${name} organization</b> 
                        <hr> 
                        <button style="margin-left: 5%; type="button" id="${oid}" 
                            onclick="
                                        if(!window.followOID.includes('${oid}')){
                                            window.followOID.push(this.id);
                                        } 
                                    "> Follow</button>
                        <button style="margin-left: 30%;" type="button" id="${oid}1" 
                            onclick="   
                                        if(window.followOID.includes('${oid}')){
                                            window.followOID.splice(window.followOID.indexOf('${oid}'));
                                        }  
                                    "> Unfollow</button>
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

            async getOrganizationsInfo(){
                let instanceOrg = new OrganizationUser({
                    email: undefined,
                    password: undefined,
                    name: undefined,
                    parkingSpaces: undefined,
                    coordenates: undefined,
                })

                for (const org of this.organizations){
                    await instanceOrg.getOrganizationByOID(org.oid).then( orgByOID => {
                        let o = {}
                        o.oid = org.oid
                        o.name = orgByOID.organizationName
                        o.coordenates = [orgByOID.coordenateLNG, orgByOID.coordenateLAT]
                        return o
                    }).then( orga => {
                        //this.organizationINFO = org
                        const popup = this.creatingPopup(orga.name, orga.oid)
                        this.garajeDoor = new mapboxgl.Marker().setLngLat(orga.coordenates).setPopup(popup).addTo(map)
                        this.listOID.push(orga.oid)
                    })
                }                
            },

            /**
             * Throw events to parents.
             */
            confirmForm(){
                this.$emit('followOIDFromMap', window.followOID);
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

    .test {
        position: relative;
        top: 400px;
    }
</style>

