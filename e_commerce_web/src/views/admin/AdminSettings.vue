<template>
  <div class="admin-settings fade-in">
    <h2 style="margin-bottom: 24px">{{ t('admin_settings') }}</h2>

    <!-- Currency Settings -->
    <div class="settings-card glass-card">
      <h3>&#128176; {{ t('currency_rate') }}</h3>
      <p class="settings-desc">{{ t('current_rate') }}: <strong>1 USD = {{ currentRate }} TMT</strong></p>
      <div class="rate-form">
        <input v-model.number="newRate" type="number" step="0.01" class="form-input" style="max-width: 200px" />
        <button class="btn btn-primary" @click="updateRate" :disabled="savingRate">
          {{ savingRate ? t('saving') : t('change') }}
        </button>
      </div>
      <p v-if="rateSuccess" class="success-msg">{{ t('rate_changed') }}</p>
      <p v-if="rateError" class="error-msg">{{ rateError }}</p>
    </div>

    <!-- Sales Report -->
    <div class="settings-card glass-card">
      <h3>&#128202; {{ t('sales_report') }}</h3>
      <div class="report-filters">
        <div class="form-group">
          <label class="form-label">{{ t('start_date') }}</label>
          <input v-model="reportStart" type="date" class="form-input" />
        </div>
        <div class="form-group">
          <label class="form-label">{{ t('end_date') }}</label>
          <input v-model="reportEnd" type="date" class="form-input" />
        </div>
        <button class="btn btn-primary" @click="fetchReport" :disabled="loadingReport">
          {{ loadingReport ? t('loading') : t('get_report') }}
        </button>
      </div>

      <div v-if="report" class="report-results">
        <div class="report-stat">
          <span>{{ t('total_orders') }}:</span> <strong>{{ report.total_orders }}</strong>
        </div>
        <div class="report-stat">
          <span>{{ t('total_revenue_usd') }}:</span> <strong>${{ report.total_usd.toFixed(2) }}</strong>
        </div>
        <div class="report-stat">
          <span>{{ t('total_revenue_tmt') }}:</span> <strong>{{ report.total_tmt.toFixed(2) }} TMT</strong>
        </div>
        <div class="report-stat" v-for="(count, status) in report.status_breakdown" :key="status">
          <span>{{ statusLabels[status] || status }}:</span> <strong>{{ count }}</strong>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import api from '../../api'
import { useCurrencyStore } from '../../store/currency'

const { t } = useI18n()
const currencyStore = useCurrencyStore()

const currentRate = ref(3.5)
const newRate = ref(3.5)
const savingRate = ref(false)
const rateSuccess = ref(false)
const rateError = ref('')

const reportStart = ref('')
const reportEnd = ref('')
const report = ref(null)
const loadingReport = ref(false)

const statusLabels = computed(() => ({
  pending: t('status_pending'),
  confirmed: t('status_confirmed'),
  shipped: t('status_shipped'),
  delivered: t('status_delivered'),
  cancelled: t('status_cancelled'),
}))

async function fetchCurrentRate() {
  try {
    const { data } = await api.get('/currency/')
    currentRate.value = data.usd_to_tmt
    newRate.value = data.usd_to_tmt
  } catch (e) {
    console.error(e)
  }
}

async function updateRate() {
  savingRate.value = true
  rateSuccess.value = false
  rateError.value = ''
  try {
    await currencyStore.updateRate(newRate.value)
    currentRate.value = newRate.value
    rateSuccess.value = true
    setTimeout(() => (rateSuccess.value = false), 3000)
  } catch (e) {
    rateError.value = e.response?.data?.detail || t('rate_change_failed')
  } finally {
    savingRate.value = false
  }
}

async function fetchReport() {
  loadingReport.value = true
  try {
    const params = {}
    if (reportStart.value) params.start_date = reportStart.value
    if (reportEnd.value) params.end_date = reportEnd.value

    const { data } = await api.get('/reports/sales', { params })
    report.value = data
  } catch (e) {
    console.error(e)
  } finally {
    loadingReport.value = false
  }
}

onMounted(fetchCurrentRate)
</script>

<style scoped>
.settings-card {
  padding: 24px;
  margin-bottom: 20px;
}

.settings-card h3 {
  font-size: 18px;
  margin-bottom: 8px;
}

.settings-desc {
  font-size: 14px;
  color: var(--text-secondary);
  margin-bottom: 16px;
}

.rate-form {
  display: flex;
  gap: 12px;
  align-items: center;
}

.success-msg {
  color: var(--success);
  font-size: 14px;
  margin-top: 8px;
  font-weight: 500;
}

.error-msg {
  color: var(--danger);
  font-size: 14px;
  margin-top: 8px;
  font-weight: 500;
}

.report-filters {
  display: flex;
  gap: 16px;
  align-items: flex-end;
  flex-wrap: wrap;
  margin-bottom: 20px;
}

.report-filters .form-group {
  margin-bottom: 0;
}

.report-results {
  border-top: 1px solid var(--border);
  padding-top: 16px;
}

.report-stat {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  font-size: 14px;
  border-bottom: 1px solid var(--border);
}

.report-stat:last-child {
  border-bottom: none;
}
</style>
