<template>
	
    <div class="diagonal">
        <v-app-bar 
        color="transparent"				 
        app
        flat
        absolute
        >		
        <div>
            <v-list-item >
                <v-list-item-avatar color="white">
                    <v-img src='../../assets/core/SideBar/logo.jpg' height="34" contain/>
                </v-list-item-avatar>
                <v-list-item-title class="title">
                    SmartGaraje
                </v-list-item-title>
                </v-list-item>
        </div>

                
            <v-spacer></v-spacer>  

            <v-toolbar-items>
                <v-row align="center">
                    <div >
                        <v-btn rounded small>Login</v-btn>
                    </div>
                    <div class="mx-6">
                        <v-btn rounded small>Register</v-btn>
                    </div>     
                </v-row>
            </v-toolbar-items>

        </v-app-bar>

        <v-slide-y-transition mode="out-in">                  
            <v-container fill-height>
                <router-view></router-view>
                <v-row no-gutters justify="center" class="ma-6">
                    <h1 class="display-4 d-none d-sm-flex ">Welcome to SmartGaraje!!</h1>                            
                </v-row>                                
            </v-container>    
        </v-slide-y-transition>
    </div>



</template>



<script>

	export default {
		components: {

		},
		data(){
			return{
				
			}
		},
		
	};
</script>

<style lang="css">
    .diagonal {
        width: 100%;
        height: 100%;
        background-image: linear-gradient( 30deg, #E0E0E0 75%, #164E77 25%);
    }

    .diagonalAnterior {
        width: 100%;
        height: 100%;
        background: rgb(17, 89, 139);
        background-image: repeating-linear-gradient( 45deg,
                        hsla(0, 0%, 100%, .1),
                        hsla(0, 0%, 100%, .1) 15px,
                        transparent 0, transparent 40px);
    }


</style>