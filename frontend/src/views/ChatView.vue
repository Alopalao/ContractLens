<template>
  <div class="chat-page">
    <div class="coming-soon-wrapper">
      <div class="chat-icon">💬</div>
      <h1>To be worked</h1>
      <p class="coming-tagline">Chat is coming soon.</p>

      <div class="card planned-features">
        <h2>What's Planned</h2>
        <ul>
          <li>Ask questions about any of your uploaded contracts</li>
          <li>Reference analysis results in your questions</li>
          <li>Compare clauses across multiple agreements</li>
          <li>Get explanations of specific legal terms</li>
          <li>Generate questions to ask a lawyer</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<style scoped>
.chat-page {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 70vh;
}
.coming-soon-wrapper { text-align: center; max-width: 540px; width: 100%; }
.chat-icon { font-size: 5rem; margin-bottom: 1rem; }
h1 { font-size: 2.5rem; font-weight: 800; color: var(--text); margin-bottom: .5rem; }
.coming-tagline { color: var(--muted); font-size: 1.1rem; margin-bottom: 2rem; }

.planned-features { text-align: left; }
.planned-features h2 { font-weight: 700; margin-bottom: .9rem; color: var(--primary); }
.planned-features ul { list-style: none; display: flex; flex-direction: column; gap: .6rem; }
.planned-features li {
  padding: .5rem .75rem;
  background: var(--primary-light);
  border-radius: 6px;
  font-size: .92rem;
  color: var(--text);
}
.planned-features li::before { content: '→ '; color: var(--primary); font-weight: 700; }
</style>
