<template>
  <div class="admin-layout">
    <aside class="sidebar glass">
      <div class="sidebar-brand">
        <span class="brand-icon">&#9830;</span>
        <span>Admin Panel</span>
      </div>
      <nav class="sidebar-nav">
        <router-link to="/admin" class="nav-item" :class="{ active: $route.name === 'admin-dashboard' }">
          <span class="nav-icon">&#128202;</span> {{ t('admin_dashboard') }}
        </router-link>
        <router-link to="/admin/products" class="nav-item" :class="{ active: $route.name === 'admin-products' }">
          <span class="nav-icon">&#128230;</span> {{ t('admin_products') }}
        </router-link>
        <router-link to="/admin/categories" class="nav-item" :class="{ active: $route.name === 'admin-categories' }">
          <span class="nav-icon">&#128193;</span> {{ t('admin_categories') }}
        </router-link>
        <router-link to="/admin/orders" class="nav-item" :class="{ active: $route.name === 'admin-orders' }">
          <span class="nav-icon">&#128220;</span> {{ t('admin_orders') }}
        </router-link>
        <router-link to="/admin/settings" class="nav-item" :class="{ active: $route.name === 'admin-settings' }">
          <span class="nav-icon">&#9881;</span> {{ t('admin_settings') }}
        </router-link>
      </nav>
      <div class="sidebar-footer">
        <router-link to="/" class="nav-item">
          <span class="nav-icon">&#127968;</span> {{ t('go_to_shop_admin') }}
        </router-link>
        <button class="nav-item" @click="logout">
          <span class="nav-icon">&#128682;</span> {{ t('logout') }}
        </button>
      </div>
    </aside>

    <main class="admin-main">
      <header class="admin-header glass">
        <button class="mobile-menu-btn btn btn-icon btn-secondary" @click="menuOpen = !menuOpen">
          &#9776;
        </button>
        <h2 class="header-title">{{ pageTitle }}</h2>
        <div class="header-actions">
          <div class="language-switcher">
            <button
              class="lang-btn"
              :class="{ active: currentLocale === 'tk' }"
              @click="changeLanguage('tk')"
            >
              TM
            </button>
            <button
              class="lang-btn"
              :class="{ active: currentLocale === 'ru' }"
              @click="changeLanguage('ru')"
            >
              RU
            </button>
          </div>
          <div class="header-user">
            <span>{{ authStore.user?.full_name || 'Admin' }}</span>
          </div>
        </div>
      </header>
      <div class="admin-content">
        <router-view />
      </div>
    </main>

    <!-- Mobile overlay -->
    <div class="mobile-overlay" v-if="menuOpen" @click="menuOpen = false"></div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../../store/auth'
import { useI18n } from 'vue-i18n'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const menuOpen = ref(false)
const { locale, t } = useI18n()

const currentLocale = computed(() => locale.value)

const pageTitle = computed(() => {
  const titles = {
    'admin-dashboard': t('admin_dashboard'),
    'admin-products': t('admin_products'),
    'admin-categories': t('admin_categories'),
    'admin-orders': t('admin_orders'),
    'admin-settings': t('admin_settings'),
  }
  return titles[route.name] || 'Admin'
})

function changeLanguage(lang) {
  locale.value = lang
  localStorage.setItem('locale', lang)
}

function logout() {
  authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.admin-layout {
  display: flex;
  min-height: 100vh;
}

.sidebar {
  width: 260px;
  padding: 20px 16px;
  display: flex;
  flex-direction: column;
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  z-index: 50;
  border-right: 1px solid var(--border);
}

.sidebar-brand {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 20px;
  font-weight: 800;
  color: var(--primary);
  padding: 8px 12px;
  margin-bottom: 24px;
}

.brand-icon {
  font-size: 24px;
  background: linear-gradient(135deg, var(--primary), var(--accent));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.sidebar-nav {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border-radius: var(--radius-md);
  font-size: 14px;
  font-weight: 500;
  color: var(--text-secondary);
  transition: var(--transition);
  cursor: pointer;
  border: none;
  background: none;
  width: 100%;
  text-align: left;
}

.nav-item:hover {
  background: rgba(108, 92, 231, 0.06);
  color: var(--primary);
}

.nav-item.active {
  background: rgba(108, 92, 231, 0.1);
  color: var(--primary);
  font-weight: 600;
}

.nav-icon {
  font-size: 18px;
  width: 24px;
  text-align: center;
}

.sidebar-footer {
  border-top: 1px solid var(--border);
  padding-top: 12px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.admin-main {
  flex: 1;
  margin-left: 260px;
  display: flex;
  flex-direction: column;
}

.admin-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 28px;
  border-bottom: 1px solid var(--border);
  position: sticky;
  top: 0;
  z-index: 40;
}

.header-title {
  font-size: 20px;
  font-weight: 700;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 20px;
}

.language-switcher {
  display: flex;
  gap: 4px;
  background: rgba(108, 92, 231, 0.08);
  padding: 4px;
  border-radius: var(--radius-md);
}

.lang-btn {
  padding: 6px 12px;
  border: none;
  background: transparent;
  color: var(--text-secondary);
  font-size: 13px;
  font-weight: 600;
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: var(--transition);
}

.lang-btn:hover {
  background: rgba(108, 92, 231, 0.1);
  color: var(--primary);
}

.lang-btn.active {
  background: var(--primary);
  color: white;
}

.header-user {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-secondary);
}

.admin-content {
  padding: 28px;
  flex: 1;
}

.mobile-menu-btn {
  display: none;
}

.mobile-overlay {
  display: none;
}

@media (max-width: 900px) {
  .sidebar {
    transform: translateX(-100%);
    transition: var(--transition);
  }

  .admin-layout:has(.mobile-overlay) .sidebar {
    transform: translateX(0);
  }

  .admin-main {
    margin-left: 0;
  }

  .mobile-menu-btn {
    display: flex;
  }

  .mobile-overlay {
    display: block;
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.3);
    z-index: 45;
  }

  .admin-content {
    padding: 16px;
  }

  .header-actions {
    gap: 12px;
  }

  .header-user span {
    display: none;
  }

  .language-switcher {
    padding: 3px;
  }

  .lang-btn {
    padding: 5px 10px;
    font-size: 12px;
  }
}
</style>
