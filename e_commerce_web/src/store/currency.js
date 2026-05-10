import { defineStore } from 'pinia'
import api from '../api'

export const useCurrencyStore = defineStore('currency', {
  state: () => ({
    rate: 3.5,
    loading: false,
  }),

  getters: {
    toTMT: (state) => (usd) => Math.round(usd * state.rate * 100) / 100,
  },

  actions: {
    async fetchRate() {
      try {
        this.loading = true
        const { data } = await api.get('/currency/')
        this.rate = data.usd_to_tmt
      } catch (e) {
        console.error('Walýuta kursy alynmady:', e)
      } finally {
        this.loading = false
      }
    },

    async updateRate(newRate) {
      const { data } = await api.put('/currency/', { usd_to_tmt: newRate })
      this.rate = data.usd_to_tmt
      return data
    },
  },
})
