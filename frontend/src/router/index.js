import { createRouter, createWebHistory } from 'vue-router'
import Home from '../pages/Home.vue'
import Category from '../pages/Category.vue'
import Matching from '../pages/Matching.vue'
import Info from '../pages/Info.vue'

const routes = [
    { path: '/', component: Home },
    { path: '/category', component: Category },
    { path: '/matching', component: Matching },
    { path: '/info/:id', component: Info },
]

const router = createRouter({
    history: createWebHistory(),
    routes,
    scrollBehavior(to, from, savedPosition) {
        if (savedPosition) {
            return savedPosition
        } else {
            return { top: 0 }
        }
    },
})

export default router
