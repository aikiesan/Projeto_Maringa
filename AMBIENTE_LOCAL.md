# Ambiente local

## Subir

Com o Docker Desktop em execução, na raiz do repositório:

```powershell
.\start.ps1
```

O script cria o `.env` a partir do `.env.example`, sobe PostgreSQL 16 e Adminer,
espera o banco responder, aplica o schema e carrega o codebook e as evidências.

Manualmente, se preferir:

```powershell
copy .env.example .env
docker compose up -d
$env:DATABASE_URL = "postgresql://maringa:maringa@localhost:55432/maringa"
python -m database.migrate
python -m tools.load_evidence --all
```

Dependência Python: `pip install "psycopg[binary]"`.

- Banco: `localhost:55432`, base `maringa`, usuário `maringa`.
- Adminer: <http://localhost:8080> — sistema PostgreSQL, servidor `db`.
- `docker compose down` para; `docker compose down -v` apaga o volume `pgdata`.

## O que é fonte de verdade

Os CSV de `codebook/`. **O banco é derivado deles** e pode ser destruído e
reconstruído a qualquer momento — `migrate` e `load_evidence` são idempotentes.
Nunca edite dados direto no banco esperando que sobrevivam.

## Fluxo de uma entrevista

```powershell
python -m tools.triage ENT-XXX --md > saida_triagem\ENT-XXX.md   # 1. roteiro de leitura
#                                                                  2. ler a transcrição inteira
#                                                                  3. escrever codebook\evidencias\ENT-XXX.csv
python -m tools.load_evidence ENT-XXX --dry                       # 4. validar
python -m tools.load_evidence ENT-XXX                             # 5. carregar
python -m tools.export_dashboard                                  # 6. regerar dashboard.json
python -m tools.build_site                                        # 7. regerar index.html
```

A saída da triagem contém nomes de falantes: é material de trabalho, fica fora
do git (`saida_triagem/` está no `.gitignore`).

## Consultas úteis

```sql
SELECT * FROM v_axis_coverage;                      -- cobertura por eixo
SELECT * FROM v_dimension_coverage WHERE uncovered; -- dimensões sem evidência
SELECT * FROM v_divergences;                        -- conflitos entre fontes
SELECT * FROM v_integrity;                          -- pendências do acervo
SELECT * FROM v_evidence_public WHERE dimension = '2.3.1';
```

## Acervo e privacidade

As transcrições, gravações, termos e a Lista de Entrevistas **não entram no
git** (ver `.gitignore`). A camada anonimizada autoritativa é
`codebook/interviews.csv`; a identificação existe apenas em
`participants_vault`, no banco local, sem endpoint de leitura.

O repositório é público — antes de qualquer `git add`, confira com
`git status` que nada do acervo entrou.
