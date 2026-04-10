<template>
  <div class="chat-page">
    <div class="chat-layout">
      <aside class="chat-sidebar card">
        <div class="sidebar-head">
          <div>
            <h1>Chat With Your Documents</h1>
            <p>Ask Gemini about uploaded contracts and saved analysis results.</p>
          </div>
          <button class="btn btn-secondary btn-sm" @click="loadDocuments">↻ Refresh</button>
        </div>

        <div v-if="loadingDocuments" class="sidebar-loading">
          <div class="spinner"></div>
        </div>

        <div v-else-if="!documents.length" class="empty-docs">
          <p>No analyzed documents yet.</p>
          <p class="empty-sub">Upload and analyze at least one contract from the Analyze tab first.</p>
        </div>

        <template v-else>
          <div class="selection-head">
            <strong>Chat Scope</strong>
            <button class="mini-link" @click="toggleAllDocuments">
              {{ allSelected ? 'Clear all' : 'Select all' }}
            </button>
          </div>

          <ul class="document-list">
            <li
              v-for="doc in documents"
              :key="doc.id"
              class="document-item"
              :class="{ selected: selectedDocumentIds.includes(doc.id) }"
              @click="toggleDocument(doc.id)"
            >
              <div class="document-check">
                <input
                  :checked="selectedDocumentIds.includes(doc.id)"
                  type="checkbox"
                  @click.stop="toggleDocument(doc.id)"
                />
              </div>
              <div class="document-meta">
                <span class="document-name">{{ doc.filename }}</span>
                <span class="document-date">{{ formatDate(doc.created_at) }}</span>
              </div>
            </li>
          </ul>

          <div class="quick-prompts">
            <h2>Try asking</h2>
            <button v-for="prompt in quickPrompts" :key="prompt" class="prompt-chip" @click="usePrompt(prompt)">
              {{ prompt }}
            </button>
          </div>
        </template>
      </aside>

      <section class="chat-main card">
        <div class="chat-header">
          <div>
            <h2>Gemini Legal Q&amp;A</h2>
            <p>
              {{ selectedDocumentIds.length ? `${selectedDocumentIds.length} document(s) selected` : 'Select one or more documents to ground the conversation' }}
            </p>
          </div>
          <button class="btn btn-outline btn-sm" :disabled="!messages.length" @click="clearChat">New chat</button>
        </div>

        <div class="messages-panel">
          <div v-if="!messages.length" class="empty-chat">
            <div class="empty-chat-icon">💬</div>
            <h3>Ask about clauses, risks, or comparisons</h3>
            <p>Gemini will answer using your uploaded document text and stored analysis results.</p>
          </div>

          <div v-for="(message, index) in messages" :key="index" class="message-row" :class="message.role">
            <div class="message-bubble">
              <div class="message-role">{{ message.role === 'user' ? 'You' : 'ContractLens' }}</div>
              <p class="message-content">{{ message.content }}</p>
              <div v-if="message.referencedDocuments?.length" class="reference-list">
                Based on:
                {{ message.referencedDocuments.map((doc) => doc.filename).join(', ') }}
              </div>
            </div>
          </div>

          <div v-if="sending" class="message-row assistant">
            <div class="message-bubble loading-bubble">
              <div class="message-role">ContractLens</div>
              <div class="loading-line"><span class="spinner-sm"></span> Gemini is thinking…</div>
            </div>
          </div>
        </div>

        <div v-if="error" class="error-msg chat-error">{{ error }}</div>

        <form class="composer" @submit.prevent="sendMessage">
          <textarea
            v-model="draft"
            class="composer-input"
            placeholder="Example: Is the arbitration clause likely to prevent me from joining a class action?"
            rows="4"
            :disabled="sending || !documents.length"
          ></textarea>
          <div class="composer-actions">
            <span class="composer-hint">Grounded in selected uploaded documents only</span>
            <button class="btn btn-primary" type="submit" :disabled="sendDisabled">
              <span v-if="sending" class="spinner-sm"></span>
              {{ sending ? 'Sending…' : 'Send' }}
            </button>
          </div>
        </form>
      </section>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import api from '../api'

const documents = ref([])
const selectedDocumentIds = ref([])
const messages = ref([])
const draft = ref('')
const loadingDocuments = ref(false)
const sending = ref(false)
const error = ref('')

const quickPrompts = [
  'What is the biggest risk in these documents for a regular user?',
  'Compare the cancellation terms across the selected contracts.',
  'Which clause should I read carefully before agreeing?',
  'Explain the arbitration language in plain English.',
]

const allSelected = computed(() => (
  documents.value.length > 0 && selectedDocumentIds.value.length === documents.value.length
))

const sendDisabled = computed(() => (
  sending.value || !draft.value.trim() || !selectedDocumentIds.value.length
))

async function loadDocuments() {
  loadingDocuments.value = true
  error.value = ''
  try {
    const { data } = await api.get('/documents/')
    documents.value = data
    if (!selectedDocumentIds.value.length) {
      selectedDocumentIds.value = data.map((doc) => doc.id)
    } else {
      selectedDocumentIds.value = selectedDocumentIds.value.filter((id) => data.some((doc) => doc.id === id))
    }
  } catch (e) {
    error.value = e.response?.data?.detail || 'Failed to load analyzed documents.'
  } finally {
    loadingDocuments.value = false
  }
}

function toggleDocument(id) {
  if (selectedDocumentIds.value.includes(id)) {
    selectedDocumentIds.value = selectedDocumentIds.value.filter((value) => value !== id)
    return
  }
  selectedDocumentIds.value = [...selectedDocumentIds.value, id]
}

function toggleAllDocuments() {
  selectedDocumentIds.value = allSelected.value ? [] : documents.value.map((doc) => doc.id)
}

function usePrompt(prompt) {
  draft.value = prompt
}

function clearChat() {
  messages.value = []
  draft.value = ''
  error.value = ''
}

async function sendMessage() {
  if (sendDisabled.value) return

  error.value = ''
  const userMessage = {
    role: 'user',
    content: draft.value.trim(),
  }
  messages.value = [...messages.value, userMessage]
  const history = messages.value.map(({ role, content }) => ({ role, content }))
  draft.value = ''
  sending.value = true

  try {
    const { data } = await api.post('/chat/', {
      message: userMessage.content,
      document_ids: selectedDocumentIds.value,
      history,
    })

    messages.value = [
      ...messages.value,
      {
        role: 'assistant',
        content: data.answer,
        referencedDocuments: data.referenced_documents,
      },
    ]
  } catch (e) {
    error.value = e.response?.data?.detail || 'Chat request failed.'
    messages.value = messages.value.filter((message, index) => index !== messages.value.length - 1 || message.role !== 'user')
  } finally {
    sending.value = false
  }
}

function formatDate(value) {
  return new Date(value).toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric' })
}

onMounted(loadDocuments)
</script>

<style scoped>
.chat-page { max-width: 1280px; margin: 0 auto; }
.chat-layout { display: grid; grid-template-columns: 340px 1fr; gap: 1.5rem; min-height: 74vh; }

.chat-sidebar,
.chat-main {
  display: flex;
  flex-direction: column;
}

.sidebar-head,
.chat-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 1rem;
}

.sidebar-head h1,
.chat-header h2 {
  font-size: 1.25rem;
  font-weight: 800;
  margin-bottom: .25rem;
}

.sidebar-head p,
.chat-header p,
.empty-sub,
.composer-hint,
.document-date,
.reference-list,
.message-role {
  color: var(--muted);
}

.btn-sm { padding: .35rem .8rem; font-size: .8rem; }

.sidebar-loading,
.empty-docs {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 180px;
  text-align: center;
}

.empty-docs { flex-direction: column; gap: .4rem; }

.selection-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin: 1.25rem 0 .75rem;
}

.mini-link {
  background: none;
  border: none;
  color: var(--primary);
  font-weight: 700;
  cursor: pointer;
}

.document-list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: .6rem;
  margin-bottom: 1.25rem;
}

.document-item {
  display: flex;
  align-items: center;
  gap: .75rem;
  padding: .8rem .9rem;
  border: 1px solid var(--border);
  border-radius: 8px;
  cursor: pointer;
  background: #fff;
}

.document-item.selected {
  border-color: var(--primary);
  background: var(--primary-light);
}

.document-check input { cursor: pointer; }
.document-meta { min-width: 0; display: flex; flex-direction: column; }
.document-name {
  font-weight: 700;
  font-size: .9rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.document-date,
.reference-list,
.message-role,
.composer-hint {
  font-size: .8rem;
}

.quick-prompts h2 {
  font-size: .95rem;
  margin-bottom: .75rem;
}

.quick-prompts {
  display: flex;
  flex-direction: column;
  gap: .55rem;
}

.prompt-chip {
  text-align: left;
  border: 1px solid var(--border);
  background: #fff;
  border-radius: 999px;
  padding: .65rem .9rem;
  cursor: pointer;
  font-size: .86rem;
}

.prompt-chip:hover { border-color: var(--primary); background: var(--primary-light); }

.messages-panel {
  flex: 1;
  min-height: 420px;
  max-height: 62vh;
  overflow: auto;
  margin: 1.25rem 0;
  padding-right: .25rem;
}

.empty-chat {
  min-height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  text-align: center;
  gap: .5rem;
}

.empty-chat-icon { font-size: 3rem; }
.empty-chat h3 { font-size: 1.15rem; }

.message-row {
  display: flex;
  margin-bottom: 1rem;
}

.message-row.user { justify-content: flex-end; }
.message-row.assistant { justify-content: flex-start; }

.message-bubble {
  max-width: min(85%, 720px);
  padding: .9rem 1rem;
  border-radius: 14px;
  border: 1px solid var(--border);
  background: #fff;
  box-shadow: 0 1px 4px rgba(0, 0, 0, .04);
}

.message-row.user .message-bubble {
  background: var(--primary);
  color: #fff;
  border-color: var(--primary);
}

.message-row.user .message-role,
.message-row.user .reference-list {
  color: rgba(255, 255, 255, .85);
}

.message-content {
  white-space: pre-wrap;
  line-height: 1.65;
  margin-top: .35rem;
}

.loading-bubble { min-width: 220px; }
.loading-line { display: flex; align-items: center; gap: .6rem; margin-top: .35rem; }

.chat-error { margin-bottom: 1rem; }

.composer {
  border-top: 1px solid var(--border);
  padding-top: 1rem;
}

.composer-input {
  width: 100%;
  resize: vertical;
  min-height: 110px;
  padding: .9rem 1rem;
  border: 1.5px solid var(--border);
  border-radius: 10px;
  outline: none;
  background: #f8fafc;
  font: inherit;
}

.composer-input:focus {
  border-color: var(--primary);
  background: #fff;
}

.composer-actions {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  margin-top: .8rem;
}

.spinner-sm {
  width: 1rem;
  height: 1rem;
  border: 2px solid rgba(255,255,255,.35);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin .7s linear infinite;
}

.loading-line .spinner-sm {
  border-color: rgba(37, 99, 235, .2);
  border-top-color: var(--primary);
}

@keyframes spin { to { transform: rotate(360deg); } }

@media (max-width: 960px) {
  .chat-layout { grid-template-columns: 1fr; }
  .messages-panel { max-height: none; }
}
</style>
