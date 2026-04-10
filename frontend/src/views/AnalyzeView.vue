<template>
  <div class="analyze-page">
    <div class="page-layout">
      <!-- ── Left column: upload + results ── -->
      <div class="main-col">
        <h1 class="page-title">Analyze a Contract</h1>

        <!-- Upload area -->
        <div
          class="upload-zone card"
          :class="{ dragging, 'has-file': selectedFile }"
          @dragover.prevent="dragging = true"
          @dragleave="dragging = false"
          @drop.prevent="onDrop"
          @click="fileInput.click()"
        >
          <input ref="fileInput" type="file" accept=".pdf,.docx,.txt" hidden @change="onFileChange" />

          <div v-if="!selectedFile" class="upload-placeholder">
            <span class="upload-icon">📂</span>
            <p class="upload-hint">Drag &amp; drop your contract here</p>
            <p class="upload-sub">or <span class="link">click to browse</span> — PDF, DOCX, TXT supported</p>
          </div>

          <div v-else class="file-preview">
            <span class="file-icon">{{ fileIcon }}</span>
            <div>
              <p class="file-name">{{ selectedFile.name }}</p>
              <p class="file-size">{{ fileSizeLabel }}</p>
            </div>
            <button class="clear-btn" @click.stop="clearFile">✕</button>
          </div>
        </div>

        <div class="upload-actions">
          <button
            class="btn btn-primary"
            :disabled="!selectedFile || analyzing"
            @click="runAnalysis"
          >
            <span v-if="analyzing" class="spinner-sm"></span>
            {{ analyzing ? 'Analyzing…' : '🔍 Analyze Document' }}
          </button>
          <p v-if="analyzing" class="analyzing-hint">
            Sending to Gemini AI — this may take a few seconds…
          </p>
        </div>

        <div v-if="error" class="error-msg" style="margin-top:1rem">{{ error }}</div>

        <!-- Analysis result -->
        <div v-if="currentResult" class="result-wrapper">
          <div class="result-meta card">
            <span class="result-file">📄 {{ currentResult.filename }}</span>
            <span class="result-date">{{ formatDate(currentResult.created_at) }}</span>
          </div>
          <AnalysisResult :result="currentResult.analysis" />
        </div>
      </div>

      <!-- ── Right column: history ── -->
      <aside class="history-col">
        <div class="history-header">
          <h2 class="history-title">📁 Document History</h2>
          <button class="btn btn-secondary btn-sm" @click="loadHistory">↻ Refresh</button>
        </div>

        <div v-if="historyLoading" class="history-loading">
          <div class="spinner"></div>
        </div>

        <p v-else-if="!history.length" class="empty-history">No documents yet.</p>

        <ul v-else class="history-list">
          <li
            v-for="doc in history"
            :key="doc.id"
            class="history-item"
            :class="{ active: currentResult?.id === doc.id }"
            @click="selectHistoryItem(doc)"
          >
            <div class="hi-info">
              <span class="hi-name">{{ doc.filename }}</span>
              <span class="hi-date">{{ formatDate(doc.created_at) }}</span>
            </div>
            <button
              class="del-btn"
              title="Delete"
              @click.stop="deleteDoc(doc.id)"
            >🗑</button>
          </li>
        </ul>
      </aside>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import api from '../api'
import AnalysisResult from '../components/AnalysisResult.vue'

const fileInput = ref(null)
const selectedFile = ref(null)
const dragging = ref(false)
const analyzing = ref(false)
const error = ref('')
const currentResult = ref(null)

const history = ref([])
const historyLoading = ref(false)

const FILE_ICONS = { pdf: '📕', docx: '📘', doc: '📘', txt: '📄' }
const fileIcon = computed(() => {
  const ext = selectedFile.value?.name.split('.').pop().toLowerCase()
  return FILE_ICONS[ext] || '📄'
})
const fileSizeLabel = computed(() => {
  const s = selectedFile.value?.size || 0
  return s < 1024 * 1024 ? `${(s / 1024).toFixed(1)} KB` : `${(s / 1024 / 1024).toFixed(1)} MB`
})

function onFileChange(e) {
  const f = e.target.files[0]
  if (f) selectedFile.value = f
}
function onDrop(e) {
  dragging.value = false
  const f = e.dataTransfer.files[0]
  if (f) selectedFile.value = f
}
function clearFile() {
  selectedFile.value = null
  if (fileInput.value) fileInput.value.value = ''
}

async function runAnalysis() {
  if (!selectedFile.value) return
  error.value = ''
  analyzing.value = true
  currentResult.value = null

  const formData = new FormData()
  formData.append('file', selectedFile.value)

  try {
    const { data } = await api.post('/documents/analyze', formData)
    currentResult.value = data
    await loadHistory()
  } catch (e) {
    error.value = e.response?.data?.detail || 'Analysis failed. Please try again.'
  } finally {
    analyzing.value = false
  }
}

async function loadHistory() {
  historyLoading.value = true
  try {
    const { data } = await api.get('/documents/')
    history.value = data
  } catch {
    // silent
  } finally {
    historyLoading.value = false
  }
}

function selectHistoryItem(doc) {
  currentResult.value = doc
}

async function deleteDoc(id) {
  if (!confirm('Delete this document and its analysis?')) return
  try {
    await api.delete(`/documents/${id}`)
    if (currentResult.value?.id === id) currentResult.value = null
    await loadHistory()
  } catch (e) {
    alert(e.response?.data?.detail || 'Could not delete document.')
  }
}

function formatDate(d) {
  if (!d) return ''
  return new Date(d).toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric' })
}

onMounted(loadHistory)
</script>

<style scoped>
.analyze-page { max-width: 1280px; margin: 0 auto; }

.page-title { font-size: 1.6rem; font-weight: 700; margin-bottom: 1.5rem; }

.page-layout { display: grid; grid-template-columns: 1fr 300px; gap: 2rem; }

/* Upload zone */
.upload-zone {
  border: 2px dashed var(--border);
  cursor: pointer;
  transition: border-color .2s, background .2s;
  padding: 2.5rem;
  text-align: center;
  margin-bottom: 1rem;
}
.upload-zone:hover, .upload-zone.dragging { border-color: var(--primary); background: var(--primary-light); }
.upload-zone.has-file { border-style: solid; border-color: var(--primary); }

.upload-icon { font-size: 2.5rem; display: block; margin-bottom: .6rem; }
.upload-hint { font-weight: 600; font-size: 1rem; color: var(--text); }
.upload-sub { font-size: .85rem; color: var(--muted); margin-top: .3rem; }
.link { color: var(--primary); text-decoration: underline; cursor: pointer; }

.file-preview { display: flex; align-items: center; gap: 1rem; text-align: left; }
.file-icon { font-size: 2rem; }
.file-name { font-weight: 600; font-size: .95rem; word-break: break-all; }
.file-size { font-size: .8rem; color: var(--muted); margin-top: .15rem; }
.clear-btn { margin-left: auto; background: none; border: none; font-size: 1rem; cursor: pointer; color: var(--muted); padding: .25rem .5rem; border-radius: 4px; }
.clear-btn:hover { background: #fee2e2; color: var(--danger); }

.upload-actions { display: flex; align-items: center; gap: 1.2rem; flex-wrap: wrap; }
.analyzing-hint { font-size: .85rem; color: var(--muted); font-style: italic; }
.spinner-sm { width: 1rem; height: 1rem; border: 2px solid rgba(255,255,255,.4); border-top-color: #fff; border-radius: 50%; animation: spin .6s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

.result-wrapper { margin-top: 2rem; display: flex; flex-direction: column; gap: 1rem; }
.result-meta { display: flex; align-items: center; justify-content: space-between; padding: .8rem 1.2rem; }
.result-file { font-weight: 600; }
.result-date { font-size: .82rem; color: var(--muted); }

/* History */
.history-col { display: flex; flex-direction: column; gap: 1rem; }
.history-header { display: flex; align-items: center; justify-content: space-between; gap: .5rem; }
.history-title { font-size: 1rem; font-weight: 700; }
.btn-sm { padding: .3rem .7rem; font-size: .8rem; }
.history-loading { display: flex; justify-content: center; padding: 1.5rem; }
.empty-history { color: var(--muted); font-size: .9rem; font-style: italic; }

.history-list { list-style: none; display: flex; flex-direction: column; gap: .5rem; }
.history-item {
  display: flex;
  align-items: center;
  gap: .5rem;
  padding: .75rem 1rem;
  background: var(--card);
  border: 1.5px solid var(--border);
  border-radius: 8px;
  cursor: pointer;
  transition: border-color .15s, background .15s;
}
.history-item:hover { border-color: var(--primary); background: var(--primary-light); }
.history-item.active { border-color: var(--primary); background: var(--primary-light); }
.hi-info { flex: 1; min-width: 0; }
.hi-name { display: block; font-weight: 600; font-size: .88rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.hi-date { font-size: .76rem; color: var(--muted); }
.del-btn { background: none; border: none; cursor: pointer; font-size: .9rem; padding: .15rem .3rem; border-radius: 4px; opacity: .6; transition: opacity .15s; }
.del-btn:hover { opacity: 1; background: #fee2e2; }

@media (max-width: 900px) {
  .page-layout { grid-template-columns: 1fr; }
  .history-col { order: -1; }
}
</style>
