// ============================================================
// PROJETO MARINGÁ — LÓGICA FRONTEND & COMPATIBILIDADE GITHUB PAGES
// ============================================================

document.addEventListener('DOMContentLoaded', () => {
    initTabs();
    initAuth();
    loadDashboardData();
    initFilters();
});

// Global App State
let currentUser = null;
let allOrganizations = [];
let allContacts = [];
let allInterviews = [];

// Helper: Smart Fetch with GitHub Pages Static Fallback
async function apiFetch(endpoint, staticFallbackPath) {
    try {
        const res = await fetch(endpoint);
        if (res.ok) {
            return await res.json();
        }
        throw new Error('API backend não disponível');
    } catch (e) {
        // Fallback for static hosts like GitHub Pages
        console.log(`Fallback estático ativado para: ${staticFallbackPath}`);
        const staticRes = await fetch(staticFallbackPath);
        return await staticRes.json();
    }
}

// -------------------------------------------------------------
// 1. NAVEGAÇÃO POR ABAS
// -------------------------------------------------------------
function initTabs() {
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const targetTab = btn.getAttribute('data-tab');

            tabButtons.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));

            btn.classList.add('active');
            document.getElementById(targetTab).classList.add('active');
        });
    });
}

// -------------------------------------------------------------
// 2. AUTENTICAÇÃO E SESSÃO (LGPD RESTRIÇÃO DE ACESSO)
// -------------------------------------------------------------
function initAuth() {
    const modalLogin = document.getElementById('modal-login');
    const btnOpenLogin = document.getElementById('btn-open-login');
    const btnCloseLogin = document.getElementById('btn-close-login');
    const formLogin = document.getElementById('form-login');
    const btnLogout = document.getElementById('btn-logout');

    btnOpenLogin.addEventListener('click', () => modalLogin.classList.remove('hidden'));
    btnCloseLogin.addEventListener('click', () => modalLogin.classList.add('hidden'));

    formLogin.addEventListener('submit', async (e) => {
        e.preventDefault();
        const username = document.getElementById('input-username').value.trim();
        const password = document.getElementById('input-password').value.trim();
        const errorDiv = document.getElementById('login-error');

        errorDiv.classList.add('hidden');

        try {
            // Try backend login first
            const res = await fetch('/api/auth/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            });

            if (res.ok) {
                const data = await res.json();
                if (data.success) {
                    currentUser = data.user;
                    updateAuthUI();
                    modalLogin.classList.add('hidden');
                    formLogin.reset();
                    renderContactsTable();
                    return;
                }
            }
        } catch (err) {
            console.log('Ambiente estático detectado, simulando login cliente...');
        }

        // Static / Client Fallback Authentication for GitHub Pages
        if (password === 'Maringa2026!') {
            let role = 'visualizador';
            let name = 'Visitante / Stakeholder';

            if (username === 'admin') {
                role = 'admin';
                name = 'Administrador LGPD';
            } else if (username === 'pesquisador') {
                role = 'pesquisador';
                name = 'Pesquisador Consultoria';
            }

            currentUser = { username, name, role };
            updateAuthUI();
            modalLogin.classList.add('hidden');
            formLogin.reset();
            renderContactsTable();
        } else {
            errorDiv.textContent = 'Usuário ou senha incorretos. Use Maringa2026!';
            errorDiv.classList.remove('hidden');
        }
    });

    btnLogout.addEventListener('click', async () => {
        try { await fetch('/api/auth/logout', { method: 'POST' }); } catch(e) {}
        currentUser = null;
        updateAuthUI();
        renderContactsTable();
    });

    checkSession();
}

async function checkSession() {
    try {
        const res = await fetch('/api/auth/me');
        const data = await res.json();
        if (data.authenticated) {
            currentUser = data.user;
        } else {
            currentUser = null;
        }
    } catch (e) {
        currentUser = null;
    }
    updateAuthUI();
}

function updateAuthUI() {
    const btnOpenLogin = document.getElementById('btn-open-login');
    const userProfile = document.getElementById('user-profile');
    const userDisplayName = document.getElementById('user-display-name');
    const userRoleBadge = document.getElementById('user-role-badge');
    const profileLabel = document.getElementById('current-profile-label');

    if (currentUser) {
        btnOpenLogin.classList.add('hidden');
        userProfile.classList.remove('hidden');
        userDisplayName.textContent = currentUser.name;
        userRoleBadge.textContent = currentUser.role;

        if (currentUser.role === 'admin') {
            profileLabel.textContent = 'Administrador (Acesso Total aos Contatos PII)';
            profileLabel.style.color = '#B86B43';
        } else if (currentUser.role === 'pesquisador') {
            profileLabel.textContent = 'Pesquisador (Acesso a Dados de Pesquisa)';
            profileLabel.style.color = '#4A3B32';
        } else {
            profileLabel.textContent = 'Visitante (Dados Pessoais Mascarados sob LGPD)';
            profileLabel.style.color = '#6E5A4E';
        }
    } else {
        btnOpenLogin.classList.remove('hidden');
        userProfile.classList.add('hidden');
        profileLabel.textContent = 'Visitante (Dados Pessoais Mascarados sob LGPD)';
        profileLabel.style.color = '#6E5A4E';
    }
}

// -------------------------------------------------------------
// 3. CARREGAMENTO DE DADOS
// -------------------------------------------------------------
async function loadDashboardData() {
    loadOverviewStats();
    loadOrganizations();
    loadContacts();
    loadComdema();
    loadInterviews();
}

async function loadOverviewStats() {
    try {
        const data = await apiFetch('/api/stats/overview', './data/overview.json');
        document.getElementById('kpi-orgs').textContent = data.total_orgs;
        document.getElementById('kpi-contacts').textContent = data.confirmed_contacts;
        document.getElementById('kpi-comdema').textContent = data.comdema_members;
        document.getElementById('kpi-interviews').textContent = data.total_interviews;

        if (window.renderCharts) {
            window.renderCharts(data.orgs_by_group);
        }
    } catch (e) {
        console.error('Erro ao carregar estatísticas:', e);
    }
}

async function loadOrganizations() {
    try {
        const data = await apiFetch('/api/organizations', './data/organizations.json');
        allOrganizations = data.organizations || [];
        renderOrganizationsTable();
    } catch (e) {
        console.error('Erro ao carregar organizações:', e);
    }
}

function renderOrganizationsTable() {
    const groupFilter = document.getElementById('filter-group-orgs').value;
    const searchVal = document.getElementById('search-orgs').value.toLowerCase();
    const tbody = document.getElementById('tbody-orgs');

    const filtered = allOrganizations.filter(org => {
        const matchGroup = !groupFilter || org.group_type === groupFilter;
        const matchSearch = !searchVal || 
            org.name.toLowerCase().includes(searchVal) || 
            org.acronym.toLowerCase().includes(searchVal) || 
            org.ccfla_main.toLowerCase().includes(searchVal);
        return matchGroup && matchSearch;
    });

    tbody.innerHTML = filtered.map(org => `
        <tr>
            <td><strong>${org.code}</strong></td>
            <td><strong>${org.name}</strong></td>
            <td><span class="badge-group badge-public">${org.acronym}</span></td>
            <td>${org.sphere}</td>
            <td><span class="badge-group ${getGroupBadgeClass(org.group_type)}">${org.group_type}</span></td>
            <td>${org.ccfla_main}</td>
            <td>${org.contact_status === 'Confirmado (Ponto Focal)' ? 
                '<span class="badge-status-confirmed">Ponto Focal Confirmado</span>' : 
                '<span class="badge-status-pending">A confirmar</span>'}</td>
        </tr>
    `).join('');
}

async function loadContacts() {
    try {
        const data = await apiFetch('/api/contacts', './data/contacts.json');
        allContacts = data.contacts || [];
        renderContactsTable();
    } catch (e) {
        console.error('Erro ao carregar contatos:', e);
    }
}

function renderContactsTable() {
    const tbody = document.getElementById('tbody-contacts');
    const userRole = currentUser ? currentUser.role : 'visualizador';

    tbody.innerHTML = allContacts.map(c => {
        let email = c.email || 'A confirmar';
        let phone = c.phone || 'A confirmar';

        // LGPD Masking for non-admin viewers
        if (userRole === 'visualizador') {
            if (email.includes('@')) {
                const parts = email.split('@');
                email = parts[0].substring(0, 2) + '***@' + parts[1];
            }
            if (phone.length > 4) {
                phone = phone.substring(0, 6) + '****';
            }
        }

        return `
            <tr class="${c.is_top_priority ? 'priority-row' : ''}">
                <td><strong>${c.code}</strong></td>
                <td>${c.contact_status === 'CONFIRMADO' ? 
                    '<span class="badge-status-confirmed">CONFIRMADO</span>' : 
                    '<span class="badge-status-pending">A confirmar</span>'}</td>
                <td><strong>${c.name}</strong></td>
                <td>${c.organization} (${c.acronym})</td>
                <td>${c.role || '-'}</td>
                <td><code>${email}</code></td>
                <td><code>${phone}</code></td>
            </tr>
        `;
    }).join('');
}

async function loadComdema() {
    try {
        const data = await apiFetch('/api/comdema', './data/comdema.json');
        const tbody = document.getElementById('tbody-comdema');

        tbody.innerHTML = (data.members || []).map(m => `
            <tr>
                <td><strong>${m.name}</strong> ${m.is_six_years ? '<span class="badge-status-confirmed" style="margin-left:6px;">6 Anos (2021-2026)</span>' : ''}</td>
                <td><span class="badge-group ${getGroupBadgeClass(m.group_represented)}">${m.group_represented}</span></td>
                <td>${m.affiliation}</td>
                <td>${m.years_present}</td>
            </tr>
        `).join('');

        if (window.renderComdemaTimeline) {
            window.renderComdemaTimeline(data.yearly_stats || []);
        }
    } catch (e) {
        console.error('Erro ao carregar COMDEMA:', e);
    }
}

async function loadInterviews() {
    try {
        const data = await apiFetch('/api/interviews', './data/interviews.json');
        allInterviews = data.interviews || [];
        renderInterviewsGrid();
    } catch (e) {
        console.error('Erro ao carregar entrevistas:', e);
    }
}

function renderInterviewsGrid() {
    const dimFilter = document.getElementById('filter-interviews-dim').value;
    const grid = document.getElementById('grid-interviews');

    const filtered = allInterviews.filter(inv => !dimFilter || inv.ccfla_dimension.includes(dimFilter));

    grid.innerHTML = filtered.map(inv => `
        <div class="interview-card">
            <div>
                <div class="interview-header">
                    <span class="interview-code">${inv.interview_code}</span>
                    <span class="actor-code-badge">${inv.actor_code}</span>
                </div>
                <div class="interview-body">
                    <h4>${inv.institution_type}</h4>
                    <div class="interview-dim">${inv.ccfla_dimension}</div>
                    <div class="interview-quote">"${inv.key_findings_coded}"</div>
                </div>
            </div>
            <div class="interview-footer">
                <span>Instrumento: ${inv.instrument}</span>
                <span>Data: ${inv.interview_date}</span>
            </div>
        </div>
    `).join('');
}

// -------------------------------------------------------------
// 4. FILTROS E PESQUISA
// -------------------------------------------------------------
function initFilters() {
    const searchOrgs = document.getElementById('search-orgs');
    const filterGroupOrgs = document.getElementById('filter-group-orgs');
    const filterInterviewsDim = document.getElementById('filter-interviews-dim');

    searchOrgs.addEventListener('input', renderOrganizationsTable);
    filterGroupOrgs.addEventListener('change', renderOrganizationsTable);
    filterInterviewsDim.addEventListener('change', renderInterviewsGrid);
}

function getGroupBadgeClass(group) {
    switch (group) {
        case 'Público': return 'badge-public';
        case 'Privado': return 'badge-private';
        case 'Academia': return 'badge-academia';
        case 'Sociedade Civil': return 'badge-civil';
        default: return 'badge-public';
    }
}
