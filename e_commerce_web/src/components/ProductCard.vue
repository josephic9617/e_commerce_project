<template>
  <div class="product-card glass-card" @click="$router.push(`/product/${product.id}`)">
    <div class="card-image">
      <img
        :src="product.image_url || '/placeholder.svg'"
        :alt="getLocalized(product, 'name', locale)"
        loading="lazy"
      />
      <div class="card-badge" v-if="product.stock < 5 && product.stock > 0">
        {{ $t('low_stock') }}
      </div>
      <div class="card-badge out" v-if="product.stock === 0">
        {{ $t('out_of_stock') }}
      </div>
    </div>
    <div class="card-body">
      <p class="card-category">{{ getLocalized(product, 'category_name', locale) }}</p>
      <h3 class="card-title">{{ getLocalized(product, 'name', locale) }}</h3>
      <div class="card-prices">
        <span class="price-usd">${{ product.price_usd.toFixed(2) }}</span>
        <span class="price-tmt">{{ currencyStore.toTMT(product.price_usd).toFixed(2) }} TMT</span>
      </div>
      <button
        class="btn btn-primary btn-sm card-btn"
        @click.stop="addToCart"
        :disabled="product.stock === 0"
      >
        &#128722; {{ $t('add_to_cart') }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { useCartStore } from '../store/cart'
import { useCurrencyStore } from '../store/currency'
import { useI18n } from 'vue-i18n'
import { getLocalized } from '../utils/i18nHelper'

const props = defineProps({
  product: { type: Object, required: true }
})

const cartStore = useCartStore()
const currencyStore = useCurrencyStore()
const { locale } = useI18n()

function addToCart() {
  cartStore.addItem(props.product)
}
</script>

<style scoped>
.product-card {
  cursor: pointer;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.card-image {
  position: relative;
  aspect-ratio: 1;
  overflow: hidden;
  background: var(--bg-primary);
}

.card-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: var(--transition-slow);
}

.product-card:hover .card-image img {
  transform: scale(1.08);
}

.card-badge {
  position: absolute;
  top: 10px;
  left: 10px;
  padding: 4px 10px;
  background: var(--warning);
  color: var(--text-primary);
  border-radius: var(--radius-full);
  font-size: 11px;
  font-weight: 700;
}

.card-badge.out {
  background: var(--danger);
  color: white;
}

.card-body {
  padding: 14px;
  display: flex;
  flex-direction: column;
  gap: 6px;
  flex: 1;
}

.card-category {
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: var(--primary);
  font-weight: 600;
}

.card-title {
  font-size: 15px;
  font-weight: 600;
  line-height: 1.3;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-prices {
  display: flex;
  align-items: baseline;
  gap: 8px;
  margin-top: 4px;
}

.price-usd {
  font-size: 18px;
  font-weight: 800;
  color: var(--primary);
}

.price-tmt {
  font-size: 13px;
  color: var(--text-secondary);
  font-weight: 500;
}

.card-btn {
  margin-top: auto;
  width: 100%;
}

@media (max-width: 480px) {
  .card-body {
    padding: 10px;
  }
  .card-title {
    font-size: 13px;
  }
  .price-usd {
    font-size: 15px;
  }
}
</style>
