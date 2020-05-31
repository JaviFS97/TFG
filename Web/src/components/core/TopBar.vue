<template>

	<v-app-bar 
		color="transparent"				 
		app
		flat
		absolute
		>		

		<v-toolbar-title class=" font-weight-light tertiary--text">
			<v-btn 
				v-if="isResponsive"
				icon
				@click="sideBarVisible">
				<v-icon>mdi-view-list</v-icon>
			</v-btn>
			{{currentPageName}}
		</v-toolbar-title>


		<v-spacer></v-spacer>  

		<v-toolbar-items v-if="userLogged">
			<v-row align="center">

				<v-badge :overlap=true color="warning" class="mx-2">
					<template v-slot:badge > ! </template>
					<v-icon>mdi-bell</v-icon>
				</v-badge>
								
				<v-chip pill class="mx-4" outlined color="primary" text-color="primary" @click="">
					<v-icon class="mr-1"> mdi-account-circle</v-icon>
					{{userLogged.name}}
				</v-chip>
			</v-row>
		</v-toolbar-items>

	</v-app-bar>

</template>


<script>

	import { mapMutations } from 'vuex'

	export default {
		components: {
			
		},
		data(){
			return{
			}
		},
		methods: {
			...mapMutations('core', ['setVisibleSideBar']),
			sideBarVisible(){
				let isSideBarVisible = this.$store.state.core.visibleSideBar
				this.setVisibleSideBar(!isSideBarVisible)
			}
		},
		computed:{
			/**
             * Determine if the dimensions are appropriate for responsive use.
             */
            isResponsive(){
                return true
			},
			
			/**
			 * Determine if a user is logged in the app.
			 */
			userLogged(){
				return this.$store.state.session.user
			},

			/**
			 * Determine the name of the current page (inside PrincipalView)
			 */
			currentPageName(){
				return this.$store.state.core.topBarName
			}


		}
	};
</script>
