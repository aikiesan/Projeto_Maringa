# Metodologia de codificação das entrevistas

**Projeto CEPAL/IPPLAM — Maringá (PR).** Avaliação das condições habilitantes ao
financiamento climático urbano. Metodologia *Assessing Subnational Enabling Framework
Conditions for Urban Climate Finance* (CCFLA / Urban-Act, 2024), priorizada para Maringá
no Produto 2.

> Documento reconstruído em 06/09/2026 a partir do protocolo publicado e do
> `dashboard.json` recuperado (versão de 01/09/2026), atualizado no mesmo dia
> contra o acervo completo (17 sessões) e **revisado ao fim da codificação
> integral** — as 17 sessões estão codificadas, com 494 evidências. Substitui o
> artefato como registro versionável do método.

---

## 1. O que esta etapa precisa produzir

O Produto 2 fixou a exigência que governa tudo o que vem depois: a avaliação não pode se
limitar a constatar que uma política existe. Precisa distinguir **existência formal** de
**regulamentação**, de **implementação**, de **financiamento**, de **monitoramento** e de
**efetividade** — e, ao final, permitir o caminho inverso: partir de uma conclusão do
diagnóstico e chegar à evidência que a sustenta.

Isso define a unidade de registro.

### Unidade de registro: evidência × dimensão

Não é a entrevista, nem a resposta a uma pergunta. É a **evidência**: um trecho
anonimizado, com marca de tempo, vinculado a **uma** dimensão CCFLA, classificado quanto à
maturidade que revela e ao grau de confiança que merece. Uma entrevista de cinquenta
minutos produz dezenas dessas unidades, espalhadas pelos quatro eixos. Um mesmo trecho
pode gerar duas evidências em dimensões diferentes.

**A ausência de evidência é resultado, não falha.** Quando uma dimensão de prioridade
«Muito alta» atravessa o corpus inteiro sem produzir uma única evidência, isso é um
achado do diagnóstico.

### Cadeia da evidência

| Etapa | Produto |
|---|---|
| Fonte | Transcrição + resumo, com marca de tempo, sob TCLE assinado |
| Recorte | Trecho anonimizado, `00:00:00` preservado |
| Vínculo | Uma das 55 dimensões + a pergunta do instrumental que a suscitou |
| Juízo | Maturidade + tipo + alinhamento + confiança |
| Consolidação | Cobertura por eixo; convergências, divergências e lacunas prioritárias |

---

## 2. Estrutura do codebook

- **4 eixos**: Política Climática · Orçamento e Finanças · Dados Climáticos ·
  Coordenação Vertical e Horizontal
- **13 subcategorias**
- **55 dimensões**, cada uma com prioridade atribuída a Maringá no Produto 2
  (`Muito alta` = rank 4 … `Baixa` = 1) e um léxico próprio — **328 palavras-chave** no total
- **37 perguntas** do instrumental, em quatro blocos: `PUB`, `PRI`, `ACA`, `SOC`
- **112 vínculos** pergunta × dimensão (`D` direta, `I` indireta)

O eixo 2 concentra **25 das 55 dimensões** — é onde a metodologia atribuiu mais
prioridade «Muito alta».

### Duas falhas conhecidas no crosswalk

1. **13 das 37 perguntas** não têm nenhuma marcação D/I — praticamente todo o bloco de
   sociedade civil e boa parte de academia e setor privado.
2. As linhas `PRI1`, `ACA1` e `SOC1` repetem, marca por marca, o padrão de `PUB1`, embora
   perguntem outra coisa: as três tratam de riscos e impactos percebidos e apontam para
   estratégia de mitigação, não para avaliação de risco.

**Consequência:** três dimensões não recebem evidência de nenhuma pergunta — `1.1.4`
Estratégia de adaptação com metas claras (Muito alta, e objeto estratégico da iniciativa),
`2.3.3` Diversificação de receitas ambientais (Alta) e `3.1.3` Inventário municipal de GEE
(Muito alta).

**Decisão de projeto:** por isso o modelo vincula a evidência **diretamente à dimensão**.
O crosswalk fica como controle de qualidade do instrumental, não como caminho obrigatório
da codificação.

---

## 3. Anonimização

A camada de análise identifica a entrevista por **código, setor e tipo genérico de
instituição**. Nome, e-mail, telefone, cargo e instituição nominal ficam em
`participants_vault` — tabela que **nenhum endpoint expõe**. Isso atende o Anexo 02 sem
esvaziar a matriz, que precisa cruzar dimensão × tipo de ator.

| Entra na camada de análise | Nunca entra |
|---|---|
| Código da entrevista e marca de tempo | Nome do participante ou do entrevistador |
| Setor: público, privado, academia, sociedade civil | Cargo específico |
| Tipo genérico: «órgão ambiental municipal» | Instituição nominal do próprio participante |
| Organizações terceiras de fato público: contratos publicados, concessionárias, órgãos estaduais | Contato, endereço, qualquer identificador direto |
| Instrumentos e leis municipais citados | Terceiros mencionados de passagem |

### Risco residual assumido

Maringá tem *um* órgão ambiental municipal. Dizer «órgão ambiental municipal» já
identifica a instituição, e o cargo dentro dela reduz o conjunto a poucas pessoas. A
anonimização protege contra a leitura casual, não contra quem conhece a estrutura da
prefeitura. A alternativa — descer a «setor público» apenas — destruiria a capacidade de
cruzar dimensão × órgão, que é o eixo da Matriz 1.

**Caminho adotado:** manter o tipo genérico na base e, no relatório final, agregar por eixo
e por setor, atribuindo achados a órgão nominal só quando a informação for de fato pública
(um contrato publicado, uma lei, uma competência legal).

---

## 4. Escalas de registro

### Maturidade (9 valores)

| Valor | Significa |
|---|---|
| `sem_evidencia` | A entrevista não produziu informação sobre a condição |
| `nao_aplicavel` | A dimensão não se aplica àquele ator |
| `inexistente` | Há evidência positiva de que a condição não existe |
| `em_elaboracao` | Está sendo construída, sem resultado ainda |
| `formalizado` | Existe em norma, sem regulamentação |
| `regulamentado` | Regulamentado, ainda não plenamente operante |
| `em_implementacao` | Opera, com limitações declaradas |
| `monitorado` | Opera com acompanhamento sistemático |
| `efetivo` | Opera, é monitorada e produz resultado verificável |

A distinção entre `sem_evidencia` e `inexistente` é a que mais protege o diagnóstico: a
primeira é pendência de reinquirição, a segunda é achado.

### Tipo de evidência

`declaracao` (fato afirmado) · `percepcao` (avaliação do participante) · `lacuna` (ausência
declarada ou constatada) · `divergencia` (conflito com outra fonte) · `oportunidade`
(caminho apontado) · `documento_indicado` (pista para a Matriz 2).

### Alinhamento e confiança

`convergente` · `complementar` · `divergente` · `isolada` — e `alta` · `media` · `baixa`.

---

## 5. Os sete passos, na ordem

A ordem importa: anonimizar antes de codificar impede que um nome entre na base por
descuido; triar antes de ler dá ao pesquisador um roteiro em vez de cinquenta minutos de
leitura sem âncora.

1. **Conferir o registro contra o Anexo 03** — código, data, modalidade, duração, TCLE,
   áudio, vídeo, transcrição. Nada avança sem termo rastreável.
   `python -m tools.ingest_registros` (confere) / `--commit` (grava).
   O comando cruza os falantes da transcrição com a Lista de Entrevistas e separa em dois
   destinos: camada anonimizada em `interviews`, identificação em `participants_vault`.

2. **Triar por palavras-chave** — `python -m tools.triage ENT-XXX --md`.
   Varre a transcrição, agrupa turnos candidatos por dimensão, devolve marca de tempo,
   falante e a palavra que disparou o vínculo. **A triagem não codifica nada** — produz o
   roteiro de leitura e a trilha de auditoria. Falsos positivos são esperados.

3. **Ler a entrevista inteira** — a triagem cobre o vocabulário previsto; o que interessa
   quase sempre está no que não foi previsto. A evidência mais forte do piloto não é
   achável por palavra-chave: mora na articulação entre duas frases distantes.

4. **Recortar e anonimizar o trecho** — literal no essencial, marca de tempo preservada,
   nomes viram rótulo. Só então entra em `excerpt_anon`.

5. **Vincular, classificar e escrever a paráfrase** — uma dimensão por evidência. A
   paráfrase é o juízo analítico do codificador e é o que será citado no relatório; o
   trecho fica como lastro.

6. **Registrar no banco a partir do CSV** — `python -m tools.load_evidence ENT-XXX`.
   A codificação vive em `codebook/evidencias/ENT-XXX.csv`, versionada em git; o banco é
   derivado dela. Recarregar é idempotente.

7. **Triangular e consolidar** — cada evidência pode receber o documento que a confirma,
   qualifica ou contradiz (ponte com a Matriz 2). A consolidação sai das visões do banco,
   **com as divergências preservadas em vez de resolvidas por predominância de fonte**.
   `GET /api/analysis/coverage` · `GET /api/evidence?dimension=1.2.2`

---

## 6. Estado do acervo e ressalvas

**17 sessões distintas ocupando 20 códigos ENT · 13h05 de registro · 7.778 turnos.**
Levantamento automático por `tools/ingest_registros.py`, que cruza os falantes de cada
transcrição com a Lista de Entrevistas, confere a pasta de termos assinados e detecta
duplicata por md5 do texto — não por nome de pasta.

Distribuição: público 4 sessões, sociedade civil 4, academia 3, especial 3, privado 3.

| Situação | Constatação | Tratamento |
|---|---|---|
| **Sem TCLE** | `ENT-009`, `ENT-012`, `ENT-014` e `ENT-016` não têm termo assinado localizado | Aparecem na matriz; não devem alimentar o diagnóstico até o termo ser localizado. `tcle` nunca por inferência |
| **Fora da Lista** | Em `ENT-009` e `ENT-017-ENT-018` há falante que não consta da Lista de Entrevistas | Casamento manual; tipo de instituição atribuído por conferência |
| **Sessões conjuntas** | `ENT-001-ENT-002`, `ENT-010-ENT-011` e `ENT-017-ENT-018` têm dois participantes | Contadas como uma sessão; codificar por falante na leitura |
| **Diarização** | A transcrição automática de `ENT-001-ENT-002` atribui todos os turnos a um único nome | Separação feita por leitura, registrada em `notes` |
| **Duplicata — corrigido** | O registro de 01/09 dava `ENT-011` e `ENT-012` como o mesmo arquivo | **Não se confirma** no acervo atual: a pasta ENT-011 traz a sessão conjunta `ENT-010-ENT-011` e `ENT-012` tem registro próprio, com md5 distinto |
| **Reidentificação** | Instituições singulares são identificáveis pelo rótulo genérico | Risco residual assumido (§3) |

---

## 7. Cobertura ao fim da codificação

**51 das 55 dimensões têm evidência codificada.** As quatro restantes são todas de
prioridade «Média»: `1.1.2` alinhamento da mitigação com NDC/plano estadual, `1.1.3` MRV
para mitigação, `2.5.4` acesso a mercado de capitais e `2.5.5` títulos verdes.

As três dimensões «Muito alta» que atravessavam o corpus sem evidência foram fechadas pela
leitura integral — nenhuma delas havia sido alcançada pela pré-triagem por palavra-chave:

| Dimensão | O que a codificação encontrou | Fonte |
|---|---|---|
| **`3.1.3`** inventário municipal de GEE | Existe como etapa contratada do plano de enfrentamento; já entregue ao município e aguardando validação | ENT-008, ENT-010-ENT-011 |
| **`2.3.2`** uso do fundo municipal de meio ambiente | Fonte ativa, alimentada por autuação e por repasse contratual da concessionária de saneamento; é o que custeia hoje o planejamento climático. Alegação não verificada de saldo expressivo não executado | ENT-008, ENT-009 |
| **`2.2.2`** rastreamento de gastos climáticos | Não existe na administração. A capacidade está instalada **fora** dela: observatório social financiado pela associação comercial acompanha todas as contas públicas e já impugnou licitação | ENT-005, ENT-012, ENT-015 |

**A lacuna institucional permanece, e mudou de natureza.** Continua sem registro de entrevista:
Fazenda/Planejamento, planejamento urbano (IPPLAM), obras públicas, urbanismo e habitação,
procuradoria, limpeza urbana, mobilidade, órgão ambiental estadual e COMDEMA. Mas o eixo 2
deixou de ser silencioso: `2.2.1` orçamento verde tem agora evidência direta do Legislativo
(«nenhuma» priorização climática identificável na peça orçamentária) e do Executivo (orçamento
transversal, sem unidade orçamentária), e a resistência à vinculação de receita foi nomeada e
localizada na área fazendária. O que falta não é mais evidência sobre o eixo 2 — é a
contraparte de quem monta o orçamento.

### O achado mais convergente do corpus

Cinco fontes independentes, de quatro setores, apontam a **ausência de projetos estruturados**
— e não a ausência de recurso — como barreira número um: ENT-004 («não temos a ideia pronta»),
ENT-007 («o município tem superávit e não consegue executar»), ENT-008 («sem projeto eu só
tenho uma ideia»), ENT-010-ENT-011 («tem fundos disponíveis, mas não se tem projetos que se
adequam») e ENT-017-ENT-018 («estruturação de projetos é uma fragilidade dos municípios como
um todo»).

**Divergência preservada:** ENT-015 sustenta que o gargalo está resolvido por via não
institucional — a prefeitura não elabora, e recebe projetos doados pelo setor privado, «milhões
nos últimos dois anos». As duas leituras se conciliam, e o resultado é o achado: a capacidade
de preparar projeto existe em Maringá, existe fora da prefeitura, por doação, sem
previsibilidade nem escala garantida.

### A convergência mais forte

Nove das 17 sessões, em quatro setores, apontam a **gestão da arborização** como vulnerabilidade
central: plano existente e não aplicado na etapa de reposição (ENT-006, ENT-007, ENT-009,
ENT-014, ENT-019, ENT-020), ausência de unidade de parques e jardins e viveiro sem porte
(ENT-019, ENT-020), fila de poda que empurra o morador para a poda clandestina (ENT-007) e
oito meses de espera por autorização de supressão (ENT-016). O mecanismo hidrológico foi
triangulado: a folha obstrui a rede e produz o alagamento (ENT-008, confirmado em campo por
ENT-010-ENT-011 e ENT-019).

## 8. Piloto ENT-003

Órgão ambiental municipal, bloco público, 51 minutos, 498 turnos.
**30 evidências em 23 das 55 dimensões, nos quatro eixos, das quais 9 são lacunas.**

| Eixo | Evid. | Achado |
|---|---:|---|
| 1 · Política Climática | 9 | Estratégia de adaptação **terceirizada** em contrato de 18 meses com ICT externa. Sem instrumento próprio com metas nem monitoramento climático — ambos produtos a entregar. Competência assumida «agora, porque virou prioridade», sem ato normativo citado. |
| 2 · Orçamento e Finanças | 10 | Único projeto climático próprio financiado por **rubrica ordinária de combustível**. Sem unidade de estruturação de projetos nem de captação: a busca de recursos é reativa e personalizada na chefia. Orçamento percebido como rígido, sem marcação climática no ciclo PPA/LDO/LOA. |
| 3 · Dados Climáticos | 5 | O gargalo não está no diagnóstico do risco, que já existe, mas na **conversão do dado em solução viável** — falta corpo técnico de engenharia. Fluxo entre secretarias depende de solicitação ativa. |
| 4 · Coordenação | 6 | Coordenação horizontal opera por **relação pessoal e escalonamento ao Chefe do Executivo**, não por instância institucional: funciona, e não é transferível entre gestões. |

### Os dois achados que estruturam o resto

**IPTU Verde suspenso (`2.3.1`, 00:31:28).** O instrumento existe e está regulamentado, a
demanda social existe — havia fila —, a proposta de ampliação está pronta, e a expansão foi
*deliberadamente suspensa* por insuficiência de capacidade administrativa. A barreira não é
normativa nem de demanda: é de gestão. Liga receita própria (`2.3.1`) diretamente a
capacidade institucional (`1.2.2`), nomeada pelo participante como barreira número um.

**Parceria científica sem formalização (`3.2.1`, 00:26:49).** Há fluxo real e produtivo de
dados técnico-científicos, incluindo dados meteorológicos primários de duas estações, sem
instrumento formal de parceria. Registrada como **divergência**: a prática contradiz o
desenho institucional, e a condição habilitante está exposta a descontinuidade a cada troca
de gestão ou de contrato. É o tipo de achado que a análise documental sozinha não
produziria — o argumento de por que a triangulação do Produto 2 não é formalidade.

### Ponto de atenção para a articulação do projeto

O contrato com a ICT externa tem como produtos a estratégia de enfrentamento às mudanças
climáticas, o sistema de monitoramento e a identificação de novas fontes de recursos. Há
sobreposição evidente com o escopo da consultoria IPPLAM–CEPAL. **Mapear os produtos dos
dois contratos antes do Roadmap**: articulados, um valida o outro; desarticulados, produzem
diagnósticos concorrentes sobre a mesma cidade.

---

## 9. Decisões pendentes

1. **As quatro sessões sem TCLE** — `ENT-009`, `ENT-012`, `ENT-014` e `ENT-016` foram
   codificadas e cada evidência delas traz a marca «sessão sem TCLE» no próprio texto. Não
   alimentam o diagnóstico enquanto o termo não for localizado. São 106 evidências em
   suspenso, incluindo achados que não têm substituto no restante do corpus (a resistência
   fazendária à vinculação de receita, o IPTU Verde empresarial, o poço de infiltração
   testado, a transferência de potencial construtivo). **Localizar esses termos é a pendência
   de maior retorno do projeto.**

2. **A divergência sobre ocupação irregular.** Cinco posições sobre o mesmo fato: o registro
   oficial informa zero ocupações (ENT-010-ENT-011), ENT-008 e ENT-015 negam ocupação em fundo
   de vale, e ENT-007, ENT-009 e ENT-014 relatam áreas irregulares, passivo fundiário e um
   movimento organizado de moradores de fundo de vale surgido na revisão do plano diretor. Se
   o número oficial for zero por ausência de registro e não por ausência do fenômeno, o recorte
   de sensibilidade do plano de adaptação em elaboração está sendo construído sobre uma lacuna.
   **Verificação documental na Matriz 2, antes do Roadmap.**

3. **O que verificar na Matriz 2**, a partir das alegações de sessões sem TCLE, registradas
   como divergência ou percepção de confiança baixa e nunca como fato: o decreto que teria
   dispensado EIA/RIMA e EIV; o saldo do fundo ambiental; o aporte público no data center;
   a lei que financia o conselho de desenvolvimento econômico; a adesão de Maringá ao programa
   federal de planos de adaptação, que nem o órgão contratante nem a consultoria conheciam.

4. **Produtos técnicos que existem e não circulam** — o inventário arbóreo premiado, a que a
   consultoria do plano de adaptação não teve acesso (ENT-010-ENT-011); o plano de manejo da
   arborização, elaborado com participação acadêmica e não aplicado (ENT-019); o plano de
   manejo do parque, entregue e engavetado (ENT-020); o plano municipal de resíduos, de quinze
   anos atrás (ENT-020); o mapa colaborativo de ocorrências, de estado desconhecido (ENT-007).
   **Antes de encomendar estudo novo, levantar o que já foi produzido sobre Maringá** — e o
   mesmo vale para o levantamento das normas municipais que incidem sobre a agenda climática,
   que nunca foi feito (ENT-020).

5. **Completar o crosswalk das 13 perguntas sem vínculo** — não bloqueia mais a codificação,
   que está encerrada, mas segue sendo entregável do Produto 2.

6. **As três sessões complementares** (fazenda/planejamento, planejamento urbano, procuradoria)
   serão realizadas, ou o eixo 2 será sustentado documentalmente? A codificação reduziu o custo
   de não fazê-las, sem eliminá-lo.
