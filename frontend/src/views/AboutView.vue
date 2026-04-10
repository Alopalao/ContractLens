<template>
  <div class="about-page">
    <div class="hero card">
      <div class="hero-icon">📄</div>
      <h1>ContractLens</h1>
      <p class="hero-tagline">Know what you're signing before you sign it.</p>
    </div>

    <div class="about-grid">
      <div class="card about-section">
        <h2>Our Mission</h2>
        <p>
          Contracts and user agreements are often dozens of pages of dense legal language designed
          to be hard to read. ContractLens was built to level the playing field — giving everyday
          users clear, plain-language analysis of any document they're asked to sign.
        </p>
        <p>
          Powered by Google Gemini AI, ContractLens identifies hidden risks, flags concerning
          clauses, and surfaces relevant real-world cases so you can make informed decisions.
        </p>
      </div>

      <div class="card about-section">
        <h2>What We Analyze</h2>
        <ul class="feature-list">
          <li v-for="f in features" :key="f.title">
            <span class="feat-icon">{{ f.icon }}</span>
            <div>
              <strong>{{ f.title }}</strong>
              <p>{{ f.desc }}</p>
            </div>
          </li>
        </ul>
      </div>

      <div class="card about-section">
        <h2>How It Works</h2>
        <ol class="steps">
          <li v-for="(step, i) in steps" :key="i">
            <span class="step-num">{{ i + 1 }}</span>
            <div>
              <strong>{{ step.title }}</strong>
              <p>{{ step.desc }}</p>
            </div>
          </li>
        </ol>
      </div>

      <div class="card about-section disclaimer">
        <h2>⚠️ Disclaimer</h2>
        <p>
          ContractLens is an informational tool powered by AI made by a student for an small hackaton.
          It does <strong>not</strong> constitute legal advice. Always consult a qualified attorney 
          before making legal decisions based on a contract or agreement.
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
const features = [
  {
    icon: '📋',
    title: 'Plain-Language Summary',
    desc: 'A clear overview of what the contract actually says — in human terms.',
  },
  {
    icon: '🚩',
    title: 'Red Flag Detection',
    desc: 'Clauses that could harm your rights, ranked by severity (High, Medium, Low).',
  },
  {
    icon: '⚖️',
    title: 'Court Cases & Settlements',
    desc: 'Real-world cases where similar clauses were litigated or settled.',
  },
  {
    icon: '🟢',
    title: 'Rarely-Enforced Clauses',
    desc: 'Scary-sounding provisions that courts have repeatedly refused to uphold.',
  },
  {
    icon: '📑',
    title: 'Comparable Agreements',
    desc: 'Similar user agreements that were revised following public or legal pressure.',
  },
]

const steps = [
  {
    title: 'Upload your document',
    desc: 'Drag and drop a PDF, DOCX, or TXT file onto the Analyze page.',
  },
  {
    title: 'AI analysis',
    desc: 'The document is sent to Google Gemini AI which reads it end-to-end.',
  },
  {
    title: 'Review your results',
    desc: 'Get an instant summary, a list of red flags, and relevant legal context.',
  },
  {
    title: 'Save for later',
    desc: 'All analyses are saved to your account so you can revisit them any time.',
  },
]
</script>

<style scoped>
.about-page { max-width: 900px; margin: 0 auto; display: flex; flex-direction: column; gap: 1.5rem; }

.hero {
  text-align: center;
  padding: 3rem 2rem;
  background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%);
  color: #fff;
  border: none;
}
.hero-icon { font-size: 3.5rem; margin-bottom: .75rem; }
.hero h1 { font-size: 2rem; font-weight: 800; }
.hero-tagline { font-size: 1.1rem; opacity: .85; margin-top: .5rem; }

.about-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; }

.about-section h2 { font-size: 1.1rem; font-weight: 700; margin-bottom: 1rem; color: var(--primary); }
.about-section p { color: var(--muted); line-height: 1.7; font-size: .93rem; }
.about-section p + p { margin-top: .75rem; }

.feature-list { list-style: none; display: flex; flex-direction: column; gap: .85rem; }
.feature-list li { display: flex; gap: .8rem; align-items: flex-start; }
.feat-icon { font-size: 1.3rem; flex-shrink: 0; }
.feature-list p { margin-top: .15rem; }
.feature-list strong { font-size: .93rem; }

.steps { list-style: none; display: flex; flex-direction: column; gap: .85rem; }
.steps li { display: flex; gap: .8rem; align-items: flex-start; }
.step-num {
  min-width: 1.6rem; height: 1.6rem; border-radius: 50%;
  background: var(--primary); color: #fff;
  display: flex; align-items: center; justify-content: center;
  font-size: .8rem; font-weight: 700; flex-shrink: 0;
}
.steps p { margin-top: .15rem; }
.steps strong { font-size: .93rem; }

.disclaimer { grid-column: 1 / -1; background: #fffbeb; border-color: #fcd34d; }
.disclaimer h2 { color: var(--warning); }
.disclaimer strong { color: var(--text); }

@media (max-width: 700px) {
  .about-grid { grid-template-columns: 1fr; }
  .disclaimer { grid-column: 1; }
}
</style>
