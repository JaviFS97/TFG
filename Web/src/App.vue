<template>
	<v-app>	
		<SideBar></SideBar>
		<TopBar></TopBar>
		<PrincipalView></PrincipalView>
		<Snackbar></Snackbar>
	</v-app>
</template>


<script>

	import SideBar from '@/components/core/SideBar'
	import TopBar from '@/components/core/TopBar'
	import PrincipalView from '@/components/core/PrincipalView'
	import Snackbar from '@/components/core/Snackbar'



	export default {
		name: 'App', 
		components: {
			SideBar, TopBar, PrincipalView, Snackbar
		},
		data(){
			return{
				
			}
		},
		computed: {

		}
		
	};
</script>
