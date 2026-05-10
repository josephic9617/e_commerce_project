<template>
  <div class="admin-products fade-in">
    <div class="page-header">
      <h2>{{ t('admin_products') }}</h2>
      <button class="btn btn-primary" @click="openModal()">+ {{ t('new_product') }}</button>
    </div>

    <div class="filters glass-card">
      <input v-model="searchQuery" class="form-input" :placeholder="t('search_placeholder')" @input="debouncedSearch" />
      <select v-model="filterCategory" class="form-input" @change="fetchProducts" style="max-width: 200px">
        <option :value="null">{{ t('all_categories') }}</option>
        <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
      </select>
    </div>

    <div v-if="loading" class="loader"><div class="spinner"></div></div>

    <div v-else class="table-wrapper">
      <table class="table">
        <thead>
          <tr>
            <th>{{ t('th_id') }}</th>
            <th>{{ t('th_image') }}</th>
            <th>{{ t('th_name') }}</th>
            <th>{{ t('th_category') }}</th>
            <th>{{ t('th_price_usd') }}</th>
            <th>{{ t('th_stock') }}</th>
            <th>{{ t('th_status') }}</th>
            <th>{{ t('th_actions') }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="product in products" :key="product.id">
            <td>{{ product.id }}</td>
            <td>
              <div class="table-img">
                <img :src="product.image_url || '/placeholder.svg'" :alt="product.name" />
              </div>
            </td>
            <td><strong>{{ product.name }}</strong></td>
            <td>{{ product.category_name }}</td>
            <td>${{ product.price_usd.toFixed(2) }}</td>
            <td>{{ product.stock }}</td>
            <td>
              <span class="badge" :class="product.is_active ? 'badge-delivered' : 'badge-cancelled'">
                {{ product.is_active ? t('active') : t('inactive') }}
              </span>
            </td>
            <td>
              <div class="action-btns">
                <button class="btn btn-sm btn-secondary" @click="openModal(product)">&#9998;</button>
                <button class="btn btn-sm btn-danger" @click="deleteProduct(product.id)">&#128465;</button>
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

    <!-- Product Modal -->
    <Modal v-if="showModal" :title="editing ? t('edit_product') : t('new_product')" @close="showModal = false">
      <form @submit.prevent="saveProduct">
        <div class="form-group">
          <label class="form-label">{{ t('th_name') }}</label>
          <input v-model="form.name" class="form-input" required />
        </div>
        <div class="form-group">
          <label class="form-label">{{ t('description_label') }}</label>
          <textarea v-model="form.description" class="form-input"></textarea>
        </div>
        <div class="form-group">
          <label class="form-label">{{ t('th_price_usd') }}</label>
          <input v-model.number="form.price_usd" type="number" step="0.01" class="form-input" required />
        </div>
        <div class="form-group">
          <label class="form-label">{{ t('category_label') }}</label>
          <select v-model.number="form.category_id" class="form-input" required>
            <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
          </select>
        </div>
        <div class="form-group">
          <label class="form-label">{{ t('stock_label') }}</label>
          <input v-model.number="form.stock" type="number" class="form-input" />
        </div>
        <div class="form-group">
          <label class="form-label">{{ t('image_label') }}</label>
          <input type="file" accept="image/*" @change="handleImageUpload" class="form-input" />
          <img v-if="form.image_url" :src="form.image_url" class="preview-img" />
        </div>
        <div class="form-group">
          <label class="form-label">
            <input type="checkbox" v-model="form.is_active" /> {{ t('active') }}
          </label>
        </div>
        <p v-if="formError" class="error-msg">{{ formError }}</p>
      </form>
      <template #footer>
        <button class="btn btn-secondary" @click="showModal = false">{{ t('cancel') }}</button>
        <button class="btn btn-primary" @click="saveProduct" :disabled="saving">
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
const products = ref([])
const categories = ref([])
const loading = ref(true)
const currentPage = ref(1)
const totalPages = ref(1)
const searchQuery = ref('')
const filterCategory = ref(null)

const showModal = ref(false)
const editing = ref(false)
const editingId = ref(null)
const saving = ref(false)
const formError = ref('')

const form = ref({
  name: '',
  description: '',
  price_usd: 0,
  category_id: null,
  stock: 0,
  image_url: '',
  is_active: true,
})

let debounceTimer = null
function debouncedSearch() {
  clearTimeout(debounceTimer)
  debounceTimer = setTimeout(() => {
    currentPage.value = 1
    fetchProducts()
  }, 300)
}

async function fetchProducts() {
  loading.value = true
  try {
    const params = { page: currentPage.value, per_page: 15 }
    if (searchQuery.value) params.search = searchQuery.value
    if (filterCategory.value) params.category_id = filterCategory.value

    const { data } = await api.get('/products/all', { params })
    products.value = data.items
    totalPages.value = data.pages
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

async function fetchCategories() {
  try {
    const { data } = await api.get('/categories/')
    categories.value = data
  } catch (e) {
    console.error(e)
  }
}

function openModal(product = null) {
  formError.value = ''
  if (product) {
    editing.value = true
    editingId.value = product.id
    form.value = {
      name: product.name,
      description: product.description || '',
      price_usd: product.price_usd,
      category_id: product.category_id,
      stock: product.stock,
      image_url: product.image_url || '',
      is_active: product.is_active,
    }
  } else {
    editing.value = false
    editingId.value = null
    form.value = {
      name: '',
      description: '',
      price_usd: 0,
      category_id: categories.value[0]?.id || null,
      stock: 0,
      image_url: '',
      is_active: true,
    }
  }
  showModal.value = true
}

async function handleImageUpload(e) {
  const file = e.target.files[0]
  if (!file) return
  const fd = new FormData()
  fd.append('file', file)
  try {
    const { data } = await api.post('/upload/image', fd, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    form.value.image_url = data.url
  } catch (err) {
    formError.value = err.response?.data?.detail || t('image_upload_failed')
  }
}

async function saveProduct() {
  formError.value = ''
  saving.value = true
  try {
    if (editing.value) {
      await api.put(`/products/${editingId.value}`, form.value)
    } else {
      await api.post('/products/', form.value)
    }
    showModal.value = false
    fetchProducts()
  } catch (e) {
    formError.value = e.response?.data?.detail || t('error_occurred')
  } finally {
    saving.value = false
  }
}

async function deleteProduct(id) {
  if (!confirm(t('confirm_delete_product'))) return
  try {
    await api.delete(`/products/${id}`)
    fetchProducts()
  } catch (e) {
    alert(e.response?.data?.detail || t('delete_failed'))
  }
}

function goToPage(page) {
  currentPage.value = page
  fetchProducts()
}

onMounted(() => {
  fetchCategories()
  fetchProducts()
})
</script>

<style scoped>
.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.filters {
  display: flex;
  gap: 12px;
  padding: 16px;
  margin-bottom: 20px;
}

.table-img {
  width: 50px;
  height: 50px;
  border-radius: var(--radius-sm);
  overflow: hidden;
  background: var(--bg-primary);
}

.table-img img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.action-btns {
  display: flex;
  gap: 6px;
}

.preview-img {
  margin-top: 8px;
  max-height: 120px;
  border-radius: var(--radius-sm);
}

.error-msg {
  color: var(--danger);
  font-size: 14px;
  margin-bottom: 8px;
}

@media (max-width: 768px) {
  .filters {
    flex-direction: column;
  }
}
</style>
