# Afirmações da Seção 3 sem âncora de evidência

**53 das 93 afirmações** não receberam âncora na seleção automática. Este arquivo existe para que a revisão humana decida caso a caso, e está ordenado por onde a leitura rende mais.

A seleção automática é conservadora de propósito: ela recusa mais do que aceita. Logo, estar nesta lista **não** significa que a afirmação não tenha sustentação. Significa que o método não conseguiu estabelecê-la com o critério declarado. Os dois desfechos possíveis da revisão são igualmente úteis: encontrar a evidência que o método não viu, ou confirmar que ela não existe, e nesse caso a ausência é achado.

## Como decidir

Para cada afirmação estão as três candidatas levantadas, com a paráfrase da evidência, que é o que se cita. Se alguma sustentar a afirmação, anote o código; se nenhuma sustentar, a afirmação fica sem âncora e isso é o resultado. Depois, marque na página `revisao_pendentes.html` ou direto em `produtos/P4_ancoras_revisao.csv`, mudando `decisao` para `aceita` e `decisor` para `humano`. A seleção automática nunca sobrescreve decisão humana.

## Resumo

| Prioridade | Grupo | Afirmações |
|---|---|---:|
| 1 | Empate entre candidatas | 3 |
| 2 | Passou perto do corte (peso 15 a 18) | 13 |
| 3 | Zona cinzenta (peso 12 a 15) | 14 |
| 4 | Peso baixo (abaixo de 12) | 21 |
| 5 | Chamada de lista | 2 |


## 1. Empate entre candidatas

O método encontrou duas candidatas com peso semelhante e se recusou a escolher, porque escolher no empate inventaria precisão. A leitura resolve depressa: basta dizer qual das duas.

### Afirmação 85, Sociedade Civil

*3.4.4. Governança e Coordenação*

> Falta de Governança Regional: A ausência de cooperação efetiva entre Maringá e municípios vizinhos (Sarandi, Paiçandu) é apontada como um problema estrutural. O "mito da melhor cidade para se viver" afasta Maringá de sua realidade metropolitana, impedindo o reconhecimento de que os impactos climáticos e as vulnerabilidades são compartilhados regionalmente. A Associação dos Municípios do Setentrião Paranaense (AMUSEP) possui estrutura para consórcios (como o SAMU), mas essa potencialidade não é explorada para a cooperação ambiental.

Motivo da recusa: **empate: 28.1 vs 26.3 (margem < 2.0)**

| | Sessão | Marca | Dimensão | Maturidade | Conf. | Peso |
|---|---|---|---|---|---|---:|
| 1 | `ENT-007` | `00:40:41` | `4.1.4` Coordenação regional/metropolitana com municípios vizinhos | efetivo | alta | 28.1 |
| 2 | `ENT-007` | `00:41:51` | `4.1.4` Coordenação regional/metropolitana com municípios vizinhos | inexistente | alta | 26.3 |
| 3 | `ENT-014` | `00:31:10` | `4.1.4` Coordenação regional/metropolitana com municípios vizinhos | inexistente | alta | 24.7 |

1. ACHADO INSTITUCIONAL. Existe e funciona na região uma associação de municípios com estrutura permanente, reuniões mensais, serviço compartilhado de saúde e — o ponto decisivo — um corpo técnico que elabora projeto para municípios sem quadro próprio. É exatamente o modelo de unidade regional de preparação de projetos que falta à agenda climática, já montado e operando em outro objeto.
2. LACUNA COM SOLUÇÃO À VISTA. A governança regional existente não tem pauta ambiental nem climática. Converge com ENT-006 (cooperação regional restrita à saúde): incluir o tema na instância que já funciona é caminho mais curto que criar consórcio climático novo.
3. ACHADO CENTRAL SOBRE A ESCALA. O título de melhor cidade para se viver opera como barreira à cooperação regional, porque a distinção em relação aos vizinhos é socialmente valorizada. Nomeia o obstáculo político — e não técnico — à integração metropolitana, e é a leitura mais aguda do corpus sobre por que ela não avança. SESSÃO SEM TCLE.

### Afirmação 62, Academia

*3.3.4. Governança e Coordenação*

> Capacidade Operacional Insuficiente: Há um consenso de que a prefeitura não possui a capacidade operacional necessária. Isso se manifesta na ausência de um departamento de parques e jardins atuante, dificuldades na poda e reposição de árvores, falhas na limpeza de bueiros e a não implementação dos fundos de vale como espaços públicos verdes.

Motivo da recusa: **empate: 20.4 vs 20.1 (margem < 2.0)**

| | Sessão | Marca | Dimensão | Maturidade | Conf. | Peso |
|---|---|---|---|---|---|---:|
| 1 | `ENT-019` | `00:06:04` | `1.2.2` Capacidade institucional para executar ações climáticas | inexistente | alta | 20.4 |
| 2 | `ENT-019` | `00:07:35` | `2.1.5` Estratégia financeira para adaptação e resiliência | inexistente | alta | 20.1 |
| 3 | `ENT-020` | `00:11:10` | `3.2.2` Qualidade, atualização e acessibilidade dos dados climáticos | inexistente | alta | 12.2 |

1. LACUNA DE ESTRUTURA, NOMEADA COM PRECISÃO. Não existe unidade municipal dedicada a parques e jardins — a cidade cuja identidade e cujo maior risco são a arborização não tem órgão para geri-la. É a explicação estrutural da falha de reposição relatada em ENT-006, ENT-007, ENT-009 e ENT-014.
2. Prioridade convergente: qualificação dos fundos de vale como infraestrutura verde de uso público e função climática. Converge com o parque-esponja de ENT-017-ENT-018, a passarela suspensa de ENT-015, a trilha de ENT-016 e o uso público de ENT-016 — cinco sessões de quatro setores apontando o mesmo território como prioridade de investimento.
3. DISTINÇÃO DECISIVA. O município tem indicador agregado e não tem dado de gestão. Reformula com precisão a lacuna «Muito alta» de qualidade e acessibilidade dos dados: o problema não é a ausência de número, é a ausência de resolução espacial suficiente para decidir onde intervir — e os 85 km de fundo de vale, o principal ativo ambiental da cidade, estão sem diagnóstico de condição.

### Afirmação 63, Academia

*3.3.4. Governança e Coordenação*

> Fragmentação Institucional e Política: A relação entre academia e prefeitura é descrita como fragmentada, frequentemente influenciada por questões políticas e partidárias. Isso cria uma barreira para a colaboração, com secretários e dirigentes alinhados a interesses institucionais específicos, dificultando uma interlocução técnica e contínua.

Motivo da recusa: **empate: 18.9 vs 18.0 (margem < 2.0)**

| | Sessão | Marca | Dimensão | Maturidade | Conf. | Peso |
|---|---|---|---|---|---|---:|
| 1 | `ENT-020` | `00:22:28` | `3.2.1` Parcerias com universidades e centros de pesquisa | inexistente | alta | 18.9 |
| 2 | `ENT-019` | `00:12:47` | `3.2.1` Parcerias com universidades e centros de pesquisa | inexistente | alta | 18.0 |
| 3 | `ENT-019` | `00:11:11` | `3.2.1` Parcerias com universidades e centros de pesquisa | inexistente | alta | 14.6 |

1. Quarta confirmação da lacuna de parceria científica (com ENT-006, ENT-012 e ENT-019). O acesso ao conhecimento acadêmico depende de relação pessoal com dirigentes — mesmo padrão de personalização que ENT-003 registra na coordenação horizontal e ENT-015 na titularidade da agenda. Dimensão «Muito alta».
2. ACHADO SOBRE A CAUSA DA LACUNA. A resistência é atribuída a uma leitura interna da universidade que confunde política pública com política de governo. Identifica um obstáculo cultural, e não de instrumento — o que muda a recomendação: antes de propor convênio, é preciso desfazer essa distinção.
3. ACHADO DE INCENTIVO ALINHADO. A exigência institucional de extensão universitária cria demanda por problemas reais, do mesmo modo que a prefeitura demanda base técnica. Os incentivos das duas instituições já apontam na mesma direção e o único elo ausente é o canal — o que torna essa a lacuna mais barata de fechar em todo o diagnóstico.


## 2. Passou perto do corte (peso 15 a 18)

Ficaram logo abaixo do corte. São as mais prováveis de serem falsos negativos do método.

### Afirmação 25, Setor Público

*3.1.5. Ações e Soluções Propostas*

> Projetos Piloto: Descarbonização da frota com biodiesel e projetos de "núcleos de bairro" para identificação de riscos.

Motivo da recusa: **peso informacional 17.8 < 18.0**

| | Sessão | Marca | Dimensão | Maturidade | Conf. | Peso |
|---|---|---|---|---|---|---:|
| 1 | `ENT-003` | `00:22:24` | `2.1.6` Estratégia financeira para mitigação e baixo carbono | em_implementacao | alta | 17.8 |
| 2 | `ENT-015` | `00:47:41` | `1.1.1` Estratégia de mitigação com metas claras | em_implementacao | alta | 13.4 |
| 3 | `ENT-008` | `00:43:40` | `2.1.4` Capacidade de preparar projetos para financiamento | em_implementacao | alta | 11.0 |

1. Existe ação de mitigação em curso, mas originada em determinação individual do Chefe do Executivo e não em estratégia de baixo carbono formalizada. Coerente com a prioridade «Média» atribuída a esta dimensão em Maringá.
2. AÇÃO DE MITIGAÇÃO EM CURSO, COM CUSTO E RISCO ASSUMIDOS. Substituição integral do diesel da frota por biocombustível, com redução declarada de 90% das emissões e exposição do orçamento à volatilidade da soja. Confirma e amplia o projeto de descarbonização citado em ENT-004 e ENT-008 — e é a decisão de mitigação de maior efeito e maior risco fiscal do corpus.
3. Existe carteira estruturada de quatro projetos, com objetivos definidos e um deles orientado ao encerramento do aterro. Qualifica o achado de ENT-004: a ausência de carteira vale para as pastas executoras, não para o órgão ambiental — a capacidade de estruturar projeto existe, concentrada em uma unidade e em duas pessoas.

### Afirmação 77, Sociedade Civil

*3.4.2. Finanças: orçamento, financiamento e captação de recursos*

> Necessidade de Comitê Deliberativo/Consultivo: A criação de um comitê deliberativo ou consultivo é apontada como fundamental para facilitar a gestão do plano e a tomada de decisões, integrando dados e dando continuidade à captação de recursos financeiros.

Motivo da recusa: **peso informacional 17.5 < 18.0**

| | Sessão | Marca | Dimensão | Maturidade | Conf. | Peso |
|---|---|---|---|---|---|---:|
| 1 | `ENT-010-ENT-011` | `00:29:11` | `1.2.1` Responsabilidades institucionais para implementação climática | inexistente | alta | 17.5 |
| 2 | `ENT-010-ENT-011` | `00:33:51` | `1.1.7` Monitoramento e avaliação da adaptação | inexistente | alta | 9.5 |
| 3 | `ENT-005` | `00:44:12` | `2.3.3` Diversificação de receitas ambientais/climáticas | efetivo | alta | 5.3 |

1. LACUNA DE GOVERNANÇA, COM PROPOSTA JÁ NA MESA. Não existe instância intersetorial de coordenação climática, ela foi formalmente proposta pela consultoria e não foi constituída — e sua ausência afeta tanto a elaboração do plano quanto a elegibilidade a financiamento. Dimensão «Muito alta»; é a recomendação com maior grau de convergência entre os dois contratos em curso na cidade.
2. Avaliação externa de que Maringá produz bons instrumentos e falha na continuidade. Converge com o «plano de gaveta» de ENT-007 e com a divergência de ENT-003 sobre a parceria científica exposta à troca de gestão: o risco da agenda climática local não é a formulação, é a permanência.
3. ACHADO REPLICÁVEL. Existe em Maringá um precedente institucional de estrutura dedicada à captação por renúncia fiscal, criada por indução do poder público e operada fora dele, com resultado comprovado no setor cultural. É o desenho institucional que falta à agenda climática — e a dimensão de diversificação de receitas ambientais, que não recebia evidência de nenhuma pergunta do instrumental, passa a ter lastro empírico.

### Afirmação 58, Academia

*3.3.3. Dados, Monitoramento e Planejamento*

> Desconexão Academia-Prefeitura: Há uma forte percepção de que o vasto conhecimento produzido na universidade (sobre ilhas de calor, fundos de vale, impacto da verticalização) não é acessado ou utilizado pela prefeitura. Apesar de muitos técnicos municipais terem formação nas universidades locais, falta um diálogo efetivo e sistematizado. A metáfora da "Avenida [participante] como barreira simbólica" ilustra essa desconexão.

Motivo da recusa: **peso informacional 17.2 < 18.0**

| | Sessão | Marca | Dimensão | Maturidade | Conf. | Peso |
|---|---|---|---|---|---|---:|
| 1 | `ENT-020` | `00:22:28` | `3.2.1` Parcerias com universidades e centros de pesquisa | inexistente | alta | 17.2 |
| 2 | `ENT-006` | `00:27:41` | `3.2.1` Parcerias com universidades e centros de pesquisa | inexistente | alta | 17.0 |
| 3 | `ENT-019` | `00:11:11` | `3.2.1` Parcerias com universidades e centros de pesquisa | inexistente | alta | 14.3 |

1. Quarta confirmação da lacuna de parceria científica (com ENT-006, ENT-012 e ENT-019). O acesso ao conhecimento acadêmico depende de relação pessoal com dirigentes — mesmo padrão de personalização que ENT-003 registra na coordenação horizontal e ENT-015 na titularidade da agenda. Dimensão «Muito alta».
2. LACUNA CENTRAL. A universidade privada não tem canal com o município. Confirma, de outro ponto do sistema, o achado de ENT-004: a parceria científica registrada em ENT-003 é um caso isolado no órgão ambiental, não uma prática municipal. Dimensão «Muito alta».
3. ACHADO DE INCENTIVO ALINHADO. A exigência institucional de extensão universitária cria demanda por problemas reais, do mesmo modo que a prefeitura demanda base técnica. Os incentivos das duas instituições já apontam na mesma direção e o único elo ausente é o canal — o que torna essa a lacuna mais barata de fechar em todo o diagnóstico.

### Afirmação 80, Sociedade Civil

*3.4.3. Dados, Monitoramento e Planejamento*

> Dificuldade de Acesso e Transparência: A sociedade civil relata dificuldades constantes no acesso a documentos públicos, processos de licitação e dados sobre crimes ambientais. A transparência sobre ações, políticas e investimentos climáticos é considerada insuficiente.

Motivo da recusa: **peso informacional 17.0 < 18.0**

| | Sessão | Marca | Dimensão | Maturidade | Conf. | Peso |
|---|---|---|---|---|---|---:|
| 1 | `ENT-005` | `00:25:59` | `2.2.2` Rastreamento de gastos climáticos | em_implementacao | alta | 17.0 |
| 2 | `ENT-014` | `00:23:08` | `3.1.1` Sistema municipal de dados climáticos e territoriais | inexistente | alta | 15.5 |
| 3 | `ENT-014` | `00:20:41` | `4.2.3` Participação de conselhos, COMDEMA e sociedade civil | inexistente | alta | 13.5 |

1. ACHADO. Existe na cidade uma estrutura permanente e financiada de acompanhamento do gasto público, com capacidade demonstrada de impugnar licitação. O rastreamento de gastos — dimensão «Muito alta» sem evidência codificada até aqui — existe na sociedade civil e não na administração: a capacidade está instalada fora do município e não está orientada a marcação climática.
2. LACUNA. Não há ponto único de acesso a dado climático para a sociedade, confirmado por profissional que atua em política urbana na cidade. Converge com ENT-004, ENT-009, ENT-010-ENT-011 e ENT-013 — cinco sessões. Dimensão «Muito alta». SESSÃO SEM TCLE.
3. CONVERGÊNCIA DE PROPOSTA. Integração entre política habitacional e agenda climática, com melhoria habitacional e equipamentos públicos nas bordas. Converge com a proposta de ATHIS como instrumento de adaptação de ENT-007 — duas sessões do mesmo setor, independentes, apontando o mesmo desenho. É a recomendação de adaptação com recorte distributivo mais consistente do corpus. SESSÃO SEM TCLE.

### Afirmação 84, Sociedade Civil

*3.4.4. Governança e Coordenação*

> Instituto Ambiental (IAM) sob Críticas: Há uma crítica contundente à atuação do IAM. A autarquia é acusada de sofrer com indicações políticas, falta de transparência e a inconstitucional dispensa de laudos técnicos (Estudos de Impacto de Vizinhança e Relatório de Impacto Ambiental) para novos empreendimentos. A substituição de profissionais de carreira por aliados políticos é vista como um esvaziamento da capacidade técnica do órgão.

Motivo da recusa: **peso informacional 16.6 < 18.0**

| | Sessão | Marca | Dimensão | Maturidade | Conf. | Peso |
|---|---|---|---|---|---|---:|
| 1 | `ENT-014` | `00:38:44` | `2.1.4` Capacidade de preparar projetos para financiamento | em_implementacao | alta | 16.6 |
| 2 | `ENT-010-ENT-011` | `00:14:52` | `1.1.5` Avaliação de riscos e vulnerabilidades climáticas | em_implementacao | alta | 6.1 |
| 3 | `ENT-010-ENT-011` | `00:23:16` | `3.1.1` Sistema municipal de dados climáticos e territoriais | inexistente | alta | 6.1 |

1. Avaliação de que a capacidade técnica de base existe e está bem dirigida, e de que a conjuntura política é favorável. Diverge da leitura de escassez de ENT-008 e ENT-004 em um ponto importante: a qualificação existe, o que falta é quantidade e alocação. SESSÃO SEM TCLE.
2. TRIANGULAÇÃO CONFIRMADA. O mecanismo folha–obstrução–alagamento descrito pela direção do órgão ambiental (ENT-008) é confirmado independentemente pela equipe técnica em campo. Deixa de ser hipótese de um gestor e passa a ser achado do diagnóstico.
3. ACHADO ESTRUTURANTE, DE FONTE TÉCNICA EXTERNA. O problema não é ausência de dado, é governança: o que existe está desatualizado ou inacessível, inclusive para o próprio órgão contratante. Reformula a dimensão de sistema municipal de dados — a prioridade é catalogar, atualizar e dar acesso, não coletar de novo. Dimensão «Muito alta».

### Afirmação 57, Academia

*3.3.3. Dados, Monitoramento e Planejamento*

> Inexistência de Dados Públicos e Sistematizados: Os acadêmicos afirmam desconhecer a existência de dados sistematizados e públicos sobre a questão climática em Maringá. O município possui apenas dados genéricos (ex: IBGE) e carece de monitoramento meteorológico (precipitação, ventos) e informações detalhadas sobre vegetação urbana para a tomada de decisão.

Motivo da recusa: **peso informacional 16.5 < 18.0**

| | Sessão | Marca | Dimensão | Maturidade | Conf. | Peso |
|---|---|---|---|---|---|---:|
| 1 | `ENT-020` | `00:11:10` | `3.1.1` Sistema municipal de dados climáticos e territoriais | inexistente | alta | 16.5 |
| 2 | `ENT-020` | `00:06:45` | `1.1.6` Alinhamento da adaptação com políticas nacionais/estaduais | inexistente | alta | 13.9 |
| 3 | `ENT-019` | `00:09:17` | `3.1.1` Sistema municipal de dados climáticos e territoriais | inexistente | alta | 11.4 |

1. ACHADO CRÍTICO. Existe estação meteorológica de referência na universidade local e seus dados não alimentam o planejamento municipal. Converge com ENT-003 (dados meteorológicos primários de duas estações circulando sem instrumento formal) e qualifica a rede de vinte estações em contratação (ENT-015): o município está comprando capacidade de monitoramento sem antes ter incorporado a que já existe na cidade. Dimensão «Muito alta».
2. ACHADO DEFINITIVO. O plano diretor vigente, aprovado há menos de dois anos, foi calibrado com série climática antiga e não incorpora a variável climática. É a evidência mais forte do corpus sobre desalinhamento do instrumento urbanístico central com a agenda climática — e explica, na origem, a maladaptação documentada em ENT-006, a pressão sobre áreas verdes de ENT-007 e o subdimensionamento da drenagem apontado por todos.
3. LACUNA DE PUBLICIDADE. Pesquisador vinculado à universidade pública local desconhece qualquer base climática municipal sistematizada e pública. Converge com ENT-004, ENT-009, ENT-013 e ENT-014 — e a ressalva «talvez existam» é ela mesma parte do achado: o dado, quando existe, não é conhecido nem por quem trabalharia com ele. Dimensão «Muito alta».

### Afirmação 40, Setor Privado

*3.2.4. Governança e Coordenação*

> Morosidade Regulatória e Falta de Regras Claras: Há uma crítica contundente à lentidão do poder público. A falta de celeridade nas ações e a ausência de regras claras geram impactos negativos na economia. Exemplos concretos incluem prazos de até oito meses para autorizações de manejo de árvores, o que inviabiliza ações preventivas e desestimula a participação privada.

Motivo da recusa: **peso informacional 16.2 < 18.0**

| | Sessão | Marca | Dimensão | Maturidade | Conf. | Peso |
|---|---|---|---|---|---|---:|
| 1 | `ENT-016` | `00:35:18` | `2.4.1` Mobilização de investimento privado em infraestrutura climática | inexistente | alta | 16.2 |
| 2 | `ENT-009` | `00:05:44` | `1.1.4` Estratégia de adaptação com metas claras | formalizado | alta | 15.5 |
| 3 | `ENT-016` | `00:28:43` | `4.2.3` Participação de conselhos, COMDEMA e sociedade civil | inexistente | alta | 10.0 |

1. BARREIRA NÚMERO UM SEGUNDO O SETOR PRIVADO, COM MEDIDA. Oito meses de espera por autorização de supressão arbórea com laudo pronto. Converge com a fila de poda relatada em ENT-007 e com a restrição de equipe do órgão ambiental descrita em ENT-008 — a mesma escassez de capacidade que atrasa o serviço público atrasa o investimento privado, e produz aqui o mesmo efeito perverso: pressão pela via informal. SESSÃO SEM TCLE.
2. LACUNA DE IMPLEMENTAÇÃO. O plano de arborização existe em norma e não é executado na etapa de reposição. Converge com o déficit relatado em ENT-006 e com a ausência de plano de manejo apontada em ENT-007 — três sessões independentes descrevendo a mesma falha. SESSÃO SEM TCLE.
3. O canal de diálogo entre setor privado organizado e administração ambiental é avaliado como insuficiente. Converge com a carta sem resposta de ENT-007 e as 25 propostas sem desdobramento de ENT-009 — três setores distintos relatando ausência de fluxo institucional de recepção e resposta a proposta externa. SESSÃO SEM TCLE.

### Afirmação 61, Academia

*3.3.4. Governança e Coordenação*

> Gestão Reativa e Improvisada: A atuação da prefeitura é classificada como improvisada e reativa, focada em ações paliativas em vez de um planejamento preventivo e estruturado. A gestão "reage aos problemas sem planejamento preventivo", o que é evidenciado pela falta de aplicação de planos existentes, como o plano de manejo para arborização.

Motivo da recusa: **peso informacional 16.2 < 18.0**

| | Sessão | Marca | Dimensão | Maturidade | Conf. | Peso |
|---|---|---|---|---|---|---:|
| 1 | `ENT-019` | `00:11:11` | `3.2.1` Parcerias com universidades e centros de pesquisa | inexistente | alta | 16.2 |
| 2 | `ENT-019` | `00:06:04` | `1.2.2` Capacidade institucional para executar ações climáticas | inexistente | alta | 13.3 |
| 3 | `ENT-020` | `00:11:10` | `1.1.7` Monitoramento e avaliação da adaptação | inexistente | alta | 11.0 |

1. ACHADO DE INCENTIVO ALINHADO. A exigência institucional de extensão universitária cria demanda por problemas reais, do mesmo modo que a prefeitura demanda base técnica. Os incentivos das duas instituições já apontam na mesma direção e o único elo ausente é o canal — o que torna essa a lacuna mais barata de fechar em todo o diagnóstico.
2. LACUNA DE ESTRUTURA, NOMEADA COM PRECISÃO. Não existe unidade municipal dedicada a parques e jardins — a cidade cuja identidade e cujo maior risco são a arborização não tem órgão para geri-la. É a explicação estrutural da falha de reposição relatada em ENT-006, ENT-007, ENT-009 e ENT-014.
3. SEGUNDO CASO DE PLANO NÃO IMPLEMENTADO, COM SÉRIE DE QUINZE ANOS. Junto ao plano de manejo da arborização de ENT-019 e ao plano de manejo do parque citado adiante, compõe o padrão que ENT-007 chama de «plano de gaveta»: Maringá produz instrumento técnico de qualidade e não o executa nem o monitora. O risco para o plano climático em elaboração é explícito.

### Afirmação 21, Setor Público

*3.1.4. Governança e Coordenação*

> Fragmentação e Integração: Não há uma secretaria ou departamento central que coordene as ações de forma global. As responsabilidades estão distribuídas, com destaque para o IAM (Instituto Ambiental), a SEMOP (Secretaria de Obras), a Defesa Civil e a Secretaria de Infraestrutura. A integração, embora reconhecida como desafiadora devido à descentralização, tem melhorado com reuniões semanais promovidas pela gestão, facilitando a comunicação entre os diretores.

Motivo da recusa: **peso informacional 15.9 < 18.0**

| | Sessão | Marca | Dimensão | Maturidade | Conf. | Peso |
|---|---|---|---|---|---|---:|
| 1 | `ENT-001-ENT-002` | `00:35:20` | `1.2.1` Responsabilidades institucionais para implementação climática | em_implementacao | alta | 15.9 |
| 2 | `ENT-008` | `00:31:47` | `1.2.1` Responsabilidades institucionais para implementação climática | inexistente | alta | 15.9 |
| 3 | `ENT-013` | `00:22:00` | `1.2.2` Capacidade institucional para executar ações climáticas | em_implementacao | alta | 14.8 |

1. As responsabilidades setoriais são claras e prontamente identificadas por um servidor de área-meio — o que indica desenho institucional legível. O que não existe é competência climática transversal: cada órgão responde por um fragmento e nenhum responde pelo conjunto.
2. ACHADO ESTRUTURANTE. A atribuição sobre a drenagem se define pelo domínio do território e não pela natureza do serviço: dentro de área de preservação, a rede vira responsabilidade ambiental. Cria uma zona sem titular efetivo exatamente no trecho onde a água chega ao rio. Dimensão «Muito alta».
3. Reestruturação administrativa recente do órgão de defesa civil, com introdução de método de mapeamento e de integração de dados. Converge com ENT-012 sobre a recomposição institucional de 2025 e mostra um caso em que ela produziu capacidade nova.

### Afirmação 16, Setor Público

*3.1.3. Dados, Monitoramento e Planejamento*

> Levantamentos Próprios: Contratação de robôs para mapeamento da rede de drenagem subterrânea e aquisição de 20 miniestações meteorológicas para previsibilidade climática.

Motivo da recusa: **peso informacional 15.9 < 18.0**

| | Sessão | Marca | Dimensão | Maturidade | Conf. | Peso |
|---|---|---|---|---|---|---:|
| 1 | `ENT-015` | `00:12:31` | `3.2.3` Dados de risco, vulnerabilidade e exposição | em_elaboracao | alta | 15.9 |
| 2 | `ENT-013` | `00:24:49` | `4.2.3` Participação de conselhos, COMDEMA e sociedade civil | em_elaboracao | alta | 10.8 |
| 3 | `ENT-008` | `00:30:37` | `3.2.2` Qualidade, atualização e acessibilidade dos dados climáticos | em_elaboracao | alta | 6.4 |

1. ACHADO DECISIVO. Rede própria de vinte estações meteorológicas em contratação, com previsão contratada de três dias. É a primeira capacidade de monitoramento climático em tempo real da cidade, e ataca diretamente a lacuna «Muito alta» de dados de risco. Converge com o achado de ENT-003 sobre dados meteorológicos primários já em circulação — a diferença é que aqui a capacidade passa a ser municipal e formalizada.
2. PROJETO ESTRUTURANTE, JÁ SUBMETIDO. Rede de núcleos comunitários de defesa civil como canal bidirecional — a comunidade identifica o risco local que o mapeamento não alcança, e recebe o alerta em linguagem própria. Responde de uma vez às lacunas de dado territorial fino (ENT-005, ENT-007) e de comunicação (cinco sessões), e se apoia na densidade associativa que ENT-007 documenta. É a proposta com melhor relação entre custo e alcance no corpus.
3. A base cadastral da infraestrutura de drenagem está sendo reconstituída dentro do plano climático — ou seja, o município não sabe hoje, de forma sistematizada, onde estão os pontos de saída de sua própria rede. Pré-condição de qualquer projeto financiável de drenagem, e está em construção.

### Afirmação 18, Setor Público

*3.1.3. Dados, Monitoramento e Planejamento*

> Monitoramento em Construção: Não há metas específicas para a agenda climática, e o monitoramento é um produto em desenvolvimento. O plano de metas geral do IPPLAM engloba o tema de forma transversal, mas não isolada.

Motivo da recusa: **peso informacional 15.6 < 18.0**

| | Sessão | Marca | Dimensão | Maturidade | Conf. | Peso |
|---|---|---|---|---|---|---:|
| 1 | `ENT-003` | `00:19:17` | `1.1.7` Monitoramento e avaliação da adaptação | inexistente | alta | 15.6 |
| 2 | `ENT-001-ENT-002` | `00:23:24` | `1.1.7` Monitoramento e avaliação da adaptação | inexistente | alta | 14.9 |
| 3 | `ENT-003` | `00:20:55` | `1.1.7` Monitoramento e avaliação da adaptação | monitorado | media | 13.3 |

1. LACUNA CRÍTICA. Não existe hoje meta, indicador ou mecanismo de monitoramento específico para mudança climática. A dimensão tem prioridade «Muito alta» na matriz de Maringá e depende integralmente da entrega do contrato de consultoria.
2. Existe plano de metas municipal com acompanhamento periódico de percentual de execução, mas nenhum indicador climático próprio. O monitoramento da ação climática não tem instrumento dedicado: depende de leitura indireta de metas setoriais gerais.
3. Existe monitoramento setorial (saneamento e resíduos), mas movido por obrigação legal e reconhecido como incompleto pelo próprio órgão. Não há ponte declarada entre esses indicadores setoriais e a agenda climática.

### Afirmação 13, Setor Público

*3.1.3. Dados, Monitoramento e Planejamento*

> Lacuna de Dados Integrados: A falta de um sistema centralizado e integrado de dados é um gargalo crítico. As informações estão dispersas, muitas vezes em estudos acadêmicos, e o conhecimento técnico sobre infraestrutura é, em grande parte, empírico, obtido por profissionais que vão a campo.

Motivo da recusa: **peso informacional 15.6 < 18.0**

| | Sessão | Marca | Dimensão | Maturidade | Conf. | Peso |
|---|---|---|---|---|---|---:|
| 1 | `ENT-003` | `00:19:17` | `3.2.5` Integração dos dados em planejamento e projetos financiáveis | em_implementacao | alta | 15.6 |
| 2 | `ENT-013` | `00:23:04` | `3.1.1` Sistema municipal de dados climáticos e territoriais | inexistente | alta | 15.1 |
| 3 | `ENT-008` | `00:30:37` | `3.1.1` Sistema municipal de dados climáticos e territoriais | em_implementacao | alta | 12.4 |

1. LACUNA DE CONVERSÃO. O gargalo não está no diagnóstico do risco (que existe há tempo) mas na tradução do dado em solução técnica e economicamente viável. É precisamente a fronteira entre o eixo Dados e o eixo Finanças: dado sem capacidade de engenharia não gera projeto financiável.
2. A lacuna de sistema integrado é apresentada como padrão nacional das defesas civis municipais, e não como falha local. Reposiciona a recomendação: Maringá pode se posicionar como referência ao resolvê-la, o que dialoga com o capital reputacional apontado em ENT-005, ENT-007 e ENT-012.
3. Existe portal geoespacial municipal com camadas utilizáveis em escala de planejamento e insuficientes em escala de intervenção. Qualifica a lacuna registrada em ENT-004: o problema não é ausência de sistema, é resolução — e é justamente na escala da rua que o projeto de drenagem se define.

### Afirmação 7, Setor Público

*3.1.1. Política Climática: incorporação, riscos e desafios*

> Desafios Culturais e Técnicos: As principais barreiras são a falta de consciência e educação ambiental da população e da máquina pública, a falta de servidores qualificados e a morosidade e burocracia dos processos licitatórios.

Motivo da recusa: **peso informacional 15.6 < 18.0**

| | Sessão | Marca | Dimensão | Maturidade | Conf. | Peso |
|---|---|---|---|---|---|---:|
| 1 | `ENT-012` | `00:52:47` | `4.2.1` Participação pública na agenda climática | inexistente | alta | 15.6 |
| 2 | `ENT-003` | `00:42:14` | `1.2.2` Capacidade institucional para executar ações climáticas | em_implementacao | alta | 12.9 |
| 3 | `ENT-001-ENT-002` | `00:26:51` | `4.2.2` Engajamento do setor privado | inexistente | media | 12.3 |

1. BARREIRA NÚMERO UM, SEGUNDO O LEGISLATIVO, COM SUA PRÓPRIA EXPLICAÇÃO. A formação é apontada como condição habilitante primeira, e imediatamente qualificada pelo desalinhamento entre o horizonte do resultado e o do mandato. Converge literalmente com ENT-009 («não dá voto») e nomeia por que a prevenção perde na disputa orçamentária. SESSÃO SEM TCLE.
2. LACUNA PRINCIPAL declarada pelo participante como barreira número um, de forma espontânea e sem hesitação. Capacidade institucional insuficiente é o gargalo que limita simultaneamente preparação de projetos, captação e ampliação de instrumentos existentes.
3. O mercado local de execução ainda não está formado para obra de baixo carbono. A restrição está do lado da oferta, não só da demanda pública — o que significa que exigir critério verde em licitação, isoladamente, pode esvaziar certames.


## 3. Zona cinzenta (peso 12 a 15)

Zona cinzenta: o vocabulário em comum existe, mas é pouco distintivo. Pode ser sustentação real com vocabulário divergente.

### Afirmação 49, Academia

*3.3.1. Política Climática: incorporação, riscos e desafios*

> Tempestades e Arborização: Eventos severos que derrubam árvores antigas, causando acidentes e cortes de energia.

Motivo da recusa: **peso informacional 14.5 < 18.0**

| | Sessão | Marca | Dimensão | Maturidade | Conf. | Peso |
|---|---|---|---|---|---|---:|
| 1 | `ENT-020` | `00:04:56` | `1.1.5` Avaliação de riscos e vulnerabilidades climáticas | em_implementacao | alta | 14.5 |
| 2 | `ENT-019` | `00:04:20` | `1.1.5` Avaliação de riscos e vulnerabilidades climáticas | em_implementacao | alta | 11.1 |
| 3 | `ENT-006` | `00:45:34` | `1.2.2` Capacidade institucional para executar ações climáticas | em_implementacao | media | 5.6 |

1. Nona e última confirmação do corpus sobre o par vento–arborização, com os três agravantes acumulados: idade, porte e poda irregular. A poda irregular liga este achado à fila de espera relatada em ENT-007 e ao prazo de oito meses de ENT-016 — o déficit de capacidade administrativa produz, por essa via, o próprio dano.
2. Oitava confirmação do par arborização envelhecida–tempestade severa como risco principal. O corpus inteiro converge nesse ponto: nove das dezessete sessões o apontam, em quatro setores.
3. A resposta à insuficiência de equipe própria foi a terceirização do serviço de manejo arbóreo, avaliada positivamente por seu efeito na redução de ocorrências. Solução de capacidade por contrato, e não por quadro — mesmo padrão do contrato com ICT externa em ENT-003.

### Afirmação 89, Sociedade Civil

*3.4.5. Soluções Propostas*

> Prioridades: Diagnóstico detalhado da arborização, plano de manejo e substituição, investimento em viveiro municipal, galerias pluviais e poços de infiltração.

Motivo da recusa: **peso informacional 14.5 < 18.0**

| | Sessão | Marca | Dimensão | Maturidade | Conf. | Peso |
|---|---|---|---|---|---|---:|
| 1 | `ENT-007` | `00:18:28` | `3.2.3` Dados de risco, vulnerabilidade e exposição | inexistente | alta | 14.5 |
| 2 | `ENT-007` | `00:06:56` | `1.1.4` Estratégia de adaptação com metas claras | inexistente | alta | 12.0 |
| 3 | `ENT-007` | `00:19:46` | `2.1.5` Estratégia financeira para adaptação e resiliência | inexistente | media | 11.4 |

1. PRIORIDADE PROPOSTA. Inventário georreferenciado do estoque arbóreo com classificação de risco, articulado a plano de substituição e a recorte de áreas críticas. É projeto de dado de risco com escopo definido, custo modesto e efeito direto sobre a ocorrência que mais paralisa a cidade — o candidato mais maduro a projeto financiável surgido no corpus.
2. LACUNA. O plano de arborização histórico definiu o plantio e nunca tratou da substituição do estoque envelhecido. A cidade tem uma política de implantação sem política de manejo — e é o envelhecimento desse estoque, somado ao vento, que produz o risco descrito.
3. Proposta de recuperar o viveiro municipal como ativo de suporte à política de arborização. Investimento de adaptação de baixo custo unitário e efeito prolongado, hoje inexistente na carteira do município — e que responde ao déficit de reposição registrado em ENT-006.

### Afirmação 70, Sociedade Civil

*3.4.1. Política Climática: incorporação, riscos e desafios*

> Desigualdade na Arborização e Gestão Ineficaz: A arborização é desigual, concentrando-se em áreas centrais e sendo precária em bairros periféricos, o que acentua a diferença de temperatura e a sensação térmica. Apesar da existência de um plano de arborização, a efetividade é baixa, com ausência de replantio adequado, falta de fiscalização e negligência na substituição por espécies nativas.

Motivo da recusa: **peso informacional 14.4 < 18.0**

| | Sessão | Marca | Dimensão | Maturidade | Conf. | Peso |
|---|---|---|---|---|---|---:|
| 1 | `ENT-007` | `00:06:56` | `3.2.4` Dados socioeconômicos e territoriais para adaptação inclusiva | inexistente | alta | 14.4 |
| 2 | `ENT-007` | `00:18:28` | `3.2.3` Dados de risco, vulnerabilidade e exposição | inexistente | alta | 11.1 |
| 3 | `ENT-007` | `00:25:03` | `3.2.3` Dados de risco, vulnerabilidade e exposição | em_implementacao | alta | 7.2 |

1. ACHADO DISTRIBUTIVO. A desigualdade territorial se reproduz na infraestrutura verde: a periferia tem menos arborização e menos manutenção. Consequência dupla — menor sombreamento e conforto térmico onde a vulnerabilidade é maior, e concentração do investimento de manutenção onde ela é menor. Dado de exposição que nenhuma base municipal citada no corpus organiza.
2. PRIORIDADE PROPOSTA. Inventário georreferenciado do estoque arbóreo com classificação de risco, articulado a plano de substituição e a recorte de áreas críticas. É projeto de dado de risco com escopo definido, custo modesto e efeito direto sobre a ocorrência que mais paralisa a cidade — o candidato mais maduro a projeto financiável surgido no corpus.
3. O mapeamento de risco existente no plano diretor cobre passivo ambiental grave e não cobre o risco climático cotidiano — queda de árvore, alagamento de rua, ilha de calor. A base de risco disponível está calibrada para a exceção catastrófica, não para o evento recorrente que produz o dano acumulado.

### Afirmação 90, Sociedade Civil

*3.4.5. Soluções Propostas*

> Reforma no IAM: Reforma na gestão do instituto, aumento da fiscalização e revogação do decreto que dispensa estudos de impacto ambiental. A criação de uma central de inteligência de crise, integrando Defesa Civil, Corpo de Bombeiros e lideranças comunitárias, também é defendida.

Motivo da recusa: **peso informacional 14.3 < 18.0**

| | Sessão | Marca | Dimensão | Maturidade | Conf. | Peso |
|---|---|---|---|---|---|---:|
| 1 | `ENT-005` | `00:35:18` | `3.1.1` Sistema municipal de dados climáticos e territoriais | em_elaboracao | media | 27.2 |
| 2 | `ENT-005` | `00:10:02` | `2.1.7` Financiamento para riscos e desastres | em_implementacao | alta | 14.3 |
| 3 | `ENT-007` | `00:06:56` | `1.1.5` Avaliação de riscos e vulnerabilidades climáticas | em_implementacao | alta | 8.4 |

1. OPORTUNIDADE. Há uma proposta em circulação de central integrada de informação de emergência, cruzando município e Estado. Seria o embrião do sistema municipal de dados que o corpus registra como inexistente — e nasce da ponta operacional, não do planejamento.
2. Avaliação positiva da capacidade de resposta imediata a evento extremo, vinda de fora da administração. Qualifica o achado: o município responde bem ao evento e mal à recuperação — que levou mais de uma semana nos dois casos relatados e dependeu de reforço externo.
3. Segunda confirmação, de outra entidade da sociedade civil, do vendaval como risco prioritário, com magnitude: centenas de árvores por evento. A arborização — principal ativo ambiental e identitário da cidade — é também seu maior vetor de dano em evento extremo.

### Afirmação 9, Setor Público

*3.1.2. Finanças: orçamento, financiamento e captação de recursos*

> Capacidade de Endividamento e Financiamentos: O município tem capacidade de endividamento, mas a execução de financiamentos (ex: Banco do Brasil) é prejudicada pela falta de projetos de engenharia prontos ("na gaveta"). Este é apontado como o principal gargalo, levando à perda de prazos e oportunidades em editais.

Motivo da recusa: **peso informacional 14.2 < 18.0**

| | Sessão | Marca | Dimensão | Maturidade | Conf. | Peso |
|---|---|---|---|---|---|---:|
| 1 | `ENT-001-ENT-002` | `00:32:07` | `2.5.2` Histórico de operações de crédito para infraestrutura climática | em_implementacao | alta | 14.2 |
| 2 | `ENT-001-ENT-002` | `00:29:37` | `2.1.4` Capacidade de preparar projetos para financiamento | inexistente | alta | 13.6 |
| 3 | `ENT-001-ENT-002` | `00:27:47` | `2.1.4` Capacidade de preparar projetos para financiamento | inexistente | alta | 10.7 |

1. Há histórico de operação de crédito, mas contratado sem projeto: oito anos de contrato vivo, tarifa anual de renovação e custo de obra corrigido antes da execução. O histórico de crédito, isoladamente, não indica capacidade de investimento.
2. Três perdas documentadas de janela por imaturidade de projeto, uma delas com convênio assinado há três anos e recurso garantido. A capacidade de preparação é a restrição que converte oportunidade em passivo — e é ela, não a disponibilidade de fonte, que determina o que o município consegue executar.
3. Ausência declarada de carteira de projetos. A captação é feita sobre estimativas, não sobre projeto executivo — o que compromete tanto o valor pleiteado quanto o prazo de execução.

### Afirmação 10, Setor Público

*3.1.2. Finanças: orçamento, financiamento e captação de recursos*

> Esforços e Mecanismos de Captação: A prefeitura busca recursos via Transfer GOV, estuda parcerias público-privadas e concessões, e explora recursos internacionais via plataforma Exitos. No entanto, a falta de uma equipe técnica dedicada à captação é um grande limitador. A criação de um "Núcleo de Captação" é defendida como solução.

Motivo da recusa: **peso informacional 14.1 < 18.0**

| | Sessão | Marca | Dimensão | Maturidade | Conf. | Peso |
|---|---|---|---|---|---|---:|
| 1 | `ENT-001-ENT-002` | `00:33:13` | `2.4.2` PPPs/concessões verdes para resíduos, mobilidade e infraestrutura | em_elaboracao | media | 17.6 |
| 2 | `ENT-003` | `00:40:49` | `2.1.4` Capacidade de preparar projetos para financiamento | inexistente | alta | 14.1 |
| 3 | `ENT-001-ENT-002` | `00:48:14` | `2.1.3` Acesso a fundos climáticos internacionais | inexistente | alta | 12.9 |

1. PPPs e concessões estão em exploração inicial, atribuídas a uma pessoa no instituto de planejamento e a uma intenção da liderança. Não há modelagem, PMI ou chamamento em curso — o instrumento está no campo da ideia.
2. LACUNA ESTRUTURAL. Não existe unidade dedicada à estruturação de projetos e captação; a busca de recursos é reativa, personalizada na chefia e oportunista (inscrição em prêmios quando surgem). Dimensão com prioridade «Muito alta» e classificada pelo Produto 2 como ponto crucial da avaliação.
3. Nenhuma captação internacional em dezessete anos, e o único precedente — uma operação com banco multilateral — não deixou capacidade instalada: perdeu-se com a saída da equipe. É a mesma falha de institucionalização observada em ENT-003 na parceria científica: a condição existiu na prática e não sobreviveu à troca de pessoas.

### Afirmação 38, Setor Privado

*3.2.3. Dados, Monitoramento e Planejamento*

> Projetos como Gargalo Central: A fragilidade técnica dos municípios em elaborar projetos é apontada como um gargalo central que impede o desenvolvimento de políticas climáticas eficazes. A falta de projetos bem estruturados inviabiliza a participação em editais e a captação de recursos.

Motivo da recusa: **peso informacional 13.7 < 18.0**

| | Sessão | Marca | Dimensão | Maturidade | Conf. | Peso |
|---|---|---|---|---|---|---:|
| 1 | `ENT-017-ENT-018` | `00:37:15` | `2.6.1` Cofinanciamento com bancos públicos e multilaterais | em_implementacao | alta | 13.7 |
| 2 | `ENT-017-ENT-018` | `00:24:00` | `2.1.4` Capacidade de preparar projetos para financiamento | inexistente | alta | 12.9 |
| 3 | `ENT-009` | `00:14:28` | `1.2.2` Capacidade institucional para executar ações climáticas | inexistente | baixa | 9.6 |

1. ACHADO SOBRE COMPETITIVIDADE. A linha climática subsidiada federal esgota em dias — a disputa é por velocidade e prontidão, não por mérito ambiental. Confirma o argumento central do projeto: quem tem projeto pronto capta; quem começa a elaborar quando o edital abre, não. Dimensão «Muito alta».
2. QUINTA CONFIRMAÇÃO DO ACHADO CENTRAL, AGORA DO FINANCIADOR REGIONAL. A ausência de capacidade de estruturação de projeto é diagnosticada como padrão dos municípios, não como falha de Maringá. Converge com ENT-004, ENT-007, ENT-008 e ENT-010-ENT-011 — e reposiciona a recomendação: montar essa capacidade colocaria Maringá à frente de quase todos os concorrentes pelas mesmas fontes. Dimensão «Muito alta».
3. ALEGAÇÃO DE ESVAZIAMENTO TÉCNICO. Relato de afastamento de servidores de carreira das funções de análise ambiental por decisão política. Registrada como divergência a triangular: diverge da leitura de ENT-008, que atribui a fragilidade da equipe à ausência de priorização orçamentária ao longo de oito anos, não a afastamento deliberado. As duas leituras descrevem a mesma escassez com causas opostas. SESSÃO SEM TCLE.

### Afirmação 53, Academia

*3.3.1. Política Climática: incorporação, riscos e desafios*

> Desafios Estruturais: Os principais desafios são a falta de uma cultura de planejamento preventivo, a desconexão entre ciência e política e a carência de fiscalização (ex: falta de coleta seletiva em grandes condomínios e pontos de coleta de lixo eletrônico desorganizados).

Motivo da recusa: **peso informacional 13.7 < 18.0**

| | Sessão | Marca | Dimensão | Maturidade | Conf. | Peso |
|---|---|---|---|---|---|---:|
| 1 | `ENT-006` | `00:21:09` | `1.2.2` Capacidade institucional para executar ações climáticas | inexistente | alta | 13.7 |
| 2 | `ENT-006` | `00:17:31` | `2.3.1` Mobilização de receitas próprias para clima | regulamentado | alta | 8.3 |
| 3 | `ENT-006` | `00:11:11` | `1.1.5` Avaliação de riscos e vulnerabilidades climáticas | em_implementacao | alta | 5.0 |

1. A capacidade de fiscalização ambiental é insuficiente para induzir cumprimento sem autuação. Relato inclui fauna silvestre de área de proteção adjacente alimentando-se em caçambas de resíduo do condomínio — falha de fiscalização com efeito ecológico direto.
2. Quarta menção espontânea ao IPTU Verde, agora da academia e com detalhamento dos critérios técnicos premiados. O instrumento é reconhecido transversalmente por todos os setores entrevistados — e é o único que ocupa esse lugar no corpus.
3. Risco de alagamento confirmado, e imediatamente associado a uma causa de política pública municipal: a substituição de canteiro gramado por pavimento na implantação de ciclovia. Não é o clima agindo sobre a cidade, é a obra recente ampliando a exposição.

### Afirmação 22, Setor Público

*3.1.4. Governança e Coordenação*

> Sobreposição de Funções: O IAM acaba assumindo funções operacionais que seriam de outras secretarias, especialmente em áreas de preservação permanente, gerando sobrecarga e retrabalho.

Motivo da recusa: **peso informacional 13.5 < 18.0**

| | Sessão | Marca | Dimensão | Maturidade | Conf. | Peso |
|---|---|---|---|---|---|---:|
| 1 | `ENT-008` | `00:37:15` | `1.2.2` Capacidade institucional para executar ações climáticas | inexistente | alta | 13.5 |
| 2 | `ENT-004` | `00:44:26` | `1.2.2` Capacidade institucional para executar ações climáticas | inexistente | alta | 8.0 |
| 3 | `ENT-013` | `00:22:00` | `1.2.2` Capacidade institucional para executar ações climáticas | em_implementacao | alta | 7.0 |

1. Acúmulo de funções regulatórias, operacionais e de planejamento em uma mesma unidade, acrescido do resíduo institucional que nenhuma outra pasta assume. O órgão que deveria formular a política climática é o mesmo que opera parque, licencia e fiscaliza.
2. A sobrecarga por demanda reativa impede a produção de solução técnica para os próprios pontos críticos identificados. É a mesma barreira de capacidade administrativa nomeada em ENT-003 para o IPTU Verde, aqui aplicada ao projeto de drenagem: o limite não é orçamentário nem normativo, é de tempo técnico disponível.
3. Reestruturação administrativa recente do órgão de defesa civil, com introdução de método de mapeamento e de integração de dados. Converge com ENT-012 sobre a recomposição institucional de 2025 e mostra um caso em que ela produziu capacidade nova.

### Afirmação 4, Setor Público

*3.1.1. Política Climática: incorporação, riscos e desafios*

> Alagamentos e Drenagem: A infraestrutura de drenagem existente está sobrecarregada pela impermeabilização do solo e chuvas mais intensas.

Motivo da recusa: **peso informacional 12.9 < 18.0**

| | Sessão | Marca | Dimensão | Maturidade | Conf. | Peso |
|---|---|---|---|---|---|---:|
| 1 | `ENT-015` | `00:24:19` | `2.4.2` PPPs/concessões verdes para resíduos, mobilidade e infraestrutura | em_elaboracao | alta | 12.9 |
| 2 | `ENT-004` | `00:14:14` | `1.1.5` Avaliação de riscos e vulnerabilidades climáticas | em_implementacao | alta | 11.4 |
| 3 | `ENT-001-ENT-002` | `00:17:58` | `1.1.5` Avaliação de riscos e vulnerabilidades climáticas | em_elaboracao | baixa | 9.4 |

1. DESENHO DE INCENTIVO ALINHADO. Flexibilização da exigência de drenagem permitindo solução baseada na natureza que valoriza o empreendimento — o terreno de fundo de vale, historicamente o mais barato, passa a ser o mais valorizado. Alinha interesse privado e redução de risco sem subsídio público, e responde à impermeabilização apontada em ENT-006, ENT-007 e ENT-012.
2. Evidência de campo sobre o risco prioritário: a área operacional constata aumento de intensidade e concentração das chuvas e o efeito sobre a rede de drenagem. Converge com a identificação de alagamento e erosão como riscos prioritários em ENT-003, mas aqui por observação operacional, não por estudo.
3. O risco climático é lido por recorrência de ocorrência — vento, chuva, queda de árvore, alagamento — e não por avaliação estruturada. O participante remete explicitamente a avaliação técnica às secretarias de infraestrutura e à Defesa Civil, o que limita a confiança desta evidência sobre a existência do instrumento.

### Afirmação 79, Sociedade Civil

*3.4.3. Dados, Monitoramento e Planejamento*

> Foco em Urgências, não em Planejamento: Os dados disponíveis focam em emergências e urgências, e não no planejamento estratégico. Isso dificulta a tomada de decisão informada e a elaboração de projetos estruturados.

Motivo da recusa: **peso informacional 12.3 < 18.0**

| | Sessão | Marca | Dimensão | Maturidade | Conf. | Peso |
|---|---|---|---|---|---|---:|
| 1 | `ENT-010-ENT-011` | `00:34:47` | `2.1.4` Capacidade de preparar projetos para financiamento | inexistente | alta | 12.3 |
| 2 | `ENT-005` | `00:35:18` | `3.1.1` Sistema municipal de dados climáticos e territoriais | em_elaboracao | media | 4.4 |
| 3 | `ENT-007` | `00:18:28` | `3.2.3` Dados de risco, vulnerabilidade e exposição | inexistente | alta | 4.4 |

1. QUARTA CONFIRMAÇÃO DO ACHADO CENTRAL. Consultoria especializada em financiamento climático identifica a ausência de projetos estruturados como barreira número um, com oferta de fundos disponível. Converge com ENT-004, ENT-007 e ENT-008 — quatro fontes independentes, de quatro setores, apontando o mesmo gargalo. Dimensão «Muito alta».
2. OPORTUNIDADE. Há uma proposta em circulação de central integrada de informação de emergência, cruzando município e Estado. Seria o embrião do sistema municipal de dados que o corpus registra como inexistente — e nasce da ponta operacional, não do planejamento.
3. PRIORIDADE PROPOSTA. Inventário georreferenciado do estoque arbóreo com classificação de risco, articulado a plano de substituição e a recorte de áreas críticas. É projeto de dado de risco com escopo definido, custo modesto e efeito direto sobre a ocorrência que mais paralisa a cidade — o candidato mais maduro a projeto financiável surgido no corpus.

### Afirmação 27, Setor Público

*3.1.5. Ações e Soluções Propostas*

> Conscientização: Necessidade de campanhas de comunicação com linguagem acessível para engajar a população e o setor privado.

Motivo da recusa: **peso informacional 12.3 < 18.0**

| | Sessão | Marca | Dimensão | Maturidade | Conf. | Peso |
|---|---|---|---|---|---|---:|
| 1 | `ENT-013` | `00:42:25` | `4.2.4` Transparência e devolutiva das contribuições | em_implementacao | alta | 12.3 |
| 2 | `ENT-003` | `00:46:28` | `4.2.1` Participação pública na agenda climática | em_implementacao | media | 10.6 |
| 3 | `ENT-001-ENT-002` | `00:26:51` | `4.2.2` Engajamento do setor privado | inexistente | media | 4.8 |

1. DIVERGÊNCIA. Avaliação positiva da comunicação municipal, inclusive climática, com prática própria de vídeos de linguagem acessível. Diverge de ENT-008, que declara não ter pessoa para comunicar e considerar a comunicação central insuficiente. As duas podem ser verdadeiras: a comunicação de emergência funciona, a comunicação da política ambiental não. Divergência preservada.
2. A participação social é lida como pré-condição de viabilidade dos instrumentos econômicos, não como etapa formal de processo. Convergente com a dimensão transversal de percepção social prevista no Produto 2.
3. O mercado local de execução ainda não está formado para obra de baixo carbono. A restrição está do lado da oferta, não só da demanda pública — o que significa que exigir critério verde em licitação, isoladamente, pode esvaziar certames.

### Afirmação 30, Setor Privado

*3.2.1. Política Climática: incorporação, riscos e desafios*

> Falta de Preparo Preventivo: A prefeitura é vista como reativa, sem preparo preventivo para lidar com eventos climáticos, mesmo diante de alertas meteorológicos. A "celeridade" é um ponto central da crítica: o poder público é lento para agir, o que agrava os riscos econômicos e sociais.

Motivo da recusa: **peso informacional 12.2 < 18.0**

| | Sessão | Marca | Dimensão | Maturidade | Conf. | Peso |
|---|---|---|---|---|---|---:|
| 1 | `ENT-017-ENT-018` | `00:34:44` | `4.1.1` Coordenação com Governo do Paraná/SEDEST | inexistente | alta | 12.2 |
| 2 | `ENT-009` | `00:17:06` | `1.1.5` Avaliação de riscos e vulnerabilidades climáticas | inexistente | alta | 12.2 |
| 3 | `ENT-017-ENT-018` | `00:29:23` | `2.6.2` Blended finance para projetos climáticos | efetivo | alta | 9.5 |

1. Recomendação de indução estadual da agenda climática municipal. Converge com a estratégia de ENT-015 de buscar regulamentação federal para a taxa de drenagem — em ambos os casos, o ente superior é acionado para destravar o que não avança localmente. Dimensão «Muito alta».
2. Segunda confirmação independente do desabastecimento por alagamento da captação (a primeira é ENT-005), com a mesma proposta de redundância entre bacias. Duas fontes de setores diferentes descrevendo o mesmo evento e a mesma solução — a convergência mais específica do corpus sobre infraestrutura crítica. SESSÃO SEM TCLE.
3. FONTE CONCRETA, REGIONAL E NÃO CITADA POR NENHUMA OUTRA SESSÃO. Banco público dos estados do Sul destina 1,5% do lucro líquido a fundo verde com editais abertos. É financiamento não reembolsável de origem regional, acessível a município e a sociedade civil — e responde à crítica de ENT-008 sobre editais nacionais de escopo piloto, por ser mais próximo e mais dirigido.

### Afirmação 75, Sociedade Civil

*3.4.2. Finanças: orçamento, financiamento e captação de recursos*

> Falta de Pessoal e Capacidade Administrativa: A falta de pessoal qualificado e de capacidade administrativa nas secretarias municipais impede que a prefeitura dê continuidade aos projetos, independentemente da disponibilidade de recursos.

Motivo da recusa: **peso informacional 12.2 < 18.0**

| | Sessão | Marca | Dimensão | Maturidade | Conf. | Peso |
|---|---|---|---|---|---|---:|
| 1 | `ENT-005` | `00:31:57` | `1.2.2` Capacidade institucional para executar ações climáticas | inexistente | alta | 12.2 |
| 2 | `ENT-007` | `00:46:36` | `2.1.4` Capacidade de preparar projetos para financiamento | inexistente | alta | 7.9 |
| 3 | `ENT-014` | `00:08:22` | `1.2.2` Capacidade institucional para executar ações climáticas | inexistente | alta | 7.9 |

1. A ausência de capacidade administrativa impede o município de usar um instrumento que já está à sua disposição — o concurso de projeto. Terceira aparição do mesmo padrão no corpus (IPTU Verde em ENT-003, projeto de drenagem em ENT-004): o gargalo não é o instrumento, é o braço para operá-lo.
2. ACHADO ESTRUTURANTE, TERCEIRA CONFIRMAÇÃO. A restrição declarada não é de receita, é de capacidade de executar. Converge com ENT-004 («não temos a ideia pronta») e com ENT-003 (IPTU Verde suspenso por capacidade administrativa), agora dito por quem observa o orçamento de fora. Reorienta o objeto do plano de ação: capacidade de estruturação e execução antes de captação de recurso novo.
3. ACHADO. A supressão arbórea é induzida por pedido de morador amedrontado pelo risco de queda, e deferida sem contrapartida de replantio nem mediação técnica. O risco climático está produzindo, por via administrativa, a perda do ativo que reduz esse mesmo risco. SESSÃO SEM TCLE.


## 4. Peso baixo (abaixo de 12)

Pouca sobreposição de vocabulário específico. A hipótese mais provável é que o corpus realmente não sustente a afirmação, e confirmar isso é resultado do diagnóstico, não trabalho perdido.

### Afirmação 11, Setor Público

*3.1.2. Finanças: orçamento, financiamento e captação de recursos*

> Incentivos Fiscais: O "IPTU Verde" existe, mas é pouco divulgado, restrito a residências e passa por reestruturação. Sugere-se a criação de um "IPTU Verde Empresarial" como ferramenta de financiamento.

Motivo da recusa: **peso informacional 11.7 < 18.0**

| | Sessão | Marca | Dimensão | Maturidade | Conf. | Peso |
|---|---|---|---|---|---|---:|
| 1 | `ENT-012` | `00:44:36` | `2.4.1` Mobilização de investimento privado em infraestrutura climática | inexistente | alta | 11.7 |
| 2 | `ENT-015` | `00:18:24` | `2.4.1` Mobilização de investimento privado em infraestrutura climática | regulamentado | alta | 9.3 |
| 3 | `ENT-001-ENT-002` | `00:33:13` | `2.3.1` Mobilização de receitas próprias para clima | regulamentado | alta | 5.6 |

1. ACHADO ESTRUTURANTE. Desenho de instrumento que converte renúncia futura de IPTU em investimento privado antecipado em infraestrutura climática, capturando o diferencial de custo de execução privada. É financiamento antecipado com contrapartida em obra — e responde diretamente à crítica que o próprio participante faz ao IPTU Verde atual. Converge com a proposta de compensação por intervenção de ENT-004 e merece exame jurídico-fiscal no Roadmap. SESSÃO SEM TCLE.
2. ACHADO ESTRUTURANTE, JÁ EM VIGOR. Conversão de outorga onerosa em obra climática executada pelo empreendedor, com parte da legislação já aprovada. Responde exatamente à proposta espontânea de ENT-004 («receber intervenções em vez de dinheiro») e ao IPTU Verde empresarial de ENT-012 — três formulações independentes do mesmo mecanismo, e esta já é lei. É a condição habilitante mais avançada identificada em Maringá.
3. Divergência com ENT-003, que descreve o IPTU Verde como regulamentado, com fila de pedidos e proposta de ampliação pronta. O conflito não é sobre a existência do instrumento, e sim sobre seu alcance: um servidor da administração central, que lida diariamente com captação, não sabe como ele funciona. O instrumento de receita própria mais relevante da agenda climática municipal não circula fora do órgão ambiental — o que qualifica a barreira administrativa relatada em ENT-003 como sendo também de difusão interna.

### Afirmação 94, Sociedade Civil

*3.4.5. Soluções Propostas*

> Participação Popular: Defender o uso do orçamento participativo e de canais eficientes de comunicação para envolver a população nas decisões públicas, especialmente em investimentos onerosos, como o rebaixamento da fiação elétrica.

Motivo da recusa: **peso informacional 11.7 < 18.0**

| | Sessão | Marca | Dimensão | Maturidade | Conf. | Peso |
|---|---|---|---|---|---|---:|
| 1 | `ENT-007` | `00:26:17` | `4.2.1` Participação pública na agenda climática | inexistente | alta | 11.7 |
| 2 | `ENT-005` | `00:41:22` | `4.2.1` Participação pública na agenda climática | em_implementacao | alta | 9.8 |
| 3 | `ENT-005` | `00:36:14` | `3.2.4` Dados socioeconômicos e territoriais para adaptação inclusiva | em_elaboracao | alta | 9.2 |

1. ACHADO ESTRUTURAL. O capital associativo de Maringá — celebrado em ENT-005 — é de base empresarial, e não há contraparte popular organizada equivalente. Explica por que a participação nos canais formais é assimétrica e por que a agenda climática de recorte distributivo não encontra sujeito que a sustente.
2. Diagnóstico da participação: os canais formais são ocupados por interesse setorial concentrado, e o interesse difuso não comparece. Explica por que a agenda climática — de benefício difuso e custo concentrado — perde nas audiências mesmo com apoio majoritário fora delas.
3. O conhecimento territorial fino sobre causas locais de alagamento existe na população e já foi manifestado em audiência pública. É dado de vulnerabilidade disponível e não sistematizado — e liga diretamente resíduo sólido a obstrução de drenagem, nexo que nenhuma base municipal citada registra.

### Afirmação 41, Setor Privado

*3.2.4. Governança e Coordenação*

> Conflitos na Relação Público-Privada: A ampliação das matas ciliares de 30 para 60 metros, sem a devida desapropriação, é um exemplo de conflito. Os proprietários dessas áreas arcam com obrigações (limpeza, IPTU) sem poder utilizá-las economicamente, gerando insatisfação. Os entrevistados defendem modelos de interação comunitária, em contraste com a abordagem punitiva atual.

Motivo da recusa: **peso informacional 11.2 < 18.0**

| | Sessão | Marca | Dimensão | Maturidade | Conf. | Peso |
|---|---|---|---|---|---|---:|
| 1 | `ENT-016` | `00:24:18` | `2.4.1` Mobilização de investimento privado em infraestrutura climática | inexistente | alta | 11.2 |
| 2 | `ENT-009` | `00:49:01` | `2.4.1` Mobilização de investimento privado em infraestrutura climática | em_implementacao | baixa | 11.2 |
| 3 | `ENT-016` | `00:21:33` | `2.3.3` Diversificação de receitas ambientais/climáticas | inexistente | alta | 9.4 |

1. Avaliação categórica do setor privado organizado: a relação com a agenda ambiental municipal é exclusivamente punitiva. Contrasta com ENT-015, que descreve consciência privada elevada e legislação de compensação já aprovada — as duas leituras convivem se os instrumentos novos ainda não chegaram a quem os percebe. Divergência a resolver com a cronologia das leis. SESSÃO SEM TCLE.
2. DIVERGÊNCIA SOBRE PRIORIDADE DE INVESTIMENTO. Alegação de aporte público expressivo em desapropriação e infraestrutura viária para atrair empreendimento intensivo em água, em cidade cuja captação é de ponto único. Registra o conflito entre política de atração econômica e agenda hídrica — e a ordem de grandeza citada supera em muito qualquer valor de investimento climático mencionado no corpus. Verificar na Matriz 2. SESSÃO SEM TCLE.
3. ACHADO ESTRUTURANTE. Transferência de potencial construtivo e isenção fiscal condicionadas à conservação de área ambiental privada, com prazo. Converte passivo em ativo, substitui fiscalização por incentivo e não exige desembolso do município. Converge com a outorga onerosa já regulamentada em ENT-015 e com o IPTU Verde empresarial de ENT-012 — três desenhos convergentes de compensação por conservação. SESSÃO SEM TCLE.

### Afirmação 24, Setor Público

*3.1.5. Ações e Soluções Propostas*

> Obras Estruturantes: Foco em obras de drenagem, desobstrução de canais e soluções de engenharia verde.

Motivo da recusa: **peso informacional 11.2 < 18.0**

| | Sessão | Marca | Dimensão | Maturidade | Conf. | Peso |
|---|---|---|---|---|---|---:|
| 1 | `ENT-001-ENT-002` | `00:15:36` | `3.1.1` Sistema municipal de dados climáticos e territoriais | em_implementacao | media | 13.6 |
| 2 | `ENT-001-ENT-002` | `00:26:51` | `2.1.6` Estratégia financeira para mitigação e baixo carbono | em_elaboracao | alta | 11.2 |
| 3 | `ENT-001-ENT-002` | `00:35:20` | `1.2.1` Responsabilidades institucionais para implementação climática | em_implementacao | alta | 5.9 |

1. O único sistema de dados citado nesta sessão é o de reporte à Defesa Civil, alimentado com regularidade. É reporte a sistema externo, não sistema municipal de dados territoriais — a base própria segue sem menção.
2. Critérios construtivos de baixo carbono começam a entrar nas obras novas por decisão de projeto, não por norma. O limite declarado é de capacidade técnica interna: a equipe de engenharia ainda está aprendendo a especificar.
3. As responsabilidades setoriais são claras e prontamente identificadas por um servidor de área-meio — o que indica desenho institucional legível. O que não existe é competência climática transversal: cada órgão responde por um fragmento e nenhum responde pelo conjunto.

### Afirmação 91, Sociedade Civil

*3.4.5. Soluções Propostas*

> Educação Ambiental e Comunicação: Implementação da educação ambiental como disciplina obrigatória e comunicação estratégica que alerte a população sobre os riscos reais de desastres, em vez de uma comunicação amenizada.

Motivo da recusa: **peso informacional 10.3 < 18.0**

| | Sessão | Marca | Dimensão | Maturidade | Conf. | Peso |
|---|---|---|---|---|---|---:|
| 1 | `ENT-005` | `00:10:02` | `2.1.7` Financiamento para riscos e desastres | em_implementacao | alta | 10.3 |
| 2 | `ENT-005` | `00:06:29` | `2.1.7` Financiamento para riscos e desastres | inexistente | alta | 10.3 |
| 3 | `ENT-007` | `00:06:56` | `1.1.5` Avaliação de riscos e vulnerabilidades climáticas | em_implementacao | alta | 5.8 |

1. Avaliação positiva da capacidade de resposta imediata a evento extremo, vinda de fora da administração. Qualifica o achado: o município responde bem ao evento e mal à recuperação — que levou mais de uma semana nos dois casos relatados e dependeu de reforço externo.
2. A recuperação pós-evento depende de mobilização de equipes de fora do município. Não há capacidade instalada nem contrato de prontidão dimensionado para o evento extremo — o que converge com a realocação de equipes descrita em ENT-004.
3. Segunda confirmação, de outra entidade da sociedade civil, do vendaval como risco prioritário, com magnitude: centenas de árvores por evento. A arborização — principal ativo ambiental e identitário da cidade — é também seu maior vetor de dano em evento extremo.

### Afirmação 56, Academia

*3.3.2. Finanças: orçamento, financiamento e captação de recursos*

> Priorização de Recursos e Interesses Econômicos: Há a percepção de que a agenda ambiental (e, por extensão, a climática) é submetida a interesses econômicos, sendo secundária na alocação de recursos. A agenda climática fica atrás da agenda ambiental, que por sua vez cede espaço a interesses do mercado imobiliário, que pressiona por alterações nas leis de zoneamento.

Motivo da recusa: **peso informacional 10.1 < 18.0**

| | Sessão | Marca | Dimensão | Maturidade | Conf. | Peso |
|---|---|---|---|---|---|---:|
| 1 | `ENT-006` | `00:19:57` | `2.4.1` Mobilização de investimento privado em infraestrutura climática | inexistente | alta | 10.1 |
| 2 | `ENT-006` | `00:40:06` | `1.1.8` Revisão periódica da política climática | regulamentado | media | 10.1 |
| 3 | `ENT-020` | `00:06:45` | `1.1.6` Alinhamento da adaptação com políticas nacionais/estaduais | inexistente | alta | 8.7 |

1. OPORTUNIDADE. Usar o mercado imobiliário como canal de difusão do IPTU Verde, alinhando o interesse comercial do corretor ao do instrumento. Custo público próximo de zero e resposta direta à lacuna de alcance informacional registrada em ENT-004.
2. DIVERGÊNCIA PROSPECTIVA. Instrumento urbanístico que protege área verde central está sob pressão do mercado imobiliário, com expectativa declarada de revogação. A revisão da política pode se dar em sentido contrário ao da adaptação — risco de retrocesso regulatório que nenhum instrumento municipal monitora.
3. ACHADO DEFINITIVO. O plano diretor vigente, aprovado há menos de dois anos, foi calibrado com série climática antiga e não incorpora a variável climática. É a evidência mais forte do corpus sobre desalinhamento do instrumento urbanístico central com a agenda climática — e explica, na origem, a maladaptação documentada em ENT-006, a pressão sobre áreas verdes de ENT-007 e o subdimensionamento da drenagem apontado por todos.

### Afirmação 17, Setor Público

*3.1.3. Dados, Monitoramento e Planejamento*

> Desenvolvimento de Sistema: A AMTECH está criando um sistema para organizar informações de áreas de risco, Defesa Civil e vulnerabilidade social.

Motivo da recusa: **peso informacional 10.1 < 18.0**

| | Sessão | Marca | Dimensão | Maturidade | Conf. | Peso |
|---|---|---|---|---|---|---:|
| 1 | `ENT-013` | `00:45:24` | `1.2.1` Responsabilidades institucionais para implementação climática | inexistente | media | 13.4 |
| 2 | `ENT-013` | `00:18:55` | `3.1.2` Compartilhamento de dados com Estado/União | em_implementacao | alta | 10.1 |
| 3 | `ENT-001-ENT-002` | `00:17:58` | `1.1.5` Avaliação de riscos e vulnerabilidades climáticas | em_elaboracao | baixa | 9.9 |

1. O órgão de defesa civil se coloca como titular natural do sistema municipal de dados de risco, com o argumento de já agregar informação das demais pastas. Registra uma candidatura concreta à titularidade — questão que a criação de qualquer instância de governança de dados terá de resolver.
2. ACHADO. Há sistema estadual em uso pelo município, alimentado com áreas de risco, pontos de atenção e pessoas vulneráveis. É a única base estruturada e compartilhada com outro ente identificada no corpus — e ela existe fora do município, o que a torna simultaneamente um ativo e uma dependência.
3. O risco climático é lido por recorrência de ocorrência — vento, chuva, queda de árvore, alagamento — e não por avaliação estruturada. O participante remete explicitamente a avaliação técnica às secretarias de infraestrutura e à Defesa Civil, o que limita a confiança desta evidência sobre a existência do instrumento.

### Afirmação 34, Setor Privado

*3.2.2. Finanças: orçamento, financiamento e captação de recursos*

> Críticas ao IPTU Verde e Burocracia: O IPTU Verde é criticado por ser restrito a pessoas físicas (CPFs), excluindo empresas (CNPJs), e por sua burocracia excessiva. Os entrevistados defendem que o poder público abra espaço para um diálogo mais colaborativo e que simplifique os processos para destravar iniciativas privadas.

Motivo da recusa: **peso informacional 10.0 < 18.0**

| | Sessão | Marca | Dimensão | Maturidade | Conf. | Peso |
|---|---|---|---|---|---|---:|
| 1 | `ENT-016` | `00:27:31` | `2.3.1` Mobilização de receitas próprias para clima | regulamentado | alta | 10.0 |
| 2 | `ENT-016` | `00:28:43` | `4.2.3` Participação de conselhos, COMDEMA e sociedade civil | inexistente | alta | 9.5 |
| 3 | `ENT-016` | `00:21:33` | `2.3.3` Diversificação de receitas ambientais/climáticas | inexistente | alta | 8.6 |

1. SEGUNDA CONVERGÊNCIA SOBRE A LACUNA DO INSTRUMENTO. O IPTU Verde não alcança pessoa jurídica e é burocrático — mesmo diagnóstico de ENT-012, agora do lado do contribuinte empresarial. Duas fontes independentes, de setores distintos, apontam a mesma correção no único instrumento econômico-climático da cidade. SESSÃO SEM TCLE.
2. O canal de diálogo entre setor privado organizado e administração ambiental é avaliado como insuficiente. Converge com a carta sem resposta de ENT-007 e as 25 propostas sem desdobramento de ENT-009 — três setores distintos relatando ausência de fluxo institucional de recepção e resposta a proposta externa. SESSÃO SEM TCLE.
3. ACHADO ESTRUTURANTE. Transferência de potencial construtivo e isenção fiscal condicionadas à conservação de área ambiental privada, com prazo. Converte passivo em ativo, substitui fiscalização por incentivo e não exige desembolso do município. Converge com a outorga onerosa já regulamentada em ENT-015 e com o IPTU Verde empresarial de ENT-012 — três desenhos convergentes de compensação por conservação. SESSÃO SEM TCLE.

### Afirmação 92, Sociedade Civil

*3.4.5. Soluções Propostas*

> Uso do Associativismo e Soluções Baseadas na Natureza: Aproveitar a vasta rede de associações para capilarizar políticas urbanas. Implementar jardins de chuva, plantio de árvores como quebra-ventos e renaturalização das cidades.

Motivo da recusa: **peso informacional 10.0 < 18.0**

| | Sessão | Marca | Dimensão | Maturidade | Conf. | Peso |
|---|---|---|---|---|---|---:|
| 1 | `ENT-007` | `00:06:56` | `1.1.5` Avaliação de riscos e vulnerabilidades climáticas | em_implementacao | alta | 10.0 |
| 2 | `ENT-005` | `00:06:29` | `1.1.5` Avaliação de riscos e vulnerabilidades climáticas | em_implementacao | alta | 9.4 |
| 3 | `ENT-005` | `00:11:09` | `1.1.5` Avaliação de riscos e vulnerabilidades climáticas | em_implementacao | alta | 5.5 |

1. Segunda confirmação, de outra entidade da sociedade civil, do vendaval como risco prioritário, com magnitude: centenas de árvores por evento. A arborização — principal ativo ambiental e identitário da cidade — é também seu maior vetor de dano em evento extremo.
2. Risco prioritário identificado da perspectiva da sociedade civil: vendaval, com interrupção prolongada do serviço de energia. Acrescenta ao par erosão/alagamento registrado no bloco público um terceiro vetor — vento — cujo impacto se dá sobre a rede elétrica aérea, ativo que não é municipal.
3. Constatação de que a rede de drenagem projetada há décadas deixou de comportar o regime atual de chuva, com dois fatores somados: mudança do padrão pluviométrico e impermeabilização do solo. Converge com a evidência operacional de ENT-004, aqui a partir de observação técnica externa à prefeitura.

### Afirmação 5, Setor Público

*3.1.1. Política Climática: incorporação, riscos e desafios*

> Erosão: Processos erosivos em fundos de vale e "boçorocas" ameaçam a infraestrutura urbana.

Motivo da recusa: **peso informacional 9.9 < 18.0**

| | Sessão | Marca | Dimensão | Maturidade | Conf. | Peso |
|---|---|---|---|---|---|---:|
| 1 | `ENT-015` | `00:07:34` | `1.1.5` Avaliação de riscos e vulnerabilidades climáticas | em_implementacao | alta | 9.9 |
| 2 | `ENT-008` | `00:22:43` | `1.1.5` Avaliação de riscos e vulnerabilidades climáticas | em_implementacao | alta | 9.4 |
| 3 | `ENT-015` | `00:29:03` | `2.1.3` Acesso a fundos climáticos internacionais | inexistente | alta | 9.1 |

1. Hierarquia oficial de risco em três níveis: vento sobre a arborização, alagamento e erosão em fundo de vale. Converge com todas as demais sessões quanto ao primeiro item — sexta confirmação de que a arborização é a vulnerabilidade central de Maringá.
2. Leitura oficial do perfil de risco: erosão como vetor principal e alagamento pontual e mapeado, sustentados pela ausência de ocupação em fundo de vale e de relevo acidentado. Delimita o risco a partir da estrutura urbana — e será contestado por outras sessões, que registram ocupação irregular de fundo de vale.
3. POSIÇÃO DIVERGENTE DA PREMISSA DO PROJETO. A liderança do Executivo avalia como improvável a captação internacional para infraestrutura urbana no Brasil, por razões de justiça climática e de competição global. Converge com a crítica de ENT-008 aos editais e reorienta o plano de ação: se a leitura estiver correta, o esforço deve concentrar-se em receita própria, crédito interno e recurso privado, não em fundos internacionais. Divergência preservada.

### Afirmação 46, Setor Privado

*3.2.5. Soluções Propostas*

> Diálogo Colaborativo: O poder público precisa abrir espaço para um diálogo mais colaborativo e simplificar seus processos.

Motivo da recusa: **peso informacional 9.5 < 18.0**

| | Sessão | Marca | Dimensão | Maturidade | Conf. | Peso |
|---|---|---|---|---|---|---:|
| 1 | `ENT-016` | `00:28:43` | `4.2.3` Participação de conselhos, COMDEMA e sociedade civil | inexistente | alta | 9.5 |
| 2 | `ENT-009` | `00:31:11` | `4.2.3` Participação de conselhos, COMDEMA e sociedade civil | inexistente | alta | 5.1 |
| 3 | `ENT-017-ENT-018` | `00:34:44` | `4.1.1` Coordenação com Governo do Paraná/SEDEST | inexistente | alta | 5.1 |

1. O canal de diálogo entre setor privado organizado e administração ambiental é avaliado como insuficiente. Converge com a carta sem resposta de ENT-007 e as 25 propostas sem desdobramento de ENT-009 — três setores distintos relatando ausência de fluxo institucional de recepção e resposta a proposta externa. SESSÃO SEM TCLE.
2. SEGUNDA OFERTA TÉCNICA ENTREGUE E SEM DESDOBRAMENTO. Documento com 25 propostas fundamentadas entregue diretamente ao Executivo, sem retorno relatado. Converge exatamente com a carta de ENT-007: a sociedade civil técnica de Maringá produz e entrega proposta ao poder público, e não há fluxo institucional que a receba, avalie e responda. SESSÃO SEM TCLE.
3. Recomendação de indução estadual da agenda climática municipal. Converge com a estratégia de ENT-015 de buscar regulamentação federal para a taxa de drenagem — em ambos os casos, o ente superior é acionado para destravar o que não avança localmente. Dimensão «Muito alta».

### Afirmação 82, Sociedade Civil

*3.4.3. Dados, Monitoramento e Planejamento*

> Monitoramento Contínuo como Necessidade: A sociedade civil defende a importância de transitar de uma postura reativa para uma postura proativa e planejada, com monitoramento constante, reconhecendo a responsabilidade dos profissionais diante dos riscos crescentes.

Motivo da recusa: **peso informacional 9.2 < 18.0**

| | Sessão | Marca | Dimensão | Maturidade | Conf. | Peso |
|---|---|---|---|---|---|---:|
| 1 | `ENT-005` | `00:06:29` | `1.1.5` Avaliação de riscos e vulnerabilidades climáticas | em_implementacao | alta | 9.2 |
| 2 | `ENT-007` | `00:06:56` | `1.1.5` Avaliação de riscos e vulnerabilidades climáticas | em_implementacao | alta | 9.2 |
| 3 | `ENT-005` | `00:10:02` | `2.1.7` Financiamento para riscos e desastres | em_implementacao | alta | 6.4 |

1. Risco prioritário identificado da perspectiva da sociedade civil: vendaval, com interrupção prolongada do serviço de energia. Acrescenta ao par erosão/alagamento registrado no bloco público um terceiro vetor — vento — cujo impacto se dá sobre a rede elétrica aérea, ativo que não é municipal.
2. Segunda confirmação, de outra entidade da sociedade civil, do vendaval como risco prioritário, com magnitude: centenas de árvores por evento. A arborização — principal ativo ambiental e identitário da cidade — é também seu maior vetor de dano em evento extremo.
3. Avaliação positiva da capacidade de resposta imediata a evento extremo, vinda de fora da administração. Qualifica o achado: o município responde bem ao evento e mal à recuperação — que levou mais de uma semana nos dois casos relatados e dependeu de reforço externo.

### Afirmação 19, Setor Público

*3.1.3. Dados, Monitoramento e Planejamento*

> Comunicação dos Dados: A comunicação dos dados é um desafio, pois as informações são frequentemente muito técnicas para o público leigo, dificultando a conscientização e a adesão da população.

Motivo da recusa: **peso informacional 9.0 < 18.0**

| | Sessão | Marca | Dimensão | Maturidade | Conf. | Peso |
|---|---|---|---|---|---|---:|
| 1 | `ENT-003` | `00:46:28` | `4.2.1` Participação pública na agenda climática | em_implementacao | media | 10.6 |
| 2 | `ENT-001-ENT-002` | `00:34:19` | `4.2.1` Participação pública na agenda climática | inexistente | media | 9.1 |
| 3 | `ENT-013` | `00:24:49` | `4.2.3` Participação de conselhos, COMDEMA e sociedade civil | em_elaboracao | alta | 9.0 |

1. A participação social é lida como pré-condição de viabilidade dos instrumentos econômicos, não como etapa formal de processo. Convergente com a dimensão transversal de percepção social prevista no Produto 2.
2. Divulgação e simplificação são apontadas como condição de adesão cidadã a instrumentos climático-fiscais. Dito por quem é, ele próprio, público interno que não conhece o instrumento — o que sugere que a barreira de comunicação começa dentro da prefeitura.
3. PROJETO ESTRUTURANTE, JÁ SUBMETIDO. Rede de núcleos comunitários de defesa civil como canal bidirecional — a comunidade identifica o risco local que o mapeamento não alcança, e recebe o alerta em linguagem própria. Responde de uma vez às lacunas de dado territorial fino (ENT-005, ENT-007) e de comunicação (cinco sessões), e se apoia na densidade associativa que ENT-007 documenta. É a proposta com melhor relação entre custo e alcance no corpus.

### Afirmação 3, Setor Público

*3.1.1. Política Climática: incorporação, riscos e desafios*

> Quedas de árvores e danos à fiação: Devido à alta arborização, que é uma vulnerabilidade democrática, afetando todas as classes sociais.

Motivo da recusa: **peso informacional 8.3 < 18.0**

| | Sessão | Marca | Dimensão | Maturidade | Conf. | Peso |
|---|---|---|---|---|---|---:|
| 1 | `ENT-004` | `00:17:20` | `4.2.1` Participação pública na agenda climática | em_elaboracao | alta | 8.3 |
| 2 | `ENT-013` | `00:17:08` | `4.1.1` Coordenação com Governo do Paraná/SEDEST | em_implementacao | alta | 6.3 |
| 3 | `ENT-013` | `00:18:55` | `3.2.4` Dados socioeconômicos e territoriais para adaptação inclusiva | em_elaboracao | alta | 4.7 |

1. LACUNA COM RECORTE DISTRIBUTIVO. O único instrumento econômico-climático do município tem alcance informacional desigual, e o próprio servidor identifica as classes vulneráveis como as menos informadas. O incentivo tende a ser capturado por quem já tem acesso à informação e capacidade de investir.
2. ACHADO. Existe estrutura permanente de articulação com o Estado por núcleo regional, com acionamento conjunto em calamidade. É a coordenação vertical mais consolidada identificada no corpus — e a única que já opera em base territorial regional. Dimensão «Muito alta».
3. ACHADO DECISIVO. Está em curso o cruzamento entre áreas de risco e cadastro socioassistencial — exatamente o dado de sensibilidade que a consultoria do plano climático (ENT-010-ENT-011) declarou não conseguir obter e estar substituindo por proxy. O dado está sendo construído em uma secretaria e a equipe que elabora o plano de adaptação não sabe disso. É a demonstração mais concreta do custo da falta de governança de dados. Dimensão «Muito alta».

### Afirmação 44, Setor Privado

*3.2.5. Soluções Propostas*

> Inclusão Social nas Políticas: Políticas de descarbonização e arborização devem beneficiar também áreas menos desenvolvidas, não apenas regiões ricas.

Motivo da recusa: **peso informacional 8.2 < 18.0**

| | Sessão | Marca | Dimensão | Maturidade | Conf. | Peso |
|---|---|---|---|---|---|---:|
| 1 | `ENT-017-ENT-018` | `00:14:24` | `3.2.4` Dados socioeconômicos e territoriais para adaptação inclusiva | inexistente | alta | 8.2 |
| 2 | `ENT-009` | `00:05:44` | `1.1.5` Avaliação de riscos e vulnerabilidades climáticas | em_implementacao | alta | 2.4 |
| 3 | `ENT-009` | `00:08:39` | `3.2.4` Dados socioeconômicos e territoriais para adaptação inclusiva | inexistente | alta | 2.4 |

1. Recomendação de equidade territorial vinda do agente financeiro. Converge com ENT-007, ENT-009 e ENT-014 sobre o gradiente centro–periferia da infraestrutura verde — e o fato de vir de quem analisa crédito indica que o recorte distributivo tem peso na avaliação do projeto, não apenas valor normativo.
2. Causa técnica da queda de árvores identificada na escolha de espécies exóticas de enraizamento superficial no projeto paisagístico original. É a explicação estrutural para a convergência de quatro sessões sobre arborização como vulnerabilidade — e implica substituição de estoque, não apenas manejo. SESSÃO SEM TCLE.
3. Segunda confirmação da desigualdade territorial da infraestrutura verde (a primeira é ENT-007), com acréscimo relevante: o loteamento novo nasce sem arborização e a fiscalização não alcança nem o centro nem a periferia. O passivo se amplia a cada novo empreendimento. SESSÃO SEM TCLE.

### Afirmação 73, Sociedade Civil

*3.4.2. Finanças: orçamento, financiamento e captação de recursos*

> Recursos Existem, mas são Mal Aplicados: Há a percepção de que existem recursos financeiros disponíveis (inclusive do governo federal), mas o uso incorreto desses fundos, a corrupção e a falta de vontade política em priorizar pautas ambientais (que não trazem retorno eleitoral imediato) são os principais obstáculos.

Motivo da recusa: **peso informacional 7.6 < 18.0**

| | Sessão | Marca | Dimensão | Maturidade | Conf. | Peso |
|---|---|---|---|---|---|---:|
| 1 | `ENT-010-ENT-011` | `00:11:56` | `1.1.5` Avaliação de riscos e vulnerabilidades climáticas | em_elaboracao | alta | 7.6 |
| 2 | `ENT-010-ENT-011` | `00:21:23` | `3.2.4` Dados socioeconômicos e territoriais para adaptação inclusiva | inexistente | alta | 7.6 |
| 3 | `ENT-007` | `00:49:24` | `4.2.3` Participação de conselhos, COMDEMA e sociedade civil | efetivo | alta | 5.7 |

1. ACHADO QUANTITATIVO. A série histórica de eventos extremos mostra a ventania convergindo em frequência para a trovoada, que era dominante. É a validação estatística do que quatro sessões relataram por percepção — o vento como risco emergente — e o dado que sustenta priorizar arborização e rede elétrica.
2. DIVERGÊNCIA CENTRAL DO CORPUS. A prefeitura informa oficialmente zero ocupações irregulares; ENT-007 relata ocupações em fundo de vale e um movimento organizado desses moradores; ENT-008 nega ocupação em fundo de vale. Se o número oficial for zero por ausência de registro e não por ausência do fenômeno, toda a análise de sensibilidade do plano de adaptação está sendo construída sobre uma lacuna — e a população mais exposta fica fora dela. Divergência preservada para verificação documental.
3. Densidade excepcional de organizações da sociedade civil, com reconhecimento legal. Base de capilaridade disponível para execução territorializada de política — e que hoje não está vinculada à agenda climática.

### Afirmação 35, Setor Privado

*3.2.2. Finanças: orçamento, financiamento e captação de recursos*

> Taxas de Juros e Capacidade Técnica: As principais barreiras para o investimento são a necessidade de taxas de juros subsidiadas, a carência de políticas públicas bem definidas e a falta de capacidade técnica nos municípios para elaborar projetos competitivos.

Motivo da recusa: **peso informacional 7.4 < 18.0**

| | Sessão | Marca | Dimensão | Maturidade | Conf. | Peso |
|---|---|---|---|---|---|---:|
| 1 | `ENT-009` | `00:41:47` | `2.1.4` Capacidade de preparar projetos para financiamento | inexistente | media | 10.6 |
| 2 | `ENT-017-ENT-018` | `00:24:00` | `2.1.4` Capacidade de preparar projetos para financiamento | inexistente | alta | 7.4 |
| 3 | `ENT-016` | `00:35:18` | `1.2.2` Capacidade institucional para executar ações climáticas | inexistente | alta | 6.4 |

1. Duas barreiras alegadas à captação: risco de desvio e ausência de retorno eleitoral do investimento em prevenção. A segunda é estrutural e independe de qualquer juízo sobre a primeira — obra que evita dano não é visível, e por isso perde na disputa orçamentária. SESSÃO SEM TCLE.
2. QUINTA CONFIRMAÇÃO DO ACHADO CENTRAL, AGORA DO FINANCIADOR REGIONAL. A ausência de capacidade de estruturação de projeto é diagnosticada como padrão dos municípios, não como falha de Maringá. Converge com ENT-004, ENT-007, ENT-008 e ENT-010-ENT-011 — e reposiciona a recomendação: montar essa capacidade colocaria Maringá à frente de quase todos os concorrentes pelas mesmas fontes. Dimensão «Muito alta».
3. O setor privado percebe a lentidão sem identificar sua causa. ENT-008 e ENT-012 a fornecem: municipalização recente do licenciamento e equipe insuficiente. A modernização do licenciamento, citada em ENT-008 como um dos quatro projetos da pasta, é a resposta direta a esta reclamação. SESSÃO SEM TCLE.

### Afirmação 45, Setor Privado

*3.2.5. Soluções Propostas*

> Enterramento da Fiação: Deve ser integrado a outras tecnologias urbanas de drenagem para ser efetivo, como já está sendo planejado em Curitiba.

Motivo da recusa: **peso informacional 6.9 < 18.0**

| | Sessão | Marca | Dimensão | Maturidade | Conf. | Peso |
|---|---|---|---|---|---|---:|
| 1 | `ENT-009` | `00:17:06` | `3.2.1` Parcerias com universidades e centros de pesquisa | em_implementacao | media | 7.1 |
| 2 | `ENT-017-ENT-018` | `00:15:41` | `2.4.2` PPPs/concessões verdes para resíduos, mobilidade e infraestrutura | em_elaboracao | alta | 6.9 |
| 3 | `ENT-017-ENT-018` | `00:12:54` | `2.1.5` Estratégia financeira para adaptação e resiliência | em_implementacao | alta | 5.8 |

1. O estudo do poço de infiltração foi produzido pela academia local e validado em campo, e não foi convertido em programa municipal. Mais um caso do padrão registrado em ENT-006: conhecimento local disponível e não integrado à decisão de investimento. SESSÃO SEM TCLE.
2. ACHADO DECISIVO. Existe modelo de PPP em estruturação para enterramento de rede elétrica em município do mesmo estado, com a recomendação técnica de combiná-lo a infraestrutura de drenagem na mesma obra. Responde diretamente à disputa registrada em ENT-005 e à proposta de estudo faseado de ENT-007 — o instrumento financeiro para a medida mais cara do corpus existe e tem precedente regional.
3. Parque como infraestrutura de drenagem, financiável por concessão. Responde diretamente ao alagamento de microdrenagem diagnosticado em ENT-010-ENT-011 e converge com os poços de infiltração de ENT-009 e os jardins de chuva de ENT-006 e ENT-012 — todas soluções baseadas na natureza, e esta com modelo de financiamento associado.

### Afirmação 43, Setor Privado

*3.2.5. Soluções Propostas*

> Adoção de PPPs para viabilizar grandes projetos de infraestrutura verde.

Motivo da recusa: **peso informacional 5.0 < 18.0**

| | Sessão | Marca | Dimensão | Maturidade | Conf. | Peso |
|---|---|---|---|---|---|---:|
| 1 | `ENT-009` | `00:17:06` | `2.4.2` PPPs/concessões verdes para resíduos, mobilidade e infraestrutura | em_implementacao | media | 7.1 |
| 2 | `ENT-009` | `00:08:39` | `3.2.4` Dados socioeconômicos e territoriais para adaptação inclusiva | inexistente | alta | 5.0 |
| 3 | `ENT-009` | `00:41:47` | `2.4.1` Mobilização de investimento privado em infraestrutura climática | inexistente | media | 5.0 |

1. Alegação de descumprimento do plano de saneamento por concessionária com contrato renovado. Contrasta com ENT-008, que registra repasse da mesma concessionária ao fundo ambiental: o contrato de concessão é simultaneamente fonte de recurso ambiental e objeto de inadimplemento alegado. Ponto a verificar documentalmente. SESSÃO SEM TCLE.
2. Segunda confirmação da desigualdade territorial da infraestrutura verde (a primeira é ENT-007), com acréscimo relevante: o loteamento novo nasce sem arborização e a fiscalização não alcança nem o centro nem a periferia. O passivo se amplia a cada novo empreendimento. SESSÃO SEM TCLE.
3. Sugestão de acoplar a exigência ambiental ao vetor de expansão imobiliária que a cidade já tem, em vez de opô-la a ele. Mesma lógica da proposta de ENT-006 (usar o mercado imobiliário como canal do IPTU Verde): trabalhar com o incentivo existente, não contra ele. SESSÃO SEM TCLE.

### Afirmação 67, Academia

*3.3.5. Soluções Propostas*

> Mitigação de Desastres: Investir em soluções baseadas na natureza (SBN), como "jardins de chuva", testando em pontos críticos para posterior replicação.

Motivo da recusa: **peso informacional 2.8 < 18.0**

| | Sessão | Marca | Dimensão | Maturidade | Conf. | Peso |
|---|---|---|---|---|---|---:|
| 1 | `ENT-006` | `00:45:34` | `2.1.7` Financiamento para riscos e desastres | em_implementacao | media | 11.3 |
| 2 | `ENT-006` | `00:11:11` | `1.1.5` Avaliação de riscos e vulnerabilidades climáticas | em_implementacao | alta | 2.8 |
| 3 | `ENT-006` | `00:21:09` | `3.1.1` Sistema municipal de dados climáticos e territoriais | inexistente | alta | 2.8 |

1. Avaliação externa de que a capacidade de resposta a desastre é insuficiente em pessoal. Diverge da leitura de ENT-005, que considera a resposta rápida — a diferença é o objeto: resposta imediata ao evento versus recomposição posterior do dano.
2. Risco de alagamento confirmado, e imediatamente associado a uma causa de política pública municipal: a substituição de canteiro gramado por pavimento na implantação de ciclovia. Não é o clima agindo sobre a cidade, é a obra recente ampliando a exposição.
3. DIVERGÊNCIA VERIFICADA EM CAMPO. A informação publicada pelo município sobre pontos de destinação de resíduo eletrônico não corresponde à realidade, constatado por tentativa direta da participante. O dado público existe e está errado — o que é pior que ausência de dado para qualquer decisão que dele dependa.

### Afirmação 6, Setor Público

*3.1.1. Política Climática: incorporação, riscos e desafios*

> Abastecimento de Água: O Rio Pirapó é vulnerável a secas e inundações que afetam a captação de água.

Motivo da recusa: **peso informacional 2.4 < 18.0**

| | Sessão | Marca | Dimensão | Maturidade | Conf. | Peso |
|---|---|---|---|---|---|---:|
| 1 | `ENT-001-ENT-002` | `00:15:36` | `2.1.2` Fontes estaduais/federais para ação climática urbana | em_implementacao | alta | 2.4 |
| 2 | `ENT-001-ENT-002` | `00:48:14` | `2.1.3` Acesso a fundos climáticos internacionais | inexistente | alta | 2.4 |
| 3 | `ENT-001-ENT-002` | `00:27:47` | `2.1.4` Capacidade de preparar projetos para financiamento | inexistente | alta | 2.4 |

1. Monitoramento ativo e rotinizado de fontes federais, com filtro temático ambiental já incorporado à rotina de captação. É a condição habilitante mais consolidada que a entrevista revela — e ela é de processo, não de política.
2. Nenhuma captação internacional em dezessete anos, e o único precedente — uma operação com banco multilateral — não deixou capacidade instalada: perdeu-se com a saída da equipe. É a mesma falha de institucionalização observada em ENT-003 na parceria científica: a condição existiu na prática e não sobreviveu à troca de pessoas.
3. Ausência declarada de carteira de projetos. A captação é feita sobre estimativas, não sobre projeto executivo — o que compromete tanto o valor pleiteado quanto o prazo de execução.


## 5. Chamada de lista

Não afirmam nada: anunciam a lista que vem a seguir. Só confirmar que não devem receber âncora.

### Afirmação 48, Academia

*3.3.1. Política Climática: incorporação, riscos e desafios*

> Riscos e Vulnerabilidades Ignorados: Os acadêmicos apontam riscos já conhecidos, como:

Motivo da recusa: **chamada de lista**

| | Sessão | Marca | Dimensão | Maturidade | Conf. | Peso |
|---|---|---|---|---|---|---:|
| 1 | `ENT-019` | `00:04:20` | `1.1.5` Avaliação de riscos e vulnerabilidades climáticas | em_implementacao | alta | 13.9 |
| 2 | `ENT-006` | `00:11:11` | `1.1.5` Avaliação de riscos e vulnerabilidades climáticas | em_implementacao | alta | 9.6 |
| 3 | `ENT-006` | `00:12:51` | `1.1.5` Avaliação de riscos e vulnerabilidades climáticas | em_implementacao | alta | 9.6 |

1. Oitava confirmação do par arborização envelhecida–tempestade severa como risco principal. O corpus inteiro converge nesse ponto: nove das dezessete sessões o apontam, em quatro setores.
2. Risco de alagamento confirmado, e imediatamente associado a uma causa de política pública municipal: a substituição de canteiro gramado por pavimento na implantação de ciclovia. Não é o clima agindo sobre a cidade, é a obra recente ampliando a exposição.
3. DIVERGÊNCIA. Uma intervenção de mobilidade sustentável foi executada em ponto com histórico conhecido de alagamento, impermeabilizando-o ainda mais. A ação climática de um setor agrava o risco climático de outro — caso concreto de maladaptação por falta de coordenação, e o único do corpus com localização precisa.

### Afirmação 14, Setor Público

*3.1.3. Dados, Monitoramento e Planejamento*

> Esforços em Andamento: A prefeitura está realizando investimentos significativos para superar essa lacuna, incluindo:

Motivo da recusa: **chamada de lista**

| | Sessão | Marca | Dimensão | Maturidade | Conf. | Peso |
|---|---|---|---|---|---|---:|
| 1 | `ENT-001-ENT-002` | `00:43:26` | `2.3.4` Sustentabilidade fiscal para investimentos climáticos recorrentes | inexistente | alta | 9.2 |
| 2 | `ENT-013` | `00:22:00` | `3.1.1` Sistema municipal de dados climáticos e territoriais | em_elaboracao | alta | 8.9 |
| 3 | `ENT-001-ENT-002` | `00:47:13` | `2.1.5` Estratégia financeira para adaptação e resiliência | em_elaboracao | alta | 4.1 |

1. Caso extremo do mecanismo anterior: uma contrapartida que era zero chegou a treze milhões por decurso de prazo. Quantifica o custo fiscal da imaturidade de projeto e mostra que ele não é hipotético nem marginal.
2. LACUNA CONFIRMADA, COM TRABALHO EM ANDAMENTO. Não existe base compartilhada de áreas de risco na prefeitura, e há desenvolvimento em curso com a área de tecnologia. Converge com ENT-004, ENT-008 e ENT-010-ENT-011 — e mostra que a construção começou. Dimensão «Muito alta».
3. Não existe unidade de captação: a função está sendo montada informalmente dentro da secretaria de governo, apoiada em uma pessoa com dois meses de casa. Converge com ENT-003, que registrou a mesma ausência a partir do órgão ambiental — a lacuna é da estrutura, não de um órgão.
