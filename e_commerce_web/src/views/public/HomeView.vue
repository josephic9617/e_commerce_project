<template>
  <div class="home-page container fade-in">
    <!-- Hero Section -->
    <section class="hero glass-card">
      <div class="hero-content">
        <h1 class="hero-title">{{ $t('hero_title_1') }} <span>{{ $t('hero_title_2') }}</span></h1>
        <p class="hero-subtitle">{{ $t('hero_subtitle') }}</p>
        <div class="hero-search-mobile">
          <input
            type="text"
            class="form-input"
            :placeholder="$t('search_placeholder')"
            v-model="searchQuery"
            @keyup.enter="search"
          />
        </div>
      </div>
    </section>

    <!-- Categories -->
    <section class="section" v-if="categories.length">
      <h2 class="section-title">{{ $t('categories') }}</h2>
      <div class="categories-grid">
        <button
          v-for="cat in categories"
          :key="cat.id"
          class="category-chip"
          :class="{ active: selectedCategory === cat.id }"
          @click="toggleCategory(cat.id)"
        >
          {{ cat.name }}
        </button>
        <button
          class="category-chip"
          :class="{ active: selectedCategory === null }"
          @click="toggleCategory(null)"
        >
          {{ $t('all') }}
        </button>
      </div>
    </section>

    <!-- Products -->
    <section class="section">
      <div class="section-header">
        <h2 class="section-title">{{ $t('products') }}</h2>
        <span class="product-count" v-if="totalProducts > 0">{{ $t('product_count', { count: totalProducts }) }}</span>
      </div>

      <div v-if="loading" class="loader">
        <div class="spinner"></div>
      </div>

      <div v-else-if="products.length === 0" class="empty-state">
        <div class="icon">&#128722;</div>
        <h3>{{ $t('no_results') }}</h3>
        <p>{{ $t('no_results_desc') }}</p>
      </div>

      <div v-else class="product-grid">
        <ProductCard v-for="product in products" :key="product.id" :product="product" />
      </div>

      <!-- Pagination -->
      <div class="pagination" v-if="totalPages > 1">
        <button :disabled="currentPage <= 1" @click="goToPage(currentPage - 1)">&laquo;</button>
        <button
          v-for="p in visiblePages"
          :key="p"
          :class="{ active: p === currentPage }"
          @click="goToPage(p)"
        >
          {{ p }}
        </button>
        <button :disabled="currentPage >= totalPages" @click="goToPage(currentPage + 1)">&raquo;</button>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../../api'
import ProductCard from '../../components/ProductCard.vue'

const route = useRoute()
const router = useRouter()

const products = ref([])
const categories = ref([])
const loading = ref(true)
const selectedCategory = ref(null)
const searchQuery = ref('')
const currentPage = ref(1)
const totalPages = ref(1)
const totalProducts = ref(0)

const visiblePages = computed(() => {
  const pages = []
  const start = Math.max(1, currentPage.value - 2)
  const end = Math.min(totalPages.value, start + 4)
  for (let i = start; i <= end; i++) pages.push(i)
  return pages
})

async function fetchProducts() {
  loading.value = true
  try {
    const params = { page: currentPage.value, per_page: 12 }
    if (selectedCategory.value) params.category_id = selectedCategory.value
    if (searchQuery.value) params.search = searchQuery.value

    const { data } = await api.get('/products/', { params })
    products.value = data.items
    totalPages.value = data.pages
    totalProducts.value = data.total
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

function toggleCategory(id) {
  selectedCategory.value = id
  currentPage.value = 1
  fetchProducts()
}

function goToPage(page) {
  currentPage.value = page
  fetchProducts()
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

function search() {
  currentPage.value = 1
  fetchProducts()
}

// Watch for search query from navbar
watch(() => route.query.search, (val) => {
  if (val) {
    searchQuery.value = val
    currentPage.value = 1
    fetchProducts()
  }
})

onMounted(() => {
  if (route.query.search) {
    searchQuery.value = route.query.search
  }
  fetchCategories()
  fetchProducts()
})
</script>

<style scoped>
.hero {
  padding: 48px 40px;
  margin-bottom: 32px;
  text-align: center;
  background: linear-gradient(135deg, rgba(108, 92, 231, 0.08), rgba(253, 121, 168, 0.08));
}

.hero-title {
  font-size: 42px;
  font-weight: 800;
  margin-bottom: 8px;
}

.hero-title span {
  background: linear-gradient(135deg, var(--primary), var(--accent));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.hero-subtitle {
  font-size: 18px;
  color: var(--text-secondary);
  margin-bottom: 20px;
}

.hero-search-mobile {
  display: none;
  max-width: 400px;
  margin: 0 auto;
}

.section {
  margin-bottom: 32px;
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.section-title {
  font-size: 22px;
  font-weight: 700;
}

.product-count {
  font-size: 14px;
  color: var(--text-secondary);
}

.categories-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 24px;
}

.category-chip {
  padding: 8px 20px;
  border: 1px solid var(--border);
  background: var(--bg-secondary);
  border-radius: var(--radius-full);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: var(--transition);
}

.category-chip:hover {
  border-color: var(--primary-light);
  color: var(--primary);
}

.category-chip.active {
  background: var(--primary);
  color: white;
  border-color: var(--primary);
}

@media (max-width: 768px) {
  .hero {
    padding: 32px 20px;
  }
  .hero-title {
    font-size: 28px;
  }
  .hero-subtitle {
    font-size: 15px;
  }
  .hero-search-mobile {
    display: block;
  }
}
</style>
