<template>
  <div class="dashboard fade-in">
    <div v-if="loading" class="loader"><div class="spinner"></div></div>

    <template v-else>
      <!-- Stat Cards -->
      <div class="stats-grid">
        <div class="stat-card glass-card">
          <div class="stat-icon" style="background: rgba(108,92,231,0.1); color: var(--primary)">&#128230;</div>
          <div class="stat-info">
            <p class="stat-label">{{ t('stat_products') }}</p>
            <h3 class="stat-value">{{ stats.total_products }}</h3>
          </div>
        </div>
        <div class="stat-card glass-card">
          <div class="stat-icon" style="background: rgba(0,206,201,0.1); color: var(--secondary)">&#128220;</div>
          <div class="stat-info">
            <p class="stat-label">{{ t('stat_orders') }}</p>
            <h3 class="stat-value">{{ stats.total_orders }}</h3>
          </div>
        </div>
        <div class="stat-card glass-card">
          <div class="stat-icon" style="background: rgba(253,121,168,0.1); color: var(--accent)">&#128100;</div>
          <div class="stat-info">
            <p class="stat-label">{{ t('stat_users') }}</p>
            <h3 class="stat-value">{{ stats.total_users }}</h3>
          </div>
        </div>
        <div class="stat-card glass-card">
          <div class="stat-icon" style="background: rgba(0,184,148,0.1); color: var(--success)">&#128176;</div>
          <div class="stat-info">
            <p class="stat-label">{{ t('stat_revenue') }}</p>
            <h3 class="stat-value">${{ stats.revenue_usd.toFixed(2) }}</h3>
          </div>
        </div>
      </div>

      <!-- Additional Info -->
      <div class="dashboard-grid">
        <div class="glass-card info-card">
          <h3>&#128680; {{ t('pending_orders') }}</h3>
          <p class="big-number">{{ stats.pending_orders }}</p>
        </div>
        <div class="glass-card info-card">
          <h3>&#128176; {{ t('revenue_tmt') }}</h3>
          <p class="big-number">{{ stats.revenue_tmt.toFixed(2) }} TMT</p>
        </div>
        <div class="glass-card info-card">
          <h3>&#128193; {{ t('admin_categories') }}</h3>
          <p class="big-number">{{ stats.total_categories }}</p>
        </div>
      </div>

      <!-- Top Products -->
      <div class="glass-card top-products" v-if="stats.top_products?.length">
        <h3 style="margin-bottom: 16px">&#127942; {{ t('top_products') }}</h3>
        <div class="table-wrapper">
          <table class="table">
            <thead>
              <tr>
                <th>#</th>
                <th>{{ t('th_product') }}</th>
                <th>{{ t('th_sold_qty') }}</th>
                <th>{{ t('th_revenue') }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(p, i) in stats.top_products" :key="i">
                <td>{{ i + 1 }}</td>
                <td>{{ p.name }}</td>
                <td>{{ p.total_qty }}</td>
                <td>${{ p.total_revenue.toFixed(2) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import api from '../../api'

const { t } = useI18n()
const loading = ref(true)
const stats = ref({
  total_products: 0,
  total_categories: 0,
  total_users: 0,
  total_orders: 0,
  pending_orders: 0,
  revenue_usd: 0,
  revenue_tmt: 0,
  top_products: [],
})

async function fetchDashboard() {
  try {
    const { data } = await api.get('/reports/dashboard')
    stats.value = data
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

onMounted(fetchDashboard)
</script>

<style scoped>
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
}

.stat-icon {
  width: 52px;
  height: 52px;
  border-radius: var(--radius-lg);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  flex-shrink: 0;
}

.stat-label {
  font-size: 13px;
  color: var(--text-secondary);
  font-weight: 500;
}

.stat-value {
  font-size: 24px;
  font-weight: 800;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}

.info-card {
  padding: 20px;
}

.info-card h3 {
  font-size: 14px;
  color: var(--text-secondary);
  margin-bottom: 8px;
}

.big-number {
  font-size: 28px;
  font-weight: 800;
  color: var(--primary);
}

.top-products {
  padding: 20px;
}
</style>
