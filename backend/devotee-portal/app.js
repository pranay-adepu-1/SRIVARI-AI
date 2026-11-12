// Srivari AI - Devotee Web Portal JavaScript
let currentLanguage = localStorage.getItem('srivari_lang') || 'en';
let devoteeToken = localStorage.getItem('srivari_devotee_token') || null;
let currentSessionId = localStorage.getItem('srivari_session_id') || null;

const API_BASE = window.location.origin + '/api/v1';

// DOM Elements
const chatMessages = document.getElementById('chat-messages');
const chatForm = document.getElementById('chat-form');
const chatInput = document.getElementById('chat-input');
const btnSend = document.getElementById('btn-send');
const langToggleBtn = document.getElementById('lang-toggle');
const announcementsList = document.getElementById('announcements-list');

// Quick prompt questions
const quickQuestions = {
  en: [
    "What are the rules for ₹300 Special Entry Darshan?",
    "How to register for Srivari Seva voluntary service?",
    "What is the dress code for Tirumala darshan?",
    "How does accommodation checkout deposit refund work?",
    "Where can I collect Sarva Darshan (free) tokens in Tirupati?"
  ],
  te: [
    "రూ. 300 ప్రత్యేక ప్రవేశ దర్శనం నియమాలు ఏమిటి?",
    "శ్రీవారి సేవ ఆన్‌లైన్ రిజిస్ట్రేషన్ ఎలా చేయాలి?",
    "శ్రీవారి దర్శనానికి సాంప్రదాయ దుస్తుల నిబంధన ఏమిటి?",
    "తిరుమలలో రూమ్ కాషన్ డిపాజిట్ రీఫండ్ ఎలా జరుగుతుంది?",
    "తిరుపతిలో ఉచిత సర్వ దర్శనం టోకెన్లు ఎక్కడ ఇస్తారు?"
  ]
};

// Initialize devotee session
async function initDevotee() {
  if (devoteeToken) return devoteeToken;

  const deviceId = 'web_' + Math.random().toString(36).substring(2, 12);
  try {
    const res = await fetch(`${API_BASE}/auth/devotee-init`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        device_id: deviceId,
        preferred_language: currentLanguage
      })
    });
    if (res.ok) {
      const data = await res.json();
      devoteeToken = data.access_token;
      localStorage.setItem('srivari_devotee_token', devoteeToken);
      return devoteeToken;
    }
  } catch (err) {
    console.warn("Devotee init error:", err);
  }
  return null;
}

// Render Quick Question Chips
function renderQuickChips() {
  const container = document.getElementById('quick-chips');
  if (!container) return;
  container.innerHTML = '';
  const list = quickQuestions[currentLanguage] || quickQuestions.en;

  list.forEach(q => {
    const chip = document.createElement('span');
    chip.className = 'chip';
    chip.textContent = q;
    chip.onclick = () => {
      chatInput.value = q;
      handleSendMessage();
    };
    container.appendChild(chip);
  });
}

// Append a message to chat window
function appendMessage(sender, text, citations = [], suggestedQuestions = []) {
  const msgDiv = document.createElement('div');
  msgDiv.className = `msg ${sender}`;

  let formatted = text
    .replace(/\n\n/g, '<br><br>')
    .replace(/\n/g, '<br>')
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

  let citationsHtml = '';
  if (citations && citations.length > 0) {
    citationsHtml = `
      <div class="msg-citations">
        <strong>${currentLanguage === 'te' ? 'అధికారిక మూలాలు:' : 'Official Citations:'}</strong>
        ${citations.map(c => `<a href="${c.url}" target="_blank" rel="noopener">🔗 ${c.title} (${c.source})</a>`).join('')}
      </div>
    `;
  }

  msgDiv.innerHTML = `
    <div class="msg-bubble">
      <div>${formatted}</div>
      ${citationsHtml}
    </div>
  `;

  chatMessages.appendChild(msgDiv);
  chatMessages.scrollTop = chatMessages.scrollHeight;

  // Render suggested questions as chips if returned
  if (suggestedQuestions && suggestedQuestions.length > 0) {
    const chipsWrapper = document.getElementById('quick-chips');
    if (chipsWrapper) {
      chipsWrapper.innerHTML = '';
      suggestedQuestions.forEach(q => {
        const chip = document.createElement('span');
        chip.className = 'chip';
        chip.textContent = q;
        chip.onclick = () => {
          chatInput.value = q;
          handleSendMessage();
        };
        chipsWrapper.appendChild(chip);
      });
    }
  }
}

// Show Typing Indicator
function showTyping() {
  const typingDiv = document.createElement('div');
  typingDiv.id = 'typing-indicator';
  typingDiv.className = 'msg assistant';
  typingDiv.innerHTML = `
    <div class="msg-bubble" style="opacity: 0.8; font-style: italic;">
      <span class="material-symbols-outlined" style="font-size: 16px; vertical-align: middle;">sync</span>
      ${currentLanguage === 'te' ? 'శ్రీవారి సమాధానం సిద్ధమవుతోంది...' : 'Consulting official TTD announcements...'}
    </div>
  `;
  chatMessages.appendChild(typingDiv);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

function removeTyping() {
  const typing = document.getElementById('typing-indicator');
  if (typing) typing.remove();
}

// Send Message Handler
async function handleSendMessage() {
  const text = chatInput.value.trim();
  if (!text) return;

  appendMessage('user', text);
  chatInput.value = '';
  showTyping();

  const token = await initDevotee();

  try {
    const headers = { 'Content-Type': 'application/json' };
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    const res = await fetch(`${API_BASE}/chat/query`, {
      method: 'POST',
      headers: headers,
      body: JSON.stringify({
        query: text,
        session_id: currentSessionId,
        language: currentLanguage
      })
    });

    removeTyping();

    if (res.ok) {
      const data = await res.json();
      currentSessionId = data.session_id;
      localStorage.setItem('srivari_session_id', currentSessionId);
      appendMessage('assistant', data.answer, data.citations, data.suggested_questions);
    } else {
      appendMessage('assistant', currentLanguage === 'te' 
        ? "క్షమించండి, సమాధానాన్ని పొందడంలో సాంకేతిక సమస్య ఏర్పడింది. దయచేసి కాసేపటి తర్వాత మళ్ళీ ప్రయత్నించండి."
        : "We encountered an issue retrieving verified temple details. Please try again or check official portal https://ttdevasthanams.ap.gov.in/.");
    }
  } catch (err) {
    removeTyping();
    appendMessage('assistant', "Network connection error. Please ensure you are connected to the internet.");
  }
}

// Load Official Announcements
async function loadAnnouncements() {
  try {
    const res = await fetch(`${API_BASE}/announcements?limit=6`);
    if (res.ok) {
      const data = await res.json();
      announcementsList.innerHTML = '';

      if (!data.items || data.items.length === 0) {
        announcementsList.innerHTML = `<p style="color: var(--text-muted); font-size: 0.85rem;">No active announcements currently.</p>`;
        return;
      }

      data.items.forEach(ann => {
        const item = document.createElement('div');
        item.className = 'ann-item';

        const isTe = currentLanguage === 'te';
        const title = isTe && ann.title_te ? ann.title_te : ann.title_en;
        const content = isTe && ann.content_te ? ann.content_te : ann.content_en;
        const dateStr = ann.publication_date ? new Date(ann.publication_date).toLocaleDateString() : 'Official Notice';

        item.innerHTML = `
          <div class="ann-item-header">
            ${ann.is_quota_alert ? `<span class="ann-badge-quota">⚡ ${isTe ? 'కోటా అప్‌డేట్' : 'QUOTA ALERT'}</span>` : `<span></span>`}
            <span class="ann-date">${dateStr}</span>
          </div>
          <h4>${title}</h4>
          <p>${content.length > 140 ? content.substring(0, 140) + '...' : content}</p>
          <a href="${ann.source_url}" target="_blank" rel="noopener" class="ann-link">
            ${isTe ? 'అధికారిక వివరాలు' : 'Read Official Source'} →
          </a>
        `;
        announcementsList.appendChild(item);
      });
    }
  } catch (err) {
    console.warn("Error loading announcements:", err);
  }
}

// Language Switch Handler
function setLanguage(lang) {
  currentLanguage = lang;
  localStorage.setItem('srivari_lang', lang);
  langToggleBtn.textContent = lang === 'en' ? 'తెలుగు' : 'English';
  renderQuickChips();
  loadAnnouncements();
}

// Event Listeners
document.addEventListener('DOMContentLoaded', async () => {
  renderQuickChips();
  initDevotee();
  loadAnnouncements();

  langToggleBtn.addEventListener('click', () => {
    setLanguage(currentLanguage === 'en' ? 'te' : 'en');
  });

  chatForm.addEventListener('submit', (e) => {
    e.preventDefault();
    handleSendMessage();
  });
});
