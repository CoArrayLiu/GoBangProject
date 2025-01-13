import {createStore} from 'vuex'


export default createStore({
    state:{
        showIndex : false
    },
    mutations:{
        flipShowIndex(state){
            state.showIndex = !state.showIndex;
        }
    },
    actions:{

    },
    modules:{
        
    }
})
