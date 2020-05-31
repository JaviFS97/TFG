<template>
	<v-content class="principalViewStyle">
		<v-fade-transition mode="out-in">
			<router-view></router-view>
		</v-fade-transition>
	</v-content>

</template>


<script>
	export default {
		components: {
			
		},
		data(){
			return{
				
			}
		}
	};
</script>


<style lang="css">
	.principalViewStyle{
		background-color: #E0E0E0;
	}
</style>