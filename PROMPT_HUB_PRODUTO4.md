# Prompt de continuidade — Hub público e Produto 4

Cole este arquivo inteiro no início de uma sessão nova do Claude Code, a partir de
`A:\Projeto_Maringa`. Ele é autossuficiente: não depende de nada dito em conversas
anteriores.

---

## 1. Quem você é nesta tarefa

Você apoia a consultoria técnica **IPPLAM–CEPAL/ONU** sobre **condições habilitantes
ao financiamento climático urbano de Maringá (PR)**, executada pela Brisa Soluções
Ambientais. O interlocutor é Lucas Nakamura Cerejo, arquiteto e urbanista,
pós-doutorando no NIPE/CP2b da Unicamp, responsável pela sistematização analítica.

A metodologia é *Assessing Subnational Enabling Framework Conditions for Urban
Climate Finance* (CCFLA / Urban-Act, 2024), adaptada e priorizada para Maringá no
Produto 2.

**O objetivo desta fase: entregar o Produto 04 e publicá-lo como peça central de um
Hub público** — um site que apresenta o projeto, expõe o diagnóstico e abre o
repositório de evidências para quem quiser conferir.

## 2. Como trabalhar

- Português. Direto: aponte o que está errado nos dados em vez de contornar.
- **Verifique antes de afirmar.** Rode o código, confira as contagens, abra a página
  num navegador. Número que não bate com o CSV é erro grave.
- Quando encontrar inconsistência no acervo — código sem pasta, termo faltando,
  falante fora da lista, duplicata — **registre como achado**, não conserte em
  silêncio.
- **`git fetch` e leia `origin/main` antes de escrever ferramenta nova.** Em
  12/09/2026 duas linhas de trabalho paralelas reconstruíram o mesmo anonimizador
  sem saber uma da outra. Foi caro.
- Ao terminar, diga em uma linha o que mudou **no diagnóstico**, não só o que foi
  processado.

---

## 3. Onde tudo está

### Repositórios

| Repositório | Conteúdo | Visibilidade |
|---|---|---|
| `aikiesan/Projeto_Maringa` | codebook, ferramentas, produtos, acervo fora do git | **privado** |
| `aikiesan/Maringa` | o Hub público | **público** — <https://aikiesan.github.io/Maringa/> |

Clones locais: `A:\Projeto_Maringa` e `A:\Maringa`.
Backup espelho pré-reescrita: `A:\Projeto_Maringa_backup.git` (**não apague**).

O histórico do repositório privado **foi reescrito** em 12/09/2026 com
`git-filter-repo`, removendo as três cópias de `contacts.json`, o `index.html` e o
`public/index.html` que embutiam os 24 pontos focais, as planilhas de entrevistados
e convidados, e quatro binários. Passou de 55 MB para 4,7 MB, de 29 para 23 commits.
**Qualquer clone anterior a essa data é inválido** — apague e reclone, nunca `git pull`.

### Estrutura do repositório privado

```
codebook/                     fonte de verdade, versionada
  dimensions.csv                55 dimensões CCFLA, prioridade e léxico
  questions.csv                 37 perguntas do instrumental (PUB/PRI/ACA/SOC)
  question_dimension.csv        112 vínculos pergunta × dimensão
  interviews.csv                camada anonimizada das sessões — NUNCA contém nome
  triage_matrix.csv             matriz entrevista × dimensão da pré-triagem
  evidencias/ENT-XXX.csv        a codificação de cada sessão (494 evidências)
  anonimizacao_lexico.csv       instituições, para o motor de redação
  anonimizacao_permitidos.csv   allowlist de tokens capitalizados
  dashboard.json                retrato consumido pelo painel (gerado)
database/                     codebook.py, schema_v2.sql, migrate.py (PostgreSQL 16)
tools/
  transcript.py ingest_registros.py triage.py load_evidence.py export_dashboard.py
  project_base.py build_site.py lock.py
  redacao.py                    motor de anonimização: substituição + varredura
  anonimizar_transcricoes.py    passo 8 do protocolo; escreve FORA do git
  p4_base.py                    contagens do Produto 4
  p4_ancorar.py                 âncoras de evidência para as afirmações da Seção 3
  publico.py                    saneia site/artifact.html para a camada aberta
  scan_pii.py                   varredura da saída aberta; recusa publicação
  hub/                          gerador do Hub — base.py dados.py paginas.py
                                transcricoes.py build.py varre_hub.py
produtos/
  LEIA-ME.md  P4_matriz_v2.md  P4_ancoras_secao3.csv
tests/test_redacao.py
anexos/Produto_4.docx         o produto (versionado)
hub_saida/                    saída do Hub (gerada; fora do git)
site/, index.html, public/    saídas geradas (fora do git)
vault/                        identificação dos participantes (fora do git)
DRIVE_FILES/                  acervo bruto (fora do git)
METODOLOGIA.md  HOSPEDAGEM.md  AMBIENTE_LOCAL.md  PROMPT_CODIFICACAO.md
```

Acervo bruto em `A:\Projeto_Maringa\DRIVE_FILES`: uma pasta por sessão com
`_Transcrição.docx`, `_Resumo.docx` e `_Gravação.mp4`; `Termos Entrevistas/Assinados/`;
`pasta integra legislação/` com a legislação municipal consolidada; a Lista de
Entrevistas; os produtos 1, 2 e 3; a metodologia CEPAL.

---

## 4. Estado do corpus — números conferidos

**17 sessões distintas em 20 códigos · 785 min (13h05) · 7.778 turnos · 20 participantes.**

- **494 evidências**, todas codificadas.
- **51 das 55 dimensões** têm evidência; **47 triangulam** duas ou mais sessões.
- Sem fonte oral: `1.1.2` (alinhamento da mitigação com NDC/plano estadual),
  `1.1.3` (MRV para mitigação), `2.5.4` (acesso a mercado de capitais),
  `2.5.5` (títulos verdes) — todas de prioridade **Média**.
- As quatro «Muito alta» que estavam mudas em 06/09 — `2.2.1` orçamento verde,
  `2.2.2` rastreamento de gastos, `2.2.3` integração orçamentária, `3.1.3`
  inventário de GEE — **foram cobertas** pelo campo.

Maturidade das 494: **inexistente 206 · em elaboração 77 · formalizado 14 ·
regulamentado 13 · em implementação 159 · monitorado 1 · efetivo 17.**

Alinhamento: convergente 252 · complementar 105 · isolada 85 · divergente 50.

Tipo: declaração 264 · lacuna 82 · percepção 59 · oportunidade 59 · divergência 30.

Setores (após extinguir «Especial», que voltou a Público): Público 7 sessões e 226
evidências · Sociedade Civil 4 e 115 · Privado 3 e 77 · Academia 3 e 76.

Sessões conjuntas, dois participantes: `ENT-001-ENT-002`, `ENT-010-ENT-011`,
`ENT-017-ENT-018`.

### O achado que organiza tudo

**42% das evidências dizem que a condição avaliada é inexistente; 17 dizem que é
efetiva; uma diz que é monitorada.** Maringá não tem problema de ausência de agenda
climática — tem problema de travessia, da formalização até a efetividade. O gargalo
não é criar instrumento novo; é regulamentar, financiar e monitorar os que existem.

A `produtos/P4_matriz_v2.md` chega ao mesmo lugar por outro caminho: a maturidade
por **moda**, não por média, porque a distribuição é **bimodal em oito das treze
subcategorias** — condição que existe numa frente e não existe noutra.

### Bases do Produto 3 e documental

- `data/comdema.json` — **124 conselheiros** do COMDEMA, 2021–2026, com afiliação e
  anos de presença. **Três** atravessaram os seis anos; **92 (74%)** passaram por um
  ou dois anos apenas. Composição anual: 47 · 50 · 46 · 53 · 48 · 27.
- `data/organizations.json` — **34 organizações** mapeadas, classificadas pelas
  dimensões D1–D4.
- Legislação: **22 normas** municipais mapeadas (listagem em
  `DRIVE_FILES\pasta integra legislação\LIstagem atualizada da legislação.docx`;
  extraída para `hub_saida\dados\legislacao.csv`).

---

## 5. As regras que governam tudo

### 5.1 A unidade de registro é a evidência

Não é a entrevista nem a resposta a uma pergunta. Uma evidência é um trecho
anonimizado, com marca de tempo, vinculado a **uma** dimensão, com tipo, maturidade,
alinhamento e confiança. Um mesmo trecho pode gerar duas evidências em dimensões
diferentes.

Esquema de `codebook/evidencias/ENT-XXX.csv`, nesta ordem:

`interview,dim,question,type,excerpt,paraphrase,ts,keywords,maturity,alignment,confidence`

- **type** — `declaracao` · `percepcao` · `lacuna` · `divergencia` · `oportunidade` ·
  `documento_indicado`
- **maturity** — `sem_evidencia` · `nao_aplicavel` · `inexistente` · `em_elaboracao` ·
  `formalizado` · `regulamentado` · `em_implementacao` · `monitorado` · `efetivo`.
  A distinção entre `sem_evidencia` (pendência de reinquirição) e `inexistente`
  (achado) é a que mais protege o diagnóstico.
- **alignment** — `convergente` · `complementar` · `divergente` · `isolada`
- **confidence** — `alta` · `media` · `baixa`. Baixa quando o participante remete a
  outro órgão, quando a formulação partiu do entrevistador e foi apenas confirmada,
  ou quando o trecho é ambíguo.

A **paráfrase é o juízo analítico do codificador** e é o que se cita; o trecho fica
como lastro.

### 5.2 Ausência de evidência é resultado

Uma dimensão «Muito alta» que atravessa o corpus sem evidência é achado do
diagnóstico, não falha de coleta. **Não invente cobertura.**

### 5.3 Divergência não se resolve

As 50 evidências divergentes são preservadas, nunca resolvidas por predominância de
fonte. São o material da validação participativa (oficinas de 22–24/09).

### 5.4 Tudo é derivado, nada é digitado

Se um número aparece numa página ou num produto, ele saiu de uma ferramenta que leu
um CSV versionado. `produtos/LEIA-ME.md` diz isso do lado do Produto 4; o
`tools/hub/` faz o mesmo do lado do Hub. **Corrigir um número significa corrigir o
codebook ou a ferramenta, nunca a saída.**

### 5.5 Anonimização — o que nunca entra

| Entra | Nunca entra |
|---|---|
| Código da sessão e marca de tempo | Nome de participante ou entrevistador |
| Setor: público, privado, academia, sociedade civil | Cargo específico |
| Tipo genérico: «órgão ambiental municipal» | Instituição nominal do participante |
| Órgãos de fato público (SEMOP, IPPLAM, Defesa Civil), leis, instrumentos | Contato, endereço, identificador direto |
| Contratos publicados, concessionárias, órgãos estaduais | Terceiros mencionados de passagem |

Maringá tem *um* órgão ambiental municipal: o rótulo genérico já identifica a
instituição. A anonimização protege contra leitura casual, não contra quem conhece a
estrutura da prefeitura — **risco residual assumido e registrado**.

**Conselheiro é exceção declarada.** A composição de conselho municipal é ato
público, publicada em portaria, e aparece **nominalmente** no Hub — mas só em
`conselhos.html` e `dados/comdema.csv`. Em qualquer outra página, nome de
conselheiro é achado da varredura.

### 5.6 Três sessões o nome não protege

`ENT-008` (órgão ambiental), `ENT-012` (Legislativo) e `ENT-015` (Executivo) são
reidentificáveis **pelo cargo**, não pelo nome. Nelas, além da substituição, foram
suprimidos os trechos autoidentificadores — vínculo familiar, voto declarado,
presidência de comissão nominal, referência direta à função. Cada corte está em
`anexos\cortes.csv` com sessão, parágrafo, motivo e texto removido, e aparece no
texto como `(…)`.

Na camada aberta, `ENT-008` e `ENT-015` têm o rótulo institucional generalizado ao
nível do órgão (`Direção de órgão ambiental municipal` → `Órgão ambiental
municipal`; `Liderança política do Executivo municipal` → `Gabinete do Executivo
municipal`), e o setor «Especial» foi extinto — as três voltam a `Publico`.

### 5.7 Guarda-corpos de publicação

1. **O acervo nunca entra no git.** Transcrições, gravações, termos, Lista de
   Entrevistas e `vault/` estão no `.gitignore`. Antes de todo commit: `git status -s`.
2. **Saída de anonimização não entra no git**, nem no repositório privado —
   `saida_anonimizacao/` e `anexos/Anexo_05*.zip` são ignorados. Histórico de git
   não se apaga com `rm`.
3. **`anexos/cortes.csv` e `anexos/revisao_nomes.csv` nunca vão a lugar nenhum.**
   O primeiro guarda exatamente o texto autoidentificador que foi suprimido.
4. **Nada é publicado sem passar na varredura.** `tools/scan_pii.py` para o painel,
   `tools/hub/varre_hub.py` para o Hub. Ambos saem com código ≠ 0 e recusam.
5. **O banco é derivado dos CSV.** Pode ser destruído e reconstruído.

---

## 6. O que já está pronto

### 6.1 O Hub (`A:\Projeto_Maringa\hub_saida\`, gerador em `tools\hub\`)

Sete páginas, 35 arquivos, varredura limpa:

| Página | Conteúdo |
|---|---|
| `index.html` | faixa de abertura, quatro números, o achado dos 42%, distribuição de maturidade, quem foi ouvido, cartões para as demais |
| `painel.html` | o painel de evidências completo (gerado por `tools/publico.py`) |
| `conselhos.html` | 124 conselheiros com busca e filtro, continuidade, composição por grupo ano a ano |
| `instituicoes.html` | 34 organizações por dimensão CCFLA, com busca |
| `legislacao.html` | 22 normas, com busca |
| `transcricoes.html` | índice das 17 sessões → `transcricoes/ENT-XXX.html` |
| `dados.html` | 7 arquivos para download + dicionário de dados completo |

Regenerar: `python -m tools.hub.build` e depois `python -m tools.hub.varre_hub`.

### 6.2 Identidade visual

Família verde do material de apresentação: **verde-floresta `#255438`**,
**verde-menta `#33DD9A`**. A marca de onda foi extraída do logotipo da Brisa e
recolorida (`hub_saida\marca\onda.png`); o wordmark preto (`brisa.png`) e o da
CEPAL (`cepal.png`) aparecem no cabeçalho e no rodapé, com inversão automática no
modo escuro via `--logo`.

**A paleta dos gráficos é outra coisa e não se mexe sem validar.** A ordem
categórica é `#1baf7a · #eb6834 · #2a78d6 · #eda100` (claro) e
`#199e70 · #d95926 · #3987e5 · #c98500` (escuro) — verde na primeira posição para
casar com a marca, e validada em ambos os modos (pior par adjacente ΔE 9.2
protan/deutan, 27.6 visão normal). A ordem alternativa que põe amarelo ao lado de
laranja **falha** o piso de visão normal (ΔE 13.7). Trocar cor de série por cor de
marca exige rodar o validador de novo.

### 6.3 Produto 4 — duas metades que encaixam

- **Seções 1 a 3** já existiam: introdução, processo participativo, instrumentais e
  metodologia, e a análise por grupo de atores × eixo (3.1 a 3.4).
- **Capítulo 4 (Relação com o Plano de Ação), Considerações Finais e Anexos 01–06**
  foram escritos e estão em **`A:\Projeto_Maringa\anexos\Produto_4.docx`** —
  367 parágrafos. *Atenção: circula por aí uma cópia de 328 parágrafos, que é a
  versão anterior, sem esses capítulos. Confira a contagem antes de editar.*
- **`produtos/P4_ancoras_secao3.csv`** traz três âncoras candidatas para cada uma
  das 93 afirmações da Seção 3, com sessão, dimensão, marca de tempo e `score`:
  34 afirmações com candidato forte (≥0,30), 51 médio, 8 fracas. **Não estão
  validadas** — sobreposição léxica acha candidato, não prova sustentação.
- **`produtos/P4_matriz_v2.md`** é a Matriz de Avaliação que o TdR exige
  (Produto 1, §2.2), com maturidade por moda e a coluna *perfil* declarando a forma
  da distribuição.

---

## 7. O que fazer agora

O pedido: **entregar um Hub com o Produto 4 bem elaborado.** Traduzindo em trabalho:

### Tarefa 1 — O Produto 4 como peça do Hub

Hoje o Hub expõe o *material* (evidências, conselhos, instituições, legislação,
transcrições) mas não expõe **o produto**. Criar `produto4.html`:

- o Produto 04 em versão web legível, navegável por seção, gerado a partir do
  `.docx` — não recopiado à mão;
- **cada afirmação da Seção 3 ligada às suas âncoras de evidência**, usando
  `produtos/P4_ancoras_secao3.csv`. Uma afirmação com âncora aceita vira link para a
  evidência no painel; uma sem âncora aceita fica sem link, e isso precisa ser
  visível — é o mesmo princípio de «ausência de evidência é resultado»;
- a Matriz de Avaliação (`P4_matriz_v2.md`) renderizada como tabela, com o perfil de
  distribuição por subcategoria;
- o `.docx` disponível para download, com a data da versão.

**Antes disso, rode `python -m tools.p4_ancorar` de novo contra o `.docx` de 367
parágrafos.** As âncoras atuais foram geradas contra a versão de 328 e as contagens
do `LEIA-ME.md` (93 afirmações, 34 fortes) vão mudar. Atualize o `LEIA-ME.md` com as
contagens novas.

### Tarefa 2 — A validação humana das âncoras

O `p4_ancorar` ordena por `score`, não decide. Construir o fluxo de aceitação:
uma planilha ou CSV de revisão em que Lucas marca cada âncora como aceita, rejeitada
ou substituída, e a página do Produto 4 só cita as aceitas. As 8 afirmações com
candidato fraco precisam de leitura antes de virar citação.

### Tarefa 3 — Portar a supressão de trecho para o pipeline

`tools/redacao.py` substitui nomes e **detecta** cargo como resíduo, mas não tem o
conceito de **suprimir trecho**. Os 10 cortes hoje vivem em `anexos\cortes.csv`, fora
do fluxo. Transformar em `codebook/supressoes.csv` — sessão, âncora textual, motivo —
aplicado por `anonimizar_transcricoes.py` depois da substituição, com teste em
`tests/test_redacao.py`. Enquanto isso não existir, regerar as transcrições **desfaz**
a proteção de ENT-008, ENT-012 e ENT-015.

### Tarefa 4 — Semear o `vault/terceiros.csv`

`anexos\revisao_nomes.csv` traz 124 ocorrências de 72 candidatos a nome próprio de
terceiro citado em entrevista, com contexto. Levantar de novo é desperdício.
Figuras públicas mundiais (Trump, Guterres, Bolsonaro, Getúlio Vargas) foram
preservadas de propósito e não devem ir para o dicionário.

### Tarefa 5 — Publicar

```bash
cd /a/Projeto_Maringa
python -m tools.hub.build
python -m tools.hub.varre_hub          # tem que sair 0
cp -r hub_saida/* /a/Maringa/
cd /a/Maringa
git add -A && git commit -m "..." && git push
```

O Pages serve `main` / `(root)` e leva um a dois minutos.

---

## 8. Critérios de aceitação

1. `python -m tools.hub.varre_hub` sai **0** — nenhum nome de participante, contato,
   rótulo de risco ou setor «Especial» em qualquer página.
2. Todo número exibido no Hub e no Produto 4 bate com o CSV de origem. Confira pelo
   menos: 494 evidências, 51/55 dimensões, 47 trianguladas, 206 inexistentes,
   124 conselheiros, 3 com seis anos, 34 organizações, 22 normas.
3. As páginas abrem e renderizam em 1180 px e em 390 px, nos modos claro e escuro.
   **Olhe as capturas** — o validador confere cor, não layout. Um bug real que já
   aconteceu: barra de gráfico com largura em `<i>` inline, que não aplica sem
   `display:block`.
4. Nenhuma afirmação do Produto 4 cita âncora não validada por humano.
5. `git status -s` limpo antes do push, sem `contacts.json`, `index.html`,
   `saida_anonimizacao/` nem `anexos/*.csv`.

---

## 9. Pendências herdadas

1. **Termos de consentimento.** A coordenação confirmou que há termo assinado para as
   17 sessões, e a marca no codebook reflete isso. Mas a pasta
   `DRIVE_FILES\Termos Entrevistas\Assinados\` tem **18 PDFs**, e não estão entre
   eles os participantes de `ENT-009`, `ENT-012`, `ENT-014` e `ENT-016` — exatamente
   as quatro que o codebook marcava `tcle: false` antes. O `anonimizar_transcricoes.py`
   as exclui por padrão (`--incluir-sem-tcle` liga). Com transcrição em página
   pública, vale localizar os arquivos e registrar a procedência.
2. **Sobreposição conselho × corpus.** Oito pessoas estão nas duas bases. Sete
   responderam ao questionário, não à entrevista. A oitava é o participante de
   `ENT-012`, que aparece no conselho pela Câmara Municipal — e o conselho lista três
   pessoas da Câmara. Publicar a composição não cria informação nova (é ato público),
   mas põe o cruzamento a um clique. Risco já assumido e registrado; decisão de Lucas.
3. **Sessões complementares** — fazenda/planejamento, planejamento urbano e
   procuradoria cobririam a maior parte do vazio do eixo 2. Decisão pendente com o
   coordenador desde 06/09.
4. **Matriz 2 (evidência documental)** — as dimensões sem fonte oral se sustentam em
   PPA, LDO, LOA, QDD e relatórios de execução. A legislação municipal consolidada já
   está no acervo.
5. **Crosswalk incompleto** — 13 das 37 perguntas não têm marcação D/I, e `PRI1`,
   `ACA1` e `SOC1` replicam o padrão de `PUB1` embora perguntem outra coisa. Três
   dimensões não recebem evidência de nenhuma pergunta: `1.1.4`, `2.3.3`, `3.1.3`.
   É entregável do Produto 2 e vai aparecer na revisão.
6. **Produtos 5 e 6** — oficinas de validação (22–24/09) e Roadmap. O contrato do
   município com ICT externa (estratégia climática, monitoramento e captação) se
   sobrepõe ao escopo: mapear os produtos dos dois antes do Roadmap.
7. **Branch `claude/temp-mock-password-ii2y9b`** no remoto, nunca inspecionada.
8. **`nipe-pq-13`** guarda uma camada pública de 09/09 que nunca foi enviada e hoje
   diverge do `tools/publico.py` que está no remoto. Reclonar resolve — e é
   obrigatório de qualquer forma, por causa da reescrita do histórico.

---

## 10. Armadilhas que já custaram tempo

- **`git reset --mixed origin/main` não traz os arquivos para o disco.** O índice vai
  para o remoto, o disco fica como estava, e o git passa a achar que você apagou tudo
  que veio no `fetch`. Um `git commit -a` distraído apaga o pipeline inteiro do
  repositório. Depois do reset: `git restore $(git diff --name-only --diff-filter=D)`.
- **`.gitignore` não desversiona nada que o git já rastreia.** Precisa de
  `git rm --cached`.
- **`git-filter-repo` não entra no PATH como subcomando** numa instalação de usuário
  no Windows: use `python -m git_filter_repo`.
- **Force-push não apaga nada do GitHub.** Objetos órfãos continuam alcançáveis por
  SHA, e `refs/pull/N/head` preserva a árvore antiga permanentemente. Para limpar de
  verdade, apague e recrie o repositório.
- **No Git Bash, `git show origin/main:.gitignore` é mastigado** pela conversão de
  caminhos do MSYS. Use `origin/main:./.gitignore`.
- **`git show` cai no pager** e engole a saída quando encadeado. Redirecione para
  arquivo.
- **Anonimização por token isolado gera ruído**: «Civil» (Defesa Civil), «Paulo»
  (São Paulo), «Defesa», «Dias». Case por nome completo e mantenha uma lista de
  ambíguos; depois confira os resíduos com contexto, à mão.
- **A diarização automática não separa participantes** em sessão conjunta: em
  `ENT-001-ENT-002` todos os turnos vão para um nome só. A separação por falante foi
  feita por leitura e não é reproduzível na transcrição integral.
