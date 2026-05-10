import { defineStore } from 'pinia'

export const useCartStore = defineStore('cart', {
  state: () => ({
    items: JSON.parse(localStorage.getItem('cart') || '[]'),
  }),

  getters: {
    totalItems: (state) => state.items.reduce((sum, item) => sum + item.quantity, 0),
    totalUSD: (state) => state.items.reduce((sum, item) => sum + item.price_usd * item.quantity, 0),
  },

  actions: {
    addItem(product, quantity = 1) {
      const existing = this.items.find((i) => i.product_id === product.id)
      if (existing) {
        existing.quantity += quantity
      } else {
        this.items.push({
          product_id: product.id,
          name: product.name,
          price_usd: product.price_usd,
          image_url: product.image_url,
          quantity,
        })
      }
      this.saveToStorage()
    },

    removeItem(productId) {
      this.items = this.items.filter((i) => i.product_id !== productId)
      this.saveToStorage()
    },

    updateQuantity(productId, quantity) {
      const item = this.items.find((i) => i.product_id === productId)
      if (item) {
        item.quantity = Math.max(1, quantity)
        this.saveToStorage()
      }
    },

    clearCart() {
      this.items = []
      this.saveToStorage()
    },

    saveToStorage() {
      localStorage.setItem('cart', JSON.stringify(this.items))
    },
  },
})
