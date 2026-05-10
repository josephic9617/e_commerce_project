<template>
  <div class="admin-orders fade-in">
    <div class="page-header">
      <h2>{{ t('admin_orders') }}</h2>
      <div class="filters">
        <select v-model="statusFilter" class="form-input" @change="fetchOrders" style="max-width: 180px">
          <option value="">{{ t('all_statuses') }}</option>
          <option value="pending">{{ t('status_pending') }}</option>
          <option value="confirmed">{{ t('status_confirmed') }}</option>
          <option value="shipped">{{ t('status_shipped') }}</option>
          <option value="delivered">{{ t('status_delivered') }}</option>
          <option value="cancelled">{{ t('status_cancelled') }}</option>
        </select>
      </div>
    </div>

    <div v-if="loading" class="loader"><div class="spinner"></div></div>

    <div v-else-if="orders.length === 0" class="empty-state">
      <div class="icon">&#128220;</div>
      <h3>{{ t('no_orders') }}</h3>
    </div>

    <div v-else class="table-wrapper">
      <table class="table">
        <thead>
          <tr>
            <th>{{ t('th_id') }}</th>
            <th>{{ t('th_customer') }}</th>
            <th>{{ t('th_status') }}</th>
            <th>{{ t('th_total_usd') }}</th>
            <th>{{ t('th_total_tmt') }}</th>
            <th>{{ t('th_date') }}</th>
            <th>{{ t('th_actions') }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="order in orders" :key="order.id">
            <td><strong>#{{ order.id }}</strong></td>
            <td>
              <template v-if="order.guest_phone">
                {{ order.guest_name || t('guest') }}<br />
                <small>{{ order.guest_phone }}</small>
              </template>
              <template v-else>
                {{ t('user_id') }} #{{ order.user_id }}
              </template>
            </td>
            <td>
              <span class="badge" :class="'badge-' + order.status">
                {{ statusLabels[order.status] }}
              </span>
            </td>
            <td>${{ order.total_usd.toFixed(2) }}</td>
            <td>{{ order.total_tmt.toFixed(2) }} TMT</td>
            <td>{{ new Date(order.created_at).toLocaleString() }}</td>
            <td>
              <div class="action-btns">
                <button class="btn btn-sm btn-secondary" @click="viewOrder(order)">&#128065;</button>
                <select
                  :value="order.status"
                  class="form-input status-select"
                  @change="updateStatus(order.id, $event.target.value)"
                >
                  <option value="pending">{{ t('status_pending') }}</option>
                  <option value="confirmed">{{ t('status_confirm_action') }}</option>
                  <option value="shipped">{{ t('status_ship_action') }}</option>
                  <option value="delivered">{{ t('status_deliver_action') }}</option>
                  <option value="cancelled">{{ t('status_cancel_action') }}</option>
                </select>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="pagination" v-if="totalPages > 1">
      <button :disabled="currentPage <= 1" @click="goToPage(currentPage - 1)">&laquo;</button>
      <button v-for="p in totalPages" :key="p" :class="{ active: p === currentPage }" @click="goToPage(p)">{{ p }}</button>
      <button :disabled="currentPage >= totalPages" @click="goToPage(currentPage + 1)">&raquo;</button>
    </div>

    <!-- Order Detail Modal -->
    <Modal v-if="showModal" :title="t('order_details')" @close="showModal = false" width="600px">
      <div v-if="selectedOrder" class="order-detail">
        <div class="detail-row">
          <span>{{ t('order_id') }}:</span> <strong>#{{ selectedOrder.id }}</strong>
        </div>
        <div class="detail-row">
          <span>{{ t('th_status') }}:</span>
          <span class="badge" :class="'badge-' + selectedOrder.status">{{ statusLabels[selectedOrder.status] }}</span>
        </div>
        <div class="detail-row" v-if="selectedOrder.address">
          <span>{{ t('address') }}:</span> <span>{{ selectedOrder.address }}</span>
        </div>
        <div class="detail-row" v-if="selectedOrder.note">
          <span>{{ t('note') }}:</span> <span>{{ selectedOrder.note }}</span>
        </div>

        <h4 style="margin: 16px 0 8px">{{ t('order_items') }}:</h4>
        <div class="table-wrapper">
          <table class="table">
            <thead>
              <tr>
                <th>{{ t('th_product') }}</th>
                <th>{{ t('th_qty') }}</th>
                <th>{{ t('th_price_usd') }}</th>
                <th>{{ t('th_price_tmt') }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in selectedOrder.items" :key="item.id">
                <td>{{ item.product_name }}</td>
                <td>{{ item.quantity }}</td>
                <td>${{ item.price_usd.toFixed(2) }}</td>
                <td>{{ item.price_tmt.toFixed(2) }} TMT</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="detail-total">
          <span>{{ t('total') }}: <strong>${{ selectedOrder.total_usd.toFixed(2) }}</strong> / <strong>{{ selectedOrder.total_tmt.toFixed(2) }} TMT</strong></span>
        </div>
      </div>
    </Modal>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import api from '../../api'
import Modal from '../../components/Modal.vue'

const { t } = useI18n()
const orders = ref([])
const loading = ref(true)
const currentPage = ref(1)
const totalPages = ref(1)
const statusFilter = ref('')
const showModal = ref(false)
const selectedOrder = ref(null)

const statusLabels = computed(() => ({
  pending: t('status_pending'),
  confirmed: t('status_confirmed'),
  shipped: t('status_shipped'),
  delivered: t('status_delivered'),
  cancelled: t('status_cancelled'),
}))

async function fetchOrders() {
  loading.value = true
  try {
    const params = { page: currentPage.value, per_page: 20 }
    if (statusFilter.value) params.status = statusFilter.value

    const { data } = await api.get('/orders/', { params })
    orders.value = data.items
    totalPages.value = data.pages
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

async function updateStatus(orderId, newStatus) {
  try {
    await api.put(`/orders/${orderId}/status`, { status: newStatus })
    fetchOrders()
  } catch (e) {
    alert(e.response?.data?.detail || t('status_change_failed'))
  }
}

function viewOrder(order) {
  selectedOrder.value = order
  showModal.value = true
}

function goToPage(page) {
  currentPage.value = page
  fetchOrders()
}

onMounted(fetchOrders)
</script>

<style scoped>
.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
  flex-wrap: wrap;
  gap: 12px;
}

.action-btns {
  display: flex;
  gap: 6px;
  align-items: center;
}

.status-select {
  padding: 6px 10px;
  font-size: 12px;
  max-width: 140px;
}

.order-detail .detail-row {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  border-bottom: 1px solid var(--border);
  font-size: 14px;
}

.detail-total {
  text-align: right;
  padding-top: 12px;
  font-size: 16px;
}
</style>
