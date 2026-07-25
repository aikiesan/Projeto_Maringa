-- ============================================================
-- PROJETO MARINGÁ - CAMINHOS PARA O FINANCIAMENTO CLIMÁTICO
-- DDL DE BANCO DE DADOS PARA DEPLOY EM NUVEM (POSTGRESQL)
-- COMPATÍVEL COM SUPABASE, RENDER, RAILWAY, NEON E AWS RDS
-- ============================================================

-- 1. Tabela de Usuários e Autenticação (RBAC & LGPD)
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('admin', 'pesquisador', 'visualizador')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Tabela de Organizações Mapeadas (34 Organizações)
CREATE TABLE IF NOT EXISTS organizations (
    id SERIAL PRIMARY KEY,
    code VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    acronym VARCHAR(50) NOT NULL,
    sphere VARCHAR(50) NOT NULL,
    nature VARCHAR(100) NOT NULL,
    group_type VARCHAR(50) NOT NULL CHECK (group_type IN ('Público', 'Privado', 'Academia', 'Sociedade Civil')),
    ccfla_main VARCHAR(100) NOT NULL,
    ccfla_secondary VARCHAR(100),
    justification TEXT NOT NULL,
    contact_status VARCHAR(50) NOT NULL,
    reference_materials TEXT
);

-- 3. Tabela de Pessoas e Pontos Focais (Proteção de PII / LGPD)
CREATE TABLE IF NOT EXISTS people_contacts (
    id SERIAL PRIMARY KEY,
    code VARCHAR(20) NOT NULL,
    contact_status VARCHAR(50) NOT NULL,
    name VARCHAR(150) NOT NULL,
    organization VARCHAR(255) NOT NULL,
    acronym VARCHAR(50) NOT NULL,
    role VARCHAR(100),
    group_type VARCHAR(50) NOT NULL,
    email VARCHAR(150),
    phone VARCHAR(50),
    source TEXT,
    is_top_priority INT DEFAULT 0
);

-- 4. Tabela de Estatísticas do COMDEMA (2021-2026)
CREATE TABLE IF NOT EXISTS comdema_yearly_stats (
    year INT PRIMARY KEY,
    total INT NOT NULL,
    public_count INT NOT NULL,
    private_count INT NOT NULL,
    academia_count INT NOT NULL,
    soc_civil_count INT NOT NULL
);

-- 5. Tabela do Roster Completo do COMDEMA
CREATE TABLE IF NOT EXISTS comdema_members (
    id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    group_represented VARCHAR(50) NOT NULL,
    affiliation VARCHAR(100) NOT NULL,
    years_present TEXT NOT NULL,
    is_six_years INT DEFAULT 0
);

-- 6. Tabela de Entrevistas Codificadas (LGPD Anonymized)
CREATE TABLE IF NOT EXISTS encoded_interviews (
    id SERIAL PRIMARY KEY,
    interview_code VARCHAR(20) UNIQUE NOT NULL,
    actor_code VARCHAR(20) NOT NULL,
    institution_type VARCHAR(150) NOT NULL,
    sector_group VARCHAR(50) NOT NULL,
    ccfla_dimension VARCHAR(100) NOT NULL,
    interview_date VARCHAR(20) NOT NULL,
    instrument VARCHAR(100) NOT NULL,
    status VARCHAR(50) NOT NULL,
    key_findings_coded TEXT NOT NULL
);

-- 7. Tabela de Auditoria e Conformidade LGPD
CREATE TABLE IF NOT EXISTS audit_logs (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INT REFERENCES users(id),
    username VARCHAR(50) NOT NULL,
    action VARCHAR(100) NOT NULL,
    details TEXT NOT NULL
);

-- Índices de Performance
CREATE INDEX IF NOT EXISTS idx_orgs_group ON organizations(group_type);
CREATE INDEX IF NOT EXISTS idx_contacts_priority ON people_contacts(is_top_priority);
CREATE INDEX IF NOT EXISTS idx_interviews_code ON encoded_interviews(interview_code);
