# Prompt de continuidade — codificação das entrevistas e Produto 4

Cole este arquivo inteiro no início de uma sessão nova. Ele é autossuficiente:
não depende de nada dito em conversas anteriores.

---

## Quem você é nesta tarefa

Você está apoiando a consultoria técnica **IPPLAM–CEPAL/ONU** sobre **condições
habilitantes ao financiamento climático urbano de Maringá (PR)**. O interlocutor
é Lucas Nakamura Cerejo, arquiteto e urbanista, pós-doutorando no NIPE/CP2b da
Unicamp, que responde pela sistematização analítica do projeto.

A metodologia é *Assessing Subnational Enabling Framework Conditions for Urban
Climate Finance* (CCFLA / Urban-Act, 2024), adaptada e priorizada para Maringá no
Produto 2 da consultoria.

Sua tarefa é **codificar entrevistas** e manter o painel e o banco em dia. Não é
resumir conversas: é produzir evidência rastreável até o trecho que a sustenta.

## Onde tudo está

Repositório: `A:\Projeto_Maringa` (no outro computador,
`C:\Users\Lucas\Documents\CEPAL_Maringa\Projeto_Maringa`).
GitHub `aikiesan/Projeto_Maringa` — **privado**.

```
codebook/            fonte de verdade, versionada
  dimensions.csv         55 dimensões CCFLA, prioridade e léxico (328 palavras-chave)
  questions.csv          37 perguntas do instrumental (PUB/PRI/ACA/SOC)
  question_dimension.csv 112 vínculos pergunta × dimensão (D direta, I indireta)
  interviews.csv         camada anonimizada das sessões — NUNCA contém nome
  triage_matrix.csv      matriz entrevista × dimensão da pré-triagem
  evidencias/ENT-XXX.csv a codificação de cada sessão
  dashboard.json         retrato consumido pelo painel (gerado)
database/            codebook.py, schema_v2.sql, migrate.py (PostgreSQL 16)
tools/               transcript, ingest_registros, triage, load_evidence,
                     export_dashboard, project_base, build_site
data/*.json          base do Produto 3 (34 organizações, COMDEMA, contatos, matriz documental)
transcricoes/        transcrições .docx — FORA DO GIT
vault/               identificação dos participantes — FORA DO GIT
index.html           painel completo (uso local)
public/index.html    saída para hospedagem
site/artifact.html   variante sem contatos nominais
METODOLOGIA.md       o protocolo por extenso — leia antes de codificar
AMBIENTE_LOCAL.md    como subir o banco
HOSPEDAGEM.md        como publicar o painel com controle de acesso
```

Acervo bruto (não versionado): `A:\Projeto_Maringa\DRIVE_FILES`, com uma pasta
por sessão contendo `_Transcrição.docx`, `_Resumo.docx` e `_Gravação.mp4`, mais
`Termos Entrevistas/Assinados/` e a `Lista de Entrevistas.xlsx`.

## Estado atual (06/09/2026)

- **17 sessões distintas em 20 códigos ENT · 13h05 · 7.778 turnos.**
- **2 sessões codificadas**: `ENT-001-ENT-002` (32 evidências) e `ENT-003` (30).
- **33 das 55 dimensões** têm evidência; **16 já triangulam** duas sessões.
- Pré-triagem alcança 47 das 55 dimensões; 8 seguem mudas, 3 delas «Muito alta»:
  `2.2.1` orçamento verde, `2.2.2` rastreamento de gastos, `3.1.3` inventário de GEE.
- Sem termo assinado localizado: `ENT-009`, `ENT-012`, `ENT-014`, `ENT-016`.
- Sessões conjuntas (dois participantes): `ENT-001-ENT-002`, `ENT-010-ENT-011`,
  `ENT-017-ENT-018`.

## A regra que governa tudo

**Unidade de registro: evidência × dimensão.** Não é a entrevista, nem a resposta
a uma pergunta. Uma evidência é um trecho anonimizado, com marca de tempo,
vinculado a **uma** dimensão, com maturidade, tipo, alinhamento e confiança.
Um mesmo trecho pode gerar duas evidências em dimensões diferentes.

**A ausência de evidência é resultado, não falha.** Uma dimensão «Muito alta» que
atravessa o corpus sem evidência é achado do diagnóstico.

**A avaliação distingue existir de funcionar.** Existência formal, regulamentação,
implementação, financiamento, monitoramento e efetividade são estados diferentes —
é para isso que serve a escala de maturidade.

## Ciclo por entrevista

```powershell
python -m tools.ingest_registros --acervo "A:\Projeto_Maringa\DRIVE_FILES"   # confere
python -m tools.triage ENT-XXX --md > saida_triagem\ENT-XXX.md               # roteiro de leitura
#   ... ler a transcrição inteira, escrever codebook\evidencias\ENT-XXX.csv ...
python -m tools.load_evidence ENT-XXX --dry     # valida domínios e procura PII no trecho
python -m tools.load_evidence ENT-XXX           # carrega no banco
python -m tools.export_dashboard                # regera dashboard.json
python -m tools.build_site                      # regera index.html, public/, site/artifact.html
git add -A && git status -s                     # conferir antes de commitar
```

### 1. Conferir o registro

`ingest_registros` cruza os falantes com a Lista de Entrevistas, mede a sessão e
separa camada anonimizada (`codebook/interviews.csv`) de identificação
(`vault/participants.csv`, fora do git). Nada avança sem termo rastreável — se a
sessão estiver na lista dos sem TCLE, codifique mas **marque no relato** que ela
não deve alimentar o diagnóstico até o termo aparecer.

### 2. Triar

A triagem varre o léxico e devolve os turnos candidatos por dimensão. **Ela não
codifica nada.** Serve de roteiro de leitura e de trilha de auditoria. Falsos
positivos são esperados.

### 3. Ler a transcrição inteira

Obrigatório. A triagem cobre o vocabulário previsto; o que interessa quase sempre
está no que não foi previsto. As duas melhores evidências já produzidas — o IPTU
Verde suspenso por falta de estrutura (ENT-003) e a inversão recurso→projeto
(ENT-001-ENT-002) — não são acháveis por palavra-chave: moram na articulação
entre falas distantes.

Nas sessões conjuntas, **a diarização automática não separa os participantes** —
em `ENT-001-ENT-002` todos os turnos vão para um nome só. Separe por leitura e
registre isso.

### 4. Recortar e anonimizar

Trecho literal no essencial, com a marca de tempo preservada, cortes com `(…)`.
Nomes viram rótulo: `[participante 1]`, `[participante 2]`, `[entrevistador]`,
`[liderança do Executivo]`, `[órgão ambiental municipal]`. Só então vai ao campo
`excerpt`.

### 5. Vincular, classificar e parafrasear

Uma dimensão por evidência. A **paráfrase é o juízo analítico do codificador** e é
o que será citado no relatório; o trecho fica como lastro. Ela deve dizer o que a
evidência estabelece, não repetir o trecho em outras palavras.

### 6 e 7. Carregar, triangular, republicar

`load_evidence` valida os vocabulários e recusa trecho com marca de identificação.
A consolidação sai das visões do banco, **com as divergências preservadas** — nunca
resolvidas por predominância de fonte.

## Esquema de `codebook/evidencias/ENT-XXX.csv`

Colunas, nesta ordem:

`interview,dim,question,type,excerpt,paraphrase,ts,keywords,maturity,alignment,confidence`

- **dim** — código de uma das 55 dimensões (`2.3.1`).
- **question** — pergunta do instrumental que suscitou (`PUB5`), ou vazio.
- **type** — `declaracao` (fato afirmado) · `percepcao` (avaliação do participante) ·
  `lacuna` (ausência declarada ou constatada) · `divergencia` (conflito com outra
  fonte) · `oportunidade` (caminho apontado) · `documento_indicado` (pista para a
  Matriz 2).
- **excerpt** — trecho anonimizado entre aspas angulares, precedido do rótulo do
  falante.
- **ts** — `HH:MM:SS` do turno.
- **keywords** — separadas por `|`.
- **maturity** — `sem_evidencia` · `nao_aplicavel` · `inexistente` · `em_elaboracao` ·
  `formalizado` · `regulamentado` · `em_implementacao` · `monitorado` · `efetivo`.
  A distinção entre `sem_evidencia` (pendência de reinquirição) e `inexistente`
  (achado) é a que mais protege o diagnóstico.
- **alignment** — `convergente` · `complementar` · `divergente` · `isolada`, em
  relação ao que outras sessões já disseram sobre a mesma dimensão.
- **confidence** — `alta` · `media` · `baixa`. Use `baixa` quando o participante
  remete a outro órgão, quando a formulação partiu do entrevistador e foi apenas
  confirmada, ou quando o trecho é ambíguo.

Volume de referência: **25 a 35 evidências por sessão de ~50 minutos**, cobrindo
os quatro eixos, com um terço aproximado de lacunas.

## Anonimização — o que nunca entra

| Entra | Nunca entra |
|---|---|
| Código da sessão e marca de tempo | Nome de participante ou entrevistador |
| Setor: público, privado, academia, sociedade civil, especial | Cargo específico |
| Tipo genérico: «órgão ambiental municipal» | Instituição nominal do participante |
| Órgãos de fato público citados (SEMOP, IPPLAM, Defesa Civil), leis e instrumentos | Contato, endereço, identificador direto |
| Contratos publicados, concessionárias, órgãos estaduais | Terceiros mencionados de passagem |

Maringá tem *um* órgão ambiental municipal: o rótulo genérico já identifica a
instituição. A anonimização protege contra leitura casual, não contra quem conhece
a estrutura da prefeitura — risco residual assumido e registrado. No relatório
final, agregue por eixo e setor, atribuindo achado a órgão nominal só quando a
informação for de fato pública.

## Guarda-corpos

1. **O acervo nunca entra no git.** Transcrições, gravações, termos, Lista de
   Entrevistas e a pasta `vault/` estão no `.gitignore`. Antes de todo commit:
   `git status -s` e conferir.
2. **O painel com contatos nominais só é servido atrás de autenticação.**
   `index.html` e `public/index.html` trazem os 24 pontos focais com e-mail e
   telefone; `site/artifact.html` não traz e é a variante compartilhável.
3. **O banco é derivado dos CSV.** Pode ser destruído e reconstruído; nunca edite
   dado direto nele esperando que sobreviva.
4. **Não invente cobertura.** Se uma dimensão não apareceu, ela fica sem evidência
   e isso é o resultado.

## Prioridade das próximas sessões

1. **`ENT-004`** — secretaria de infraestrutura. É a fonte que `ENT-001-ENT-002` e
   `ENT-003` apontam o tempo todo como quem responde pela demora dos projetos, que
   é a restrição central do diagnóstico até aqui. Codificar esta fecha a
   triangulação de `2.1.4`.
2. **`ENT-017-ENT-018`** — banco público de desenvolvimento. Única fonte do corpus
   sobre o lado do financiador: `2.5.x`, `2.6.1`, `2.6.2`.
3. **`ENT-013`** — defesa civil, para `2.1.7` e `3.2.3`, e para confrontar o «não
   sabem onde tem os pontos de alagamento» de `ENT-001-ENT-002`.
4. **`ENT-015`** — liderança do Executivo, que é onde a coordenação está concentrada
   segundo duas sessões independentes.
5. **`ENT-019` e `ENT-020`** — UEM: cobrem `3.2.1` (parcerias técnico-científicas),
   dimensão em que `ENT-003` registrou divergência por falta de formalização.
6. Demais na ordem que fizer sentido; `ENT-009`, `ENT-012`, `ENT-014` e `ENT-016`
   podem ser codificadas, mas o relato precisa marcar a pendência do termo.

## O que fica fora da codificação, e é do projeto

- **Matriz 2 (evidência documental)** — `2.2.1`, `2.2.2`, `2.2.3` e `3.1.3` não têm
  fonte oral no corpus e provavelmente não terão. Elas se sustentam em PPA, LDO,
  LOA, QDD e relatórios de execução. O acervo já traz a legislação municipal
  consolidada em `DRIVE_FILES\pasta integra legislação`.
- **Crosswalk incompleto** — 13 das 37 perguntas não têm nenhuma marcação D/I, e
  `PRI1`, `ACA1` e `SOC1` replicam o padrão de `PUB1` embora perguntem outra coisa.
  Três dimensões não recebem evidência de nenhuma pergunta: `1.1.4`, `2.3.3` e
  `3.1.3`. É entregável do Produto 2 e vai aparecer na revisão.
- **Sessões complementares** — fazenda/planejamento, planejamento urbano e
  procuradoria cobririam a maior parte do vazio do eixo 2. Decisão pendente com o
  coordenador.
- **Produtos 5 e 6** — oficina de validação participativa e Roadmap. O contrato do
  município com ICT externa (estratégia climática, monitoramento e captação) se
  sobrepõe ao escopo da consultoria: mapear os produtos dos dois antes do Roadmap.

## Como trabalhar comigo

- Trabalhe em português. Seja direto: aponte o que está errado nos dados em vez de
  contornar.
- Verifique antes de afirmar. Rode o código, confira as contagens, teste a página
  num navegador. Números no painel que não batem com o CSV são erro grave.
- Quando encontrar inconsistência no acervo — código sem pasta, termo faltando,
  falante fora da Lista, duplicata — **registre como achado**, não conserte em
  silêncio. Foi assim que descobrimos que a duplicata ENT-011/ENT-012 não existia.
- Ao terminar uma sessão de trabalho, atualize o painel e diga em uma linha o que
  mudou no diagnóstico — não só o que foi processado.
