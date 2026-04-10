import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '../api'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || null)
  const user = ref(JSON.parse(localStorage.getItem('user') || 'null'))

  const isAuthenticated = computed(() => !!token.value)

  function _persist(t, u) {
    token.value = t
    user.value = u
    localStorage.setItem('token', t)
    localStorage.setItem('user', JSON.stringify(u))
  }

  async function login(username, password) {
    const { data } = await api.post('/auth/login', { username, password })
    _persist(data.access_token, data.user)
  }

  async function register(payload) {
    const { data } = await api.post('/auth/register', payload)
    _persist(data.access_token, data.user)
  }

  async function refreshMe() {
    const { data } = await api.get('/auth/me')
    user.value = data
    localStorage.setItem('user', JSON.stringify(data))
    return data
  }

  async function updateProfile(payload) {
    const { data } = await api.put('/users/me', payload)
    user.value = { ...user.value, ...data }
    localStorage.setItem('user', JSON.stringify(user.value))
    return data
  }

  function logout() {
    token.value = null
    user.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }

  return { token, user, isAuthenticated, login, register, refreshMe, updateProfile, logout }
})
