<template>
  <div class="lang-switcher">
    <button class="lang-toggle" @click="toggleDropdown">
      <span class="lang-current">{{ currentLocale }}</span>
      <svg class="lang-arrow" :class="{ open: isOpen }" width="14" height="14" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
      </svg>
    </button>
    <transition name="dropdown">
      <div v-if="isOpen" class="lang-dropdown">
        <button
          v-for="loc in availableLocales"
          :key="loc.code"
          @click="changeLocale(loc.code)"
          class="lang-option"
          :class="{ active: loc.code === locale }"
        >
          {{ loc.name }}
        </button>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { computed, ref, onMounted, onBeforeUnmount } from 'vue'
import { useI18n } from 'vue-i18n'

const { locale } = useI18n({ useScope: 'global' })

const isOpen = ref(false)

const availableLocales = [
  { code: 'tk', name: 'TM' },
  { code: 'ru', name: 'RU' }
]

const currentLocale = computed(() => {
  const current = availableLocales.find(l => l.code === locale.value)
  return current ? current.name : locale.value
})

const toggleDropdown = () => {
  isOpen.value = !isOpen.value
}

const changeLocale = (code) => {
  locale.value = code
  localStorage.setItem('locale', code)
  isOpen.value = false
}

const closeDropdown = (e) => {
  if (!e.target.closest('.lang-switcher')) {
    isOpen.value = false
  }
}

onMounted(() => document.addEventListener('click', closeDropdown))
onBeforeUnmount(() => document.removeEventListener('click', closeDropdown))
</script>

<style scoped>
.lang-switcher {
  position: relative;
}

.lang-toggle {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 8px 14px;
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: var(--radius-full);
  cursor: pointer;
  transition: var(--transition);
  color: var(--text-primary);
}

.lang-toggle:hover {
  border-color: var(--primary-light);
  box-shadow: var(--shadow-sm);
  transform: translateY(-1px);
}

.lang-current {
  font-size: 13px;
  font-weight: 600;
  letter-spacing: 0.5px;
  text-transform: uppercase;
}

.lang-arrow {
  transition: transform 0.25s ease;
  color: var(--text-secondary);
}

.lang-arrow.open {
  transform: rotate(180deg);
}

.lang-dropdown {
  position: absolute;
  right: 0;
  top: calc(100% + 8px);
  min-width: 100%;
  background: var(--bg-glass);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-md);
  overflow: hidden;
  z-index: 50;
}

.lang-option {
  display: block;
  width: 100%;
  padding: 10px 16px;
  border: none;
  background: transparent;
  cursor: pointer;
  font-size: 13px;
  font-weight: 500;
  letter-spacing: 0.5px;
  text-transform: uppercase;
  text-align: left;
  color: var(--text-secondary);
  transition: var(--transition-fast);
}

.lang-option:hover {
  background: rgba(108, 92, 231, 0.08);
  color: var(--primary);
}

.lang-option.active {
  color: var(--primary);
  font-weight: 700;
  background: rgba(108, 92, 231, 0.05);
}

/* Dropdown transition */
.dropdown-enter-active,
.dropdown-leave-active {
  transition: all 0.2s ease;
  transform-origin: top right;
}

.dropdown-enter-from,
.dropdown-leave-to {
  opacity: 0;
  transform: scale(0.95) translateY(-4px);
}
</style>