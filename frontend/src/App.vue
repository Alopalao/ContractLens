<template>
  <div id="app-root">
    <NavBar v-if="auth.isAuthenticated" />
    <main :class="auth.isAuthenticated ? 'with-nav' : 'no-nav'">
      <RouterView />
    </main>
  </div>
</template>

<script setup>
import { useAuthStore } from './stores/auth'
import NavBar from './components/NavBar.vue'

const auth = useAuthStore()
</script>

<style>
/* ── Reset / globals ──────────────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
  --primary:       #2563eb;
  --primary-dark:  #1d4ed8;
  --primary-light: #dbeafe;
  --danger:        #dc2626;
  --warning:       #d97706;
  --success:       #16a34a;
  --bg:            #f1f5f9;
  --card:          #ffffff;
  --border:        #e2e8f0;
  --text:          #1e293b;
  --muted:         #64748b;
  --radius:        10px;
  --shadow:        0 1px 4px rgba(0,0,0,.08), 0 4px 16px rgba(0,0,0,.06);
}

html, body { height: 100%; font-family: system-ui, -apple-system, sans-serif; background: var(--bg); color: var(--text); }

#app-root { min-height: 100vh; display: flex; flex-direction: column; }

main.with-nav { flex: 1; padding: 2rem 1.5rem; }
main.no-nav   { flex: 1; }

/* ── Utility classes ──────────────────────────────────────────── */
.card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  padding: 1.5rem;
}

.btn {
  display: inline-flex; align-items: center; gap: .4rem;
  padding: .55rem 1.2rem;
  border: none; border-radius: 6px;
  font-size: .9rem; font-weight: 600; cursor: pointer;
  transition: filter .15s, transform .1s;
  text-decoration: none;
}
.btn:active { transform: scale(.97); }
.btn-primary { background: var(--primary); color: #fff; }
.btn-primary:hover { filter: brightness(1.1); }
.btn-secondary { background: var(--border); color: var(--text); }
.btn-secondary:hover { background: #d1d5db; }
.btn-danger { background: var(--danger); color: #fff; }
.btn-danger:hover { filter: brightness(1.1); }
.btn-outline { background: transparent; border: 1.5px solid var(--primary); color: var(--primary); }
.btn-outline:hover { background: var(--primary-light); }
.btn:disabled { opacity: .55; cursor: not-allowed; }

.input-group { display: flex; flex-direction: column; gap: .35rem; }
.input-group label { font-size: .85rem; font-weight: 600; color: var(--muted); text-transform: uppercase; letter-spacing: .04em; }
.input-group input, .input-group textarea, .input-group select {
  padding: .6rem .85rem;
  border: 1.5px solid var(--border);
  border-radius: 6px;
  font-size: .95rem;
  background: #f8fafc;
  outline: none;
  transition: border-color .15s;
}
.input-group input:focus, .input-group textarea:focus { border-color: var(--primary); background: #fff; }

.badge {
  display: inline-block;
  padding: .2rem .6rem;
  border-radius: 99px;
  font-size: .75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: .05em;
}
.badge-high    { background: #fee2e2; color: #b91c1c; }
.badge-medium  { background: #fef3c7; color: #92400e; }
.badge-low     { background: #dcfce7; color: #166534; }

.spinner {
  width: 2.2rem; height: 2.2rem;
  border: 3px solid var(--border);
  border-top-color: var(--primary);
  border-radius: 50%;
  animation: spin .7s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

.error-msg { color: var(--danger); font-size: .9rem; padding: .5rem .75rem; background: #fee2e2; border-radius: 6px; }
.success-msg { color: var(--success); font-size: .9rem; padding: .5rem .75rem; background: #dcfce7; border-radius: 6px; }
</style>
