<template>
  <div class="auth-page fade-in">
    <div class="auth-card glass-card">
      <div class="auth-header">
        <h2>{{ $t('register_title') }}</h2>
        <p>{{ $t('register_subtitle') }}</p>
      </div>

      <form @submit.prevent="handleRegister">
        <template v-if="!otpSent">
          <div class="form-group">
            <label class="form-label">{{ $t('name_label') || 'Adyňyz' }}</label>
            <input v-model="fullName" class="form-input" :placeholder="$t('name_placeholder') || 'Adyňyzy giriziň'" />
          </div>
          <div class="form-group">
            <label class="form-label">{{ $t('phone_label') || 'Telefon belgi' }}</label>
            <input v-model="phone" class="form-input" placeholder="+99361XXXXXX" required />
          </div>
          <div class="form-group">
            <label class="form-label">{{ $t('password_label') || 'Parol' }}</label>
            <input v-model="password" type="password" class="form-input" :placeholder="$t('password_min') || 'Iň az 6 simwol'" required />
          </div>
          <div class="form-group">
            <label class="form-label">{{ $t('confirm_password') || 'Paroly tassyklaň' }}</label>
            <input v-model="confirmPassword" type="password" class="form-input" :placeholder="$t('confirm_password_placeholder') || 'Paroly gaýtadan giriziň'" required />
          </div>
        </template>

        <template v-else>
          <div class="form-group">
            <label class="form-label">SMS Kod</label>
            <input v-model="otpCode" type="text" class="form-input" placeholder="Telefona gelen kody giriziň" required />
          </div>
        </template>

        <p v-if="error" class="error-msg">{{ error }}</p>

        <button type="submit" class="btn btn-primary btn-lg" style="width: 100%" :disabled="loading">
          {{ loading ? 'Garaşyň...' : (otpSent ? ($t('create_account') || 'Hasap döret') : 'SMS Kody Iber') }}
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
const otpCode = ref('')
const otpSent = ref(false)
const loading = ref(false)
const error = ref('')

async function handleRegister() {
  error.value = ''

  if (!otpSent.value) {
    if (password.value !== confirmPassword.value) {
      error.value = t('passwords_not_match') || 'Parollar deň däl'
      return
    }
    
    loading.value = true
    try {
      await authStore.sendOtp(phone.value)
      otpSent.value = true
    } catch (e) {
      error.value = e.response?.data?.detail || 'SMS iberip bolmady'
    } finally {
      loading.value = false
    }
    return
  }

  loading.value = true
  try {
    await authStore.register(phone.value, password.value, fullName.value || null, otpCode.value)
    router.push('/')
  } catch (e) {
    error.value = e.response?.data?.detail || t('register_failed') || 'Hasaba alynyp bilinmedi'
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
