<template>
  <div class="analysis">
    <!-- Summary -->
    <section class="section">
      <h2 class="section-title">📋 Summary</h2>
      <div class="summary-text card">
        <p v-for="(para, i) in paragraphs" :key="i">{{ para }}</p>
      </div>
    </section>

    <!-- Red Flags -->
    <section class="section">
      <h2 class="section-title">
        🚩 Red Flags
        <span class="count-badge">{{ result.red_flags?.length || 0 }}</span>
      </h2>

      <div v-if="!result.red_flags?.length" class="empty-state">No significant red flags detected.</div>

      <div v-for="(flag, i) in sortedFlags" :key="i" class="flag-card card">
        <div class="flag-header">
          <span class="flag-title">{{ flag.title }}</span>
          <span class="badge" :class="`badge-${flag.severity}`">{{ flag.severity }}</span>
        </div>
        <p class="flag-desc">{{ flag.description }}</p>
      </div>
    </section>

    <!-- Similar Cases -->
    <section class="section">
      <h2 class="section-title">
        ⚖️ Reference Cases &amp; Context
        <span class="count-badge">{{ result.similar_cases?.length || 0 }}</span>
      </h2>

      <div v-if="!result.similar_cases?.length" class="empty-state">No reference cases found.</div>

      <div v-for="(item, i) in result.similar_cases" :key="i" class="case-card card">
        <div class="case-header">
          <span class="case-type-badge" :class="`type-${item.type}`">{{ typeLabel(item.type) }}</span>
          <span class="case-title">{{ item.title }}</span>
        </div>
        <p class="case-desc">{{ item.description }}</p>
        <div class="relevance">
          <span class="relevance-label">Relevance:</span> {{ item.relevance }}
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  result: { type: Object, required: true },
})

const paragraphs = computed(() =>
  (props.result.summary || '').split('\n').filter(Boolean)
)

const severityOrder = { high: 0, medium: 1, low: 2 }
const sortedFlags = computed(() =>
  [...(props.result.red_flags || [])].sort(
    (a, b) => (severityOrder[a.severity] ?? 3) - (severityOrder[b.severity] ?? 3)
  )
)

const TYPE_LABELS = {
  court_settlement:  '⚖️ Court Settlement',
  similar_agreement: '📑 Similar Agreement',
  ignored_clause:    '🟢 Clause Rarely Enforced',
  helpful_info:      'ℹ️ Helpful Context',
}
function typeLabel(t) { return TYPE_LABELS[t] || t }
</script>

<style scoped>
.analysis { display: flex; flex-direction: column; gap: 2rem; }

.section-title {
  display: flex;
  align-items: center;
  gap: .6rem;
  font-size: 1.15rem;
  font-weight: 700;
  margin-bottom: .9rem;
  color: var(--text);
}
.count-badge {
  background: var(--primary-light);
  color: var(--primary);
  font-size: .75rem;
  font-weight: 700;
  padding: .1rem .5rem;
  border-radius: 99px;
}

.summary-text { display: flex; flex-direction: column; gap: .8rem; line-height: 1.7; color: var(--text); }

.flag-card { margin-bottom: .75rem; }
.flag-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: .5rem; gap: .5rem; }
.flag-title { font-weight: 700; font-size: 1rem; }
.flag-desc { color: var(--muted); line-height: 1.6; font-size: .92rem; }

.case-card { margin-bottom: .75rem; }
.case-header { display: flex; align-items: center; gap: .6rem; flex-wrap: wrap; margin-bottom: .5rem; }
.case-title { font-weight: 700; font-size: .95rem; }
.case-type-badge {
  font-size: .72rem; font-weight: 700; padding: .2rem .6rem; border-radius: 99px;
}
.type-court_settlement  { background: #e0e7ff; color: #3730a3; }
.type-similar_agreement { background: #f3e8ff; color: #6b21a8; }
.type-ignored_clause    { background: #dcfce7; color: #166534; }
.type-helpful_info      { background: #dbeafe; color: #1e40af; }

.case-desc { color: var(--muted); font-size: .92rem; line-height: 1.6; margin-bottom: .5rem; }
.relevance { font-size: .85rem; background: #f8fafc; border-left: 3px solid var(--primary); padding: .4rem .75rem; border-radius: 0 4px 4px 0; }
.relevance-label { font-weight: 700; color: var(--primary); }

.empty-state { color: var(--muted); font-style: italic; padding: .5rem 0; }
</style>
