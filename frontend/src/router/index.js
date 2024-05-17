import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import RegisterView from "../views/RegisterView.vue";
import LoginView from "../views/LoginView.vue";
import AnalyseView from "../views/AnalyseView.vue";

const state = {
  token: localStorage.getItem('user-token') || '',
  status: '',
}

const getters = {
  isAuthenticated: !!state.token,
  authStatus: state.status,
}

const ifNotAuthenticated = (to, from, next) => {
  if (!getters.isAuthenticated) {
    next()
    return
  }
  next('/')
}

const ifAuthenticated = (to, from, next) => {
  if (getters.isAuthenticated) {
    next()
    return
  }
  next('/login')
}

export function updateState(){
  state.token = localStorage.getItem('user-token') || '';
  getters.isAuthenticated = !!state.token;
}

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView,
      beforeEnter: ifNotAuthenticated,
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
      beforeEnter: ifNotAuthenticated,
    },
    {
      path: '/analyzes',
      name: 'analyzes',
      component: AnalyseView,
      beforeEnter: ifAuthenticated
    },
  ]
})

export default router
