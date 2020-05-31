export default {
    namespaced: true,
    state: {
        snackbarProperties: {
            visible: false,
            color: '',
            msg: '',
            timeout: 0,
            axisX: '',
            axisY: '',

        }

    },
    mutations: {
        showNotification(state, {color, msg, timeout=5000, axisX='center', axisY='top'}){
            state.snackbarProperties.color = color
            state.snackbarProperties.msg = msg
            state.snackbarProperties.timeout = timeout
            state.snackbarProperties.axisX = axisX
            state.snackbarProperties.axisY = axisY

            state.snackbarProperties.visible = true
        },

        hideNotification(state){
            state.snackbarProperties.visible = false
        }

    },
    actions: {
        showNotificationInfo(context, {msg, timeout, axisX, axisY}){
            context.commit('showNotification', { color: 'info', msg: msg, timeout: timeout, axisX: axisX, axisY: axisY })
        },

        showNotificationSuccess(context, {msg, timeout, axisX, axisY}){
            context.commit('showNotification', { color: 'success', msg: msg, timeout: timeout, axisX: axisX, axisY: axisY })
        },       

        showNotificationWarning(context, {msg, timeout, axisX, axisY}){
            context.commit('showNotification', { color: 'warning', msg: msg, timeout: timeout, axisX: axisX, axisY: axisY })
        },        

        showNotificationError(context, {msg, timeout, axisX, axisY}){
            context.commit('showNotification', { color: 'error', msg: msg, timeout: timeout, axisX: axisX, axisY: axisY } )
        },      
    }
}
