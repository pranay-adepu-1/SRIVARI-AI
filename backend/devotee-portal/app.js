// Srivari AI (శ్రీవారి AI) - Devotee Web Portal Script
let currentLanguage = localStorage.getItem('srivari_lang') || 'en';
let devoteeToken = localStorage.getItem('srivari_devotee_token') || null;
let currentSessionId = localStorage.getItem('srivari_session_id') || null;

const API_BASE = window.location.origin + '/api/v1';

// DOM Elements
const chatMessages = document.getElementById('chat-messages');
const chatForm = document.getElementById('chat-form');
const chatInput = document.getElementById('chat-input');
const btnSend = document.getElementById('btn-send');
const langToggleBtn = document.getElementById('lang-toggle-btn');
const langEnSegment = document.getElementById('lang-en');
const langTeSegment = document.getElementById('lang-te');
const announcementsList = document.getElementById('announcements-list');

// Translations Dictionary
const translations = {
  en: {
    brandTagline: "Tirumala Devotee Assistant",
    btnTtd: "TTD Official Portal",
    disclaimerTag: "Devotee Notice:",
    disclaimerText: "Srivari AI is an independent informational guide and is <strong>not</strong> officially affiliated with TTD. All bookings must be completed directly on <a href='https://ttdevasthanams.ap.gov.in/' target='_blank' rel='noopener'>ttdevasthanams.ap.gov.in</a>.",
    heroTitle: "Welcome to <span>Srivari AI</span>",
    heroSubtitle: "Your intelligent guide for Lord Venkateswara Darshan timings, ₹300 tickets, Srivari Seva registration, Tirumala cottages, and official announcements.",
    chatHeaderTitle: "Ask Srivari Devotional Assistant",
    chatHeaderSub: "Verified TTD Data & RAG Engine",
    welcomeMessage: "<strong>Om Namo Venkatesaya! (ఓం నమో వేంకటేశాయ!)</strong><br><br>Welcome to Srivari AI. How may I assist your pilgrimage today? You can ask questions in English or Telugu regarding ₹300 Special Entry Darshan, free Sarva Darshan tokens, Srivari Seva voluntary service, room bookings, laddu prasadam, or dress code.",
    inputPlaceholder: "Ask in English or Telugu (e.g. ₹300 darshan rules)...",
    btnSendLabel: "Ask",
    panelAnnTitle: "Official TTD Announcements",
    panelGuidesTitle: "Quick Pilgrimage Guides",
    connectingNotice: "Connecting to Srivari AI... this may take up to 30 seconds if the server is waking up.",
    connectingSub: "Checking verified official TTD knowledge base...",
    errorFallbackText: "Unable to load real-time announcements at this moment due to a network or server delay.",
    retryBtn: "🔄 Retry Announcements",
    officialLink: "Visit Official news.tirumala.org ↗",
    officialCitationsHeader: "Official Citations:",
    askAssistant: "Ask Assistant →",
    footerDisclaimer: "Srivari AI (శ్రీవారి AI) is an independent non-commercial informational tool built to help pilgrims navigate official temple guidelines. It has no official affiliation with Tirumala Tirupati Devasthanams (TTD). Official darshan tickets, accommodation, and arjitha seva tokens must be booked strictly on <a href='https://ttdevasthanams.ap.gov.in/' target='_blank' rel='noopener' style='color: var(--gold);'>ttdevasthanams.ap.gov.in</a>.",
    chips: [
      { text: "₹300 Darshan Timings", query: "What are the rules and timings for ₹300 Special Entry Darshan?" },
      { text: "Srivari Seva Registration", query: "How to register for Srivari Seva voluntary service?" },
      { text: "Dress Code Rules", query: "What is the mandatory dress code for Tirumala darshan?" },
      { text: "Room Booking Rules", query: "How does accommodation checkout deposit refund work?" }
    ],
    guides: {
      sed: {
        title: "₹300 Darshan (SED)",
        desc: "Online booking mandatory; Traditional attire required.",
        query: "What are the rules, timings, and booking guidelines for ₹300 Special Entry Darshan?"
      },
      seva: {
        title: "Srivari Seva",
        desc: "Voluntary service (Ages 18-60); 100% free registration.",
        query: "How do I register for Srivari Seva voluntary service and what are the age and eligibility rules?"
      },
      accommodation: {
        title: "Accommodation",
        desc: "Max 24-hr stay; Caution deposit auto-refunded to bank.",
        query: "What are the rules for Tirumala room booking, 24-hour limit, and caution deposit refund?"
      },
      dresscode: {
        title: "Dress Code",
        desc: "Men: Dhoti/Pyjama; Women: Saree/Chudidar with Dupatta.",
        query: "What is the mandatory traditional dress code and prohibited electronic items for Tirumala darshan?"
      }
    }
  },
  te: {
    brandTagline: "తిరుమల భక్తుల సహాయకుడు",
    btnTtd: "టీటీడీ అధికారిక పోర్టల్",
    disclaimerTag: "భక్తుల గమనిక:",
    disclaimerText: "శ్రీవారి AI అనేది భక్తులకు అధికారిక సమాచారాన్ని అందించడానికి రూపొందించబడిన స్వతంత్ర సమాచార వేదిక. దీనికి టీటీడీతో ఎలాంటి ప్రత్యక్ష అధికారిక అనుబంధం లేదు. అన్ని బుకింగ్స్ <a href='https://ttdevasthanams.ap.gov.in/' target='_blank' rel='noopener'>ttdevasthanams.ap.gov.in</a> ద్వారా మాత్రమే చేసుకోవాలి.",
    heroTitle: "<span>శ్రీవారి AI</span> కి స్వాగతం",
    heroSubtitle: "శ్రీ వేంకటేశ్వర స్వామివారి దర్శన సమయాలు, రూ. 300 టికెట్లు, శ్రీవారి సేవ, గదుల కేటాయింపు మరియు అధికారిక ప్రకటనల కొరకు మీ సహాయకుడు.",
    chatHeaderTitle: "శ్రీవారి భక్తి సహాయకుడిని అడగండి",
    chatHeaderSub: "ధృవీకరించబడిన టీటీడీ సమాచారం & RAG ఇంజిన్",
    welcomeMessage: "<strong>ఓం నమో వేంకటేశాయ! (Om Namo Venkatesaya!)</strong><br><br>శ్రీవారి AI కి స్వాగతం. మీ తీర్థయాత్రలో మీకు ఎలా సహాయపడగలను? రూ. 300 ప్రత్యేక ప్రవేశ దర్శనం, ఉచిత సర్వ దర్శనం టోకెన్లు, శ్రీవారి సేవ ఆన్‌లైన్ రిజిస్ట్రేషన్, గదుల బుకింగ్, లడ్డూ ప్రసాదం లేదా సాంప్రదాయ వస్త్రధారణ నియమాల గురించి ఇంగ్లీషు లేదా తెలుగులో అడగవచ్చు.",
    inputPlaceholder: "తెలుగు లేదా ఇంగ్లీషులో అడగండి (ఉదా: రూ. 300 దర్శనం నియమాలు)...",
    btnSendLabel: "అడగండి",
    panelAnnTitle: "టీటీడీ అధికారిక ప్రకటనలు",
    panelGuidesTitle: "ముఖ్యమైన యాత్ర మార్గదర్శకాలు",
    connectingNotice: "శ్రీవారి AI కనెక్ట్ అవుతోంది... సర్వర్ ప్రారంభమయ్యేందుకు 30 సెకన్లు పట్టవచ్చు.",
    connectingSub: "టీటీడీ అధికారిక సమాచారాన్ని పరిశీలిస్తోంది...",
    errorFallbackText: "నెట్‌వర్క్ లేదా సర్వర్ ఆలస్యం కారణంగా లైవ్ ప్రకటనలు లోడ్ కాలేదు.",
    retryBtn: "🔄 మళ్ళీ ప్రయత్నించండి",
    officialLink: "అధికారిక news.tirumala.org ని సందర్శించండి ↗",
    officialCitationsHeader: "అధికారిక మూలాలు:",
    askAssistant: "సహాయకుడిని అడగండి →",
    footerDisclaimer: "శ్రీవారి AI అనేది భక్తులకు ఖచ్చితమైన మరియు అధికారిక సమాచారాన్ని అందించడానికి రూపొందించబడిన స్వతంత్ర సమాచార వేదిక. దీనికి తిరుమల తిరుపతి దేవస్థానం (టీటీడీ) తో ఎలాంటి ప్రత్యక్ష అధికారిక అనుబంధం లేదు. అధికారిక దర్శనం, సేవలు మరియు వసతి బుకింగ్స్ <a href='https://ttdevasthanams.ap.gov.in/' target='_blank' rel='noopener' style='color: var(--gold);'>ttdevasthanams.ap.gov.in</a> ద్వారా మాత్రమే చేసుకోవాలి.",
    chips: [
      { text: "రూ. 300 దర్శనం సమయాలు", query: "రూ. 300 ప్రత్యేక ప్రవేశ దర్శనం నియమాలు మరియు సమయాలు ఏమిటి?" },
      { text: "శ్రీవారి సేవ రిజిస్ట్రేషన్", query: "శ్రీవారి సేవ ఆన్‌లైన్ రిజిస్ట్రేషన్ ఎలా చేయాలి?" },
      { text: "వస్త్రధారణ నిబంధనలు", query: "శ్రీవారి దర్శనానికి సాంప్రదాయ దుస్తుల నిబంధన ఏమిటి?" },
      { text: "గదుల బుకింగ్ నిబంధనలు", query: "తిరుమలలో రూమ్ కాషన్ డిపాజిట్ రీఫండ్ ఎలా జరుగుతుంది?" }
    ],
    guides: {
      sed: {
        title: "రూ. 300 దర్శనం (SED)",
        desc: "ఆన్‌లైన్ బుకింగ్ తప్పనిసరి; సాంప్రదాయ వస్త్రధారణ నిబంధన.",
        query: "రూ. 300 ప్రత్యేక ప్రవేశ దర్శనం నియమాలు, సమయాలు మరియు బుకింగ్ మార్గదర్శకాలు ఏమిటి?"
      },
      seva: {
        title: "శ్రీవారి సేవ",
        desc: "స్వచ్ఛంద సేవ (వయస్సు 18-60); 100% ఉచిత రిజిస్ట్రేషన్.",
        query: "శ్రీవారి సేవ స్వచ్ఛంద సేవకు ఎలా రిజిస్టర్ చేసుకోవాలి? వయస్సు మరియు అర్హత నిబంధనలు ఏమిటి?"
      },
      accommodation: {
        title: "తిరుమల వసతి",
        desc: "గరిష్టంగా 24 గంటలు; కాషన్ డిపాజిట్ బ్యాంక్ ఖాతాకు రీఫండ్.",
        query: "తిరుమలలో రూమ్ బుకింగ్, గరిష్ట 24 గంటల పరిమితి మరియు కాషన్ డిపాజిట్ రీఫండ్ నిబంధనలు ఏమిటి?"
      },
      dresscode: {
        title: "దుస్తుల నిబంధన",
        desc: "పురుషులు: పంచె/కుర్తా; మహిళలు: చీర/చుడీదార్ దుపట్టాతో.",
        query: "శ్రీవారి దర్శనానికి తప్పనిసరి సాంప్రదాయ వస్త్రధారణ మరియు నిషేధించబడిన ఎలక్ట్రానిక్ వస్తువుల వివరాలు ఏమిటి?"
      }
    }
  }
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

// Render Quick Prompt Chips
function renderQuickChips() {
  const container = document.getElementById('quick-chips');
  if (!container) return;
  container.innerHTML = '';
  const t = translations[currentLanguage] || translations.en;

  t.chips.forEach(chipData => {
    const chipBtn = document.createElement('button');
    chipBtn.type = 'button';
    chipBtn.className = 'chip-btn';
    chipBtn.textContent = chipData.text;
    chipBtn.setAttribute('data-query', chipData.query);
    chipBtn.onclick = () => submitSpecificQuery(chipData.query);
    container.appendChild(chipBtn);
  });
}

// Update Interactive Guides Text
function updateGuidesUI() {
  const t = translations[currentLanguage] || translations.en;
  document.querySelectorAll('.guide-card-btn').forEach(btn => {
    const key = btn.getAttribute('data-guide');
    if (t.guides[key]) {
      const titleEl = btn.querySelector('.guide-title');
      const descEl = btn.querySelector('.guide-desc');
      const actionEl = btn.querySelector('.guide-card-action');
      if (titleEl) titleEl.textContent = t.guides[key].title;
      if (descEl) descEl.textContent = t.guides[key].desc;
      if (actionEl) actionEl.textContent = t.askAssistant;
    }
  });
}

// Submit a specific query directly to AI assistant
function submitSpecificQuery(queryText) {
  chatInput.value = queryText;
  handleSendMessage();
  // Scroll chat card into focus on mobile
  const chatCard = document.querySelector('.chat-card');
  if (chatCard && window.innerWidth <= 768) {
    chatCard.scrollIntoView({ behavior: 'smooth' });
  }
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
    const t = translations[currentLanguage] || translations.en;
    citationsHtml = `
      <div class="msg-citations">
        <strong>${t.officialCitationsHeader}</strong>
        ${citations.map(c => `
          <a href="${c.url}" target="_blank" rel="noopener">
            🔗 ${c.title} (${c.source})
          </a>
        `).join('')}
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

  // Render suggested questions if returned
  if (suggestedQuestions && suggestedQuestions.length > 0) {
    const container = document.getElementById('quick-chips');
    if (container) {
      container.innerHTML = '';
      suggestedQuestions.forEach(q => {
        const chipBtn = document.createElement('button');
        chipBtn.type = 'button';
        chipBtn.className = 'chip-btn';
        chipBtn.textContent = q;
        chipBtn.onclick = () => submitSpecificQuery(q);
        container.appendChild(chipBtn);
      });
    }
  }
}

// Cold-Start & Typing Indicator (handles Render free-tier cold starts gracefully)
let typingTimer = null;

function showTyping() {
  const t = translations[currentLanguage] || translations.en;
  const typingDiv = document.createElement('div');
  typingDiv.id = 'typing-indicator';
  typingDiv.className = 'msg assistant';
  typingDiv.innerHTML = `
    <div class="msg-bubble cold-start-indicator">
      <div class="spinner-wrapper">
        <svg class="svg-icon spinner" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <path d="M21.5 2v6h-6M21.34 15.57a10 10 0 1 1-.57-8.38l5.67-5.67"/>
        </svg>
      </div>
      <div>
        <p id="cold-start-main">${t.connectingNotice}</p>
        <small id="cold-start-sub">${t.connectingSub}</small>
      </div>
    </div>
  `;
  chatMessages.appendChild(typingDiv);
  chatMessages.scrollTop = chatMessages.scrollHeight;

  // If server is on a cold start, update indicator message after 6 seconds to reassure devotee
  typingTimer = setTimeout(() => {
    const subText = document.getElementById('cold-start-sub');
    if (subText) {
      subText.textContent = currentLanguage === 'te' 
        ? "సర్వర్ నిద్రలేస్తోంది... మీ ప్రశ్నకు సమగ్ర సమాధానం సిద్ధమవుతోంది..."
        : "Server is waking up on cloud instance... processing sacred knowledge retrieval...";
    }
  }, 6000);
}

function removeTyping() {
  if (typingTimer) clearTimeout(typingTimer);
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
        ? "క్షమించండి, టీటీడీ సమాచారాన్ని పొందడంలో తాత్కాలిక సమస్య ఏర్పడింది. దయచేసి కాసేపటి తర్వాత మళ్ళీ ప్రయత్నించండి లేదా అధికారిక పోర్టల్ https://ttdevasthanams.ap.gov.in/ ని చూడండి."
        : "We encountered an issue retrieving verified temple details. Please try again or visit official TTD portal https://ttdevasthanams.ap.gov.in/.");
    }
  } catch (err) {
    removeTyping();
    appendMessage('assistant', currentLanguage === 'te'
      ? "నెట్‌వర్క్ కనెక్షన్ లోపం. దయచేసి మీ ఇంటర్నెట్ కనెక్షన్‌ని పరిశీలించండి."
      : "Network connection error. Please verify your connection or try again shortly.");
  }
}

// Render Announcements Skeleton Loader
function renderAnnouncementsSkeleton() {
  announcementsList.innerHTML = `
    <div class="skeleton-card">
      <div class="skeleton-line short"></div>
      <div class="skeleton-line full"></div>
      <div class="skeleton-line medium"></div>
    </div>
    <div class="skeleton-card">
      <div class="skeleton-line short"></div>
      <div class="skeleton-line full"></div>
      <div class="skeleton-line medium"></div>
    </div>
    <div class="skeleton-card">
      <div class="skeleton-line short"></div>
      <div class="skeleton-line full"></div>
      <div class="skeleton-line medium"></div>
    </div>
  `;
}

// Render Fallback if Announcements API times out or fails
function renderAnnouncementsFallback() {
  const t = translations[currentLanguage] || translations.en;
  announcementsList.innerHTML = `
    <div class="ann-fallback-card">
      <p>${t.errorFallbackText}</p>
      <div class="ann-fallback-actions">
        <button type="button" id="btn-retry-ann" class="btn btn-gold btn-sm">
          ${t.retryBtn}
        </button>
        <a href="https://news.tirumala.org/" target="_blank" rel="noopener" class="btn btn-outline btn-sm">
          ${t.officialLink}
        </a>
      </div>
    </div>
  `;

  const btnRetry = document.getElementById('btn-retry-ann');
  if (btnRetry) {
    btnRetry.addEventListener('click', () => {
      loadAnnouncements();
    });
  }
}

// Load Official Announcements (with 10-second timeout & AbortController)
async function loadAnnouncements() {
  renderAnnouncementsSkeleton();

  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 10000);

  try {
    const res = await fetch(`${API_BASE}/announcements?limit=6`, {
      signal: controller.signal
    });
    clearTimeout(timeoutId);

    if (!res.ok) {
      throw new Error(`Server returned ${res.status}`);
    }

    const data = await res.json();
    announcementsList.innerHTML = '';

    if (!data.items || data.items.length === 0) {
      announcementsList.innerHTML = `<p style="color: var(--text-muted); font-size: 0.85rem; padding: 12px;">No active announcements currently.</p>`;
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
  } catch (err) {
    console.warn("Announcements fetch warning/timeout:", err);
    renderAnnouncementsFallback();
  }
}

// Apply Language Changes to Entire UI
function setLanguage(lang) {
  currentLanguage = lang;
  localStorage.setItem('srivari_lang', lang);

  const t = translations[lang] || translations.en;

  // Toggle button styling
  if (lang === 'en') {
    langEnSegment.classList.add('active');
    langTeSegment.classList.remove('active');
  } else {
    langTeSegment.classList.add('active');
    langEnSegment.classList.remove('active');
  }

  // Update DOM text elements
  document.getElementById('brand-tagline').textContent = t.brandTagline;
  document.getElementById('btn-ttd-label').textContent = t.btnTtd;
  document.getElementById('disclaimer-tag').textContent = t.disclaimerTag;
  document.getElementById('disclaimer-text').innerHTML = t.disclaimerText;
  document.getElementById('hero-title').innerHTML = t.heroTitle;
  document.getElementById('hero-subtitle').textContent = t.heroSubtitle;
  document.getElementById('chat-header-title').textContent = t.chatHeaderTitle;
  document.getElementById('chat-header-sub').textContent = t.chatHeaderSub;
  document.getElementById('chat-input').placeholder = t.inputPlaceholder;
  document.getElementById('btn-send-label').textContent = t.btnSendLabel;
  document.getElementById('panel-ann-title').querySelector('span').textContent = t.panelAnnTitle;
  document.getElementById('panel-guides-title').querySelector('span').textContent = t.panelGuidesTitle;
  document.getElementById('footer-disclaimer-text').innerHTML = t.footerDisclaimer;

  // Update initial welcome bubble if no conversation has taken place
  const welcomeBubble = document.getElementById('welcome-message-bubble');
  if (welcomeBubble && chatMessages.children.length === 1) {
    welcomeBubble.innerHTML = t.welcomeMessage;
  }

  renderQuickChips();
  updateGuidesUI();
  loadAnnouncements();
}

// Event Listeners Initialization
document.addEventListener('DOMContentLoaded', async () => {
  setLanguage(currentLanguage);
  initDevotee();

  // Language Toggle
  langToggleBtn.addEventListener('click', () => {
    setLanguage(currentLanguage === 'en' ? 'te' : 'en');
  });

  // Chat Form Submission
  chatForm.addEventListener('submit', (e) => {
    e.preventDefault();
    handleSendMessage();
  });

  // Static & Dynamic Quick Prompt Chips
  document.querySelectorAll('.chip-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const query = btn.getAttribute('data-query');
      if (query) submitSpecificQuery(query);
    });
  });

  // Interactive Quick Pilgrimage Guides Buttons
  document.querySelectorAll('.guide-card-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const guideKey = btn.getAttribute('data-guide');
      const t = translations[currentLanguage] || translations.en;
      if (t.guides[guideKey]) {
        submitSpecificQuery(t.guides[guideKey].query);
      }
    });
  });
});
