<template>
  <div class="product-detail container fade-in" v-if="product">
    <button class="btn btn-secondary btn-sm back-btn" @click="$router.back()">
      &larr; {{ $t('back') }}
    </button>

    <div class="detail-grid">
      <div class="detail-image glass-card">
        <img :src="product.image_url || '/placeholder.svg'" :alt="getLocalized(product, 'name', locale)" />
      </div>

      <div class="detail-info">
        <p class="detail-category">{{ getLocalized(product, 'category_name', locale) }}</p>
        <h1 class="detail-title">{{ getLocalized(product, 'name', locale) }}</h1>

        <div class="detail-prices">
          <span class="price-usd">${{ product.price_usd.toFixed(2) }}</span>
          <span class="price-tmt">{{ currencyStore.toTMT(product.price_usd).toFixed(2) }} TMT</span>
        </div>

        <p class="detail-stock" :class="{ low: product.stock < 5 }">
          <template v-if="product.stock > 0">
            {{ $t('in_stock', { count: product.stock }) }}
          </template>
          <template v-else>
            {{ $t('out_of_stock') }}
          </template>
        </p>

        <p class="detail-description" v-if="product.description">{{ getLocalized(product, 'description', locale) }}</p>

        <div class="detail-actions">
          <div class="quantity-control">
            <button class="btn btn-icon btn-secondary" @click="qty = Math.max(1, qty - 1)">-</button>
            <span class="qty-display">{{ qty }}</span>
            <button class="btn btn-icon btn-secondary" @click="qty++">+</button>
          </div>
          <button
            class="btn btn-primary btn-lg"
            @click="addToCart"
            :disabled="product.stock === 0"
          >
            &#128722; {{ $t('add_to_cart') }}
          </button>
        </div>
      </div>
    </div>
  </div>

  <div v-else class="loader">
    <div class="spinner"></div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { getLocalized } from '../../utils/i18nHelper'
import api from '../../api'
import { useCartStore } from '../../store/cart'
import { useCurrencyStore } from '../../store/currency'

const route = useRoute()
const cartStore = useCartStore()
const currencyStore = useCurrencyStore()
const { locale } = useI18n()

const product = ref(null)
const qty = ref(1)

async function fetchProduct() {
  try {
    const { data } = await api.get(`/products/${route.params.id}`)
    product.value = data
  } catch (e) {
    console.error(e)
  }
}

function addToCart() {
  if (product.value) {
    cartStore.addItem(product.value, qty.value)
  }
}

onMounted(fetchProduct)
</script>

<style scoped>
.back-btn {
  margin-bottom: 20px;
}

.detail-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 40px;
  align-items: start;
}

.detail-image {
  overflow: hidden;
  border-radius: var(--radius-xl);
}

.detail-image img {
  width: 100%;
  aspect-ratio: 1;
  object-fit: cover;
}

.detail-category {
  font-size: 13px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: var(--primary);
  font-weight: 600;
  margin-bottom: 8px;
}

.detail-title {
  font-size: 32px;
  font-weight: 800;
  line-height: 1.2;
  margin-bottom: 16px;
}

.detail-prices {
  display: flex;
  align-items: baseline;
  gap: 12px;
  margin-bottom: 12px;
}

.price-usd {
  font-size: 32px;
  font-weight: 800;
  color: var(--primary);
}

.price-tmt {
  font-size: 18px;
  color: var(--text-secondary);
  font-weight: 500;
}

.detail-stock {
  font-size: 14px;
  color: var(--success);
  font-weight: 600;
  margin-bottom: 16px;
}

.detail-stock.low {
  color: var(--warning);
}

.detail-description {
  font-size: 15px;
  color: var(--text-secondary);
  line-height: 1.7;
  margin-bottom: 24px;
}

.detail-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}

.quantity-control {
  display: flex;
  align-items: center;
  gap: 12px;
}

.qty-display {
  font-size: 18px;
  font-weight: 700;
  min-width: 30px;
  text-align: center;
}

@media (max-width: 768px) {
  .detail-grid {
    grid-template-columns: 1fr;
    gap: 24px;
  }
  .detail-title {
    font-size: 24px;
  }
  .price-usd {
    font-size: 26px;
  }
  .detail-actions {
    flex-direction: column;
    align-items: stretch;
  }
  .quantity-control {
    justify-content: center;
  }
}
</style>
