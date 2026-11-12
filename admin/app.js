// Srivari AI (శ్రీవారి AI) - Admin Portal Client Script
const API_BASE = window.location.origin.includes(':8000') 
  ? 'http://localhost:8000/api/v1' 
  : `${window.location.origin}/api/v1`;

let currentAdmin = null;
let categoriesCache = [];

// DOM Elements
const loginContainer = document.getElementById('login-container');
const appContainer = document.getElementById('app-container');
const loginForm = document.getElementById('login-form');
const loginError = document.getElementById('login-error');
const btnSignIn = document.getElementById('btn-sign-in');
const btnTogglePassword = document.getElementById('btn-toggle-password');
const togglePasswordIcon = document.getElementById('toggle-password-icon');
const passwordInput = document.getElementById('password');

const btnLogout = document.getElementById('btn-logout');
const btnHeaderLogout = document.getElementById('btn-header-logout');
const btnQuickSync = document.getElementById('btn-quick-sync');
const btnTriggerScraper = document.getElementById('btn-trigger-scraper');
const modal = document.getElementById('announcement-modal');
const announcementForm = document.getElementById('announcement-form');
const announcementSearch = document.getElementById('announcement-search');

const docModal = document.getElementById('document-modal');
const docForm = document.getElementById('document-form');
const docSearch = document.getElementById('document-search');
const btnUploadDoc = document.getElementById('btn-upload-document');
const btnRefreshDocs = document.getElementById('btn-refresh-docs');

const ragQueryInput = document.getElementById('rag-query-input');
const ragTopkSelect = document.getElementById('rag-topk-select');
const btnRunRAGTest = document.getElementById('btn-run-rag-test');
const ragResultsContainer = document.getElementById('rag-results-container');

// TOAST NOTIFICATIONS
function showToast(message, type = 'info', duration = 4000) {
  const container = document.getElementById('toast-container');
  if (!container) return;

  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  
  const icons = {
    success: 'check_circle',
    error: 'error',
    warning: 'warning',
    info: 'info'
  };

  toast.innerHTML = `
    <span class="material-symbols-outlined">${icons[type] || 'info'}</span>
    <span class="toast-message">${escapeHtml(message)}</span>
    <button class="toast-close" onclick="this.parentElement.remove()">&times;</button>
  `;

  container.appendChild(toast);
  setTimeout(() => {
    toast.classList.add('fade-out');
    setTimeout(() => toast.remove(), 300);
  }, duration);
}

// CENTRALIZED FETCH HELPER WITH credentials: "same-origin"
async function adminFetch(url, options = {}) {
  const headers = { ...(options.headers || {}) };

  const config = {
    ...options,
    headers,
    credentials: 'same-origin'
  };

  try {
    const res = await fetch(url, config);
    if (res.status === 401) {
      showToast('Administrative session expired or unauthorized. Please sign in.', 'error');
      showLogin();
      throw new Error('Unauthorized');
    }
    return res;
  } catch (err) {
    if (err.message !== 'Unauthorized') {
      showToast('Network error: unable to reach server. Please check your connection.', 'error');
    }
    throw err;
  }
}

// INITIALIZATION
document.addEventListener('DOMContentLoaded', () => {
  setupEventListeners();
  checkAdminSession();
});

async function checkAdminSession() {
  try {
    // Try both root /admin/session and prefixed /api/v1/admin/session
    let res = await fetch('/admin/session', { credentials: 'same-origin' });
    if (!res.ok) {
      res = await fetch(`${API_BASE}/admin/session`, { credentials: 'same-origin' });
    }
    if (res.ok) {
      const data = await res.json();
      currentAdmin = data;
      showDashboard();
      return;
    }
  } catch (err) {
    console.debug('No active admin session found:', err);
  }
  showLogin();
}

function setupEventListeners() {
  // Password Visibility Show / Hide Toggle
  if (btnTogglePassword && passwordInput) {
    btnTogglePassword.addEventListener('click', () => {
      const isPassword = passwordInput.type === 'password';
      passwordInput.type = isPassword ? 'text' : 'password';
      togglePasswordIcon.textContent = isPassword ? 'visibility_off' : 'visibility';
    });
  }

  // Admin Login Form
  loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    loginError.classList.add('hidden');
    loginError.textContent = '';

    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value;

    if (!username || !password) {
      loginError.textContent = 'Please enter both username and password.';
      loginError.classList.remove('hidden');
      return;
    }

    btnSignIn.disabled = true;
    const originalText = btnSignIn.innerHTML;
    btnSignIn.innerHTML = '<span class="material-symbols-outlined">hourglass_top</span> Signing in...';

    try {
      // Try root /admin/login first, then API_BASE /admin/login
      let res = await fetch('/admin/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'same-origin',
        body: JSON.stringify({ username, password })
      });

      if (res.status === 404) {
        res = await fetch(`${API_BASE}/admin/login`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          credentials: 'same-origin',
          body: JSON.stringify({ username, password })
        });
      }

      if (res.status === 429) {
        throw new Error('Rate limit exceeded: Maximum 5 failed attempts per 15 minutes reached. Please try again later.');
      }

      if (!res.ok) {
        const errorData = await res.json().catch(() => ({}));
        throw new Error(errorData.detail || 'Invalid administrator username or password.');
      }

      const data = await res.json();
      currentAdmin = {
        username: data.username || username,
        full_name: 'Srivari Admin Officer',
        role: 'super_admin'
      };

      showToast('Signed in successfully as Administrator.', 'success');
      showDashboard();
    } catch (err) {
      loginError.textContent = err.message || 'Authentication failed.';
      loginError.classList.remove('hidden');
      showToast(err.message || 'Authentication failed.', 'error');
    } finally {
      btnSignIn.disabled = false;
      btnSignIn.innerHTML = originalText;
    }
  });

  // Logout Handlers (Sidebar button & Header button)
  const handleLogout = async () => {
    try {
      await fetch('/admin/logout', { method: 'POST', credentials: 'same-origin' });
    } catch (e) {
      try {
        await fetch(`${API_BASE}/admin/logout`, { method: 'POST', credentials: 'same-origin' });
      } catch (err) {}
    }
    currentAdmin = null;
    showToast('Signed out of Admin Portal.', 'info');
    showLogin();
  };

  if (btnLogout) btnLogout.addEventListener('click', handleLogout);
  if (btnHeaderLogout) btnHeaderLogout.addEventListener('click', handleLogout);

  // Navigation Tabs
  document.querySelectorAll('.nav-item').forEach(btn => {
    btn.addEventListener('click', () => {
      const tab = btn.getAttribute('data-tab');
      switchTab(tab);
    });
  });

  // Quick Scraper Sync
  if (btnQuickSync) btnQuickSync.addEventListener('click', runScraperSync);
  if (btnTriggerScraper) btnTriggerScraper.addEventListener('click', runScraperSync);

  // Announcement Search
  let searchTimeout;
  if (announcementSearch) {
    announcementSearch.addEventListener('input', () => {
      clearTimeout(searchTimeout);
      searchTimeout = setTimeout(() => {
        loadAnnouncementsTable(announcementSearch.value);
      }, 300);
    });
  }

  // Add Announcement Button
  const btnAddAnnouncement = document.getElementById('btn-add-announcement');
  if (btnAddAnnouncement) {
    btnAddAnnouncement.addEventListener('click', () => {
      openModalForCreate();
    });
  }

  // Announcement Form Submit
  if (announcementForm) announcementForm.addEventListener('submit', handleAnnouncementSubmit);

  // Knowledge Base Document Controls
  if (btnUploadDoc) btnUploadDoc.addEventListener('click', openDocModal);
  if (btnRefreshDocs) {
    btnRefreshDocs.addEventListener('click', () => {
      loadDocumentsTable(docSearch ? docSearch.value : '');
      showToast('Knowledge sources refreshed.', 'info');
    });
  }
  if (docForm) docForm.addEventListener('submit', handleDocumentSubmit);
  if (docSearch) {
    let docTimeout;
    docSearch.addEventListener('input', () => {
      clearTimeout(docTimeout);
      docTimeout = setTimeout(() => {
        loadDocumentsTable(docSearch.value);
      }, 300);
    });
  }

  // RAG Retrieval Test Controls
  if (btnRunRAGTest) {
    btnRunRAGTest.addEventListener('click', () => {
      runRAGTest(ragQueryInput.value, parseInt(ragTopkSelect.value, 10));
    });
  }
  if (ragQueryInput) {
    ragQueryInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        e.preventDefault();
        runRAGTest(ragQueryInput.value, parseInt(ragTopkSelect.value, 10));
      }
    });
  }
  document.querySelectorAll('.rag-chip').forEach(chip => {
    chip.addEventListener('click', () => {
      const query = chip.getAttribute('data-query');
      if (ragQueryInput) ragQueryInput.value = query;
      runRAGTest(query, parseInt(ragTopkSelect.value, 10));
    });
  });

  // Notification Broadcast Form Submit
  const notifForm = document.getElementById('notification-form');
  if (notifForm) notifForm.addEventListener('submit', handleNotificationBroadcast);

  // Test AI Chat Form Submit
  const testChatForm = document.getElementById('test-chat-form');
  if (testChatForm) testChatForm.addEventListener('submit', handleTestChat);
}

function showLogin() {
  loginContainer.classList.remove('hidden');
  appContainer.classList.add('hidden');
  if (passwordInput) passwordInput.value = '';
}

function showDashboard() {
  loginContainer.classList.add('hidden');
  appContainer.classList.remove('hidden');
  document.getElementById('logged-admin-name').textContent = (currentAdmin && currentAdmin.full_name) || 'Admin Officer';
  document.getElementById('logged-admin-role').textContent = (currentAdmin && currentAdmin.role) || 'Super Admin';

  loadDashboardStats();
  loadCategories();
  loadRecentAnnouncements();
  loadAnnouncementsTable();
  loadDocumentsTable();
}

function switchTab(tabName) {
  document.querySelectorAll('.nav-item').forEach(item => {
    item.classList.toggle('active', item.getAttribute('data-tab') === tabName);
  });

  document.querySelectorAll('.tab-pane').forEach(pane => {
    pane.classList.toggle('active', pane.id === `tab-${tabName}`);
  });

  const titles = {
    'dashboard': ['Dashboard Overview', 'Real-time status of TTD news indexing, knowledge documents, and devotee services.'],
    'announcements': ['Official Announcements', 'Manage indexed press releases, quotas, pinned alerts, and verified updates.'],
    'knowledge-base': ['Knowledge Base & Documents', 'Manage indexed TTD pilgrimage guidelines, rules, circulars, and source chunks.'],
    'rag-test': ['RAG Retrieval Test', 'Inspect semantic search chunks, similarity scores, and guardrails in real-time.'],
    'scraper': ['TTD Ingestion Engine', 'Automated crawler for news.tirumala.org and booking notices.'],
    'notifications': ['Push Broadcast', 'Dispatch immediate quota alerts and daily digests to devotees.'],
    'audit': ['Audit Trail', 'Cryptographic compliance records of administrative operations.'],
    'test-chat': ['Interactive AI Chatbot', 'Verify English and Telugu responses with citations.']
  };

  if (titles[tabName]) {
    document.getElementById('page-title').textContent = titles[tabName][0];
    document.getElementById('page-subtitle').textContent = titles[tabName][1];
  }

  if (tabName === 'knowledge-base') {
    loadDocumentsTable();
  }
}

// DASHBOARD STATS
async function loadDashboardStats() {
  try {
    const res = await adminFetch(`${API_BASE}/admin/dashboard-stats`);
    const data = await res.json();

    const elAnnounce = document.getElementById('stat-announcements');
    if (elAnnounce) elAnnounce.textContent = data.total_announcements ?? 0;

    const elVerified = document.getElementById('stat-verified');
    if (elVerified) elVerified.textContent = data.verified_announcements ?? 0;

    // Total Devotee Queries (KPI Card 3)
    const elQueries = document.getElementById('stat-queries');
    if (elQueries) elQueries.textContent = data.total_queries ?? data.total_messages ?? 0;
    const elQuota = document.getElementById('stat-quotas') || document.getElementById('stat-quota');
    if (elQuota && !elQueries) elQuota.textContent = data.quota_alerts ?? 0;

    // Last Scraper Sync (KPI Card 4)
    const elLastSync = document.getElementById('stat-last-sync');
    if (elLastSync) elLastSync.textContent = data.last_scraper_sync || 'Just now';
    const elUsers = document.getElementById('stat-users');
    if (elUsers && !elLastSync) elUsers.textContent = data.total_users ?? 0;

    // Dynamic Integration Health Timestamps & Status
    if (data.integration_health) {
      const newsTime = document.getElementById('health-news-time');
      if (newsTime) newsTime.textContent = `Polled: ${data.integration_health.news_scraper?.last_checked || data.last_scraper_sync || 'Just now'}`;

      const newsBadge = document.getElementById('health-news-badge');
      if (newsBadge && data.integration_health.news_scraper?.status) {
        newsBadge.textContent = data.integration_health.news_scraper.status;
      }

      const bookingTime = document.getElementById('health-booking-time');
      if (bookingTime) bookingTime.textContent = `Status: ${data.integration_health.booking_portal?.last_checked || 'Active (Real-time)'}`;

      const bookingBadge = document.getElementById('health-booking-badge');
      if (bookingBadge && data.integration_health.booking_portal?.status) {
        bookingBadge.textContent = data.integration_health.booking_portal.status;
      }

      const ragCount = document.getElementById('health-rag-count');
      if (ragCount) {
        const count = data.integration_health.rag_knowledge_engine?.indexed_documents ?? data.knowledge_docs_count ?? 0;
        ragCount.textContent = count;
      }

      const ragBadge = document.getElementById('health-rag-badge');
      if (ragBadge && data.integration_health.rag_knowledge_engine?.status) {
        ragBadge.textContent = data.integration_health.rag_knowledge_engine.status;
      }
    }
  } catch (err) {
    console.error('Failed to load dashboard stats:', err);
  }
}

// CATEGORIES
async function loadCategories() {
  try {
    const res = await fetch(`${API_BASE}/announcements/categories`, { credentials: 'same-origin' });
    categoriesCache = await res.json();
    const select = document.getElementById('modal-category');
    select.innerHTML = categoriesCache.map(c => `
      <option value="${c.id}">${escapeHtml(c.name_en)} (${escapeHtml(c.name_te)})</option>
    `).join('');
  } catch (err) {
    console.error('Failed to load categories:', err);
  }
}

// RECENT ANNOUNCEMENTS
async function loadRecentAnnouncements() {
  const container = document.getElementById('dashboard-recent-list') || document.getElementById('recent-announcements-list');
  if (!container) return;

  // Render animated skeleton loader while fetching
  container.innerHTML = `
    <div class="skeleton-list">
      ${[1, 2, 3, 4].map(() => `
        <div class="skeleton-announcement-item">
          <div class="skeleton-line" style="width: 75%; height: 16px; margin-bottom: 6px;"></div>
          <div class="skeleton-line" style="width: 50%; height: 12px; margin-bottom: 4px;"></div>
          <div class="skeleton-line" style="width: 30%; height: 10px;"></div>
        </div>
      `).join('')}
    </div>
  `;

  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 10000);

  try {
    let res = await fetch(`${API_BASE}/announcements?limit=10`, {
      credentials: 'same-origin',
      signal: controller.signal
    });
    if (!res.ok) {
      res = await fetch(`/announcements?limit=10`, {
        credentials: 'same-origin',
        signal: controller.signal
      });
    }
    clearTimeout(timeoutId);

    if (!res.ok) throw new Error(`HTTP error ${res.status}`);

    const data = await res.json();
    const items = Array.isArray(data) ? data : (data.items || []);

    if (items.length === 0) {
      container.innerHTML = '<p class="text-muted" style="text-align: center; padding: 24px;">No announcements indexed yet.</p>';
      return;
    }

    container.innerHTML = items.map(item => `
      <div class="announcement-item">
        <div class="announcement-info">
          <h4>${item.is_pinned ? '<span class="badge-pinned">📌 Pinned</span> ' : ''}${escapeHtml(item.title_en || '')}</h4>
          ${item.title_te ? `<p class="telugu-text">${escapeHtml(item.title_te)}</p>` : ''}
          <small class="meta">${new Date(item.publication_date).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' })} • ${escapeHtml(item.source_domain || 'news.tirumala.org')}</small>
        </div>
        <span class="badge ${item.is_quota_alert ? 'badge-orange' : 'badge-gold'}">
          ${item.is_quota_alert ? 'Quota Release' : 'Official Notice'}
        </span>
      </div>
    `).join('');
  } catch (err) {
    clearTimeout(timeoutId);
    console.error('Failed to load recent announcements:', err);
    container.innerHTML = `
      <div class="error-state" style="text-align: center; padding: 24px 16px;">
        <p style="color: #b91c1c; font-size: 13.5px; margin-bottom: 12px;">Failed to load announcements (${err.name === 'AbortError' ? 'Request timed out' : 'Network error'}).</p>
        <button class="btn btn-outline btn-sm" onclick="loadRecentAnnouncements()">
          <span class="material-symbols-outlined" style="font-size: 16px; vertical-align: middle;">refresh</span> Retry
        </button>
      </div>
    `;
  }
}

window.loadRecentAnnouncements = loadRecentAnnouncements;

// ANNOUNCEMENTS TABLE
async function loadAnnouncementsTable(searchTerm = '') {
  try {
    const url = searchTerm 
      ? `${API_BASE}/announcements?search=${encodeURIComponent(searchTerm)}&limit=50`
      : `${API_BASE}/announcements?limit=50`;

    const res = await fetch(url, { credentials: 'same-origin' });
    const data = await res.json();
    const tbody = document.getElementById('announcements-table-body');

    if (!data.items || data.items.length === 0) {
      tbody.innerHTML = '<tr><td colspan="8" style="text-align:center; padding:20px;">No announcements found.</td></tr>';
      return;
    }

    tbody.innerHTML = data.items.map(a => `
      <tr>
        <td>
          <strong>${escapeHtml(a.title_en)}</strong><br>
          <small style="color:var(--text-muted);">${escapeHtml(a.title_te)}</small>
        </td>
        <td><span class="badge badge-gold">General</span></td>
        <td><a href="${a.source_url}" target="_blank" style="color:var(--maroon-primary); text-decoration:none;">View TTD Link ↗</a></td>
        <td>${new Date(a.publication_date).toLocaleDateString()}</td>
        <td>${a.is_pinned ? '<span class="badge-pinned">📌 Pinned</span>' : '<span style="color:var(--text-muted); font-size:12px;">Standard</span>'}</td>
        <td>${a.is_quota_alert ? '<span class="badge badge-orange">YES</span>' : 'No'}</td>
        <td>${a.is_verified ? '<span class="badge badge-green">VERIFIED</span>' : '<span class="badge badge-red">Pending</span>'}</td>
        <td>
          <div style="display:flex; gap:6px;">
            <button class="btn btn-outline btn-sm btn-pin" onclick="togglePinAnnouncement('${a.id}', ${!a.is_pinned})" title="Toggle Pin to Top">
              ${a.is_pinned ? 'Unpin' : '📌 Pin'}
            </button>
            <button class="btn btn-outline btn-sm" onclick="editAnnouncement('${a.id}')">Edit</button>
            <button class="btn btn-outline btn-sm" style="color:var(--danger-color)" onclick="deleteAnnouncement('${a.id}')">Delete</button>
          </div>
        </td>
      </tr>
    `).join('');
  } catch (err) {
    console.error('Failed to load table:', err);
  }
}

// SCRAPER SYNC
async function runScraperSync() {
  const logBox = document.getElementById('scraper-result-log');
  logBox.textContent += `\n[${new Date().toLocaleTimeString()}] Triggering TTD scraper poller...`;

  try {
    const res = await adminFetch(`${API_BASE}/admin/scraper/sync`, { method: 'POST' });
    const data = await res.json();
    logBox.textContent += `\n[SUCCESS] Sync completed at ${data.timestamp}`;
    logBox.textContent += `\n- New Announcements Added: ${data.new_announcements}`;
    logBox.textContent += `\n- Verified Announcements Updated: ${data.existing_announcements}`;
    logBox.textContent += `\n- Total Announcements in Knowledge Base: ${data.total_indexed}\n`;

    document.getElementById('scraper-last-run').textContent = `Last run: ${new Date().toLocaleTimeString()} (Indexed ${data.total_indexed} records)`;
    showToast(`TTD news synced successfully (${data.new_announcements} new, ${data.existing_announcements} updated).`, 'success');
    loadDashboardStats();
    loadAnnouncementsTable();
    loadRecentAnnouncements();
  } catch (err) {
    logBox.textContent += `\n[ERROR] Sync failed: ${err.message}\n`;
  }
}

// ANNOUNCEMENT CRUD
function openModalForCreate() {
  document.getElementById('modal-title').textContent = 'New Official Announcement';
  document.getElementById('modal-announcement-id').value = '';
  document.getElementById('announcement-form').reset();
  document.getElementById('modal-is-pinned').checked = false;
  modal.classList.remove('hidden');
}

function closeModal() {
  modal.classList.add('hidden');
}

async function handleAnnouncementSubmit(e) {
  e.preventDefault();
  const id = document.getElementById('modal-announcement-id').value;
  const title_en = document.getElementById('modal-title-en').value.trim();
  const title_te = document.getElementById('modal-title-te').value.trim();
  const content_en = document.getElementById('modal-content-en').value.trim();
  const content_te = document.getElementById('modal-content-te').value.trim();
  const source_url = document.getElementById('modal-source-url').value.trim();
  const category_id = document.getElementById('modal-category').value;
  const is_quota_alert = document.getElementById('modal-is-quota').checked;
  const is_verified = document.getElementById('modal-is-verified').checked;
  const is_pinned = document.getElementById('modal-is-pinned').checked;

  if (!title_en || !title_te || !content_en || !content_te || !source_url) {
    showToast('Validation error: Please fill in all required title, content, and source URL fields.', 'warning');
    return;
  }

  const payload = {
    title_en,
    title_te,
    content_en,
    content_te,
    source_url,
    category_id,
    is_quota_alert,
    is_verified,
    is_pinned,
    publication_date: new Date().toISOString()
  };

  try {
    const url = id ? `${API_BASE}/admin/announcements/${id}` : `${API_BASE}/admin/announcements`;
    const method = id ? 'PUT' : 'POST';

    const res = await adminFetch(url, {
      method,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (!res.ok) {
      const errData = await res.json().catch(() => ({}));
      throw new Error(errData.detail || 'Failed to save announcement');
    }

    closeModal();
    showToast(`Announcement saved successfully${is_pinned ? ' and pinned to top of devotee feed!' : '.'}`, 'success');
    loadDashboardStats();
    loadAnnouncementsTable();
    loadRecentAnnouncements();
  } catch (err) {
    showToast(err.message || 'Error saving announcement.', 'error');
  }
}

async function editAnnouncement(id) {
  try {
    const res = await fetch(`${API_BASE}/announcements/${id}`, { credentials: 'same-origin' });
    const data = await res.json();

    document.getElementById('modal-title').textContent = 'Edit Announcement';
    document.getElementById('modal-announcement-id').value = data.id;
    document.getElementById('modal-title-en').value = data.title_en;
    document.getElementById('modal-title-te').value = data.title_te;
    document.getElementById('modal-content-en').value = data.content_en;
    document.getElementById('modal-content-te').value = data.content_te;
    document.getElementById('modal-source-url').value = data.source_url;
    document.getElementById('modal-is-quota').checked = data.is_quota_alert;
    document.getElementById('modal-is-verified').checked = data.is_verified;
    document.getElementById('modal-is-pinned').checked = !!data.is_pinned;

    modal.classList.remove('hidden');
  } catch (err) {
    showToast('Failed to load announcement for editing.', 'error');
  }
}

async function togglePinAnnouncement(id, willPin) {
  try {
    const res = await adminFetch(`${API_BASE}/admin/announcements/${id}/pin`, { method: 'PUT' });
    if (!res.ok) throw new Error('Failed to toggle pin priority.');
    showToast(willPin ? 'Announcement pinned to top of devotee feed!' : 'Announcement unpinned.', 'success');
    loadAnnouncementsTable(announcementSearch.value);
    loadRecentAnnouncements();
  } catch (err) {
    showToast(err.message || 'Failed to toggle pin state.', 'error');
  }
}

async function deleteAnnouncement(id) {
  if (!confirm('Are you sure you want to delete this official announcement? It will be permanently removed from the public feed and RAG index.')) return;
  try {
    const res = await adminFetch(`${API_BASE}/admin/announcements/${id}`, { method: 'DELETE' });
    if (!res.ok) throw new Error('Deletion failed.');
    showToast('Announcement deleted successfully.', 'success');
    loadDashboardStats();
    loadAnnouncementsTable();
    loadRecentAnnouncements();
  } catch (err) {
    showToast(err.message || 'Deletion failed.', 'error');
  }
}

// KNOWLEDGE BASE & DOCUMENTS MANAGEMENT
function openDocModal() {
  document.getElementById('document-form').reset();
  docModal.classList.remove('hidden');
}

function closeDocModal() {
  docModal.classList.add('hidden');
}

async function loadDocumentsTable(searchTerm = '') {
  const tbody = document.getElementById('documents-table-body');
  if (!tbody) return;

  try {
    const res = await adminFetch(`${API_BASE}/admin/documents`);
    const data = await res.json();

    let items = data.items || [];
    if (searchTerm) {
      const q = searchTerm.toLowerCase();
      items = items.filter(d => 
        (d.title && d.title.toLowerCase().includes(q)) || 
        (d.filename && d.filename.toLowerCase().includes(q))
      );
    }

    if (items.length === 0) {
      tbody.innerHTML = '<tr><td colspan="6" style="text-align:center; padding:20px;">No knowledge documents indexed yet. Click "Upload New Source" above.</td></tr>';
      return;
    }

    tbody.innerHTML = items.map(doc => `
      <tr>
        <td>
          <strong>${escapeHtml(doc.title)}</strong><br>
          <code style="color:var(--text-muted); font-size:11px;">${escapeHtml(doc.filename)}</code>
        </td>
        <td><span class="badge badge-gold">${escapeHtml(doc.source_type || 'Manual Upload')}</span></td>
        <td>${new Date(doc.created_at).toLocaleDateString()}</td>
        <td><span class="badge badge-orange">${doc.chunk_count} Chunks</span></td>
        <td>
          <span class="${doc.status === 'Indexed' ? 'badge-indexed' : 'badge-failed'}">
            ● ${escapeHtml(doc.status || 'Indexed')}
          </span>
        </td>
        <td>
          <button class="btn btn-outline btn-sm" style="color:var(--danger-color)" onclick="deleteDocument('${doc.id}', '${escapeHtml(doc.filename)}')">
            Delete
          </button>
        </td>
      </tr>
    `).join('');
  } catch (err) {
    tbody.innerHTML = `<tr><td colspan="6" style="text-align:center; padding:20px; color:var(--danger-color);">Failed to load knowledge documents: ${escapeHtml(err.message)}</td></tr>`;
  }
}

async function handleDocumentSubmit(e) {
  e.preventDefault();
  const title = document.getElementById('doc-title').value.trim();
  const filename = document.getElementById('doc-filename').value.trim();
  const source_type = document.getElementById('doc-source-type').value;
  const content = document.getElementById('doc-content').value.trim();

  if (!title || !content) {
    showToast('Validation error: Document Title and Content are required.', 'warning');
    return;
  }

  const btn = document.getElementById('btn-submit-doc');
  btn.disabled = true;
  const originalHTML = btn.innerHTML;
  btn.innerHTML = '<span class="material-symbols-outlined">hourglass_top</span> Indexing Chunks...';

  try {
    const res = await adminFetch(`${API_BASE}/admin/documents/upload`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title, filename, source_type, content })
    });

    if (!res.ok) {
      const errData = await res.json().catch(() => ({}));
      throw new Error(errData.detail || 'Failed to upload document');
    }

    const data = await res.json();
    showToast(`Document "${data.filename}" uploaded and indexed into ${data.chunk_count} chunks!`, 'success');
    closeDocModal();
    loadDocumentsTable();
    loadDashboardStats();
  } catch (err) {
    showToast(err.message || 'Document upload failed.', 'error');
  } finally {
    btn.disabled = false;
    btn.innerHTML = originalHTML;
  }
}

async function deleteDocument(id, filename) {
  if (!confirm(`Are you sure you want to delete "${filename}" from the knowledge base? This will immediately remove all its chunks from the RAG search index.`)) return;

  try {
    const res = await adminFetch(`${API_BASE}/admin/documents/${id}`, { method: 'DELETE' });
    if (!res.ok) throw new Error('Deletion failed.');
    showToast(`Document "${filename}" deleted and RAG index refreshed.`, 'success');
    loadDocumentsTable(docSearch ? docSearch.value : '');
    loadDashboardStats();
  } catch (err) {
    showToast(err.message || 'Failed to delete knowledge document.', 'error');
  }
}

// RAG RETRIEVAL TEST
async function runRAGTest(query, top_k = 5) {
  query = (query || '').trim();
  if (!query) {
    showToast('Validation error: Please enter a query to test RAG retrieval.', 'warning');
    return;
  }

  if (btnRunRAGTest) {
    btnRunRAGTest.disabled = true;
    btnRunRAGTest.innerHTML = '<span class="material-symbols-outlined">hourglass_top</span> Retrieving...';
  }

  ragResultsContainer.innerHTML = `
    <div style="text-align:center; padding:30px; color:var(--text-muted); background:#FFFFFF; border-radius:10px;">
      <div class="dot live" style="margin: 0 auto 10px;"></div>
      <p>Searching hybrid vector and BM25 index across announcements & knowledge documents...</p>
    </div>
  `;

  try {
    const res = await adminFetch(`${API_BASE}/admin/rag/test`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query, top_k })
    });

    if (!res.ok) throw new Error('RAG retrieval test failed.');
    const data = await res.json();

    showToast(`Retrieved ${data.total_retrieved} matching source chunks.`, 'info');

    if (!data.results || data.results.length === 0) {
      ragResultsContainer.innerHTML = `
        <div class="rag-results-header">
          <strong>No matches found for "${escapeHtml(query)}"</strong>
          <small>Try adding keywords or index relevant documents in the Knowledge Base tab.</small>
        </div>
      `;
      return;
    }

    ragResultsContainer.innerHTML = `
      <div class="rag-results-header">
        <div>
          <strong>Query: "${escapeHtml(query)}"</strong>
          <span style="font-size:12px; color:var(--text-muted); margin-left:8px;">(${data.total_retrieved} ranked chunks retrieved)</span>
        </div>
        <span class="badge badge-gold">Top ${data.results.length} Matches</span>
      </div>
      ${data.results.map(r => `
        <div class="rag-chunk-card">
          <div class="rag-chunk-meta">
            <div style="display: flex; align-items: center; gap: 8px;">
              <span class="rag-rank-badge">#${r.rank} Match</span>
              <strong>${escapeHtml(r.title)}</strong>
              ${r.filename ? `<code style="font-size:11px; color:var(--text-muted);">(${escapeHtml(r.filename)})</code>` : ''}
            </div>
            <div style="display: flex; align-items: center; gap: 8px;">
              <span class="rag-source-badge">${escapeHtml(r.source_type)}</span>
              <span class="rag-score-badge">Similarity Score: ${r.score}</span>
            </div>
          </div>
          <div class="rag-chunk-text">${escapeHtml(r.chunk_content)}</div>
          ${r.source_url ? `<div style="font-size:12px;"><a href="${r.source_url}" target="_blank" style="color:var(--maroon-primary); text-decoration:none;">Official Link: ${escapeHtml(r.source_url)} ↗</a></div>` : ''}
        </div>
      `).join('')}
    `;
  } catch (err) {
    ragResultsContainer.innerHTML = `<div style="color:var(--danger-color); padding:20px; text-align:center;">Retrieval test failed: ${escapeHtml(err.message)}</div>`;
  } finally {
    if (btnRunRAGTest) {
      btnRunRAGTest.disabled = false;
      btnRunRAGTest.innerHTML = '<span class="material-symbols-outlined">play_arrow</span> Run Retrieval Test';
    }
  }
}

// NOTIFICATION BROADCAST
async function handleNotificationBroadcast(e) {
  e.preventDefault();
  const title_en = document.getElementById('notif-title-en').value.trim();
  const title_te = document.getElementById('notif-title-te').value.trim();
  const body_en = document.getElementById('notif-body-en').value.trim();
  const body_te = document.getElementById('notif-body-te').value.trim();
  const notification_type = document.getElementById('notif-type').value;

  if (!title_en || !title_te || !body_en || !body_te) {
    showToast('Validation error: All notification title and body fields are required.', 'warning');
    return;
  }

  const payload = { title_en, title_te, body_en, body_te, notification_type };

  try {
    const res = await adminFetch(`${API_BASE}/admin/notifications/broadcast`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (!res.ok) throw new Error('Broadcast failed');
    const result = await res.json();
    showToast('Push alert broadcast dispatched successfully to devotees!', 'success');
    document.getElementById('notification-form').reset();
    loadNotificationHistory();
  } catch (err) {
    showToast(err.message || 'Notification broadcast failed.', 'error');
  }
}

async function loadNotificationHistory() {
  try {
    const res = await fetch(`${API_BASE}/notifications/history`, { credentials: 'same-origin' });
    const items = await res.json();
    const list = document.getElementById('notification-history-list');

    if (!items || items.length === 0) {
      list.innerHTML = '<p class="text-muted">No notifications dispatched yet.</p>';
      return;
    }

    list.innerHTML = items.map(n => `
      <div class="integration-item">
        <span class="material-symbols-outlined" style="color:var(--gold-dark)">notifications</span>
        <div class="integration-meta">
          <strong>${escapeHtml(n.title_en)} (${escapeHtml(n.title_te)})</strong>
          <p>${escapeHtml(n.body_en)}</p>
          <small style="color:var(--text-muted);">${new Date(n.sent_at).toLocaleString()}</small>
        </div>
        <span class="badge badge-green">${n.notification_type}</span>
      </div>
    `).join('');
  } catch (err) {
    console.error('Failed to load notification history:', err);
  }
}

// AUDIT LOGS
async function loadAuditLogs() {
  try {
    const res = await adminFetch(`${API_BASE}/admin/audit-logs`);
    const logs = await res.json();
    const tbody = document.getElementById('audit-table-body');

    if (!logs || logs.length === 0) {
      tbody.innerHTML = '<tr><td colspan="5" style="text-align:center; padding:20px;">No audit operations recorded.</td></tr>';
      return;
    }

    tbody.innerHTML = logs.map(l => `
      <tr>
        <td>${new Date(l.created_at).toLocaleString()}</td>
        <td><strong>${escapeHtml(l.action)}</strong></td>
        <td><span class="badge badge-gold">${escapeHtml(l.entity_type)}</span></td>
        <td><code>${l.entity_id ? l.entity_id.substring(0, 8) + '...' : 'System'}</code></td>
        <td><small>${l.details ? JSON.stringify(l.details) : 'None'}</small></td>
      </tr>
    `).join('');
  } catch (err) {
    console.error('Failed to load audit logs:', err);
  }
}

// TEST AI CHAT
async function handleTestChat(e) {
  e.preventDefault();
  const input = document.getElementById('test-chat-input');
  const query = input.value.trim();
  if (!query) return;

  const chatContainer = document.getElementById('test-chat-messages');

  const userBubble = document.createElement('div');
  userBubble.className = 'chat-bubble user';
  userBubble.textContent = query;
  chatContainer.appendChild(userBubble);
  input.value = '';
  chatContainer.scrollTop = chatContainer.scrollHeight;

  const botBubble = document.createElement('div');
  botBubble.className = 'chat-bubble bot';
  botBubble.innerHTML = '<div class="sender-name">Srivari AI</div><p>Searching official TTD knowledge base...</p>';
  chatContainer.appendChild(botBubble);
  chatContainer.scrollTop = chatContainer.scrollHeight;

  try {
    const devoteeRes = await fetch(`${API_BASE}/auth/devotee-init`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'same-origin',
      body: JSON.stringify({ device_id: 'admin_test_terminal_01' })
    });
    const devoteeData = await devoteeRes.json();

    const chatRes = await fetch(`${API_BASE}/chat/query`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${devoteeData.access_token}`
      },
      credentials: 'same-origin',
      body: JSON.stringify({ query })
    });

    const chatData = await chatRes.json();
    botBubble.innerHTML = `
      <div class="sender-name">Srivari AI (శ్రీవారి AI)</div>
      <p style="white-space: pre-wrap;">${escapeHtml(chatData.answer)}</p>
      ${chatData.citations && chatData.citations.length > 0 ? `
        <div style="margin-top: 8px; font-size: 11px; color: var(--text-muted);">
          <strong>Official Citations:</strong><br>
          ${chatData.citations.map(c => `• <a href="${c.url}" target="_blank" style="color:var(--maroon-primary);">${escapeHtml(c.title)}</a>`).join('<br>')}
        </div>
      ` : ''}
    `;
    chatContainer.scrollTop = chatContainer.scrollHeight;
  } catch (err) {
    botBubble.innerHTML = `<div class="sender-name">Srivari AI</div><p style="color:var(--danger-color);">Error connecting to RAG backend: ${err.message}</p>`;
  }
}

function escapeHtml(str) {
  if (!str) return '';
  return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}
