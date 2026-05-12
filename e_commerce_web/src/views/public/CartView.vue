<template>
  <div class="cart-page container fade-in">
    <h1 class="page-title">{{ $t('cart') }}</h1>

    <div v-if="cartStore.items.length === 0" class="empty-state">
      <div class="icon">&#128722;</div>
      <h3>{{ $t('empty_cart') }}</h3>
      <p>{{ $t('empty_cart_desc') }}</p>
      <router-link to="/" class="btn btn-primary" style="margin-top: 16px">{{ $t('go_to_shop') }}</router-link>
    </div>

    <div v-else class="cart-layout">
      <div class="cart-items">
        <div class="cart-item glass-card" v-for="item in cartStore.items" :key="item.product_id">
          <div class="item-image">
            <img :src="item.image_url || '/placeholder.svg'" :alt="getLocalized(item, 'name', locale)" />
          </div>
          <div class="item-info">
            <h3 class="item-name">{{ getLocalized(item, 'name', locale) }}</h3>
            <div class="item-prices">
              <span class="price-usd">${{ item.price_usd.toFixed(2) }}</span>
              <span class="price-tmt">{{ currencyStore.toTMT(item.price_usd).toFixed(2) }} TMT</span>
            </div>
          </div>
          <div class="item-quantity">
            <button class="btn btn-icon btn-secondary btn-sm" @click="updateQty(item.product_id, item.quantity - 1)">-</button>
            <span>{{ item.quantity }}</span>
            <button class="btn btn-icon btn-secondary btn-sm" @click="updateQty(item.product_id, item.quantity + 1)">+</button>
          </div>
          <div class="item-total">
            <strong>${{ (item.price_usd * item.quantity).toFixed(2) }}</strong>
          </div>
          <button class="btn btn-icon btn-secondary btn-sm" @click="cartStore.removeItem(item.product_id)">
            &#10005;
          </button>
        </div>
      </div>

      <div class="cart-summary glass-card">
        <h3>{{ $t('order_summary') }}</h3>
        <div class="summary-row">
          <span>{{ $t('items_count', { count: cartStore.totalItems }) }}</span>
          <strong>${{ cartStore.totalUSD.toFixed(2) }}</strong>
        </div>
        <div class="summary-row tmt">
          <span>{{ $t('tmt_equivalent') }}</span>
          <strong>{{ currencyStore.toTMT(cartStore.totalUSD).toFixed(2) }} TMT</strong>
        </div>
        <hr />
        <div class="summary-row total">
          <span>{{ $t('total') }}</span>
          <strong>${{ cartStore.totalUSD.toFixed(2) }}</strong>
        </div>
        <router-link to="/checkout" class="btn btn-primary btn-lg" style="width: 100%; margin-top: 16px;">
          {{ $t('place_order') }}
        </router-link>
        <button class="btn btn-secondary btn-sm" style="width: 100%; margin-top: 8px;" @click="cartStore.clearCart()">
          {{ $t('clear_cart') }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useCartStore } from '../../store/cart'
import { useCurrencyStore } from '../../store/currency'
import { useI18n } from 'vue-i18n'
import { getLocalized } from '../../utils/i18nHelper'

const cartStore = useCartStore()
const currencyStore = useCurrencyStore()
const { locale } = useI18n()

function updateQty(productId, qty) {
  if (qty < 1) {
    cartStore.removeItem(productId)
  } else {
    cartStore.updateQuantity(productId, qty)
  }
}
</script>

<style scoped>
.page-title {
  font-size: 28px;
  font-weight: 800;
  margin-bottom: 24px;
}

.cart-layout {
  display: grid;
  grid-template-columns: 1fr 360px;
  gap: 24px;
  align-items: start;
}

.cart-items {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.cart-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
}

.item-image {
  width: 80px;
  height: 80px;
  border-radius: var(--radius-md);
  overflow: hidden;
  flex-shrink: 0;
}

.item-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.item-info {
  flex: 1;
  min-width: 0;
}

.item-name {
  font-size: 15px;
  font-weight: 600;
  margin-bottom: 4px;
}

.item-prices {
  display: flex;
  gap: 8px;
  align-items: baseline;
}

.price-usd {
  font-weight: 700;
  color: var(--primary);
}

.price-tmt {
  font-size: 13px;
  color: var(--text-secondary);
}

.item-quantity {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 700;
}

.item-total {
  min-width: 80px;
  text-align: right;
  font-size: 16px;
}

.cart-summary {
  padding: 24px;
  position: sticky;
  top: 100px;
}

.cart-summary h3 {
  font-size: 18px;
  margin-bottom: 16px;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  font-size: 14px;
}

.summary-row.tmt {
  color: var(--text-secondary);
}

.summary-row.total {
  font-size: 18px;
  font-weight: 700;
  color: var(--primary);
}

hr {
  border: none;
  border-top: 1px solid var(--border);
  margin: 8px 0;
}

@media (max-width: 768px) {
  .cart-layout {
    grid-template-columns: 1fr;
  }
  .cart-item {
    flex-wrap: wrap;
  }
  .item-total {
    min-width: auto;
  }
}
</style>
