# Metodologia de codificação das entrevistas

**Projeto CEPAL/IPPLAM — Maringá (PR).** Avaliação das condições habilitantes ao
financiamento climático urbano. Metodologia *Assessing Subnational Enabling Framework
Conditions for Urban Climate Finance* (CCFLA / Urban-Act, 2024), priorizada para Maringá
no Produto 2.

> Documento reconstruído em 06/09/2026 a partir do protocolo publicado e do
> `dashboard.json` recuperado (versão de 01/09/2026), e atualizado no mesmo dia
> contra o acervo completo (17 sessões). Substitui o artefato como registro
> versionável do método.

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

## 7. Lacuna de cobertura institucional

Oito dimensões atravessaram as 17 sessões sem menção na pré-triagem e sem evidência
codificada: `1.1.2`, `1.1.6`, **`2.2.1` orçamento verde**, **`2.2.2` rastreamento de
gastos**, **`2.2.3` integração PPA/LDO/LOA**, `2.6.4`, **`3.1.3` inventário municipal de
GEE** e `3.2.4` — as três em negrito com prioridade «Muito alta».

*(A codificação é mais fina que a triagem: `ENT-001-ENT-002` produziu evidência para
`2.2.1` e `2.2.3` por leitura, ainda que o léxico não as tenha alcançado. As dimensões
que seguem sem qualquer evidência codificada de prioridade «Muito alta» são `2.2.2`,
`2.3.2` e `3.1.3`.)*

A causa é institucional. Não há registro de entrevista para: Fazenda/Planejamento,
planejamento urbano (IPPLAM), obras públicas, urbanismo e habitação, procuradoria,
limpeza urbana, mobilidade, órgão ambiental estadual e COMDEMA. O eixo 2 concentra 25
das 55 dimensões e é justamente o eixo cuja fonte primária está ausente — **as menções
financeiras vêm de quem usa o orçamento, não de quem o monta.**

A universidade pública, que constava como ausente no levantamento de 01/09, passou a ter
registro: `ENT-019` e `ENT-020`, ambas na UEM, cobrem `3.2.1`.

**Duas saídas:** três sessões adicionais (fazenda/planejamento, planejamento urbano,
procuradoria) cobririam a maior parte do vazio; ou sustentar essas dimensões por
evidência documental na Matriz 2 (PPA, LDO, LOA, QDD, relatórios de execução).

---

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

1. **O nível de detalhe do piloto serve?** Trinta evidências por entrevista, com trecho
   literal e paráfrase analítica. Se for demais, o corte natural é abandonar a paráfrase nas
   evidências de confiança baixa.
2. **`ENT-012` é qual entrevista?** Ou o código está vago e deve sair da matriz de controle.
3. **O termo de `ENT-009` existe?** Sem ele, a entrevista fica fora do diagnóstico.
4. **Completar o crosswalk das 13 perguntas sem vínculo?** Não bloqueia a codificação, mas é
   entregável do Produto 2 e a lacuna vai aparecer na revisão.
5. **Codificar por falante nas entrevistas com mais de um participante?** Recomendado para
   `ENT-010` e `ENT-015`.
6. **As três sessões complementares** (fazenda/planejamento, planejamento urbano,
   procuradoria) serão realizadas, ou o eixo 2 será sustentado documentalmente?
