# -*- coding: utf-8 -*-
"""Conteúdo das páginas do Hub."""
import html
from base import legenda, empilhada
import graficos as G
# `barras` vem de graficos: mesma assinatura de base.barras mais `total`,
# que acrescenta a fracao ao rotulo — e o alivio de contraste que a
# validacao da paleta exige no modo claro.
from graficos import barras

S = ["var(--s1)", "var(--s2)", "var(--s3)", "var(--s4)"]
GRUPOS = ["Público", "Privado", "Academia", "Sociedade Civil"]
E = html.escape



# Rotulos legiveis das chaves do codebook. Ordem fixa, da maior contagem para a
# menor dentro de cada grupo — a ordem e do dado, o rotulo e so traducao.
_TIPO = {"declaracao": "Declaração", "lacuna": "Lacuna", "percepcao": "Percepção",
         "oportunidade": "Oportunidade", "divergencia": "Divergência",
         "documento_indicado": "Documento indicado"}
_ALINH = {"convergente": "Convergente", "complementar": "Complementar",
          "isolada": "Isolada", "divergente": "Divergente",
          "": "Sem alinhamento registrado"}
_CONF = {"alta": "Alta", "media": "Média", "baixa": "Baixa"}


def _ordena(d, rotulos):
    return [(rotulos.get(k, k or "sem registro"), v)
            for k, v in sorted(d.items(), key=lambda kv: -kv[1])]


def TIPOS_ORD(m):
    return _ordena(m["tipos"], _TIPO)


def ALINH_ORD(m):
    return _ordena(m["alinhamento"], _ALINH)


def CONF_ORD(m):
    return _ordena(m["confianca"], _CONF)


# ===================================================================== INÍCIO
def inicio(m, c, orgs, leis):
    inex = dict(m["maturidade"])["Inexistente"]
    pct = round(100 * inex / m["evidencias"])
    ESTAGIOS = sum(v for _, v in m["maturidade"])
    MUDAS = ", ".join('<span class="mono">' + E(d) + "</span>" for d in m["mudas"])
    cards = [
        ("produto4.html", "Produto 04: o relatório",
         f"O relatório de síntese das consultas, em versão web navegável, com a "
         f"Matriz de Avaliação e cada afirmação da Seção 3 ligada à evidência que "
         f"a sustenta, ou marcada como sem âncora."),
        ("painel.html", "Painel de evidências",
         f"As {m['evidencias']} evidências codificadas, cada uma vinculada a uma das "
         f"{m['dimensoes_total']} dimensões, com trecho anonimizado, marca de tempo, "
         "maturidade e alinhamento. Cobertura, lacunas e divergências."),
        ("conselhos.html", "Conselhos",
         f"Os {len(c['membros'])} conselheiros do COMDEMA entre {c['anos'][0]} e "
         f"{c['anos'][-1]}, com a análise de continuidade: quem permanece, por qual "
         "vínculo, e o que a rotatividade faz com a memória institucional."),
        ("instituicoes.html", "Instituições",
         f"As {len(orgs)} organizações mapeadas no Produto 3, classificadas pelas quatro "
         "dimensões analíticas da metodologia, com esfera, natureza e justificativa."),
        ("legislacao.html", "Legislação",
         f"As {len(leis)} normas municipais que formam o arcabouço climático de Maringá "
         "Que cada uma institui, e onde estão as lacunas de regulamentação."),
        ("transcricoes.html", "Transcrições",
         f"As {m['sessoes']} entrevistas na íntegra, em camada anonimizada, com as marcas "
         "de tempo que ancoram as evidências."),
    ]
    grade = "".join(
        f'<a class="card" href="{h}"><h3>{t}</h3><p class="sm mut">{d}</p>'
        f'<p class="sm seta">Abrir &rarr;</p></a>' for h, t, d in cards)

    return f"""
<h2>Explorar</h2>
<div class="grade g2">{grade}</div>

<h2>O que foi registrado</h2>

<div class="destaque">
  <p class="n">{pct}%</p>
  <p>Das {m['evidencias']} evidências codificadas, <strong>{inex}</strong>
  classificam a condição avaliada como <em>inexistente</em>,
  {dict(m['maturidade'])['Efetivo']} como <em>efetiva</em> e
  {dict(m['maturidade'])['Monitorado']} como <em>monitorada</em>.</p>
</div>

{G.figura(
  "Maturidade registrada, evidência a evidência",
  barras(m["maturidade_completa"], "var(--s1)", total=m["evidencias"]),
  f"As {m['evidencias']} evidências pela situação que registram. A escala de estágios "
  f"vai de <em>inexistente</em> a <em>efetivo</em> e soma {ESTAGIOS}; as "
  f"{m['evidencias'] - ESTAGIOS} restantes estão fora da escala: "
  f"<em>sem evidência</em> marca pendência de reinquirição, não ausência constatada, "
  f"e é registrada à parte justamente para não ser lida como <em>inexistente</em>. "
  f"Os extremos da escala concentram {inex} e "
  f"{dict(m['maturidade'])['Efetivo']} registros.",
  G.tabela(["Maturidade", "Evidências"], m["maturidade_completa"]))}

{G.figura(
  "Tipo de registro",
  barras(TIPOS_ORD(m), "var(--s3)", total=m["evidencias"]),
  "Cada evidência é classificada por tipo no momento da codificação. "
  "<em>Lacuna</em> marca a ausência declarada de um instrumento; "
  "<em>divergência</em>, a discordância entre fontes sobre o mesmo ponto.",
  G.tabela(["Tipo", "Evidências"], TIPOS_ORD(m)))}

{G.figura(
  "Alinhamento entre fontes",
  barras(ALINH_ORD(m), "var(--s4)", total=m["evidencias"]),
  "<em>Convergente</em>: outra sessão diz o mesmo. <em>Complementar</em>: acrescenta "
  "sem contradizer. <em>Isolada</em>: nenhuma outra sessão toca o ponto. "
  "<em>Divergente</em>: outra sessão diz o contrário. Essas são preservadas, não "
  "resolvidas. Duas evidências não têm alinhamento registrado: ambas são "
  "<em>sem evidência</em>, categoria que não tem com o que se alinhar.",
  G.tabela(["Alinhamento", "Evidências"], ALINH_ORD(m)))}

{G.figura(
  "Confiança atribuída na codificação",
  barras(CONF_ORD(m), "var(--s2)", total=m["evidencias"]),
  "Confiança baixa é marcada quando o participante remete a outro órgão, quando a "
  "formulação partiu do entrevistador e foi apenas confirmada, ou quando o trecho é "
  "ambíguo.",
  G.tabela(["Confiança", "Evidências"], CONF_ORD(m)))}

<h2>Cobertura das {m['dimensoes_total']} dimensões</h2>

{G.figura(
  "Dimensões com e sem evidência, por prioridade",
  G.pares(m["cobertura_prioridade"], ("com evidência", "sem evidência"),
          ("var(--s1)", "var(--grid)")) + legenda(
          [("com evidência oral", "var(--s1)"), ("sem evidência oral", "var(--grid)")]),
  f"{m['dimensoes_com_evidencia']} das {m['dimensoes_total']} dimensões receberam ao "
  f"menos uma evidência; {m['trianguladas']} receberam evidência de duas ou mais "
  f"sessões. As {len(m['mudas'])} sem evidência oral são {MUDAS}.",
  G.tabela(["Prioridade", "Com evidência", "Sem evidência"],
           m["cobertura_prioridade"]))}

{G.figura(
  "Evidências por eixo estratégico",
  barras(m["por_eixo"], "var(--s3)", total=m["evidencias"]),
  "Os quatro eixos da metodologia CCFLA, adaptada no Produto 2.",
  G.tabela(["Eixo", "Evidências"], m["por_eixo"]))}

<h2>Como a evidência foi produzida</h2>

<p>A unidade de registro não é a entrevista nem a resposta a uma pergunta:
é a <strong>evidência</strong>. Um trecho anonimizado, com marca de tempo,
vinculado a uma dimensão, classificado por tipo, maturidade, alinhamento e
confiança. Um mesmo trecho pode gerar duas evidências em dimensões diferentes, e
uma dimensão que atravessa todo o corpus sem evidência é achado do diagnóstico,
não falha de coleta.</p>

<div class="grade g2">
  <div class="card">
    <h3>Quatro eixos, {m['dimensoes_total']} dimensões</h3>
    <p class="sm">Política climática, finanças, dados e governança. São as categorias da
    metodologia CCFLA/CEPAL, priorizadas para Maringá no Produto 2 da consultoria.
    {m['dimensoes_com_evidencia']} receberam evidência; {m['trianguladas']} foram
    confirmadas por duas ou mais sessões independentes.</p>
  </div>
  <div class="card">
    <h3>Divergência preservada</h3>
    <p class="sm">{m['alinhamento'].get('convergente', 0)} evidências convergentes,
    {m['alinhamento'].get('complementar', 0)} complementares,
    {m['alinhamento'].get('divergente', 0)} divergentes. Onde as fontes discordam, a
    divergência foi mantida, nunca resolvida por predominância de setor. São elas o
    material da validação participativa.</p>
  </div>
</div>

<h2>Quem foi ouvido</h2>

{legenda([('Público', S[0]), ('Sociedade Civil', S[1]), ('Academia', S[2]), ('Privado', S[3])])}
<figure>
  {empilhada([('Sessões', [m['setores'].get('Publico',0), m['setores'].get('Sociedade Civil',0), m['setores'].get('Academia',0), m['setores'].get('Privado',0)]),
              ('Evidências', [m['evidencias_por_setor'].get('Publico',0), m['evidencias_por_setor'].get('Sociedade Civil',0), m['evidencias_por_setor'].get('Academia',0), m['evidencias_por_setor'].get('Privado',0)])],
             [('Público', S[0]), ('Sociedade Civil', S[1]), ('Academia', S[2]), ('Privado', S[3])])}
  <figcaption>Distribuição das {m['sessoes']} sessões e das {m['evidencias']} evidências
  pelos quatro grupos de atores-chave. Cada barra soma 100%: a primeira mostra quantas
  sessões couberam a cada grupo, a segunda quantas evidências saíram delas.</figcaption>
</figure>

<div class="nota">
  <p><strong>Sobre a anonimização.</strong> As entrevistas foram concedidas sob termo
  de consentimento que garante confidencialidade. Nomes de participantes, contatos e a
  instituição do próprio entrevistado não aparecem em nenhuma página deste Hub: cada
  sessão é identificada por código, setor e tipo institucional. Órgãos públicos, leis e
  contratos publicados são citados nominalmente, por serem informação pública.</p>
</div>
"""


# ================================================================== CONSELHOS
def conselhos(c):
    anos = c["anos"]
    linhas = []
    for s in c["stats"]:
        linhas.append((str(s["year"]), [s["public_count"], s["private_count"],
                                        s["academia_count"], s["soc_civil_count"]]))
    seis = sorted(c["seis_anos"], key=lambda m: m["name"])
    tab_seis = "".join(
        f'<tr><td>{E(m["name"])}</td><td>{E(m["group_represented"])}</td>'
        f'<td>{E(m["affiliation"])}</td></tr>' for m in seis)

    membros = sorted(c["membros"], key=lambda m: (-m["n_anos"], m["name"]))
    linhas_m = "".join(
        f'<tr data-g="{E(m["group_represented"])}" data-n="{E(m["name"].lower())}">'
        f'<td>{E(m["name"])}</td><td>{E(m["group_represented"])}</td>'
        f'<td>{E(m["affiliation"])}</td>'
        f'<td class="num">{m["n_anos"]}</td>'
        f'<td class="sm mut">{E(m["years_present"])}</td></tr>' for m in membros)

    dist = c["distribuicao_anos"]
    um_ou_dois = dist[0][1] + dist[1][1]
    opts = "".join(f'<option value="{g}">{g}</option>' for g in GRUPOS)

    return f"""
<h1>Conselhos</h1>

<p class="lede">A composição do Conselho Municipal de Defesa do Meio Ambiente
(COMDEMA) entre {anos[0]} e {anos[-1]}: {len(c['membros'])} pessoas, quem entra,
quem permanece e o que a rotatividade faz com a capacidade do conselho de
acompanhar uma agenda de prazo longo.</p>

<div class="grade g4">
  <div class="card kpi"><b>{len(c['membros'])}</b><span>conselheiros distintos em seis anos</span></div>
  <div class="card kpi"><b>{len(seis)}</b><span>atravessaram os seis anos</span></div>
  <div class="card kpi"><b>{um_ou_dois}</b><span>passaram por um ou dois anos apenas</span></div>
  <div class="card kpi"><b>{max(s['total'] for s in c['stats'])}</b><span>maior composição anual</span></div>
</div>

<h2>Permanência dos conselheiros, 2021–2026</h2>

<p>Dos {len(c['membros'])} conselheiros que passaram pelo COMDEMA nesses seis anos,
<strong>{len(seis)}</strong> estiveram presentes em todos eles. Outros
{um_ou_dois}, ou {round(100 * um_ou_dois / len(c['membros']))}% do total,
apareceram em um ou dois
anos apenas.</p>

<p>A composição é reconduzida a cada ano por portaria. O gráfico abaixo mostra a
distribuição do tempo de permanência; o seguinte, a composição por grupo
representado, ano a ano.</p>

<figure>
  {barras([(f"{n} ano" + ("s" if n > 1 else ""), v) for n, v in dist], 'var(--s1)')}
  <figcaption>Quantos conselheiros por número de anos de presença.</figcaption>
</figure>

<h3>Quem atravessou os seis anos</h3>
<div class="tw"><table>
<thead><tr><th>Conselheiro</th><th>Grupo representado</th><th>Afiliação</th></tr></thead>
<tbody>{tab_seis}</tbody></table></div>

<h2>Composição por grupo, ano a ano</h2>

{legenda(list(zip(GRUPOS, S)))}
<figure>
  {empilhada(linhas, list(zip(GRUPOS, S)))}
  <figcaption>Número de conselheiros por grupo representado em cada ano. O total
  de {anos[-1]} é menor porque o mandato estava em composição no momento do
  levantamento.</figcaption>
</figure>

<p>A representação do poder público responde por
{c['por_grupo']['Público']} das {len(c['membros'])} cadeiras-pessoa do período, contra
{c['por_grupo']['Sociedade Civil']} da sociedade civil,
{c['por_grupo']['Privado']} do setor privado e
{c['por_grupo']['Academia']} da academia.</p>

<h2>Todos os conselheiros</h2>

<div class="busca">
  <input id="q" type="search" placeholder="Buscar por nome ou afiliação…"
         aria-label="Buscar conselheiro">
  <select id="fg" aria-label="Filtrar por grupo">
    <option value="">Todos os grupos</option>{opts}
  </select>
</div>
<p class="conta" id="conta"></p>
<div class="tw"><table id="tab">
<thead><tr><th>Conselheiro</th><th>Grupo</th><th>Afiliação</th>
<th class="num">Anos</th><th>Presença</th></tr></thead>
<tbody>{linhas_m}</tbody></table></div>

<div class="nota">
  <p><strong>Por que estes nomes aparecem.</strong> A composição de conselho
  municipal é ato público, publicada em portaria. Os nomes aqui vêm dessa fonte, não
  das entrevistas, e nenhuma informação deste Hub liga um conselheiro a uma sessão
  de entrevista.</p>
</div>
"""


JS_BUSCA = """<script>
(function(){
  var q=document.getElementById("q"), fg=document.getElementById("fg"),
      tab=document.getElementById("tab"), conta=document.getElementById("conta");
  if(!tab) return;
  var linhas=[].slice.call(tab.tBodies[0].rows);
  function filtra(){
    var t=(q.value||"").trim().toLowerCase(), g=fg?fg.value:"", n=0;
    linhas.forEach(function(l){
      var ok=(!g||l.dataset.g===g) && (!t||l.textContent.toLowerCase().indexOf(t)>=0);
      l.hidden=!ok; if(ok) n++;
    });
    conta.textContent = n + (n===1?" registro":" registros") +
      (n<linhas.length? " de "+linhas.length : "");
  }
  q.addEventListener("input",filtra); if(fg) fg.addEventListener("change",filtra);
  filtra();
})();
</script>"""


# =============================================================== INSTITUIÇÕES
def instituicoes(orgs):
    import collections
    por_grupo = collections.Counter(o.get("group_type", "não informado") for o in orgs)
    por_dim = collections.Counter(o["dim"] for o in orgs if o["dim"])
    dims = {"D1": "Política climática", "D2": "Financiamento e capacidade fiscal",
            "D3": "Dados e inteligência climática", "D4": "Governança e articulação"}
    linhas = "".join(
        f'<tr data-g="{E(o.get("group_type",""))}">'
        f'<td><strong>{E(o.get("name",""))}</strong>'
        + (f'<br><span class="sm mut">{E(o["acronym"])}</span>' if o.get("acronym") else "")
        + f'</td><td>{E(o.get("group_type",""))}</td>'
          f'<td class="sm">{E(o.get("sphere",""))}<br><span class="mut">{E(o.get("nature",""))}</span></td>'
          f'<td><span class="pill">{E(o["dim"])}</span></td>'
          f'<td class="sm">{E((o.get("justification") or "")[:230])}</td></tr>'
        for o in orgs)
    opts = "".join(f'<option value="{E(g)}">{E(g)}</option>' for g in sorted(por_grupo))

    return f"""
<h1>Instituições</h1>

<p class="lede">As {len(orgs)} organizações mapeadas no Produto 3, classificadas pelas
quatro dimensões analíticas da metodologia CCFLA/CEPAL. O mapeamento foi construído
por pesquisa documental, análise institucional e busca ativa, e é ele que define de
quem a escuta precisava ouvir.</p>

<div class="grade g4">
""" + "".join(
        f'<div class="card kpi"><b>{v}</b><span>{E(k)}</span></div>'
        for k, v in por_grupo.most_common()) + f"""
</div>

<h2>Distribuição pelas dimensões da metodologia</h2>
<figure>
  {barras([(f"{k} · {dims.get(k, '')}", v) for k, v in sorted(por_dim.items())], 'var(--s3)')}
  <figcaption>Dimensão analítica principal de cada organização. Muitas atuam em mais
  de uma; aqui conta a principal.</figcaption>
</figure>

<h2>Todas as organizações</h2>
<div class="busca">
  <input id="q" type="search" placeholder="Buscar organização…" aria-label="Buscar">
  <select id="fg" aria-label="Filtrar por grupo">
    <option value="">Todos os grupos</option>{opts}
  </select>
</div>
<p class="conta" id="conta"></p>
<div class="tw"><table id="tab">
<thead><tr><th>Organização</th><th>Grupo</th><th>Esfera e natureza</th>
<th>Dimensão</th><th>Justificativa do mapeamento</th></tr></thead>
<tbody>{linhas}</tbody></table></div>
"""


# ================================================================= LEGISLAÇÃO
def legislacao_pg(leis):
    linhas = "".join(
        f'<tr><td><strong>{E(l["norma"])}</strong></td>'
        f'<td class="num">{E(l["ano"])}</td>'
        f'<td>{E(l["ementa"])}</td></tr>' for l in leis)
    return f"""
<h1>Legislação</h1>

<p class="lede">As {len(leis)} normas municipais que formam o arcabouço de política
climática e governança ambiental de Maringá, organizadas conforme as categorias de
política climática e de coordenação da metodologia CCFLA/CEPAL.</p>

<h2>O que o arcabouço sustenta, e onde ele para</h2>

<p>O município tem base normativa consolidada em adaptação urbana, estabilidade
institucional, participação pública e coordenação vertical: a Agenda 2030 adotada
como diretriz em 2021, a Política de Enfrentamento à Emergência Climática de 2023,
o Programa Cidade Verde Resiliente de 2025, um Plano Diretor revisado em 2024 e um
instituto ambiental próprio desde 2022.</p>

<p>As fragilidades se concentram em outro lugar, e a escuta institucional as
confirma uma a uma: <strong>ausência de metas climáticas quantificadas</strong>,
ausência de sistema específico de monitoramento e avaliação, e ausência de
rastreabilidade orçamentária da despesa climática. Ou seja: a lei institui, mas
não estabelece como se mede se funcionou. É a mesma distância entre formalizar e
efetivar que o diagnóstico das entrevistas registra.</p>

<div class="nota">
  <p><strong>O caso do IPTU Verde.</strong> Instituído pela Lei nº 9.860, de 2014, e
  alterado em 2024, aparece nas quatro frentes da escuta (poder público, setor
  privado, academia e sociedade civil), sempre pelo mesmo conjunto de críticas:
  divulgação insuficiente, restrição a pessoas físicas e burocracia de acesso. Um
  instrumento com dez anos de existência formal cuja efetividade nenhuma fonte do
  corpus sustenta.</p>
</div>

<h2>Normas mapeadas</h2>
<div class="busca">
  <input id="q" type="search" placeholder="Buscar por número, ano ou assunto…"
         aria-label="Buscar norma">
</div>
<p class="conta" id="conta"></p>
<div class="tw"><table id="tab">
<thead><tr><th>Norma</th><th class="num">Ano</th><th>Ementa / assunto</th></tr></thead>
<tbody>{linhas}</tbody></table></div>

<p class="sm mut">A íntegra das normas consta do acervo documental do projeto. Esta
tabela é o índice do mapeamento, não a fonte legal. Para citação, consulte o texto
publicado pelo município.</p>
"""


# ==================================================================== PROJETO
def projeto(m, c, orgs, leis, sub):
    """Delegada a `pagina_projeto`, onde o texto mora com a acentuacao correta."""
    from pagina_projeto import render
    return render(m, c, orgs, leis, sub)
