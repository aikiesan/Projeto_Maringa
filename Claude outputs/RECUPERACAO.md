# Recuperação de 06/09/2026 — proveniência e pendências

O trabalho de 01/09/2026 (schema analítico, codebook, ferramentas de codificação e piloto
ENT-003) **nunca foi commitado**. O repositório `aikiesan/Projeto_Maringa` tem 7 commits,
o último em 25/07/2026, e não contém `docker-compose.yml`, `codebook/`, `tools/` nem
`database/schema_v2.sql`.

Esta pasta reconstrói o que era recuperável, a partir do `dashboard.json` que estava
embutido no artefato **"Repositório de Entrevistas de Maringá"** (versão de 01/09/2026) e
do artefato **"Protocolo de Codificação das Entrevistas"**.

## O que foi recuperado — e como

| Arquivo | Proveniência | Confiança |
|---|---|---|
| `codebook/dimensions.csv` | extraído do `dashboard.json` | **idêntico ao original** |
| `codebook/questions.csv` | idem | **idêntico ao original** |
| `codebook/question_dimension.csv` | idem | **idêntico ao original** |
| `codebook/interviews.csv` | idem | **idêntico ao original** |
| `codebook/evidencias/ENT-003.csv` | idem | **idêntico ao original** |
| `codebook/triage_matrix.csv` | idem (bloco `triage`) | **idêntico ao original** |
| `codebook/dashboard.json` | o JSON original, reindentado | **idêntico ao original** |
| `METODOLOGIA.md` | consolidado dos dois artefatos | conteúdo fiel; documento novo |
| `database/codebook.py` | reescrito sobre os dados recuperados | **dados originais, código novo** |
| `database/schema_v2.sql` | reescrito a partir do protocolo | **código novo** |
| `database/migrate.py` | idem | **código novo** |
| `tools/load_evidence.py` | idem | **código novo** |

Os arquivos marcados como "código novo" cumprem as mesmas funções descritas no protocolo,
mas não são byte a byte os originais. Se os originais aparecerem no disco do `nipe-pq-13`,
**prefira os originais** e descarte estes.

## Verificação

Todos os números documentados foram reproduzidos exatamente:

```
                 eixos: 4          sessoes_distintas: 14
         subcategorias: 13               codigos_ent: 15
             dimensoes: 55                   minutos: 686  (11h26)
             perguntas: 37        evidências ENT-003: 30 em 23 dimensões, 9 lacunas
    vinculos_crosswalk: 112       distribuição/eixo: 9 · 10 · 5 · 6
        palavras_chave: 328
```

Achados de integridade reproduzidos pela view `v_integrity`: 13 perguntas sem crosswalk,
3 dimensões sem pergunta (`1.1.4` e `3.1.3` Muito alta, `2.3.3` Alta), 1 duplicata
(`ENT-012`), 1 sem TCLE (`ENT-009`). A divergência `3.2.1` aparece em `v_divergences`.

O schema foi aplicado num **PostgreSQL 16 real**, duas vezes (idempotente); o codebook e as
30 evidências do piloto foram carregados e consultados pelas views.

## O que continua faltando

Existe apenas no disco do `nipe-pq-13`, em
`C:\Users\Lucas\Documents\CEPAL_Maringa\Projeto_Maringa`:

- `docker-compose.yml`, `Dockerfile`, `docker/entrypoint.sh`, `.env.example`, `start.ps1`,
  `AMBIENTE_LOCAL.md` — a subida do ambiente (PostgreSQL 16, volume `pgdata`, porta 55432,
  app Flask + adminer)
- `db.py` — camada psycopg com tradução `?`→`%s` e linhas dict+índice
- `database/seed_legacy.py` — carga de `data/*.json` nas tabelas do painel legado
- `tools/triage.py` — pré-triagem por palavras-chave sobre a transcrição
- `tools/ingest_registros.py` — popula `interviews` + `participants_vault` cruzando com a
  Lista de Entrevistas
- `tools/export_dashboard.py` — gera o `dashboard.json`
- `app.py` migrado para PostgreSQL, com os endpoints de codebook/evidence/coverage/health

`triage.py` e `ingest_registros.py` dependem do formato real das transcrições e da Lista de
Entrevistas — só valem a pena reescrever com esses arquivos à mão.

**Nada do acervo com PII foi tocado nesta recuperação.** Nenhum nome, contato ou termo
assinado passou por aqui: o `dashboard.json` já era a camada anonimizada.
