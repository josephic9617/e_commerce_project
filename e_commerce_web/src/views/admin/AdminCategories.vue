<template>
  <div class="admin-categories fade-in">
    <div class="page-header">
      <h2>{{ t('admin_categories') }}</h2>
      <button class="btn btn-primary" @click="openModal()">+ {{ t('new_category') }}</button>
    </div>

    <div v-if="loading" class="loader"><div class="spinner"></div></div>

    <div v-else class="table-wrapper">
      <table class="table">
        <thead>
          <tr>
            <th>{{ t('th_id') }}</th>
            <th>{{ t('th_name') }}</th>
            <th>{{ t('th_created_date') }}</th>
            <th>{{ t('th_actions') }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="cat in categories" :key="cat.id">
            <td>{{ cat.id }}</td>
            <td><strong>{{ cat.name }}</strong></td>
            <td>{{ new Date(cat.created_at).toLocaleDateString() }}</td>
            <td>
              <div class="action-btns">
                <button class="btn btn-sm btn-secondary" @click="openModal(cat)">&#9998;</button>
                <button class="btn btn-sm btn-danger" @click="deleteCategory(cat.id)">&#128465;</button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <Modal v-if="showModal" :title="editing ? t('edit_category') : t('new_category')" @close="showModal = false">
      <div class="form-group">
        <label class="form-label">{{ t('th_name') }}</label>
        <input v-model="form.name" class="form-input" required />
      </div>
      <p v-if="formError" class="error-msg">{{ formError }}</p>
      <template #footer>
        <button class="btn btn-secondary" @click="showModal = false">{{ t('cancel') }}</button>
        <button class="btn btn-primary" @click="saveCategory" :disabled="saving">
          {{ saving ? t('saving') : t('save') }}
        </button>
      </template>
    </Modal>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import api from '../../api'
import Modal from '../../components/Modal.vue'

const { t } = useI18n()
const categories = ref([])
const loading = ref(true)
const showModal = ref(false)
const editing = ref(false)
const editingId = ref(null)
const saving = ref(false)
const formError = ref('')

const form = ref({ name: '' })

async function fetchCategories() {
  loading.value = true
  try {
    const { data } = await api.get('/categories/')
    categories.value = data
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

function openModal(cat = null) {
  formError.value = ''
  if (cat) {
    editing.value = true
    editingId.value = cat.id
    form.value = { name: cat.name }
  } else {
    editing.value = false
    editingId.value = null
    form.value = { name: '' }
  }
  showModal.value = true
}

async function saveCategory() {
  formError.value = ''
  saving.value = true
  try {
    if (editing.value) {
      await api.put(`/categories/${editingId.value}`, form.value)
    } else {
      await api.post('/categories/', form.value)
    }
    showModal.value = false
    fetchCategories()
  } catch (e) {
    formError.value = e.response?.data?.detail || t('error_occurred')
  } finally {
    saving.value = false
  }
}

async function deleteCategory(id) {
  if (!confirm(t('confirm_delete_category'))) return
  try {
    await api.delete(`/categories/${id}`)
    fetchCategories()
  } catch (e) {
    alert(e.response?.data?.detail || t('delete_failed'))
  }
}

onMounted(fetchCategories)
</script>

<style scoped>
.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.action-btns {
  display: flex;
  gap: 6px;
}

.error-msg {
  color: var(--danger);
  font-size: 14px;
  margin-bottom: 8px;
}
</style>
