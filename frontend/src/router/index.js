import { createRouter, createWebHashHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const routes = [
  { path: '/login', component: () => import('../views/LoginView.vue'), meta: { guest: true } },
  { path: '/register', component: () => import('../views/RegisterView.vue'), meta: { guest: true } },
  {
    path: '/',
    redirect: '/analyze',
    meta: { requiresAuth: true },
  },
  {
    path: '/analyze',
    component: () => import('../views/AnalyzeView.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/about',
    component: () => import('../views/AboutView.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/account',
    component: () => import('../views/AccountView.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/chat',
    component: () => import('../views/ChatView.vue'),
    meta: { requiresAuth: true },
  },
  { path: '/:pathMatch(.*)*', redirect: '/analyze' },
]

const router = createRouter({
  history: createWebHashHistory(import.meta.env.BASE_URL),
  routes,
})

router.beforeEach((to) => {
  const auth = useAuthStore()
  if (to.meta.requiresAuth && !auth.isAuthenticated) return '/login'
  if (to.meta.guest && auth.isAuthenticated) return '/analyze'
})

export default router
