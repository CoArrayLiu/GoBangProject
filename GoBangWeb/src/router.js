import { createRouter,createWebHistory } from "vue-router";
import game from './views/game.vue';
import HelloWorld from './components/HelloWorld.vue';


const routes=[
    {
        path:'/',
        name:'game',
        component:game
    },
    {
        path:'/test',
        name:'HelloWorld',
        component:HelloWorld
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router;