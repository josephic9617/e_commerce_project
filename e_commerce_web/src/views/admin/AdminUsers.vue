<template>
  <div class="admin-users fade-in">
    <div class="page-header">
      <h2>{{ t('admin_users') || 'Ulanyjylary Dolandyrmak' }}</h2>
    </div>

    <div v-if="loading" class="loader"><div class="spinner"></div></div>

    <div v-else class="table-wrapper">
      <table class="table">
        <thead>
          <tr>
            <th>ID</th>
            <th>{{ t('name_label') || 'Ady' }}</th>
            <th>{{ t('phone_label') || 'Telefon' }}</th>
            <th>Status</th>
            <th>{{ t('th_created_date') || 'Hasaba alnan senesi' }}</th>
            <th>{{ t('th_actions') || 'Hereketler' }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td>{{ user.id }}</td>
            <td>{{ user.full_name || '---' }}</td>
            <td>{{ user.phone }}</td>
            <td>
              <span class="badge" :class="user.is_active ? 'badge-delivered' : 'badge-cancelled'">
                {{ user.is_active ? 'Işjeň' : 'Blokirlenen' }}
              </span>
              <span v-if="user.is_admin" class="badge badge-pending" style="margin-left: 5px">Admin</span>
            </td>
            <td>{{ new Date(user.created_at).toLocaleDateString() }}</td>
            <td>
              <div class="action-btns" v-if="!user.is_admin">
                <button 
                  class="btn btn-sm" 
                  :class="user.is_active ? 'btn-secondary' : 'btn-success'"
                  @click="toggleStatus(user)"
                >
                  {{ user.is_active ? 'Blokirle' : 'Blokdan çykar' }}
                </button>
                <button class="btn btn-sm btn-danger" @click="deleteUser(user.id)">&#128465;</button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import api from '../../api'

const { t } = useI18n()
const users = ref([])
const loading = ref(true)

async function fetchUsers() {
  loading.value = true
  try {
    const { data } = await api.get('/users/')
    users.value = data
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

async function toggleStatus(user) {
  const newStatus = !user.is_active
  const action = newStatus ? 'blokdan çykarmak' : 'blokirlemek'
  if (!confirm(`Ulanyjyny ${action} isleýärsiňizmi?`)) return

  try {
    await api.put(`/users/${user.id}/status`, { is_active: newStatus })
    user.is_active = newStatus
  } catch (e) {
    alert(e.response?.data?.detail || 'Amaly ýerine ýetirip bolmady')
  }
}

async function deleteUser(id) {
  if (!confirm('Ulanyjyny öçürmek isleýärsiňizmi?')) return
  try {
    await api.delete(`/users/${id}`)
    users.value = users.value.filter(u => u.id !== id)
  } catch (e) {
    alert(e.response?.data?.detail || 'Öçürip bolmady')
  }
}

onMounted(fetchUsers)
</script>

<style scoped>
.page-header {
  margin-bottom: 24px;
}
.badge {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 600;
}
.badge-delivered { background: rgba(var(--success-rgb), 0.1); color: var(--success); }
.badge-cancelled { background: rgba(var(--danger-rgb), 0.1); color: var(--danger); }
.badge-pending { background: rgba(var(--warning-rgb), 0.1); color: var(--warning); }
.action-btns { display: flex; gap: 8px; }
.btn-success { background: var(--success); color: white; border: none; }
</style>
