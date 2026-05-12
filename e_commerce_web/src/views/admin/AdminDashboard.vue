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

      <!-- Charts Section -->
      <div class="charts-grid">
        <div class="glass-card chart-container">
          <h3 class="chart-title">Soňky 7 günüň söwdasy (USD)</h3>
          <div class="chart-wrapper">
            <Line :data="lineChartData" :options="chartOptions" />
          </div>
        </div>
        <div class="glass-card chart-container">
          <h3 class="chart-title">Zakazlaryň ýagdaýy</h3>
          <div class="chart-wrapper">
            <Doughnut :data="doughnutChartData" :options="chartOptions" />
          </div>
        </div>
      </div>

      <!-- Additional Info & Top Products -->
      <div class="dashboard-bottom-grid">
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

        <div class="quick-stats">
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
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import api from '../../api'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
} from 'chart.js'
import { Line, Doughnut } from 'vue-chartjs'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
)

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
  daily_sales: [],
  status_breakdown: {},
})

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
}

const lineChartData = computed(() => ({
  labels: stats.value.daily_sales.map(d => d.date),
  datasets: [
    {
      label: 'Girdeji ($)',
      backgroundColor: '#6c5ce7',
      borderColor: '#6c5ce7',
      data: stats.value.daily_sales.map(d => d.revenue),
      tension: 0.4,
    },
  ],
}))

const doughnutChartData = computed(() => {
  const labels = Object.keys(stats.value.status_breakdown)
  const data = Object.values(stats.value.status_breakdown)
  
  return {
    labels: labels.map(l => t(l) || l),
    datasets: [
      {
        backgroundColor: ['#00b894', '#fdcb6e', '#d63031', '#0984e3'],
        data: data,
      },
    ],
  }
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

.charts-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 20px;
  margin-bottom: 24px;
}

.chart-container {
  padding: 24px;
  min-height: 350px;
}

.chart-wrapper {
  height: 280px;
  position: relative;
}

.chart-title {
  font-size: 16px;
  margin-bottom: 20px;
}

.dashboard-bottom-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 20px;
}

.quick-stats {
  display: flex;
  flex-direction: column;
  gap: 16px;
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
  padding: 24px;
}

@media (max-width: 1024px) {
  .charts-grid, .dashboard-bottom-grid {
    grid-template-columns: 1fr;
  }
}
</style>
