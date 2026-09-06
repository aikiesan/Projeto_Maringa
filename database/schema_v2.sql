-- =====================================================================
-- Projeto CEPAL/IPPLAM — Maringá
-- Schema analítico v2 (PostgreSQL 16)
--
-- Unidade de registro: EVIDÊNCIA × DIMENSÃO (não resposta × pergunta).
-- Camada de análise anonimizada; PII isolada em participants_vault, que
-- nenhum endpoint da API expõe.
--
-- RECONSTRUÍDO em 06/09/2026 a partir do protocolo publicado e do
-- dashboard.json recuperado do artefato. Compatível com os CSV de
-- `codebook/`. Idempotente.
-- =====================================================================

BEGIN;

-- ------------------------------------------------------------- domínios

DO $$ BEGIN
  CREATE TYPE maturity_t AS ENUM (
    'sem_evidencia','nao_aplicavel','inexistente','em_elaboracao','formalizado',
    'regulamentado','em_implementacao','monitorado','efetivo');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
  CREATE TYPE evidence_t AS ENUM (
    'declaracao','percepcao','lacuna','divergencia','oportunidade','documento_indicado');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
  CREATE TYPE alignment_t AS ENUM ('convergente','complementar','divergente','isolada');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
  CREATE TYPE confidence_t AS ENUM ('alta','media','baixa');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
  CREATE TYPE sector_t AS ENUM ('Publico','Privado','Academia','Sociedade Civil','Especial');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

-- --------------------------------------------------------- estrutura CCFLA

CREATE TABLE IF NOT EXISTS axes (
  num          SMALLINT PRIMARY KEY,
  name         TEXT NOT NULL,
  short_name   TEXT,
  name_en      TEXT
);

CREATE TABLE IF NOT EXISTS subcategories (
  code         TEXT PRIMARY KEY,
  axis         SMALLINT NOT NULL REFERENCES axes(num),
  name         TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS dimensions (
  code         TEXT PRIMARY KEY,
  axis         SMALLINT NOT NULL REFERENCES axes(num),
  subcat       TEXT NOT NULL REFERENCES subcategories(code),
  name         TEXT NOT NULL,
  priority     TEXT,
  rank         SMALLINT NOT NULL DEFAULT 0 CHECK (rank BETWEEN 0 AND 4),
  keywords     TEXT[] NOT NULL DEFAULT '{}'
);
CREATE INDEX IF NOT EXISTS dimensions_axis_idx ON dimensions(axis);
CREATE INDEX IF NOT EXISTS dimensions_rank_idx ON dimensions(rank DESC);

CREATE TABLE IF NOT EXISTS questions (
  id           TEXT PRIMARY KEY,
  block        TEXT NOT NULL CHECK (block IN ('PUB','PRI','ACA','SOC')),
  text         TEXT NOT NULL
);

-- Crosswalk do Produto 2. Controle de qualidade do instrumental —
-- NÃO é caminho obrigatório da codificação.
CREATE TABLE IF NOT EXISTS question_dimension (
  question_id  TEXT NOT NULL REFERENCES questions(id) ON DELETE CASCADE,
  dimension    TEXT NOT NULL REFERENCES dimensions(code) ON DELETE CASCADE,
  relation     CHAR(1) NOT NULL CHECK (relation IN ('D','I')),
  PRIMARY KEY (question_id, dimension)
);

-- ------------------------------------------------- entrevistas (anonimizado)

CREATE TABLE IF NOT EXISTS interviews (
  code               TEXT PRIMARY KEY,
  canonical          TEXT NOT NULL,          -- código da sessão real (duplicatas apontam para ela)
  is_duplicate       BOOLEAN NOT NULL DEFAULT FALSE,
  sector             sector_t,
  institution_type   TEXT,                   -- tipo GENÉRICO; nunca a instituição nominal
  block              TEXT CHECK (block IN ('PUB','PRI','ACA','SOC')),
  interview_date     DATE,
  n_participants     SMALLINT DEFAULT 1,
  tcle_signed        BOOLEAN NOT NULL DEFAULT FALSE,  -- nunca por inferência
  status             TEXT,
  minutes            INTEGER,
  turns              INTEGER,
  chars              INTEGER,
  participant_share  SMALLINT,               -- % do texto que é fala do entrevistado
  notes              TEXT
);
CREATE INDEX IF NOT EXISTS interviews_sector_idx ON interviews(sector);

-- PII. Sem endpoint de leitura. Acesso apenas por conexão direta ao banco.
CREATE TABLE IF NOT EXISTS participants_vault (
  id             SERIAL PRIMARY KEY,
  interview_code TEXT NOT NULL REFERENCES interviews(code) ON DELETE CASCADE,
  full_name      TEXT,
  role_title     TEXT,
  institution    TEXT,
  email          TEXT,
  phone          TEXT,
  tcle_file      TEXT,
  matched_by     TEXT,        -- 'lista' | 'manual'
  created_at     TIMESTAMPTZ NOT NULL DEFAULT now()
);
COMMENT ON TABLE participants_vault IS
  'PII sob TCLE. Anexo 02. Nao expor em nenhum endpoint da API.';

-- ------------------------------------------------------------- evidências

CREATE TABLE IF NOT EXISTS evidence (
  id             SERIAL PRIMARY KEY,
  interview_code TEXT NOT NULL REFERENCES interviews(code) ON DELETE CASCADE,
  dimension      TEXT NOT NULL REFERENCES dimensions(code),
  question_id    TEXT REFERENCES questions(id),
  ev_type        evidence_t NOT NULL,
  excerpt_anon   TEXT NOT NULL,     -- trecho literal anonimizado, com marca de tempo
  paraphrase     TEXT,              -- juízo analítico do codificador (vai ao relatório)
  ts             TEXT,              -- 00:00:00
  keywords       TEXT[] DEFAULT '{}',
  maturity       maturity_t NOT NULL DEFAULT 'sem_evidencia',
  alignment      alignment_t,
  confidence     confidence_t NOT NULL DEFAULT 'media',
  source_file    TEXT,              -- codebook/evidencias/ENT-XXX.csv
  created_at     TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS evidence_dim_idx  ON evidence(dimension);
CREATE INDEX IF NOT EXISTS evidence_int_idx  ON evidence(interview_code);
CREATE INDEX IF NOT EXISTS evidence_mat_idx  ON evidence(maturity);

-- Ponte com a Matriz 2 (evidência documental): um documento confirma,
-- qualifica ou contradiz uma evidência de entrevista.
CREATE TABLE IF NOT EXISTS documents (
  id           SERIAL PRIMARY KEY,
  ref          TEXT UNIQUE NOT NULL,
  title        TEXT NOT NULL,
  doc_type     TEXT,               -- lei, decreto, PPA, LDO, LOA, QDD, contrato, relatorio
  year         SMALLINT,
  url          TEXT,
  notes        TEXT
);

CREATE TABLE IF NOT EXISTS evidence_document (
  evidence_id  INTEGER NOT NULL REFERENCES evidence(id) ON DELETE CASCADE,
  document_id  INTEGER NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
  relation     TEXT NOT NULL CHECK (relation IN ('confirma','qualifica','contradiz')),
  note         TEXT,
  PRIMARY KEY (evidence_id, document_id)
);

-- Pré-triagem por palavra-chave. Não é evidência — é trilha de auditoria
-- de por que aquele trecho foi lido.
CREATE TABLE IF NOT EXISTS triage_hits (
  interview_code TEXT NOT NULL REFERENCES interviews(code) ON DELETE CASCADE,
  dimension      TEXT NOT NULL REFERENCES dimensions(code) ON DELETE CASCADE,
  hits           INTEGER NOT NULL DEFAULT 0,
  PRIMARY KEY (interview_code, dimension)
);

-- --------------------------------------------------------------- visões

CREATE OR REPLACE VIEW v_evidence_public AS
SELECT e.id, e.interview_code, i.sector, i.institution_type,
       e.dimension, d.name AS dimension_name, d.axis, d.subcat, d.priority, d.rank,
       e.ev_type, e.maturity, e.alignment, e.confidence,
       e.ts, e.excerpt_anon, e.paraphrase
FROM evidence e
JOIN dimensions d ON d.code = e.dimension
JOIN interviews i ON i.code = e.interview_code
WHERE NOT i.is_duplicate;

CREATE OR REPLACE VIEW v_dimension_coverage AS
SELECT d.code, d.name, d.axis, d.subcat, d.priority, d.rank,
       COUNT(e.id)                                   AS n_evidence,
       COUNT(DISTINCT e.interview_code)              AS n_interviews,
       COUNT(*) FILTER (WHERE e.ev_type = 'lacuna')  AS n_gaps,
       MAX(e.maturity::TEXT)                         AS maturity_seen,
       (COUNT(e.id) = 0)                             AS uncovered
FROM dimensions d
LEFT JOIN evidence e   ON e.dimension = d.code
LEFT JOIN interviews i ON i.code = e.interview_code AND NOT i.is_duplicate
GROUP BY d.code, d.name, d.axis, d.subcat, d.priority, d.rank;

CREATE OR REPLACE VIEW v_axis_coverage AS
SELECT a.num AS axis, a.name,
       COUNT(DISTINCT d.code)                                    AS n_dimensions,
       COUNT(DISTINCT d.code) FILTER (WHERE c.n_evidence > 0)    AS n_covered,
       COUNT(DISTINCT d.code) FILTER (WHERE d.rank = 4 AND c.n_evidence = 0)
                                                                 AS n_gaps_priority,
       SUM(c.n_evidence)                                         AS n_evidence
FROM axes a
JOIN dimensions d          ON d.axis = a.num
JOIN v_dimension_coverage c ON c.code = d.code
GROUP BY a.num, a.name
ORDER BY a.num;

-- Divergências preservadas, não resolvidas por predominância de fonte.
CREATE OR REPLACE VIEW v_divergences AS
SELECT dimension, dimension_name, axis, priority,
       COUNT(*) AS n, array_agg(DISTINCT interview_code) AS interviews
FROM v_evidence_public
WHERE alignment = 'divergente' OR ev_type = 'divergencia'
GROUP BY dimension, dimension_name, axis, priority;

CREATE OR REPLACE VIEW v_integrity AS
SELECT 'sem_tcle' AS issue, code AS ref,
       'Entrevista sem termo assinado localizado' AS detail
FROM interviews WHERE NOT tcle_signed AND NOT is_duplicate
UNION ALL
SELECT 'duplicata', code, 'Codigo sem registro proprio; aponta para ' || canonical
FROM interviews WHERE is_duplicate
UNION ALL
SELECT 'pergunta_sem_crosswalk', q.id, 'Pergunta sem nenhuma marcacao D/I'
FROM questions q
LEFT JOIN question_dimension qd ON qd.question_id = q.id
WHERE qd.question_id IS NULL
UNION ALL
SELECT 'dimensao_sem_pergunta', d.code, 'Nenhuma pergunta aponta para a dimensao (prioridade '
       || COALESCE(d.priority,'?') || ')'
FROM dimensions d
LEFT JOIN question_dimension qd ON qd.dimension = d.code
WHERE qd.dimension IS NULL;

COMMIT;
