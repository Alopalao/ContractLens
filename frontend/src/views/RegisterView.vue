<template>
  <div class="auth-page">
    <div class="auth-card card">
      <div class="auth-logo">
        <span>📄</span>
        <h1>ContractLens</h1>
        <p>Create your free account</p>
      </div>

      <form @submit.prevent="handleRegister" class="auth-form">
        <div class="input-group">
          <label>Full Name</label>
          <input v-model="form.full_name" type="text" placeholder="Jane Doe" required />
        </div>

        <div class="input-group">
          <label>Email</label>
          <input v-model="form.email" type="email" placeholder="jane@example.com" required autocomplete="email" />
        </div>

        <div class="input-group">
          <label>Username</label>
          <input v-model="form.username" type="text" placeholder="janedoe" required autocomplete="username" />
        </div>

        <div class="input-group">
          <label>Password</label>
          <input v-model="form.password" type="password" placeholder="••••••••" required autocomplete="new-password" minlength="6" />
        </div>

        <div v-if="error" class="error-msg">{{ error }}</div>

        <button type="submit" class="btn btn-primary full-width" :disabled="loading">
          <span v-if="loading" class="spinner-sm"></span>
          {{ loading ? 'Creating account…' : 'Create Account' }}
        </button>
      </form>

      <p class="auth-switch">
        Already have an account?
        <RouterLink to="/login">Sign in</RouterLink>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()
const router = useRouter()

const form = ref({ full_name: '', email: '', username: '', password: '' })
const error = ref('')
const loading = ref(false)

async function handleRegister() {
  error.value = ''
  loading.value = true
  try {
    await auth.register(form.value)
    router.push('/analyze')
  } catch (e) {
    error.value = e.response?.data?.detail || 'Registration failed. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #1e3a8a 0%, #1d4ed8 50%, #2563eb 100%);
  padding: 1rem;
}
.auth-card { width: 100%; max-width: 420px; padding: 2.5rem; }
.auth-logo { text-align: center; margin-bottom: 2rem; }
.auth-logo span { font-size: 3rem; }
.auth-logo h1 { font-size: 1.6rem; font-weight: 700; color: var(--primary); margin: .4rem 0 .2rem; }
.auth-logo p { color: var(--muted); font-size: .9rem; }
.auth-form { display: flex; flex-direction: column; gap: 1.1rem; }
.full-width { width: 100%; justify-content: center; padding: .7rem; font-size: 1rem; }
.auth-switch { margin-top: 1.5rem; text-align: center; font-size: .9rem; color: var(--muted); }
.auth-switch a { color: var(--primary); font-weight: 600; text-decoration: none; }
.auth-switch a:hover { text-decoration: underline; }
.spinner-sm { width: 1rem; height: 1rem; border: 2px solid rgba(255,255,255,.3); border-top-color: #fff; border-radius: 50%; animation: spin .6s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
</style>
