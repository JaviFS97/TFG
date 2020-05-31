export default {
    namespaced: true,
    state: {
        // Encargada de poner visible o de esconder el SideBar.
        visibleSideBar: true,
        // To show the actual name of principalView pages.
        topBarName: '',


    },
    mutations: {
        /**
         * Setter to the variable visibleSideBar. 
         * Serves to  put on or off the SideBar.
         * @param {*} state 
         * @param {Boolean} isVisible
         */
        setVisibleSideBar(state, isVisible){
            state.visibleSideBar = isVisible
        },

        /**
         * Setter to the variable topBarName.
         * Set a title in topBar based of the actual page (inside principalView).
         * @param {*} state 
         * @param {String} name 
         */
        setTopBarName(state, name){
            state.topBarName = name
        }
    },
    actions: {

    }
}
