<template>
  <div id="app-root">
    <router-view />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useAuthStore } from './store/auth'
import { useCurrencyStore } from './store/currency'

const authStore = useAuthStore()
const currencyStore = useCurrencyStore()

onMounted(async () => {
  authStore.loadFromStorage()
  await currencyStore.fetchRate()
})
</script>
