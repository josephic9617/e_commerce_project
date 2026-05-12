import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../store/auth'

const routes = [
  // Public routes
  {
    path: '/',
    component: () => import('../views/public/PublicLayout.vue'),
    children: [
      { path: '', name: 'home', component: () => import('../views/public/HomeView.vue') },
      { path: 'product/:id', name: 'product-detail', component: () => import('../views/public/ProductDetailView.vue') },
      { path: 'cart', name: 'cart', component: () => import('../views/public/CartView.vue') },
      { path: 'checkout', name: 'checkout', component: () => import('../views/public/CheckoutView.vue') },
      { path: 'login', name: 'login', component: () => import('../views/public/LoginView.vue') },
      { path: 'register', name: 'register', component: () => import('../views/public/RegisterView.vue') },
    ],
  },
  // Admin routes
  {
    path: '/admin',
    component: () => import('../views/admin/AdminLayout.vue'),
    meta: { requiresAdmin: true },
    children: [
      { path: '', name: 'admin-dashboard', component: () => import('../views/admin/AdminDashboard.vue') },
      { path: 'products', name: 'admin-products', component: () => import('../views/admin/AdminProducts.vue') },
      { path: 'users', name: 'admin-users', component: () => import('../views/admin/AdminUsers.vue') },
      { path: 'categories', name: 'admin-categories', component: () => import('../views/admin/AdminCategories.vue') },
      { path: 'orders', name: 'admin-orders', component: () => import('../views/admin/AdminOrders.vue') },
      { path: 'settings', name: 'admin-settings', component: () => import('../views/admin/AdminSettings.vue') },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  authStore.loadFromStorage()

  if (to.meta.requiresAdmin) {
    if (!authStore.isLoggedIn || !authStore.isAdmin) {
      next({ name: 'login' })
      return
    }
  }
  next()
})

export default router
