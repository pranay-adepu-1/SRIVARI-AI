// Srivari AI (శ్రీవారి AI) - Admin Portal Client Script
const API_BASE = window.location.origin.includes(':8000') 
  ? 'http://localhost:8000/api/v1' 
  : `${window.location.origin}/api/v1`;

let authToken = localStorage.getItem('srivari_admin_token') || null;
let currentAdmin = JSON.parse(localStorage.getItem('srivari_admin_user') || 'null');
let categoriesCache = [];

// DOM Elements
const loginContainer = document.getElementById('login-container');
const appContainer = document.getElementById('app-container');
const loginForm = document.getElementById('login-form');
const loginError = document.getElementById('login-error');
const btnLogout = document.getElementById('btn-logout');
const btnQuickSync = document.getElementById('btn-quick-sync');
const btnTriggerScraper = document.getElementById('btn-trigger-scraper');
const modal = document.getElementById('announcement-modal');
const announcementForm = document.getElementById('announcement-form');
const announcementSearch = document.getElementById('announcement-search');

// INITIALIZATION
document.addEventListener('DOMContentLoaded', () => {
  if (authToken && currentAdmin) {
    showDashboard();
  } else {
    showLogin();
  }

  setupEventListeners();
});

function setupEventListeners() {
  // Login Form
  loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    loginError.classList.add('hidden');
    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value;

    try {
      const res = await fetch(`${API_BASE}/auth/admin-login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
      });

      if (!res.ok) {
        throw new Error('Invalid administrative credentials.');
      }

      const data = await res.json();
      authToken = data.access_token;
      currentAdmin = data.admin;
      localStorage.setItem('srivari_admin_token', authToken);
      localStorage.setItem('srivari_admin_user', JSON.stringify(currentAdmin));
      showDashboard();
    } catch (err) {
      loginError.textContent = err.message || 'Authentication failed.';
      loginError.classList.remove('hidden');
    }
  });

  // Logout
  btnLogout.addEventListener('click', () => {
    localStorage.removeItem('srivari_admin_token');
    localStorage.removeItem('srivari_admin_user');
    authToken = null;
    currentAdmin = null;
    showLogin();
  });

  // Navigation Tabs
  document.querySelectorAll('.nav-item').forEach(btn => {
    btn.addEventListener('click', () => {
      const tab = btn.getAttribute('data-tab');
      switchTab(tab);
    });
  });

  // Quick Scraper Sync
  btnQuickSync.addEventListener('click', runScraperSync);
  btnTriggerScraper.addEventListener('click', runScraperSync);

  // Announcement Search
  let searchTimeout;
  announcementSearch.addEventListener('input', () => {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => {
      loadAnnouncementsTable(announcementSearch.value);
    }, 300);
  });

  // Add Announcement Button
  document.getElementById('btn-add-announcement').addEventListener('click', () => {
    openModalForCreate();
  });

  // Announcement Form Submit
  announcementForm.addEventListener('submit', handleAnnouncementSubmit);

  // Notification Broadcast Form Submit
  document.getElementById('notification-form').addEventListener('submit', handleNotificationBroadcast);

  // Test AI Chat Form Submit
  document.getElementById('test-chat-form').addEventListener('submit', handleTestChat);
}

function showLogin() {
  loginContainer.classList.remove('hidden');
  appContainer.classList.add('hidden');
}

function showDashboard() {
  loginContainer.classList.add('hidden');
  appContainer.classList.remove('hidden');
  document.getElementById('logged-admin-name').textContent = currentAdmin.full_name || 'Admin Officer';
  document.getElementById('logged-admin-role').textContent = currentAdmin.role || 'Super Admin';

  loadDashboardStats();
  loadCategories();
  loadRecentAnnouncements();
  loadAnnouncementsTable();
}

function switchTab(tabName) {
  document.querySelectorAll('.nav-item').forEach(item => {
    item.classList.toggle('active', item.getAttribute('data-tab') === tabName);
  });

  document.querySelectorAll('.tab-pane').forEach(pane => {
    pane.classList.toggle('active', pane.id === `tab-${tabName}`);
  });

  const titles = {
    'dashboard': ['Dashboard Overview', 'Real-time status of TTD news indexing and devotee services.'],
    'announcements': ['Official Announcements', 'Manage indexed press releases, quotas, and verified updates.'],
    'scraper': ['TTD Ingestion Engine', 'Automated crawler for news.tirumala.org and booking notices.'],
    'notifications': ['Push Broadcast', 'Dispatch immediate quota alerts and daily digests to devotees.'],
    'audit': ['Audit Trail', 'Cryptographic compliance records of administrative operations.'],
    'test-chat': ['Interactive AI Chatbot', 'Verify English and Telugu responses with citations.']
  };

  if (titles[tabName]) {
    document.getElementById('page-title').textContent = titles[tabName][0];
    document.getElementById('page-subtitle').textContent = titles[tabName][1];
  }

  if (tabName === 'audit') loadAuditLogs();
  if (tabName === 'notifications') loadNotificationHistory();
}

// DASHBOARD DATA FETCHING
async function loadDashboardStats() {
  try {
    const res = await fetch(`${API_BASE}/admin/dashboard-stats`, {
      headers: { 'Authorization': `Bearer ${authToken}` }
    });
    if (!res.ok) return;
    const data = await res.json();
    document.getElementById('stat-announcements').textContent = data.total_announcements;
    document.getElementById('stat-verified').textContent = data.verified_announcements;
    document.getElementById('stat-quotas').textContent = data.quota_alerts;
    document.getElementById('stat-users').textContent = data.total_users;
  } catch (err) {
    console.error('Failed to load stats:', err);
  }
}

async function loadCategories() {
  try {
    const res = await fetch(`${API_BASE}/announcements/categories`);
    if (!res.ok) return;
    categoriesCache = await res.json();
    const select = document.getElementById('modal-category');
    select.innerHTML = categoriesCache.map(c => `<option value="${c.id}">${c.name_en} (${c.name_te})</option>`).join('');
  } catch (err) {
    console.error('Failed to load categories:', err);
  }
}

async function loadRecentAnnouncements() {
  try {
    const res = await fetch(`${API_BASE}/announcements?limit=5`);
    const data = await res.json();
    const list = document.getElementById('dashboard-recent-list');
    if (!data.items || data.items.length === 0) {
      list.innerHTML = '<p class="text-muted">No announcements indexed yet.</p>';
      return;
    }

    list.innerHTML = data.items.map(item => `
      <div class="integration-item">
        <span class="material-symbols-outlined" style="color: var(--maroon-primary)">campaign</span>
        <div class="integration-meta">
          <strong>${escapeHtml(item.title_en)}</strong>
          <p>${escapeHtml(item.title_te)}</p>
        </div>
        <span class="badge ${item.is_quota_alert ? 'badge-orange' : 'badge-gold'}">
          ${item.is_quota_alert ? 'Quota Release' : 'Notice'}
        </span>
      </div>
    `).join('');
  } catch (err) {
    console.error('Failed to load recent items:', err);
  }
}

async function loadAnnouncementsTable(searchTerm = '') {
  try {
    const url = searchTerm 
      ? `${API_BASE}/announcements?search=${encodeURIComponent(searchTerm)}&limit=50`
      : `${API_BASE}/announcements?limit=50`;

    const res = await fetch(url);
    const data = await res.json();
    const tbody = document.getElementById('announcements-table-body');

    if (!data.items || data.items.length === 0) {
      tbody.innerHTML = '<tr><td colspan="7" style="text-align:center; padding:20px;">No announcements found.</td></tr>';
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
        <td>${a.is_quota_alert ? '<span class="badge badge-orange">YES</span>' : 'No'}</td>
        <td>${a.is_verified ? '<span class="badge badge-green">VERIFIED</span>' : '<span class="badge badge-red">Pending</span>'}</td>
        <td>
          <button class="btn btn-outline btn-sm" onclick="editAnnouncement('${a.id}')">Edit</button>
          <button class="btn btn-outline btn-sm" style="color:var(--danger-color)" onclick="deleteAnnouncement('${a.id}')">Delete</button>
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
    const res = await fetch(`${API_BASE}/admin/scraper/sync`, {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${authToken}` }
    });

    const data = await res.json();
    logBox.textContent += `\n[SUCCESS] Sync completed at ${data.timestamp}`;
    logBox.textContent += `\n- New Announcements Added: ${data.new_announcements}`;
    logBox.textContent += `\n- Verified Announcements Updated: ${data.existing_announcements}`;
    logBox.textContent += `\n- Total Announcements in Knowledge Base: ${data.total_indexed}\n`;

    document.getElementById('scraper-last-run').textContent = `Last run: ${new Date().toLocaleTimeString()} (Indexed ${data.total_indexed} records)`;
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
  modal.classList.remove('hidden');
}

function closeModal() {
  modal.classList.add('hidden');
}

async function handleAnnouncementSubmit(e) {
  e.preventDefault();
  const id = document.getElementById('modal-announcement-id').value;
  const payload = {
    title_en: document.getElementById('modal-title-en').value.trim(),
    title_te: document.getElementById('modal-title-te').value.trim(),
    content_en: document.getElementById('modal-content-en').value.trim(),
    content_te: document.getElementById('modal-content-te').value.trim(),
    source_url: document.getElementById('modal-source-url').value.trim(),
    category_id: document.getElementById('modal-category').value,
    is_quota_alert: document.getElementById('modal-is-quota').checked,
    is_verified: document.getElementById('modal-is-verified').checked,
    publication_date: new Date().toISOString()
  };

  try {
    const url = id ? `${API_BASE}/admin/announcements/${id}` : `${API_BASE}/admin/announcements`;
    const method = id ? 'PUT' : 'POST';

    const res = await fetch(url, {
      method,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${authToken}`
      },
      body: JSON.stringify(payload)
    });

    if (!res.ok) throw new Error('Failed to save announcement');

    closeModal();
    loadDashboardStats();
    loadAnnouncementsTable();
  } catch (err) {
    alert(err.message);
  }
}

async function editAnnouncement(id) {
  try {
    const res = await fetch(`${API_BASE}/announcements/${id}`);
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

    modal.classList.remove('hidden');
  } catch (err) {
    alert('Failed to load announcement for editing');
  }
}

async function deleteAnnouncement(id) {
  if (!confirm('Are you sure you want to delete this official announcement?')) return;
  try {
    const res = await fetch(`${API_BASE}/admin/announcements/${id}`, {
      method: 'DELETE',
      headers: { 'Authorization': `Bearer ${authToken}` }
    });
    if (!res.ok) throw new Error('Deletion failed');
    loadDashboardStats();
    loadAnnouncementsTable();
  } catch (err) {
    alert(err.message);
  }
}

// NOTIFICATION BROADCAST
async function handleNotificationBroadcast(e) {
  e.preventDefault();
  const payload = {
    title_en: document.getElementById('notif-title-en').value.trim(),
    title_te: document.getElementById('notif-title-te').value.trim(),
    body_en: document.getElementById('notif-body-en').value.trim(),
    body_te: document.getElementById('notif-body-te').value.trim(),
    notification_type: document.getElementById('notif-type').value
  };

  try {
    const res = await fetch(`${API_BASE}/admin/notifications/broadcast`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${authToken}`
      },
      body: JSON.stringify(payload)
    });

    if (!res.ok) throw new Error('Broadcast failed');
    const result = await res.json();
    alert(`Broadcast dispatched successfully to registered devotees!`);
    document.getElementById('notification-form').reset();
    loadNotificationHistory();
  } catch (err) {
    alert(err.message);
  }
}

async function loadNotificationHistory() {
  try {
    const res = await fetch(`${API_BASE}/notifications/history`);
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
    const res = await fetch(`${API_BASE}/admin/audit-logs`, {
      headers: { 'Authorization': `Bearer ${authToken}` }
    });
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

  // Add User bubble
  const userBubble = document.createElement('div');
  userBubble.className = 'chat-bubble user';
  userBubble.textContent = query;
  chatContainer.appendChild(userBubble);
  input.value = '';
  chatContainer.scrollTop = chatContainer.scrollHeight;

  // Add Loading Bot bubble
  const botBubble = document.createElement('div');
  botBubble.className = 'chat-bubble bot';
  botBubble.innerHTML = '<div class="sender-name">Srivari AI</div><p>Searching official TTD knowledge base...</p>';
  chatContainer.appendChild(botBubble);
  chatContainer.scrollTop = chatContainer.scrollHeight;

  try {
    // Generate devotee device handshake token if needed
    const devoteeRes = await fetch(`${API_BASE}/auth/devotee-init`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ device_id: 'admin_test_terminal_01' })
    });
    const devoteeData = await devoteeRes.json();

    const chatRes = await fetch(`${API_BASE}/chat/query`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${devoteeData.access_token}`
      },
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

