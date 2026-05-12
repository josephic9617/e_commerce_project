<template>
  <div class="checkout-page container fade-in">
    <h1 class="page-title">{{ $t('checkout_title') }}</h1>

    <div v-if="orderSuccess" class="success-card glass-card slide-up">
      <div class="success-icon">&#10004;</div>
      <h2>{{ $t('order_success') }}</h2>
      <p>{{ $t('order_number') }}: <strong>#{{ orderId }}</strong></p>
      <router-link to="/" class="btn btn-primary" style="margin-top: 16px">{{ $t('go_back_shop') }}</router-link>
    </div>

    <div v-else class="checkout-layout">
      <div class="checkout-form glass-card">
        <h3>{{ $t('info_title') }}</h3>

        <template v-if="!authStore.isLoggedIn">
          <div class="form-group">
            <label class="form-label">{{ $t('guest_name_label') }}</label>
            <input v-model="form.guest_name" class="form-input" :placeholder="$t('guest_name_placeholder')" />
          </div>
          <div class="form-group">
            <label class="form-label">{{ $t('phone_label') }}</label>
            <input v-model="form.guest_phone" class="form-input" :placeholder="$t('phone_placeholder')" />
          </div>
        </template>

        <div class="form-group">
          <label class="form-label">{{ $t('address_label') }}</label>
          <textarea v-model="form.address" class="form-input" :placeholder="$t('address_placeholder')"></textarea>
        </div>

        <div class="form-group">
          <label class="form-label">{{ $t('note_label') }}</label>
          <textarea v-model="form.note" class="form-input" :placeholder="$t('note_placeholder')"></textarea>
        </div>

        <p v-if="error" class="error-msg">{{ error }}</p>

        <button class="btn btn-primary btn-lg" style="width: 100%" @click="placeOrder" :disabled="loading">
          {{ loading ? $t('sending') : $t('place_order') }}
        </button>
      </div>

      <div class="checkout-summary glass-card">
        <h3>{{ $t('order_content') }}</h3>
        <div class="summary-items">
          <div class="summary-item" v-for="item in cartStore.items" :key="item.product_id">
            <span>{{ getLocalized(item, 'name', locale) }} &times; {{ item.quantity }}</span>
            <strong>${{ (item.price_usd * item.quantity).toFixed(2) }}</strong>
          </div>
        </div>
        <hr />
        <div class="summary-row total">
          <span>{{ $t('total') }}</span>
          <div>
            <strong>${{ cartStore.totalUSD.toFixed(2) }}</strong>
            <p class="tmt-total">{{ currencyStore.toTMT(cartStore.totalUSD).toFixed(2) }} TMT</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../../api'
import { useAuthStore } from '../../store/auth'
import { useCartStore } from '../../store/cart'
import { useCurrencyStore } from '../../store/currency'
import { useI18n } from 'vue-i18n'
import { getLocalized } from '../../utils/i18nHelper'

const router = useRouter()
const authStore = useAuthStore()
const cartStore = useCartStore()
const currencyStore = useCurrencyStore()
const { t, locale } = useI18n({ useScope: 'global' })

const form = ref({
  guest_name: '',
  guest_phone: '',
  address: '',
  note: '',
})

const loading = ref(false)
const error = ref('')
const orderSuccess = ref(false)
const orderId = ref(null)

onMounted(() => {
  if (cartStore.items.length === 0) {
    router.push('/cart')
  }
})

async function placeOrder() {
  error.value = ''
  loading.value = true

  try {
    const payload = {
      items: cartStore.items.map((i) => ({
        product_id: i.product_id,
        quantity: i.quantity,
      })),
      address: form.value.address || null,
      note: form.value.note || null,
    }

    if (!authStore.isLoggedIn) {
      if (!form.value.guest_phone) {
        error.value = t('phone_required')
        loading.value = false
        return
      }
      payload.guest_phone = form.value.guest_phone
      payload.guest_name = form.value.guest_name || null
    }

    const { data } = await api.post('/orders/', payload)
    orderId.value = data.id
    orderSuccess.value = true
    cartStore.clearCart()
  } catch (e) {
    error.value = e.response?.data?.detail || t('order_error')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.page-title {
  font-size: 28px;
  font-weight: 800;
  margin-bottom: 24px;
}

.checkout-layout {
  display: grid;
  grid-template-columns: 1fr 380px;
  gap: 24px;
  align-items: start;
}

.checkout-form,
.checkout-summary {
  padding: 24px;
}

.checkout-form h3,
.checkout-summary h3 {
  font-size: 18px;
  margin-bottom: 20px;
}

.error-msg {
  color: var(--danger);
  font-size: 14px;
  margin-bottom: 12px;
  font-weight: 500;
}

.summary-items {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.summary-item {
  display: flex;
  justify-content: space-between;
  font-size: 14px;
}

.summary-row.total {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  font-size: 18px;
  font-weight: 700;
  padding-top: 12px;
}

.tmt-total {
  font-size: 14px;
  color: var(--text-secondary);
  font-weight: 500;
  text-align: right;
}

hr {
  border: none;
  border-top: 1px solid var(--border);
  margin: 16px 0;
}

.success-card {
  text-align: center;
  padding: 60px 40px;
  max-width: 500px;
  margin: 0 auto;
}

.success-icon {
  width: 70px;
  height: 70px;
  background: var(--success);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32px;
  margin: 0 auto 20px;
}

.success-card h2 {
  margin-bottom: 8px;
}

@media (max-width: 768px) {
  .checkout-layout {
    grid-template-columns: 1fr;
  }
}
</style>
