<template>
  <nav class="navbar glass">
    <div class="container navbar-inner">
      <router-link to="/" class="navbar-brand">
        <span class="brand-icon">&#9830;</span>
        <span class="brand-text">E-Shop</span>
      </router-link>

      <div class="navbar-search" v-if="!minimal">
        <input
          type="text"
          class="search-input"
          :placeholder="$t('search_placeholder')"
          v-model="searchQuery"
          @keyup.enter="handleSearch"
        />
        <button class="search-btn" @click="handleSearch">&#128269;</button>
      </div>

      <div class="navbar-actions">
        <LanguageSwitcher />
        <router-link to="/cart" class="nav-cart-btn">
          &#128722;
          <span v-if="cartStore.totalItems > 0" class="cart-badge">{{ cartStore.totalItems }}</span>
        </router-link>

        <template v-if="authStore.isLoggedIn">
          <router-link v-if="authStore.isAdmin" to="/admin" class="btn btn-sm btn-primary">
            {{ $t('admin_panel') }}
          </router-link>
          <button @click="handleLogout" class="btn btn-sm btn-secondary">
            {{ $t('logout') }}
          </button>
        </template>
        <template v-else>
          <router-link to="/login" class="btn btn-sm btn-primary">{{ $t('login') }}</router-link>
        </template>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../store/auth'
import { useCartStore } from '../store/cart'
import LanguageSwitcher from './LanguageSwitcher.vue'

defineProps({
  minimal: { type: Boolean, default: false }
})

const router = useRouter()
const authStore = useAuthStore()
const cartStore = useCartStore()
const searchQuery = ref('')

function handleSearch() {
  if (searchQuery.value.trim()) {
    router.push({ name: 'home', query: { search: searchQuery.value.trim() } })
  }
}

function handleLogout() {
  authStore.logout()
  cartStore.clearCart()
  router.push('/')
}
</script>

<style scoped>
.navbar {
  position: sticky;
  top: 0;
  z-index: 100;
  padding: 12px 0;
  border-bottom: 1px solid var(--border);
}

.navbar-inner {
  display: flex;
  align-items: center;
  gap: 24px;
}

.navbar-brand {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 22px;
  font-weight: 800;
  color: var(--primary);
  flex-shrink: 0;
}

.brand-icon {
  font-size: 28px;
  background: linear-gradient(135deg, var(--primary), var(--accent));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.navbar-search {
  flex: 1;
  max-width: 480px;
  position: relative;
}

.search-input {
  width: 100%;
  padding: 10px 44px 10px 16px;
  border: 1px solid var(--border);
  border-radius: var(--radius-full);
  background: var(--bg-secondary);
  font-size: 14px;
  outline: none;
  transition: var(--transition);
}

.search-input:focus {
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(108, 92, 231, 0.1);
}

.search-btn {
  position: absolute;
  right: 4px;
  top: 50%;
  transform: translateY(-50%);
  width: 34px;
  height: 34px;
  border: none;
  background: var(--primary);
  color: white;
  border-radius: 50%;
  cursor: pointer;
  font-size: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: var(--transition);
}

.search-btn:hover {
  background: var(--primary-dark);
}

.navbar-actions {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-shrink: 0;
}

.nav-cart-btn {
  position: relative;
  width: 42px;
  height: 42px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
  border-radius: var(--radius-md);
  transition: var(--transition);
  background: var(--bg-secondary);
  border: 1px solid var(--border);
}

.nav-cart-btn:hover {
  border-color: var(--primary-light);
  transform: translateY(-1px);
}

.cart-badge {
  position: absolute;
  top: -4px;
  right: -4px;
  width: 20px;
  height: 20px;
  background: var(--accent);
  color: white;
  border-radius: 50%;
  font-size: 11px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
}

@media (max-width: 768px) {
  .navbar-search {
    display: none;
  }
  .navbar-actions {
    gap: 8px;
  }
}
</style>
