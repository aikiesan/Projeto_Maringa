# Prompt de continuidade, fechamento do Produto 4 e dos quatro entregáveis

Cole este arquivo inteiro no início de uma sessão nova do Claude Code, a partir de
`A:\Projeto_Maringa`. É autossuficiente: não depende de nada dito em conversas
anteriores.

Escrito em 14/09/2026, ao fim da sessão que publicou o Hub com o Produto 4.

---

## 1. Quem você é nesta tarefa

Você apoia a consultoria técnica **IPPLAM–CEPAL/ONU** sobre **condições
habilitantes ao financiamento climático urbano de Maringá (PR)**, executada pela
Brisa Soluções Ambientais. O interlocutor é Lucas Nakamura Cerejo, arquiteto e
urbanista, pós-doutorando no NIPE/CP2b da Unicamp, responsável pela
sistematização analítica. A coordenação é do Dr. Cid.

A metodologia é *Assessing Subnational Enabling Framework Conditions for Urban
Climate Finance* (CCFLA / Urban-Act, 2024), adaptada e priorizada para Maringá no
Produto 2.

## 2. Como trabalhar

- Português. Direto: aponte o que está errado nos dados em vez de contornar.
- **Verifique antes de afirmar.** Rode o código, confira as contagens, abra a
  página. Número que não bate com o CSV é erro grave.
- Inconsistência no acervo é **achado**, não conserto silencioso.
- **`git fetch` e leia `origin/main` antes de escrever ferramenta nova.**
- **Sem travessão (—) em texto que o leitor vê.** Pedido de 13/09: a escrita não
  deve ter cara de gerada por IA. Vírgula, dois-pontos, parênteses ou ponto.
- **Não invente cobertura e não digite número.** Se um número aparece numa
  página, ele saiu de uma ferramenta que leu um CSV versionado.
- Ao terminar, diga em uma linha o que mudou **no diagnóstico**, não só o que foi
  processado.

---

## 3. O que já está pronto e publicado

Hub público no ar: <https://aikiesan.github.io/Maringa/>

| Página | Conteúdo |
|---|---|
| `index.html` | abertura, quatro números, seis figuras descritivas com tabela de números |
| `projeto.html` | o que é a consultoria, metodologia, unidade de registro, regras, risco residual |
| `produto4.html` | o Produto 04 em versão web, 93 afirmações, 40 com âncora, matriz de 13 subcategorias, download do Word |
| `painel.html` | as 494 evidências, filtráveis; recebe deep-link da Seção 3 |
| `instituicoes.html` | 34 organizações por dimensão CCFLA |
| `transcricoes.html` | índice das 17 sessões → `transcricoes/ENT-XXX.html` |

Saíram do Hub: `dados.html` (e os 7 arquivos que ela oferecia), `conselhos.html`
e `legislacao.html`. As duas últimas eram de produto anterior e não são citadas
no relatório; a de conselhos publicava 124 nomes nominalmente.

Regenerar e publicar:

```bash
cd /a/Projeto_Maringa
python -m tools.hub.build
python -m tools.hub.varre_hub              # tem que sair 0
python -m tools.varre_local_trabalho --so-participante   # tem que sair 0
python tests/test_redacao.py               # 34 testes
cp -r hub_saida/* /a/Maringa/ && cd /a/Maringa && git add -A && git commit && git push
```

### Números conferidos em 14/09

**17 sessões em 20 códigos · 785 min (13h05) · 7.778 turnos · 20 participantes ·
494 evidências · 51/55 dimensões com evidência · 47 trianguladas · 13
subcategorias.**

Maturidade: inexistente 206 · em elaboração 77 · formalizado 14 · regulamentado
13 · em implementação 159 · monitorado 1 · efetivo 17 · **sem evidência 6 ·
não aplicável 1**. Os dois últimos ficam FORA da escala de estágios e por isso a
escala soma 487, não 494: `sem_evidencia` é pendência de reinquirição, não
ausência constatada, e somá-la a `inexistente` transformaria pendência em achado.

Setores: Público 7 sessões e 226 evidências · Sociedade Civil 4 e 115 · Privado 3
e 77 · Academia 3 e 76.

---

## 4. Os quatro entregáveis pedidos

### 4.1 Produto 4 completo em `.docx` editável, sem travessões

Hoje existe `tools/p4_docx_publico.py`, que gera
`hub_saida/Produto_04_publico.docx` a partir de `anexos/Produto_4.docx`
aplicando as supressões e trocando os quadros nominais pela contagem.

**O que falta:** o texto do relatório tem **39 travessões**, que vêm do próprio
`.docx` e não da apresentação. Retirá-los é editar o texto do Lucas, e ele
autorizou em 14/09 apenas de forma condicional. Confirme antes.

Ferramenta a escrever: uma passagem que reescreve travessão por pontuação
adequada **preservando os runs** (o negrito do rótulo que abre cada afirmação da
Seção 3), no mesmo estilo de `_aplicar_supressao` em `p4_docx_publico.py`.

### 4.2 As 17 entrevistas em `.docx` editável, anonimizadas, com as correções

Hoje as transcrições publicadas vêm de
`anexos/Anexo_05_Transcricoes_Anonimizadas.zip`, um zip **já gerado**, e o Hub
aplica as supressões na hora de montar a página (`tools/hub/transcricoes.py`
chama `supressoes.aplicar_tolerante`).

**O que falta:** gerar os 17 `.docx` com as correções **dentro do arquivo**, não
só na página. Duas rotas:

1. rodar `tools/anonimizar_transcricoes.py --commit` contra o acervo, que já
   aplica `codebook/supressoes.csv` no ponto certo do pipeline. Exige `vault/`
   (hoje ausente) e o acervo em `DRIVE_FILES`;
2. reescrever o zip: ler cada `.docx`, aplicar `aplicar_tolerante` sobre
   `doc.paragraphs` e salvar. Mais simples e suficiente para o entregável,
   porque a substituição de nomes já está feita no zip.

**Antes disso, resolva o item 5.1.** Não faz sentido gerar 17 arquivos antes de
decidir o que fazer com a autoidentificação do local de trabalho.

### 4.3 Codificação de resultados em relatório `.docx` editável

Não existe ainda. O material está todo em `codebook/` e as contagens em
`tools/p4_base.py` (`base()` devolve `consultas`, `cobertura`, `subcategorias`,
`setores`) e `tools/hub/dados.py` (`metricas_corpus()`).

Sugestão de conteúdo, tudo derivado: base da avaliação; cobertura por prioridade;
a matriz das 13 subcategorias com maturidade por moda e o perfil da
distribuição; distribuição por tipo, alinhamento, confiança e eixo; as dimensões
sem evidência oral; as 50 divergências preservadas. `produtos/P4_matriz_v2.md` já
é isso em markdown e pode ser a fonte da estrutura.

**Cuidado:** este relatório descreve o corpus, então não pode trazer rótulo
institucional de sessão nem nada que ligue pessoa a sessão. Rode a varredura
sobre ele antes de entregar (o `varre_hub` já lê `.docx`).

### 4.4 Hub atualizado com o projeto finalizado

Depende dos três acima: o Word público vira download, e o relatório de
codificação também. Rode a sequência da seção 3.

---

## 5. Decisões abertas, em ordem de gravidade

### 5.1 ⚠ Autoidentificação do local de trabalho nas transcrições

**Esta é a decisão que bloqueia o entregável 4.2, e é a mais séria em aberto.**

Em 13/09 o tipo institucional saiu da camada pública, porque 13 dos 15 rótulos eram únicos de uma só sessão e, ao lado da lista nominal de entrevistados, que é
entregável do termo de referência, funcionavam como crachá.

Isso era necessário e **não é suficiente.** Em 14/09, `tools/varre_local_trabalho.py`
encontrou 12 passagens em que o participante diz onde trabalha. Dez foram
tratadas (declaradas em `codebook/supressoes.csv`) e duas foram dispensadas por
leitura, mas a medição seguinte mostrou o problema real:

**11 das 17 sessões mencionam a própria instituição, em 47 passagens com marca de
primeira pessoa a menos de 60 caracteres.**

| Sessão | Menções | Com 1ª pessoa | Tipo no codebook |
|---|---:|---:|---|
| ENT-013 | 26 | **17** | Órgão municipal de proteção e defesa civil |
| ENT-008 | 22 | **11** | Direção de órgão ambiental municipal |
| ENT-005 | 13 | 5 | Entidade profissional de arquitetura e urbanismo |
| ENT-003 | 16 | 3 | Órgão ambiental municipal |
| ENT-017-018 | 6 | 3 | Banco público de desenvolvimento regional |
| ENT-020 | 9 | 3 | Universidade pública |
| outras 5 | ≤2 | ≤2 | |

Duas frases que as dez supressões **não** cobriram, ambas no ENT-013:

- «eu entrei na Defesa Civil em 2024, abril»
- «A gente trabalha aqui dentro da Secretaria de Infraestrutura»

Instituição, setor e data de entrada. Supressão pontual não resolve: seriam 47
cortes, e o conteúdo não sobrevive a isso. ENT-008 é agravante porque é uma das
três sessões que «o nome não protege» (regra 5.6).

**A conclusão honesta é que publicar transcrição integral e proteger o local de
trabalho do participante são objetivos incompatíveis nessas sessões.** As saídas
possíveis:

1. **Tirar as transcrições do Hub** e mantê-las como anexo de entrega. O resto do
   Hub não tem esse problema. Reversível em um comando.
2. **Revisão linha a linha das 6 sessões críticas**, com supressão ampla. Custa
   leitura e mutila o conteúdo.
3. **Manter e declarar.** A página já declara risco residual; passaria a declarar
   que a autoidentificação foi identificada e mantida por decisão do projeto.
   Registre quem decidiu e quando.

Lucas escolheu em 14/09 «manter no ar e corrigir agora», com tratamento por
substituição do marcador de primeira pessoa. Isso foi feito para as 12 passagens
que a ferramenta achou. A medição das 47 veio **depois** dessa decisão, e não foi
reapresentada. **Reapresente antes de gerar os 17 arquivos.**

### 5.2 ⚠ Exposição no histórico do repositório privado

`main` local e `origin/main` de `aikiesan/Projeto_Maringa` **não têm ancestral
comum**: 23 commits contra 26. O `git-filter-repo` de 12/09 rodou só no clone
local. Continuam recuperáveis por SHA no GitHub:

| Arquivo | Blob | Alcançável em |
|---|---|---|
| `data/contacts.json` (24 pontos focais, os 24 com nome, e-mail e telefone) | `2239c25` | `bcf37ae` |
| `index.html` (painel, 605 KB) | `d58476f` | `ccd8b2b` |
| `public/index.html` (808 KB) | `b8661be` | `ccd8b2b` |
| `Lista de Entrevistas.xlsx` | `0327ef4` | `4bfa888` |
| `P3_Base_Mapeamento_Atores_Maringa.xlsx` | `94efd96` | `4bfa888` |

`refs/pull/1/head` fixa `dbd8a44`, então **force-push não resolve**. Apagar e
recriar o repositório é a única via que remove de fato. Decisão do Lucas.

### 5.3 As 53 afirmações sem âncora

`P4_afirmacoes_sem_ancora.md` e `revisao_pendentes.html` listam as 53, ordenadas
por onde a leitura rende mais: 3 empates, 13 que passaram perto do corte, 14 na
zona cinzenta, 21 de peso baixo, 2 chamadas de lista. Nada foi revisado por
humano ainda: `decisor` está `automatico` nas 279 linhas.

### 5.4 `anexos/cortes.csv` tem 7 registros, não 10

O prompt anterior afirmava 10 em dois pontos. Se três cortes se perderam, é agora
que dá para recuperar.

### 5.5 Herdadas, sem mudança

Termos de consentimento (18 PDFs em `Assinados/`, sem ENT-009, ENT-012, ENT-014 e
ENT-016) · sessões complementares de fazenda, planejamento e procuradoria ·
Matriz 2 documental · crosswalk incompleto (13 das 37 perguntas sem marcação D/I)
· Produtos 5 e 6, oficinas de 22–24/09 · branch `claude/temp-mock-password-ii2y9b`
nunca inspecionada.

---

## 6. Arquitetura: o que cada ferramenta faz

```
codebook/                    fonte de verdade, versionada
  dimensions.csv questions.csv question_dimension.csv interviews.csv
  triage_matrix.csv evidencias/ENT-XXX.csv (494 evidências)
  anonimizacao_lexico.csv anonimizacao_permitidos.csv dashboard.json
  supressoes.csv             19 supressões declaradas (ver 7.1)
data/                        comdema.json organizations.json legislacao.json
assets/marca/                brisa cepal onda projeto projeto-branco (PNG)
tools/
  redacao.py                 motor de anonimização: substituição + varredura
  supressoes.py              supressão e substituição de trecho declarada
  anonimizar_transcricoes.py passo 8; escreve FORA do git
  lista_pessoas.py           carga da lista de participantes, falha dura
  scan_pii.py                varredura da camada aberta do painel
  publico.py                 saneia site/artifact.html → site/publico.html
  build_site.py              gera o painel; deep-link por filtro no hash
  p4_base.py                 contagens do Produto 4, maturidade por moda
  p4_ancorar.py              âncoras candidatas (regex sobre word/document.xml)
  p4_selecao.py              seleção automática das âncoras, critério declarado
  p4_revisao.py              CSV de revisão + página local
  p4_pendentes.py            as 53 sem âncora, por prioridade de leitura
  p4_docx_publico.py         versão pública e editável do relatório
  varre_local_trabalho.py    auditoria de autoidentificação de empregador
  hub/
    base.py                  tokens de cor, CSS, helpers de gráfico, pagina()
    cabecalho.py             O cabeçalho, uma implementação para todas as páginas
    dados.py                 carga dos CSVs e métricas
    graficos.py              figuras descritivas com tabela de números
    paginas.py               corpo de index e instituicoes
    pagina_projeto.py        corpo de projeto.html
    produto4.py              conversão do .docx e a página do produto
    transcricoes.py          páginas por sessão, com âncora por marca de tempo
    build.py                 orquestra tudo; várias travas (ver 7)
    varre_hub.py             portão de publicação; lê .html .csv .json .css .docx
produtos/  LEIA-ME.md  P4_matriz_v2.md  P4_ancoras_secao3.csv
           P4_ancoras_revisao.csv
anexos/    Produto_4.docx (367 parágrafos)  Anexo_05_*.zip  cortes.csv
           revisao_nomes.csv  revisao_local_trabalho.csv
tests/test_redacao.py        34 testes, dados sintéticos
hub_saida/                   saída gerada, fora do git
```

### O deep-link da Seção 3

`(sessão, dimensão, marca de tempo) NÃO é chave`: 32 triplas do corpus têm mais
de uma evidência, uma tem três. Por isso o link **filtra** o painel
(`painel.html#evidencias?int=…&dim=…&ts=…`) em vez de apontar um fragmento:
mostra todas as evidências do ponto e não depende da paginação de 25.

### A seleção das âncoras

40 das 93 afirmações têm âncora; 53 não. O critério está em `p4_selecao.py`:
confiança alta como porta de entrada, a afirmação tem de afirmar algo (texto
terminado em `:` é chamada de lista), peso IDF mínimo de 18 sobre os termos
compartilhados, ao menos um termo distintivo, e margem sobre a segunda candidata.
Empate não decide.

Confiança **não discrimina** sozinha: 251 das 279 candidatas são altas e todas as
93 afirmações têm ao menos uma. O corte 18 foi calibrado por leitura: em 12, três
das seis aceitas mais fracas não sustentavam a afirmação.

A coluna `decisor` separa `humano` de `automatico`, e a página rotula «âncora por
critério automático», não «validada». A seleção automática nunca sobrescreve
decisão humana.

---

## 7. As travas: o que reprova e por quê

Cada uma existe porque o defeito correspondente aconteceu.

1. **`varre_hub`** reprova nome de participante, contato, CPF, CNPJ, rótulo de
   risco, setor «Especial», nome de conselheiro (em qualquer página, sem
   exceção, desde que `conselhos.html` saiu) e **rótulo único de tipo
   institucional**. Lê `.html .csv .json .css .docx`. **Não lê imagem**, e por
   isso as capturas de tela estão no `.gitignore`.
2. **`lista_pessoas.carregar_todas`** falha duro se a lista de participantes não
   carregar. Antes o código lia `wb["PESSOAS"]` e, se a aba não existisse,
   avisava e seguia com a lista **vazia**, saindo 0 sem ter procurado nada.
   Existem duas cópias da planilha, com abas de nome diferente e 51 e 25 nomes.
3. **`build._conferir_css`** reprova variável de CSS usada sem definição e
   **seletor órfão**. Remover regra por regex deixou `nav` solto, que colou no
   seletor seguinte e transformou `.hero-faixa` em `nav .hero-faixa`: a regra
   continuava no arquivo, sumia da página, e o sintoma foi título branco sobre
   fundo transparente.
4. **`build._conferir_ancoras`** confere cada link gerado contra o codebook: a
   evidência existe, foi codificada com confiança alta, e está marcada como
   aceita.
5. **`produto4.guarda` e `p4_ancorar.conferir_docx`** abortam se o `.docx` não
   for o completo. Existe uma cópia de **328 parágrafos** que termina em
   «3.4.5. Soluções Propostas», sem o capítulo 4, as Considerações Finais e os
   Anexos, e ela é **mais nova no disco**: «pegar o mais recente» leva ao errado. A fonte é `anexos/Produto_4.docx`, 367 parágrafos em python-docx (714
   na contagem por XML, que apanha os `<w:p>` das tabelas).
6. **`supressoes`** levanta `SupressaoNaoAplicada` quando a âncora não casa.
   `aplicar_tolerante`, usada pela camada publicada, aceita o já aplicado (o
   Anexo 05 traz os sete cortes antigos como `(…)`) e reprova o resto.
7. **`varre_local_trabalho`** sai 1 se achar autoidentificação sem tratamento
   nem dispensa declarada.
8. **`publico.troca`** sai com erro se um padrão não bater o mínimo esperado. A
   **ordem** das regras ali é correção, não estilo: a remoção do tipo
   institucional tem de vir **depois** das que generalizam o rótulo, senão elas
   não encontram o que generalizar.

### 7.1 `codebook/supressoes.csv`

19 declarações: 2 do Produto 4, 17 de transcrição. Colunas
`fonte,alvo,paragrafo,prefixo,sufixo,sha256,n_chars,substituto,motivo`.

**Nunca guarda o texto protegido.** Guarda o contexto (prefixo e sufixo curtos),
o `sha256` e o comprimento. Se guardasse o trecho, o codebook versionado viraria
o lugar onde o material identificador vive, que é o que `anexos/cortes.csv` é e
por isso está fora do git.

`substituto` é **literal**: a marca `(…)` escrita na coluna corta marcando; texto
substitui; vazio remove sem pôr nada. A coluna ser literal é deliberado, porque
antes não havia como expressar «remove o marcador e não põe nada», que é o
tratamento certo quando o que identifica é o marcador de primeira pessoa e não o
conteúdo.

---

## 8. Regras que governam tudo

1. **A unidade de registro é a evidência**, não a entrevista. Trecho anonimizado,
   com marca de tempo, vinculado a **uma** dimensão, com tipo, maturidade,
   alinhamento e confiança. A paráfrase é o juízo do codificador e é o que se cita; o trecho fica como lastro.
2. **Ausência de evidência é resultado.** Dimensão «Muito alta» que atravessa o
   corpus sem evidência é achado, não falha de coleta.
3. **Divergência não se resolve.** As 50 divergentes são preservadas, nunca
   resolvidas por predominância de fonte.
4. **Tudo é derivado, nada é digitado.** Corrigir um número significa corrigir o
   codebook ou a ferramenta, nunca a saída.
5. **Anonimização.** Entram: código da sessão, marca de tempo, setor, órgãos de
   fato público (SEMOP, IPPLAM, Defesa Civil), leis, contratos publicados.
   Nunca entram: nome de participante ou entrevistador, cargo específico,
   instituição nominal do próprio entrevistado, contato, **tipo institucional da
   sessão** (saiu em 13/09). Risco residual assumido e declarado: Maringá tem um
   único órgão ambiental municipal.
6. **Três sessões o nome não protege**: `ENT-008` (órgão ambiental), `ENT-012`
   (Legislativo) e `ENT-015` (Executivo) são reidentificáveis pelo cargo.
7. **Guarda-corpos.** O acervo nunca entra no git. Saída de anonimização não
   entra. `anexos/cortes.csv`, `revisao_nomes.csv` e `revisao_local_trabalho.csv`
   não vão a lugar nenhum. Nada é publicado sem passar nas varreduras.

### A identidade visual

Marca do projeto: **azul petróleo `#0F4C5C`**, **verde médio `#4E9F3D`**, cinza
grafite `#4A4A4A`, cinza claro `#E9ECEF`. Logotipo em `assets/marca/projeto.png`
e `projeto-branco.png`; o manual completo está fora do git.

**A paleta das séries dos gráficos é outra coisa e não se mexe sem validar.**
`#1baf7a · #eb6834 · #2a78d6 · #eda100` no claro, e `#199e70 · #d95926 · #3987e5 · #c98500` no escuro. Cor de marca e cor de dado são coisas diferentes. Dois ajustes
de contraste foram medidos, não estimados: `--mut` rendia 3,90 sobre branco e foi
escurecido até 4,56; o verde da marca sobre o petróleo rende 2,88, e o selo passou
a usar `--menta-clara #7bc66c`, em 4,59.

---

## 9. Armadilhas que já custaram tempo

- **`git reset --mixed origin/main` não traz os arquivos para o disco.** Depois
  do reset: `git restore $(git diff --name-only --diff-filter=D)`.
- **`.gitignore` não desversiona nada que o git já rastreia.** Precisa de
  `git rm --cached`.
- **`git-filter-repo` não entra no PATH** numa instalação de usuário no Windows:
  use `python -m git_filter_repo`.
- **Force-push não apaga nada do GitHub.** `refs/pull/N/head` preserva a árvore
  antiga permanentemente.
- **No Git Bash, `git show origin/main:.gitignore` é mastigado** pela conversão
  de caminhos do MSYS. Use `origin/main:./.gitignore`.
- **Anonimização por token isolado gera ruído**: «Civil» (Defesa Civil), «Paulo»
  (São Paulo), «Pedro» (bairro São Pedro), «Colombo» e «Severino» (logradouros),
  «Moreira» (Auditório Hélio Moreira). Há uma lista `AMBIGUOS` em `varre_hub`.
- **`hub_saida/transcricoes/` é capturado pela regra `transcricoes/`** do
  `.gitignore`. Um `git add -A` publicaria o Hub sem as transcrições.
- **Heredoc do Bash mastiga `\n` e contrabarras** dentro de script Python. Para
  escrever código com escapes, use a ferramenta Write ou `chr(10)`.
- **f-string não aceita contrabarra na expressão.** Pré-compute fora.
- **Substituir texto em arquivo sem `assert`** falha em silêncio. Aconteceu nesta
  sessão: uma trava inteira não foi instalada porque o padrão de busca tinha um
  `f"` que o arquivo não tinha, e eu só descobri no teste negativo.
- **Teste negativo é obrigatório.** Duas travas passaram a existir só porque o
  teste negativo mostrou que a primeira versão não pegava nada: a de rótulo de
  sessão vigiava o valor cru do codebook e deixava passar o rótulo
  **generalizado**, que era o efetivamente publicado.
- **`_casar` exigia prefixo e sufixo não vazios**, e um trecho no fim do
  parágrafo não tem sufixo. A supressão declarada era recusada pela geração.
- **O painel não é página como as outras.** É corpo de Artifact, com folha de
  estilo própria que define `.top` e `.wrap`, e não carrega o `hub.css`. Por isso
  o cabeçalho tem classes `hubbar*` e é injetado com os tokens de cor.
- **A diarização automática não separa participantes** em sessão conjunta: em
  `ENT-001-ENT-002` todos os turnos vão para um nome só.

---

## 10. Critérios de aceitação

1. `python -m tools.hub.varre_hub` sai **0** e o log mostra a lista de nomes
   carregada com número maior que zero. Sem isso o 0 não vale nada.
2. `python -m tools.varre_local_trabalho --so-participante` sai **0**.
3. `python tests/test_redacao.py` verde, 34 testes.
4. Todo número exibido bate com o CSV. Confira pelo menos: 494 evidências,
   51/55 dimensões, 47 trianguladas, 206 inexistentes, 34 organizações,
   13 subcategorias, 40 âncoras.
5. As páginas abrem em 1180 px e em 390 px, nos modos claro e escuro. **Olhe as
   capturas**: o validador confere cor, não layout.
6. Nenhuma afirmação cita âncora que não esteja marcada `aceita` no CSV de
   revisão, e todo link resolve para evidência existente de confiança alta.
7. `git status -s` limpo antes do push, sem `contacts.json`, `index.html`,
   `saida_anonimizacao/` nem `anexos/*.csv`.
8. Nenhum `.docx` publicado contém nome de participante. A varredura lê `.docx`,
   mas rode também `python -m tools.varre_local_trabalho` sobre o material novo.
