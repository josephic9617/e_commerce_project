<template>
  <div class="auth-page fade-in">
    <div class="auth-card glass-card">
      <div class="auth-header">
        <h2>{{ $t('register_title') }}</h2>
        <p>{{ $t('register_subtitle') }}</p>
      </div>

      <form @submit.prevent="handleRegister">
        <div class="form-group">
          <label class="form-label">{{ $t('name_label') }}</label>
          <input v-model="fullName" class="form-input" :placeholder="$t('name_placeholder')" />
        </div>
        <div class="form-group">
          <label class="form-label">{{ $t('phone_label') }}</label>
          <input v-model="phone" class="form-input" :placeholder="$t('phone_placeholder')" required />
        </div>
        <div class="form-group">
          <label class="form-label">{{ $t('password_label') }}</label>
          <input v-model="password" type="password" class="form-input" :placeholder="$t('password_min')" required />
        </div>
        <div class="form-group">
          <label class="form-label">{{ $t('confirm_password') }}</label>
          <input v-model="confirmPassword" type="password" class="form-input" :placeholder="$t('confirm_password_placeholder')" required />
        </div>

        <p v-if="error" class="error-msg">{{ error }}</p>

        <button type="submit" class="btn btn-primary btn-lg" style="width: 100%" :disabled="loading">
          {{ loading ? $t('creating') : $t('create_account') }}
        </button>
      </form>

      <p class="auth-footer">
        {{ $t('has_account') }} <router-link to="/login">{{ $t('login_title') }}</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../store/auth'
import { useI18n } from 'vue-i18n'

const router = useRouter()
const authStore = useAuthStore()
const { t } = useI18n({ useScope: 'global' })

const fullName = ref('')
const phone = ref('')
const password = ref('')
const confirmPassword = ref('')
const loading = ref(false)
const error = ref('')

async function handleRegister() {
  error.value = ''

  if (password.value !== confirmPassword.value) {
    error.value = t('passwords_not_match')
    return
  }

  loading.value = true
  try {
    await authStore.register(phone.value, password.value, fullName.value || null)
    router.push('/')
  } catch (e) {
    error.value = e.response?.data?.detail || t('register_failed')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-page {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
}

.auth-card {
  width: 100%;
  max-width: 420px;
  padding: 40px;
}

.auth-header {
  text-align: center;
  margin-bottom: 28px;
}

.auth-header h2 {
  font-size: 26px;
  font-weight: 800;
  margin-bottom: 4px;
}

.auth-header p {
  color: var(--text-secondary);
  font-size: 14px;
}

.error-msg {
  color: var(--danger);
  font-size: 14px;
  margin-bottom: 12px;
  font-weight: 500;
}

.auth-footer {
  text-align: center;
  margin-top: 20px;
  font-size: 14px;
  color: var(--text-secondary);
}

.auth-footer a {
  color: var(--primary);
  font-weight: 600;
}
</style>
