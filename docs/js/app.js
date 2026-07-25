// ============================================================
// PROJETO MARINGÁ — PAINEL DE GESTÃO DO PROJETO (PRODUTOS 1 A 6)
// CONSULTORIA BRISA SOLUÇÕES AMBIENTAIS | IPPLAM / CEPAL CCFLA
// ============================================================

document.addEventListener('DOMContentLoaded', () => {
    initTabs();
    initAuthGate();
    initNewInterviewModal();
    initFilters();
});

// Global App State
let currentUser = null;
let allOrganizations = [];
let allContacts = [];
let allInterviews = [];
let projectRoadmap = [];
let docEvidenceMatrix = [];

// Environment Check: Detect GitHub Pages or Static Host to prevent 404/405 console logs
const isStaticHost = window.location.hostname.includes('github.io') || 
                     window.location.protocol === 'file:' || 
                     !window.location.port;

// Helper: Smart Fetch without Console 404 Errors on GitHub Pages
async function apiFetch(endpoint, staticFallbackPath) {
    if (isStaticHost) {
        // Direct static fetch for GitHub Pages (no 404 console errors)
        const staticRes = await fetch(staticFallbackPath);
        return await staticRes.json();
    }
    
    try {
        const res = await fetch(endpoint);
        if (res.ok) {
            return await res.json();
        }
        if (res.status === 401) {
            throw new Error('UNAUTHORIZED');
        }
    } catch (e) {
        if (e.message === 'UNAUTHORIZED') throw e;
        console.log(`Fallback estático ativado para: ${staticFallbackPath}`);
    }
    const staticRes = await fetch(staticFallbackPath);
    return await staticRes.json();
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
            const target = document.getElementById(targetTab);
            if (target) target.classList.add('active');
        });
    });
}

// -------------------------------------------------------------
// 2. BLOQUEIO OBRIGATÓRIO DE LOGIN (GATE LGPD)
// -------------------------------------------------------------
function initAuthGate() {
    const loginGate = document.getElementById('login-gate');
    const appContainer = document.getElementById('app-container');
    const formGateLogin = document.getElementById('form-gate-login');
    const btnLogout = document.getElementById('btn-logout');
    const usernameInput = document.getElementById('input-gate-username');
    const passwordInput = document.getElementById('input-gate-password');
    const errorDiv = document.getElementById('gate-login-error');

    if (usernameInput) usernameInput.addEventListener('input', () => errorDiv.classList.add('hidden'));
    if (passwordInput) passwordInput.addEventListener('input', () => errorDiv.classList.add('hidden'));

    if (formGateLogin) {
        formGateLogin.addEventListener('submit', async (e) => {
            e.preventDefault();
            const username = usernameInput.value.trim().toLowerCase();
            const password = passwordInput.value.trim();

            errorDiv.classList.add('hidden');

            if (!username || !password) {
                errorDiv.textContent = 'Por favor, preencha o usuário e a senha.';
                errorDiv.classList.remove('hidden');
                return;
            }

            // Se for ambiente estático (GitHub Pages), pula chamada a /api/auth/login para evitar erro 405
            if (!isStaticHost) {
                try {
                    const res = await fetch('/api/auth/login', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ username, password })
                    });

                    if (res.ok) {
                        const data = await res.json();
                        if (data.success) {
                            currentUser = data.user;
                            unlockDashboard();
                            return;
                        }
                    } else if (res.status === 401) {
                        const data = await res.json();
                        errorDiv.textContent = data.error || 'Usuário ou senha incorretos.';
                        errorDiv.classList.remove('hidden');
                        return;
                    }
                } catch (err) {
                    console.log('Ambiente estático. Usando validação cliente...');
                }
            }

            // Validação de credenciais cliente (GitHub Pages)
            let valid = false;
            let role = 'visualizador';
            let name = 'Visualizador Stakeholder';

            if (username === 'admin' && (password === 'admin' || password === 'Maringa2026!Admin')) {
                valid = true;
                role = 'admin';
                name = 'Administrador LGPD';
            } else if (username === 'pesquisador' && (password === 'pesquisador' || password === 'Maringa2026!Pesquisa')) {
                valid = true;
                role = 'pesquisador';
                name = 'Pesquisador Consultoria';
            } else if (username === 'visitante' && (password === 'visitante' || password === 'Maringa2026!Visitante')) {
                valid = true;
                role = 'visualizador';
                name = 'Visualizador Stakeholder';
            }

            if (valid) {
                currentUser = { username, name, role };
                unlockDashboard();
            } else {
                errorDiv.textContent = '❌ Usuário ou senha incorretos! Tente admin / admin';
                errorDiv.classList.remove('hidden');
            }
        });
    }

    if (btnLogout) {
        btnLogout.addEventListener('click', async () => {
            if (!isStaticHost) {
                try { await fetch('/api/auth/logout', { method: 'POST' }); } catch(e) {}
            }
            currentUser = null;
            lockDashboard();
        });
    }

    lockDashboard();
}

function unlockDashboard() {
    const loginGate = document.getElementById('login-gate');
    const appContainer = document.getElementById('app-container');
    const userDisplayName = document.getElementById('user-display-name');
    const userRoleBadge = document.getElementById('user-role-badge');
    const profileLabel = document.getElementById('current-profile-label');

    if (loginGate) loginGate.classList.add('hidden');
    if (appContainer) appContainer.classList.remove('hidden');

    if (currentUser) {
        if (userDisplayName) userDisplayName.textContent = currentUser.name;
        if (userRoleBadge) userRoleBadge.textContent = currentUser.role;

        if (profileLabel) {
            if (currentUser.role === 'admin') {
                profileLabel.textContent = 'Administrador (Acesso Completo aos Contatos PII)';
                profileLabel.style.color = '#B86B43';
            } else if (currentUser.role === 'pesquisador') {
                profileLabel.textContent = 'Pesquisador (Dados de Pesquisa & Entrevistas)';
                profileLabel.style.color = '#4A3B32';
            } else {
                profileLabel.textContent = 'Visualizador (Dados de Contato Mascarados LGPD)';
                profileLabel.style.color = '#6E5A4E';
            }
        }
    }

    loadDashboardData();
}

function lockDashboard() {
    const loginGate = document.getElementById('login-gate');
    const appContainer = document.getElementById('app-container');

    if (loginGate) loginGate.classList.remove('hidden');
    if (appContainer) appContainer.classList.add('hidden');
}

// -------------------------------------------------------------
// 3. MODAL E GESTÃO DE ENTREVISTAS
// -------------------------------------------------------------
function initNewInterviewModal() {
    const btnOpen = document.getElementById('btn-open-new-interview');
    const btnClose = document.getElementById('btn-close-new-interview');
    const modal = document.getElementById('modal-new-interview');
    const form = document.getElementById('form-new-interview');

    if (btnOpen) btnOpen.addEventListener('click', () => modal.classList.remove('hidden'));
    if (btnClose) btnClose.addEventListener('click', () => modal.classList.add('hidden'));

    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const actor_code = document.getElementById('input-inv-actor').value;
            const institution_type = document.getElementById('input-inv-inst').value;
            const ccfla_dimension = document.getElementById('select-inv-dim').value;
            const status = document.getElementById('select-inv-status').value;
            const interview_date = document.getElementById('input-inv-date').value;
            const key_findings_coded = document.getElementById('input-inv-notes').value || 'Anotações pendentes.';

            const nextNum = String(allInterviews.length + 1).padStart(2, '0');
            const newInv = {
                interview_code: `INT-${nextNum}`,
                actor_code,
                institution_type,
                sector_group: 'Público',
                ccfla_dimension,
                interview_date,
                instrument: 'Entrevista Estruturada',
                status,
                key_findings_coded
            };

            if (!isStaticHost) {
                try {
                    await fetch('/api/interviews/add', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(newInv)
                    });
                } catch(err) {}
            }

            allInterviews.push(newInv);
            renderInterviewsGrid();
            modal.classList.add('hidden');
            form.reset();
            alert('Entrevista registrada com sucesso no pipeline de campo!');
        });
    }
}

// -------------------------------------------------------------
// 4. CARREGAMENTO E RENDERIZAÇÃO DE DADOS
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
        if (data) {
            if (document.getElementById('kpi-orgs')) document.getElementById('kpi-orgs').textContent = data.total_orgs;
            if (document.getElementById('kpi-contacts')) document.getElementById('kpi-contacts').textContent = data.confirmed_contacts;
            if (document.getElementById('kpi-comdema')) document.getElementById('kpi-comdema').textContent = data.comdema_members;
            if (document.getElementById('kpi-interviews')) document.getElementById('kpi-interviews').textContent = data.total_interviews;

            projectRoadmap = data.project_products || [];
            docEvidenceMatrix = data.doc_evidence_matrix || [];

            renderProjectRoadmap();
            renderEvidenceMatrix();

            if (window.renderCharts) {
                window.renderCharts(data.orgs_by_group);
            }
        }
    } catch (e) {
        console.error('Erro ao carregar estatísticas:', e);
    }
}

function renderProjectRoadmap() {
    const grid = document.getElementById('grid-roadmap');
    if (!grid) return;

    grid.innerHTML = projectRoadmap.map(p => `
        <div class="roadmap-card ${p.status === 'EM FINALIZAÇÃO' ? 'roadmap-card-active' : ''}">
            <div class="roadmap-badge ${getRoadmapBadgeClass(p.status)}">${p.status}</div>
            <h4>${p.id}: ${p.name}</h4>
            <span class="roadmap-phase">${p.phase}</span>
            <p>${p.desc}</p>
        </div>
    `).join('');
}

function renderEvidenceMatrix() {
    const tbody = document.getElementById('tbody-evidence');
    if (!tbody) return;

    tbody.innerHTML = docEvidenceMatrix.map(doc => `
        <tr>
            <td><strong>${doc.code}</strong></td>
            <td><strong>${doc.name}</strong></td>
            <td><span class="badge-group badge-public">${doc.category}</span></td>
            <td>${doc.type}</td>
            <td>${doc.org}</td>
            <td><span class="badge-status-confirmed">${doc.status}</span></td>
        </tr>
    `).join('');
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
    const groupFilterEl = document.getElementById('filter-group-orgs');
    const searchValEl = document.getElementById('search-orgs');
    const tbody = document.getElementById('tbody-orgs');

    if (!tbody) return;

    const groupFilter = groupFilterEl ? groupFilterEl.value : '';
    const searchVal = searchValEl ? searchValEl.value.toLowerCase() : '';

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
    if (!tbody) return;

    const userRole = currentUser ? currentUser.role : 'visualizador';

    tbody.innerHTML = allContacts.map(c => {
        let email = c.email || 'A confirmar';
        let phone = c.phone || 'A confirmar';

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

        if (tbody) {
            tbody.innerHTML = (data.members || []).map(m => `
                <tr>
                    <td><strong>${m.name}</strong> ${m.is_six_years ? '<span class="badge-status-confirmed" style="margin-left:6px;">6 Anos (2021-2026)</span>' : ''}</td>
                    <td><span class="badge-group ${getGroupBadgeClass(m.group_represented)}">${m.group_represented}</span></td>
                    <td>${m.affiliation}</td>
                    <td>${m.years_present}</td>
                </tr>
            `).join('');
        }

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
    const dimFilterEl = document.getElementById('filter-interviews-dim');
    const grid = document.getElementById('grid-interviews');

    if (!grid) return;

    const dimFilter = dimFilterEl ? dimFilterEl.value : '';

    const filtered = allInterviews.filter(inv => !dimFilter || inv.ccfla_dimension.includes(dimFilter));

    if (filtered.length === 0) {
        grid.innerHTML = `<div class="banner-note" style="grid-column: 1/-1;">Nenhuma entrevista registrada neste filtro. Clique em <strong>+ Agendar / Registrar Entrevista</strong> acima para iniciar.</div>`;
        return;
    }

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
                <span>Status: <strong>${inv.status}</strong></span>
                <span>Data: ${inv.interview_date}</span>
            </div>
        </div>
    `).join('');
}

// -------------------------------------------------------------
// 5. FILTROS E PESQUISA
// -------------------------------------------------------------
function initFilters() {
    const searchOrgs = document.getElementById('search-orgs');
    const filterGroupOrgs = document.getElementById('filter-group-orgs');
    const filterInterviewsDim = document.getElementById('filter-interviews-dim');

    if (searchOrgs) searchOrgs.addEventListener('input', renderOrganizationsTable);
    if (filterGroupOrgs) filterGroupOrgs.addEventListener('change', renderOrganizationsTable);
    if (filterInterviewsDim) filterInterviewsDim.addEventListener('change', renderInterviewsGrid);
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

function getRoadmapBadgeClass(status) {
    switch (status) {
        case 'CONCLUÍDO': return 'badge-status-confirmed';
        case 'EM FINALIZAÇÃO': return 'badge-group badge-private';
        case 'PRÓXIMO PASSO': return 'badge-group badge-civil';
        default: return 'badge-status-pending';
    }
}
