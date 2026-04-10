<template>
  <div class="account-page">
    <h1 class="page-title">Account Details</h1>

    <div class="account-grid">
      <!-- Profile card -->
      <div class="card profile-card">
        <div class="profile-avatar">{{ initials }}</div>
        <div class="profile-info">
          <h2>{{ localUser.full_name }}</h2>
          <p>@{{ localUser.username }}</p>
          <p class="member-since">Member since {{ joinDate }}</p>
        </div>
      </div>

      <!-- Edit form -->
      <div class="card edit-card">
        <div class="card-header">
          <h2>Personal Information</h2>
          <button v-if="!editing" class="btn btn-outline btn-sm" @click="startEdit">Edit</button>
          <div v-else class="header-actions">
            <button class="btn btn-secondary btn-sm" @click="cancelEdit">Cancel</button>
            <button class="btn btn-primary btn-sm" :disabled="saving" @click="saveChanges">
              {{ saving ? 'Saving…' : 'Save' }}
            </button>
          </div>
        </div>

        <div class="form-grid">
          <div class="input-group">
            <label>Full Name</label>
            <input v-model="form.full_name" :disabled="!editing" />
          </div>
          <div class="input-group">
            <label>Email</label>
            <input v-model="form.email" type="email" :disabled="!editing" />
          </div>
          <div class="input-group">
            <label>Phone</label>
            <input v-model="form.phone" type="tel" placeholder="Not set" :disabled="!editing" />
          </div>
          <div class="input-group col-span-2">
            <label>Address</label>
            <input v-model="form.address" placeholder="Not set" :disabled="!editing" />
          </div>
        </div>

        <div v-if="successMsg" class="success-msg" style="margin-top:1rem">{{ successMsg }}</div>
        <div v-if="errorMsg" class="error-msg" style="margin-top:1rem">{{ errorMsg }}</div>
      </div>

      <!-- Stats -->
      <div class="card stats-card">
        <h2 class="stats-title">Usage Stats</h2>
        <div class="stats-grid">
          <div class="stat">
            <span class="stat-value">{{ docCount }}</span>
            <span class="stat-label">Documents Analyzed</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import api from '../api'

const auth = useAuthStore()

const localUser = ref({ ...auth.user })
const form = ref({
  full_name: auth.user?.full_name || '',
  email: auth.user?.email || '',
  phone: auth.user?.phone || '',
  address: auth.user?.address || '',
})
const editing = ref(false)
const saving = ref(false)
const successMsg = ref('')
const errorMsg = ref('')
const docCount = ref(0)

const initials = computed(() => {
  const n = localUser.value.full_name || localUser.value.username || '?'
  return n.split(' ').map(w => w[0]).join('').toUpperCase().slice(0, 2)
})

const joinDate = computed(() => {
  const d = localUser.value.created_at
  if (!d) return 'Unknown'
  return new Date(d).toLocaleDateString(undefined, { year: 'numeric', month: 'long' })
})

function startEdit() {
  form.value = {
    full_name: localUser.value.full_name || '',
    email: localUser.value.email || '',
    phone: localUser.value.phone || '',
    address: localUser.value.address || '',
  }
  editing.value = true
  successMsg.value = ''
  errorMsg.value = ''
}

function cancelEdit() {
  editing.value = false
  successMsg.value = ''
  errorMsg.value = ''
}

async function saveChanges() {
  saving.value = true
  errorMsg.value = ''
  successMsg.value = ''
  try {
    const payload = Object.fromEntries(
      Object.entries(form.value).filter(([, v]) => v !== '')
    )
    const updated = await auth.updateProfile(payload)
    localUser.value = { ...localUser.value, ...updated }
    editing.value = false
    successMsg.value = 'Profile updated successfully.'
  } catch (e) {
    errorMsg.value = e.response?.data?.detail || 'Failed to update profile.'
  } finally {
    saving.value = false
  }
}

onMounted(async () => {
  try {
    const me = await auth.refreshMe()
    localUser.value = me
    form.value = {
      full_name: me.full_name || '',
      email: me.email || '',
      phone: me.phone || '',
      address: me.address || '',
    }
  } catch {/* silent */}

  try {
    const { data } = await api.get('/documents/')
    docCount.value = data.length
  } catch {/* silent */}
})
</script>

<style scoped>
.account-page { max-width: 900px; margin: 0 auto; }
.page-title { font-size: 1.6rem; font-weight: 700; margin-bottom: 1.5rem; }

.account-grid { display: grid; grid-template-columns: 1fr 2fr; gap: 1.5rem; }

/* Profile avatar */
.profile-card { display: flex; flex-direction: column; align-items: center; gap: 1rem; text-align: center; }
.profile-avatar {
  width: 80px; height: 80px; border-radius: 50%;
  background: var(--primary); color: #fff;
  display: flex; align-items: center; justify-content: center;
  font-size: 1.8rem; font-weight: 700;
}
.profile-info h2 { font-size: 1.1rem; font-weight: 700; }
.profile-info p { color: var(--muted); font-size: .9rem; margin-top: .2rem; }
.member-since { font-size: .8rem !important; margin-top: .5rem !important; }

/* Edit card */
.edit-card { grid-column: 1 / -1; }
.card-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 1.25rem; }
.card-header h2 { font-size: 1.1rem; font-weight: 700; }
.header-actions { display: flex; gap: .5rem; }
.btn-sm { padding: .35rem .8rem; font-size: .82rem; }

.form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
.col-span-2 { grid-column: 1 / -1; }
.form-grid input:disabled { background: #f1f5f9; color: var(--muted); cursor: default; }

/* Stats */
.stats-card { grid-column: 1 / -1; }
.stats-title { font-weight: 700; margin-bottom: 1rem; }
.stats-grid { display: flex; gap: 2rem; }
.stat { display: flex; flex-direction: column; align-items: center; }
.stat-value { font-size: 2rem; font-weight: 700; color: var(--primary); }
.stat-label { font-size: .82rem; color: var(--muted); }

@media (max-width: 700px) {
  .account-grid { grid-template-columns: 1fr; }
  .form-grid { grid-template-columns: 1fr; }
  .col-span-2 { grid-column: 1; }
}
</style>
