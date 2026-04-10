<template>
  <nav class="navbar">
    <div class="nav-brand">
      <span class="brand-icon">📄</span>
      <span class="brand-name">ContractLens</span>
    </div>

    <ul class="nav-tabs">
      <li v-for="tab in tabs" :key="tab.path">
        <RouterLink :to="tab.path" class="nav-tab" :class="{ active: $route.path === tab.path }">
          <span class="tab-icon">{{ tab.icon }}</span>
          {{ tab.label }}
        </RouterLink>
      </li>
    </ul>

    <div class="nav-user">
      <span class="user-name">{{ auth.user?.full_name || auth.user?.username }}</span>
      <button class="btn btn-outline btn-sm" @click="handleLogout">Logout</button>
    </div>
  </nav>
</template>

<script setup>
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'

const auth = useAuthStore()
const router = useRouter()

const tabs = [
  { path: '/analyze', label: 'Analyze', icon: '🔍' },
  { path: '/about',   label: 'About',   icon: 'ℹ️' },
  { path: '/account', label: 'Account', icon: '👤' },
  { path: '/chat',    label: 'Chat',    icon: '💬' },
]

function handleLogout() {
  auth.logout()
  router.push('/login')
}
</script>

<style scoped>
.navbar {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0 2rem;
  height: 60px;
  background: var(--card);
  border-bottom: 1px solid var(--border);
  box-shadow: 0 1px 4px rgba(0,0,0,.06);
  position: sticky;
  top: 0;
  z-index: 100;
}

.nav-brand {
  display: flex;
  align-items: center;
  gap: .5rem;
  text-decoration: none;
  flex-shrink: 0;
}
.brand-icon { font-size: 1.4rem; }
.brand-name { font-size: 1.15rem; font-weight: 700; color: var(--primary); }

.nav-tabs {
  display: flex;
  list-style: none;
  gap: .25rem;
  flex: 1;
  justify-content: center;
}

.nav-tab {
  display: flex;
  align-items: center;
  gap: .3rem;
  padding: .45rem .9rem;
  border-radius: 6px;
  text-decoration: none;
  font-size: .9rem;
  font-weight: 500;
  color: var(--muted);
  transition: background .15s, color .15s;
}
.nav-tab:hover { background: var(--bg); color: var(--text); }
.nav-tab.active { background: var(--primary-light); color: var(--primary); font-weight: 600; }
.tab-icon { font-size: 1rem; }

.nav-user {
  display: flex;
  align-items: center;
  gap: .75rem;
  flex-shrink: 0;
}
.user-name {
  font-size: .85rem;
  font-weight: 600;
  color: var(--muted);
  max-width: 160px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.btn-sm { padding: .35rem .8rem; font-size: .8rem; }
</style>
