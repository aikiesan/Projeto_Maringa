"""
Gera o painel de entrevistas do Projeto Maringá — em abas.

    python -m tools.build_site

A página é montada inteiramente a partir de `codebook/dashboard.json`; não há
mais template com texto fixo. Cada aba é renderizada só quando aberta, e a
tabela de evidências é paginada — com 494 evidências, uma página única com
rolagem é inviável.

Saídas:
  index.html          painel completo, COM os pontos focais nominais (local)
  public/index.html   idem, cifrado quando há senha configurada (hospedagem)
  site/artifact.html  só a camada anonimizada, SEM contatos (publicação)
"""

from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from tools import lock            # noqa: E402
from tools import project_base    # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "codebook" / "dashboard.json"
BASE = ROOT / "data"
OUT = ROOT / "index.html"
OUT_PUBLIC = ROOT / "public" / "index.html"
OUT_ARTIFACT = ROOT / "site" / "artifact.html"

MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho",
         "agosto", "setembro", "outubro", "novembro", "dezembro"]

ABAS = [
    ("visao", "Visão geral"),
    ("corpus", "Corpus"),
    ("codebook", "Codebook"),
    ("evidencias", "Evidências"),
    ("cobertura", "Cobertura e lacunas"),
    ("divergencias", "Divergências"),
    ("integridade", "Integridade"),
]

CSS = """
:root{
  --bg:#fbfaf8; --fg:#16181d; --mut:#5d626e; --line:#e2e0da; --card:#fff;
  --acc:#1f5f4e; --acc-bg:#e7f1ed; --warn:#8a5a12; --warn-bg:#fbf1de;
  --crit:#96331f; --crit-bg:#fbeae6; --neu-bg:#eeece7;
  --ax1:#1f5f4e; --ax2:#7a4a86; --ax3:#1d5b86; --ax4:#8a5a12;
  --mono:ui-monospace,SFMono-Regular,"SF Mono",Menlo,Consolas,monospace;
  --sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Inter,Roboto,Helvetica,Arial,sans-serif;
  --serif:"Iowan Old Style","Palatino Linotype",Palatino,Georgia,serif;
  /* Aliases do tema antigo. A tela de senha de tools/lock.py é injetada DEPOIS
     deste bloco de estilo e usa estes nomes; sem eles o cartão da senha fica
     sem fundo e sem contraste — literalmente transparente. */
  --paper:var(--bg); --surface:var(--card); --ink:var(--fg); --muted:var(--mut);
  --accent:var(--acc); --accent-bg:var(--acc-bg); --line-strong:var(--mut);
  --crit-ink:var(--crit); --shadow:0 1px 2px rgba(0,0,0,.05),0 8px 28px rgba(0,0,0,.07);
}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
  --bg:#131519; --fg:#e9e8e4; --mut:#a2a6b0; --line:#2b2f36; --card:#191c21;
  --acc:#6fc3a8; --acc-bg:#14312a; --warn:#d9a441; --warn-bg:#332811;
  --crit:#e78a72; --crit-bg:#3a1d16; --neu-bg:#23262c;
  --ax1:#6fc3a8; --ax2:#c194cd; --ax3:#7fb6e0; --ax4:#d9a441;
}}
:root[data-theme="dark"]{
  --bg:#131519; --fg:#e9e8e4; --mut:#a2a6b0; --line:#2b2f36; --card:#191c21;
  --acc:#6fc3a8; --acc-bg:#14312a; --warn:#d9a441; --warn-bg:#332811;
  --crit:#e78a72; --crit-bg:#3a1d16; --neu-bg:#23262c;
  --ax1:#6fc3a8; --ax2:#c194cd; --ax3:#7fb6e0; --ax4:#d9a441;
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.6 var(--sans);
  -webkit-font-smoothing:antialiased}
.wrap{max-width:1120px;margin:0 auto;padding:0 20px}
header.top{border-bottom:1px solid var(--line);padding:34px 0 0}
h1{font:600 27px/1.25 var(--serif);margin:0 0 8px;letter-spacing:-.01em}
.sub{color:var(--mut);max-width:62ch;margin:0 0 20px}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:14px;margin:0 0 22px}
.kpi{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px 14px}
.kpi b{display:block;font:600 24px/1.1 var(--serif);letter-spacing:-.02em}
.kpi span{display:block;color:var(--mut);font-size:12.5px;margin-top:3px}
nav.tabs{position:sticky;top:0;z-index:20;background:var(--bg);border-bottom:1px solid var(--line);
  overflow-x:auto;-webkit-overflow-scrolling:touch}
nav.tabs .in{display:flex;gap:2px;max-width:1120px;margin:0 auto;padding:0 14px}
nav.tabs button{flex:0 0 auto;background:none;border:0;border-bottom:2px solid transparent;
  color:var(--mut);font:inherit;font-size:14px;padding:12px 12px;cursor:pointer;white-space:nowrap}
nav.tabs button[aria-selected="true"]{color:var(--fg);border-bottom-color:var(--acc);font-weight:600}
nav.tabs button:hover{color:var(--fg)}
main{padding:26px 0 70px}
section.tab[hidden]{display:none!important}
h2{font:600 21px/1.3 var(--serif);margin:30px 0 10px;letter-spacing:-.01em}
h2:first-child{margin-top:0}
h3{font:600 15px/1.4 var(--sans);margin:22px 0 6px}
/* Justificacao, pedido de 14/09, com a mesma regra do Hub: hifenizacao ligada,
   porque justificar portugues sem hifenizar abre rios no meio da coluna, e o
   `lang="pt-BR"` do documento e o que a habilita. Fora da regra ficam celula de
   tabela, rotulo e legenda, onde justificar duas palavras so estica o espaco. */
p{margin:0 0 12px;max-width:74ch;text-align:justify;text-justify:inter-word;
  hyphens:auto;-webkit-hyphens:auto;text-wrap:pretty}
td p,th p,.mut.sm,.kpi p,figcaption,#lockform p{text-align:left;hyphens:manual}
.mut{color:var(--mut)}
.c{font-family:var(--mono);font-size:.88em;background:var(--neu-bg);padding:1px 5px;border-radius:4px}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:15px 17px;margin:0 0 12px}
.two{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:14px}
.three{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:14px}
.note{border-left:3px solid var(--acc);background:var(--acc-bg);border-radius:0 8px 8px 0;
  padding:13px 16px;margin:14px 0}
.note.alert{border-left-color:var(--crit);background:var(--crit-bg)}
.note.warn{border-left-color:var(--warn);background:var(--warn-bg)}
.note h3{margin:0 0 5px}
.note p:last-child{margin-bottom:0}
.pill{display:inline-block;font:500 11.5px/1 var(--sans);padding:4px 7px;border-radius:5px;
  background:var(--neu-bg);color:var(--mut);white-space:nowrap}
.pill.acc{background:var(--acc-bg);color:var(--acc)}
.pill.warn{background:var(--warn-bg);color:var(--warn)}
.pill.crit{background:var(--crit-bg);color:var(--crit)}
.pill.mono{font-family:var(--mono)}
.scroll{overflow-x:auto;border:1px solid var(--line);border-radius:10px;background:var(--card)}
table{border-collapse:collapse;width:100%;font-size:13.5px}
th,td{text-align:left;padding:9px 12px;border-bottom:1px solid var(--line);vertical-align:top}
th{font-weight:600;font-size:12px;text-transform:uppercase;letter-spacing:.04em;color:var(--mut);
  position:sticky;top:0;background:var(--card)}
tbody tr:last-child td{border-bottom:0}
td.num{text-align:right;font-family:var(--mono)}
.bar{height:7px;border-radius:4px;background:var(--neu-bg);overflow:hidden;min-width:60px}
.bar i{display:block;height:100%;background:var(--acc)}
.filters{display:flex;flex-wrap:wrap;gap:7px;align-items:center;margin:0 0 14px;
  padding:12px;border:1px solid var(--line);border-radius:10px;background:var(--card)}
.filters .lbl{font-size:11.5px;text-transform:uppercase;letter-spacing:.05em;color:var(--mut);
  margin:0 2px 0 6px}
.filters .lbl:first-child{margin-left:0}
.chip{font:inherit;font-size:12.5px;padding:5px 9px;border:1px solid var(--line);border-radius:999px;
  background:var(--bg);color:var(--mut);cursor:pointer}
.chip[aria-pressed="true"]{background:var(--acc-bg);border-color:var(--acc);color:var(--acc);font-weight:600}
select,input[type="search"]{font:inherit;font-size:13px;padding:6px 9px;border:1px solid var(--line);
  border-radius:7px;background:var(--bg);color:var(--fg);max-width:100%}
input[type="search"]{min-width:190px}
.ev{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px 16px;margin:0 0 10px}
.ev .hd{display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin:0 0 9px}
.ev .dimname{font-weight:600;font-size:13.5px;flex:1 1 100%;margin-top:2px}
.ev blockquote{margin:0 0 9px;padding:0 0 0 13px;border-left:2px solid var(--line);
  color:var(--mut);font:italic 14px/1.6 var(--serif)}
.ev .pf{margin:0;font-size:14px}
.ev .ft{margin:9px 0 0;font-size:12px;color:var(--mut);display:flex;flex-wrap:wrap;gap:5px}
.pager{display:flex;gap:8px;align-items:center;justify-content:center;margin:16px 0 0;flex-wrap:wrap}
.pager button{font:inherit;font-size:13px;padding:6px 12px;border:1px solid var(--line);
  border-radius:7px;background:var(--card);color:var(--fg);cursor:pointer}
.pager button:disabled{opacity:.4;cursor:default}
.heat{border-collapse:separate;border-spacing:2px;font-size:11px}
.heat th.v{writing-mode:vertical-rl;transform:rotate(180deg);font-size:10px;padding:4px 2px;
  position:static;background:none;text-transform:none;letter-spacing:0}
.heat td.cell{width:19px;height:19px;padding:0;border:0;border-radius:3px;background:var(--neu-bg)}
.heat td.d{font-family:var(--mono);white-space:nowrap;padding:2px 7px 2px 0;border:0;font-size:11px}
.heat th{border:0}
.axdot{display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:5px;vertical-align:baseline}
.ax1{background:var(--ax1)}.ax2{background:var(--ax2)}.ax3{background:var(--ax3)}.ax4{background:var(--ax4)}
footer{border-top:1px solid var(--line);color:var(--mut);font-size:12.5px;padding:18px 0 40px}
.count{color:var(--mut);font-size:12.5px;margin:0 0 10px}
@media (max-width:640px){h1{font-size:23px}.kpi b{font-size:20px}}
"""


def esc(s) -> str:
    return (str(s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


# --------------------------------------------------------------------------- abas

def aba_visao(d, m) -> str:
    ev, live = d["evidence"], m["live"]
    tipos = Counter(e["type"] for e in ev)
    axcount = Counter(m["dims"][e["dim"]]["axis"] for e in ev)
    linhas = "".join(
        f'<tr><td><span class="axdot ax{a}"></span>{esc(m["axname"][a])}</td>'
        f'<td class="num">{sum(1 for x in m["dims"].values() if x["axis"] == a)}</td>'
        f'<td class="num">{axcount.get(a, 0)}</td>'
        f'<td><div class="bar"><i style="width:{round(100 * axcount.get(a, 0) / max(axcount.values()))}%"></i></div></td></tr>'
        for a in sorted(m["axname"]))
    return f"""
<h2>O que este painel mostra</h2>
<p>{m['horas']} de escuta institucional em {len(live)} sessões distintas, lidas contra as
55 dimensões da metodologia CCFLA priorizadas para Maringá no Produto&nbsp;2.
<strong>Todas as {len(live)} sessões estão codificadas</strong>: {len(ev)} evidências,
cada uma um trecho anonimizado com marca de tempo, vinculado a uma dimensão e classificado
quanto à maturidade que revela e à confiança que merece.</p>
<p>A unidade de registro não é a entrevista nem a resposta: é a evidência. Por isso
{m['n_tri']} dimensões já têm evidência de mais de uma sessão, que é onde a
triangulação vale, e {m['n_div']} registros foram marcados como divergência, preservadas em vez de
resolvidas por predominância de fonte.</p>

<h2>Distribuição por eixo</h2>
<div class="scroll"><table>
<thead><tr><th>Eixo</th><th>Dimensões</th><th>Evidências</th><th style="width:38%"></th></tr></thead>
<tbody>{linhas}</tbody></table></div>

<h2>Como ler</h2>
<div class="three">
  <div class="card"><h3 style="margin-top:0">Tipos de evidência</h3>
    <p class="mut" style="font-size:13.5px;margin:0">
    <strong>{tipos.get('declaracao',0)}</strong> declarações ·
    <strong>{tipos.get('lacuna',0)}</strong> lacunas ·
    <strong>{tipos.get('oportunidade',0)}</strong> oportunidades ·
    <strong>{tipos.get('percepcao',0)}</strong> percepções ·
    <strong>{tipos.get('divergencia',0)}</strong> divergências.</p></div>
  <div class="card"><h3 style="margin-top:0">A ausência é resultado</h3>
    <p class="mut" style="font-size:13.5px;margin:0">Uma dimensão «Muito alta» que atravessa
    o corpus sem evidência é achado do diagnóstico, não falha de coleta. A aba
    <em>Cobertura e lacunas</em> mostra quais são.</p></div>
</div>
"""



def aba_corpus(d, m) -> str:
    live = m["live"]
    mx = max((i.get("minutes") or 0) for i in live) or 1
    linhas = "".join(
        f'<tr><td><span class="c">{esc(i["code"])}</span></td>'
        f'<td>{esc(i.get("sector"))}</td>'
        f'<td class="num">{esc(i.get("date","")[8:10])}/{esc(i.get("date","")[5:7])}</td>'
        f'<td class="num">{i.get("minutes") or ""}</td>'
        f'<td style="min-width:80px"><div class="bar"><i style="width:{round(100*(i.get("minutes") or 0)/mx)}%"></i></div></td>'
        f'<td class="num">{i.get("turns") or ""}</td>'
        f'<td class="num">{i.get("participant_share") or ""}%</td>'
        f'<td class="num">{m["byint"].get(i["code"], 0)}</td></tr>'
        for i in sorted(live, key=lambda x: x.get("date") or ""))
    setores = Counter(i.get("sector") for i in live)
    cards = "".join(
        f'<div class="card"><h3 style="margin-top:0">{esc(s)}</h3>'
        f'<p class="mut" style="margin:0;font-size:13.5px">{n} sessões · '
        f'{sum(m["byint"].get(i["code"],0) for i in live if i.get("sector")==s)} evidências</p></div>'
        for s, n in setores.most_common())
    return f"""
<h2>{len(live)} sessões, {len(setores)} setores</h2>
<p>Minutos calculados pela distância entre a primeira e a última marca de tempo da transcrição.
«Fala part.» é a fração de caracteres atribuída ao participante. «Evid.» é o número de
evidências codificadas a partir da sessão.</p>
<div class="three" style="margin-bottom:16px">{cards}</div>
<div class="scroll"><table>
<thead><tr><th>Código</th><th>Setor</th><th>Data</th><th>Min</th>
<th></th><th>Turnos</th><th>Fala part.</th><th>Evid.</th></tr></thead>
<tbody>{linhas}</tbody></table></div>
"""


def aba_codebook(d, m) -> str:
    bysub = defaultdict(list)
    for x in d["dimensions"]:
        bysub[(x["axis"], x["subcat"], x["subcat_name"])].append(x)
    blocos = []
    for (ax, sc, scn), dims in sorted(bysub.items()):
        linhas = "".join(
            f'<tr><td><span class="c">{esc(x["code"])}</span></td><td>{esc(x["name"])}</td>'
            f'<td><span class="pill {"crit" if x["rank"]==4 else "warn" if x["rank"]==3 else ""}">'
            f'{esc(x["priority"])}</span></td>'
            f'<td class="num">{m["bydim"].get(x["code"], 0)}</td>'
            f'<td class="num">{len(m["intbydim"].get(x["code"], set()))}</td></tr>'
            for x in dims)
        blocos.append(
            f'<h3><span class="axdot ax{ax}"></span>{esc(sc)} · {esc(scn)}</h3>'
            f'<div class="scroll" style="margin-bottom:14px"><table>'
            f'<thead><tr><th>Cód.</th><th>Dimensão</th><th>Prioridade</th>'
            f'<th>Evid.</th><th>Sessões</th></tr></thead><tbody>{linhas}</tbody></table></div>')
    return ("<h2>As 55 dimensões e o que cada uma recebeu</h2>"
            "<p>Prioridade atribuída a Maringá no Produto&nbsp;2. «Evid.» é o total de evidências "
            "codificadas na dimensão; «Sessões», de quantas entrevistas distintas elas vêm. "
            "duas ou mais é onde a triangulação começa.</p>" + "".join(blocos))


def aba_evidencias(d, m) -> str:
    ops = "".join(f'<option value="{esc(x["code"])}">{esc(x["code"])} · {esc(x["name"])}</option>'
                  for x in d["dimensions"] if m["bydim"].get(x["code"]))
    return f"""
<h2>Evidência codificada, sessão a sessão</h2>
<p>{len(d['evidence'])} evidências. Filtre por eixo, tipo, setor, sessão ou dimensão, ou
busque no trecho e na paráfrase. A lista é paginada, 25 por página.</p>
<div class="filters" id="evfil">
  <span class="lbl">Eixo</span><span id="fax"></span>
  <span class="lbl">Tipo</span><span id="fty"></span>
  <span class="lbl">Setor</span><span id="fse"></span>
  <span class="lbl">Dimensão</span>
  <select id="fdim"><option value="">todas</option>{ops}</select>
  <span class="lbl">Sessão</span>
  <select id="fint"><option value="">todas</option></select>
  <input type="search" id="fq" placeholder="buscar no texto…" aria-label="buscar">
  <button class="chip" id="fclear">limpar</button>
</div>
<p class="count" id="evcount"></p>
<div id="evlist"></div>
<div class="pager" id="evpager"></div>
"""


def aba_cobertura(d, m) -> str:
    dims, live = m["dims"], m["live"]
    tocadas = {c for v in d["triage"].values() for c, n in v.items() if n > 0}
    mudas = sorted(set(dims) - tocadas - set(m["bydim"]))
    sem_ev = sorted(c for c in dims if not m["bydim"].get(c))
    crit = [c for c in sem_ev if dims[c]["rank"] == 4]
    lac = [e for e in d["evidence"] if e["type"] == "lacuna"]
    lac_dim = Counter(e["dim"] for e in lac)

    li_sem = "".join(
        f'<tr><td><span class="c">{esc(c)}</span></td><td>{esc(dims[c]["name"])}</td>'
        f'<td><span class="pill {"crit" if dims[c]["rank"]==4 else ""}">{esc(dims[c]["priority"])}</span></td>'
        f'<td>{"não alcançada pela pré-triagem" if c in mudas else "mencionada na triagem, sem evidência codificada"}</td></tr>'
        for c in sem_ev)
    li_lac = "".join(
        f'<tr><td><span class="c">{esc(c)}</span></td><td>{esc(dims[c]["name"])}</td>'
        f'<td><span class="pill {"crit" if dims[c]["rank"]==4 else ""}">{esc(dims[c]["priority"])}</span></td>'
        f'<td class="num">{n}</td></tr>'
        for c, n in lac_dim.most_common(20))
    txt_crit = (", ".join(f'<span class="c">{esc(c)}</span> {esc(dims[c]["name"].lower())}'
                          for c in crit) or "nenhuma")
    return f"""
<h2>Cobertura: {len(m['bydim'])} das 55 dimensões têm evidência</h2>
<p>Restam <strong>{len(sem_ev)}</strong> dimensões sem qualquer evidência codificada.
Entre elas, com prioridade «Muito alta»: {txt_crit}.</p>
<div class="note">
  <h3>O que a codificação completa mudou</h3>
  <p>Três dimensões «Muito alta» que atravessavam o corpus sem evidência foram fechadas pela
  leitura integral: <span class="c">2.2.2</span> rastreamento de gastos climáticos,
  <span class="c">2.3.2</span> uso do fundo municipal de meio ambiente e
  <span class="c">3.1.3</span> inventário municipal de GEE. Nenhuma foi alcançada pela
  pré-triagem por palavra-chave, e a codificação é mais fina que a triagem.</p>
</div>

<h2>Matriz dimensão × sessão</h2>
<p>Cada célula é o número de evidências da dimensão naquela sessão. A intensidade acompanha
a contagem; a coluna à esquerda traz a prioridade.</p>
<div class="scroll" style="padding:12px"><div id="heat"></div></div>

<h2>Dimensões sem evidência</h2>
<div class="scroll"><table>
<thead><tr><th>Cód.</th><th>Dimensão</th><th>Prioridade</th><th>Situação</th></tr></thead>
<tbody>{li_sem}</tbody></table></div>

<h2>Onde estão as lacunas codificadas</h2>
<p>{len(lac)} evidências foram classificadas como <strong>lacuna</strong>, ou seja, ausência declarada
ou constatada. As vinte dimensões que mais as concentram:</p>
<div class="scroll"><table>
<thead><tr><th>Cód.</th><th>Dimensão</th><th>Prioridade</th><th>Lacunas</th></tr></thead>
<tbody>{li_lac}</tbody></table></div>
"""


def aba_divergencias(d, m) -> str:
    return """
<h2>Divergências preservadas</h2>
<p>Conflito entre fontes sobre a mesma condição habilitante. A consolidação do Produto&nbsp;2
mantém a divergência registrada em vez de resolvê-la por predominância de fonte: onde duas
fontes discordam, o que se verifica é o documento, não a autoridade de quem falou.</p>
<p class="count" id="divcount"></p>
<div id="divlist"></div>
"""


def aba_integridade(d, m) -> str:
    live = m["live"]
    sem = [i["code"] for i in live if not i["tcle"]]
    conj = [i["code"] for i in live if (i.get("n_participants") or 1) > 1]
    cod = lambda xs: ", ".join(f'<span class="c">{esc(x)}</span>' for x in xs)  # noqa: E731
    # O campo `tcle` continua vindo do codebook, e a linha segue o dado: com as
    # 17 sessões com termo assinado e arquivado, o ramo de pendência não é
    # alcançável. Ele permanece porque a alternativa — afirmar o consentimento
    # incondicionalmente — diria na página algo que o codebook não sustenta, se
    # alguém marcar uma sessão como pendente.
    linha_tcle = (
        f'<tr><td><span class="pill acc">Consentimento</span></td>\n'
        f'    <td>As {len(live)} sessões constam com termo de consentimento assinado.</td>\n'
        f'    <td>O campo <span class="c">tcle</span> vem do codebook e nunca é marcado por\n'
        f'        inferência.</td></tr>'
    ) if not sem else (
        f'<tr><td><span class="pill warn">Consentimento</span></td>\n'
        f'    <td>{len(sem)} de {len(live)} sessões sem termo assinado localizado: {cod(sem)}.</td>\n'
        f'    <td>O campo <span class="c">tcle</span> vem do codebook e nunca é marcado por\n'
        f'        inferência.</td></tr>'
    )
    return f"""
<h2>As ressalvas que acompanham estes números</h2>
<p>Levantadas por <span class="c">tools/ingest_registros.py</span>, que confere cada registro
contra a Lista de Entrevistas e a pasta de termos assinados, e detecta duplicata por md5 do
texto da transcrição, não por nome de pasta.</p>
<div class="scroll"><table>
<thead><tr><th>Item</th><th>Situação</th><th>Como está tratado aqui</th></tr></thead><tbody>
{linha_tcle}
<tr><td><span class="pill warn">Fora da Lista</span></td>
    <td>Em <span class="c">ENT-009</span> e <span class="c">ENT-017-ENT-018</span> há falante
        que não consta da Lista de Entrevistas.</td>
    <td>Casamento falante × participante feito manualmente nesses dois casos; o tipo de
        instituição foi atribuído por conferência.</td></tr>
<tr><td><span class="pill warn">Sessões conjuntas</span></td>
    <td>{cod(conj)} reúnem dois participantes na mesma sessão.</td>
    <td>Contadas como uma sessão. A codificação separa por falante na leitura, porque a diarização
        automática não separa: em <span class="c">ENT-001-ENT-002</span> ela atribui todos os
        turnos a um único nome.</td></tr>
<tr><td><span class="pill acc">Corrigido</span></td>
    <td>A duplicata registrada em 01/09 entre <span class="c">ENT-011</span> e
        <span class="c">ENT-012</span> <strong>não se confirma</strong>.</td>
    <td>A pasta ENT-011 contém a sessão conjunta <span class="c">ENT-010-ENT-011</span> e
        <span class="c">ENT-012</span> tem registro próprio, com md5 e conteúdo distintos.
        confirmado na leitura integral das duas transcrições.</td></tr>
<tr><td><span class="pill warn">Reidentificação</span></td>
    <td>Instituições singulares (órgão ambiental, liderança do Executivo, Legislativo) são
        identificáveis pelo próprio rótulo genérico.</td>
    <td>Risco residual assumido e registrado. A proteção vale contra a leitura casual, não
        contra quem conhece a estrutura da prefeitura.</td></tr>
<tr><td><span class="pill warn">Alegações de parte</span></td>
    <td>O corpus traz alegações graves não verificadas: retrocesso no licenciamento,
        saldo de fundo não executado, desvio de recurso.</td>
    <td>Codificadas como <strong>divergência</strong> ou <strong>percepção</strong> de confiança
        baixa, com remissão explícita à verificação documental na Matriz&nbsp;2. Nenhuma é
        registrada como fato.</td></tr>
</tbody></table></div>
"""


JS = r"""
const D = JSON.parse(document.getElementById("ds").textContent);
const DIM = Object.fromEntries(D.dimensions.map(d => [d.code, d]));
const INT = Object.fromEntries(D.interviews.map(i => [i.code, i]));
const LIVE = D.interviews.filter(i => !i.duplicate);
const AXN = Object.fromEntries(D.axes.map(a => [a.num, a.short || a.name]));
const TIPO = {declaracao:"Declaração", percepcao:"Percepção", lacuna:"Lacuna",
  divergencia:"Divergência", oportunidade:"Oportunidade", documento_indicado:"Documento"};
const MAT = {sem_evidencia:"sem evidência", nao_aplicavel:"não aplicável", inexistente:"inexistente",
  em_elaboracao:"em elaboração", formalizado:"formalizado", regulamentado:"regulamentado",
  em_implementacao:"em implementação", monitorado:"monitorado", efetivo:"efetivo"};
const esc = s => String(s == null ? "" : s).replace(/[&<>]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;"}[c]));

/* ---------------------------------------------------------------- abas */
const done = {};
function show(id){
  document.querySelectorAll("nav.tabs button").forEach(b =>
    b.setAttribute("aria-selected", b.dataset.t === id ? "true" : "false"));
  document.querySelectorAll("section.tab").forEach(s => s.hidden = s.id !== "tab-" + id);
  if (!done[id]) { (INIT[id] || (()=>{}))(); done[id] = 1; }
  // Em pré-visualização sandboxed (about:srcdoc) o replaceState é bloqueado por
  // política de origem. A aba já trocou; o endereço é conveniência, não estado.
  try { if (location.hash.slice(1) !== id) history.replaceState(null, "", "#" + id); }
  catch (e) { /* sandbox sem history API */ }
  window.scrollTo({top:0});
}
document.querySelectorAll("nav.tabs button").forEach(b =>
  b.addEventListener("click", () => show(b.dataset.t)));

/* ----------------------------------------------------------- evidências */
let F = {ax:0, ty:"", se:"", dim:"", int:"", ts:"", q:""}, page = 1;
const PER = 25;

function mkchip(txt, on){
  const b = document.createElement("button");
  b.className = "chip"; b.textContent = txt; b.setAttribute("aria-pressed","false");
  b.addEventListener("click", on); return b;
}
function filtered(){
  const q = F.q.trim().toLowerCase();
  return D.evidence.filter(e => {
    const d = DIM[e.dim], i = INT[e.interview] || {};
    if (F.ax && (!d || d.axis !== F.ax)) return false;
    if (F.ty && e.type !== F.ty) return false;
    if (F.se && i.sector !== F.se) return false;
    if (F.dim && e.dim !== F.dim) return false;
    if (F.int && e.interview !== F.int) return false;
    if (F.ts && (e.ts || "") !== F.ts) return false;
    if (q && !((e.excerpt||"") + " " + (e.paraphrase||"") + " " + (d?d.name:"")).toLowerCase().includes(q))
      return false;
    return true;
  });
}
let _seq = {};
function evcard(e){
  const d = DIM[e.dim] || {}, i = INT[e.interview] || {};
  /* (interview, dim, ts) NAO e unico: 32 triplas do corpus tem mais de uma
     evidencia. O sufixo ordinal existe so para o id ser valido em HTML; a
     navegacao e por filtro, nao por fragmento. */
  const _b = "ev-" + e.interview + "-" + e.dim + "-" + String(e.ts||"").replace(/:/g,"");
  _seq[_b] = (_seq[_b] || 0) + 1;
  const _id = _seq[_b] > 1 ? _b + "-" + _seq[_b] : _b;
  return `<article class="ev" id="${esc(_id)}" data-interview="${esc(e.interview)}" data-dim="${esc(e.dim)}" data-ts="${esc(e.ts||"")}">
    <div class="hd">
      <span class="pill acc mono">${esc(e.interview)}</span>
      <span class="pill mono">${esc(e.dim)}</span>
      <span class="pill">${esc(TIPO[e.type] || e.type)}</span>
      <span class="pill">${esc(MAT[e.maturity] || e.maturity)}</span>
      ${e.alignment ? `<span class="pill ${e.alignment === "divergente" ? "crit" : ""}">${esc(e.alignment)}</span>` : ""}
      <span class="pill ${e.confidence === "baixa" ? "warn" : ""}">confiança ${esc(e.confidence)}</span>
      ${e.ts ? `<span class="pill mono">${esc(e.ts)}</span>` : ""}
      <div class="dimname"><span class="axdot ax${d.axis||1}"></span>${esc(d.name || "")}</div>
    </div>
    <blockquote>${esc(e.excerpt)}</blockquote>
    <p class="pf">${esc(e.paraphrase)}</p>
    <p class="ft"><span>${esc(i.sector || "")} · ${esc(i.institution_type || "")}</span>
    ${e.question ? `<span>· pergunta ${esc(e.question)}</span>` : ""}
    ${(e.keywords||[]).length ? `<span>· ${esc(e.keywords.join(" · "))}</span>` : ""}</p>
  </article>`;
}
function renderEv(){
  _seq = {};
  const list = filtered(), tot = list.length, pages = Math.max(1, Math.ceil(tot / PER));
  if (page > pages) page = pages;
  document.getElementById("evcount").textContent =
    tot + (tot === 1 ? " evidência" : " evidências") + (tot ? ` · página ${page} de ${pages}` : "");
  document.getElementById("evlist").innerHTML =
    tot ? list.slice((page-1)*PER, page*PER).map(evcard).join("")
        : '<div class="card mut">Nenhuma evidência com esses filtros.</div>';
  const p = document.getElementById("evpager");
  p.innerHTML = "";
  if (pages > 1) {
    const b1 = document.createElement("button"); b1.textContent = "← anterior";
    b1.disabled = page === 1; b1.onclick = () => { page--; renderEv(); window.scrollTo({top:0}); };
    const sp = document.createElement("span"); sp.className = "mut";
    sp.style.fontSize = "13px"; sp.textContent = `${page} / ${pages}`;
    const b2 = document.createElement("button"); b2.textContent = "próxima →";
    b2.disabled = page === pages; b2.onclick = () => { page++; renderEv(); window.scrollTo({top:0}); };
    p.append(b1, sp, b2);
  }
}
function syncChips(){
  axB.forEach((b,k) => b.setAttribute("aria-pressed", F.ax === AXK[k] ? "true":"false"));
  tyB.forEach((b,k) => b.setAttribute("aria-pressed", F.ty === TYK[k] ? "true":"false"));
  seB.forEach((b,k) => b.setAttribute("aria-pressed", F.se === SEK[k] ? "true":"false"));
}
let axB=[], tyB=[], seB=[], AXK=[], TYK=[], SEK=[];
function initEv(){
  AXK = D.axes.map(a => a.num);
  axB = AXK.map(n => mkchip(AXN[n], () => { F.ax = F.ax === n ? 0 : n; page=1; syncChips(); renderEv(); }));
  axB.forEach(b => document.getElementById("fax").appendChild(b));
  TYK = ["lacuna","declaracao","percepcao","oportunidade","divergencia"];
  tyB = TYK.map(t => mkchip(TIPO[t], () => { F.ty = F.ty === t ? "" : t; page=1; syncChips(); renderEv(); }));
  tyB.forEach(b => document.getElementById("fty").appendChild(b));
  SEK = [...new Set(LIVE.map(i => i.sector).filter(Boolean))].sort();
  seB = SEK.map(s => mkchip(s, () => { F.se = F.se === s ? "" : s; page=1; syncChips(); renderEv(); }));
  seB.forEach(b => document.getElementById("fse").appendChild(b));

  const byint = {};
  D.evidence.forEach(e => byint[e.interview] = (byint[e.interview]||0)+1);
  const si = document.getElementById("fint");
  Object.keys(byint).sort().forEach(c => {
    const o = document.createElement("option");
    o.value = c; o.textContent = `${c} (${byint[c]})`; si.appendChild(o);
  });
  si.onchange = () => { F.int = si.value; page=1; renderEv(); };
  const sd = document.getElementById("fdim");
  sd.onchange = () => { F.dim = sd.value; page=1; renderEv(); };
  let t; const q = document.getElementById("fq");
  q.oninput = () => { clearTimeout(t); t = setTimeout(() => { F.q = q.value; page=1; renderEv(); }, 200); };
  if (ALVO) {
    F.int = ALVO.int; F.dim = ALVO.dim; F.ts = ALVO.ts; page = 1;
    if (ALVO.int) si.value = ALVO.int;
    if (ALVO.dim) sd.value = ALVO.dim;
    const av = document.getElementById("evfil");
    if (av) {
      const n = document.createElement("div");
      n.className = "card";
      n.id = "aviso-alvo";
      n.innerHTML = '<b>Filtrado a partir do Produto 4.</b> Mostrando a evidência '
        + 'ancorada em <span class="mono">' + esc(ALVO.int) + '</span>'
        + (ALVO.dim ? ' &middot; dimensão <span class="mono">' + esc(ALVO.dim) + '</span>' : '')
        + (ALVO.ts ? ' &middot; <span class="mono">' + esc(ALVO.ts) + '</span>' : '')
        + '. Use «limpar» para ver o corpus inteiro.';
      av.parentNode.insertBefore(n, av);
    }
  }
  document.getElementById("fclear").onclick = () => {
    F = {ax:0,ty:"",se:"",dim:"",int:"",ts:"",q:""}; page=1; si.value=""; sd.value=""; q.value="";
    const av = document.getElementById("aviso-alvo");
    if (av) av.remove();
    syncChips(); renderEv();
  };
  renderEv();
}

/* --------------------------------------------------------- divergências */
function initDiv(){
  const list = D.evidence.filter(e => e.type === "divergencia" || e.alignment === "divergente");
  document.getElementById("divcount").textContent = list.length + " registros";
  document.getElementById("divlist").innerHTML = list.map(evcard).join("");
}

/* -------------------------------------------------------------- heatmap */
function initHeat(){
  const codes = [...new Set(D.evidence.map(e => e.interview))].sort();
  const cnt = {};
  D.evidence.forEach(e => { (cnt[e.dim] = cnt[e.dim] || {})[e.interview] =
    (cnt[e.dim]?.[e.interview] || 0) + 1; });
  const mx = Math.max(...D.evidence.length ? Object.values(cnt).flatMap(o => Object.values(o)) : [1]);
  let h = '<table class="heat"><thead><tr><th></th><th></th>' +
    codes.map(c => `<th class="v">${esc(c)}</th>`).join("") + "<th></th></tr></thead><tbody>";
  D.dimensions.forEach(d => {
    const row = cnt[d.code] || {}, tot = Object.values(row).reduce((a,b)=>a+b, 0);
    h += `<tr><td class="d" title="${esc(d.name)}"><span class="axdot ax${d.axis}"></span>${esc(d.code)}</td>` +
      `<td class="d" style="opacity:.6">${d.rank === 4 ? "MA" : d.rank === 3 ? "A" : ""}</td>` +
      codes.map(c => {
        const n = row[c] || 0;
        const bg = n ? `background:color-mix(in srgb, var(--ax${d.axis}) ${Math.round(18 + 82*n/mx)}%, transparent)` : "";
        return `<td class="cell" style="${bg}" title="${esc(d.code)} · ${esc(c)} · ${n}">${n>2?`<span style="font-size:9px;color:#fff">${n}</span>`:""}</td>`;
      }).join("") + `<td class="d" style="opacity:.6">${tot || ""}</td></tr>`;
  });
  document.getElementById("heat").innerHTML = h + "</tbody></table>";
}

const INIT = {evidencias: initEv, divergencias: initDiv, cobertura: initHeat};

/* Deep-link vindo da pagina do Produto 4: `#evidencias?int=..&dim=..&ts=..`.
   E por FILTRO, nao por fragmento, e a razao e de dado: (interview, dim, ts) nao
   e chave — 32 triplas do corpus tem mais de uma evidencia, uma delas tem tres.
   Filtrar mostra todas as evidencias daquele ponto, que e a resposta correta, e
   ainda desarma a paginacao de 25: o alvo nunca fica numa pagina que o fragmento
   nao alcanca. */
let ALVO = null;
function rota(){
  let h = "";
  try { h = decodeURIComponent(location.hash.slice(1)); } catch (e) { h = ""; }
  const corte = h.indexOf("?");
  const aba = (corte < 0 ? h : h.slice(0, corte)) || "visao";
  const par = {};
  if (corte >= 0) h.slice(corte + 1).split("&").forEach(kv => {
    const i = kv.indexOf("=");
    if (i > 0) par[kv.slice(0, i)] = kv.slice(i + 1);
  });
  return {aba, par};
}
const R = rota();
let inicial = "visao";
try { if (R.aba && document.getElementById("tab-" + R.aba)) inicial = R.aba; } catch (e) {}
if (inicial === "evidencias" && (R.par.int || R.par.dim || R.par.ts)) {
  ALVO = {int: R.par.int || "", dim: R.par.dim || "", ts: R.par.ts || ""};
}
show(inicial);
"""


def main() -> int:
    d = json.loads(DATA.read_text(encoding="utf-8"))
    # Terceira superficie das supressoes. O `excerpt` da evidencia e publicado
    # aqui, e ate 14/09 nao passava por `tools/supressoes.py`: o corte de
    # ENT-003 valia na transcricao e o painel republicava a frase inteira.
    # Falha dura, como nas outras duas superficies.
    sys.path.insert(0, str(ROOT))
    from tools.supressoes import aplicar_em_evidencias
    _n_sup = aplicar_em_evidencias(d["evidence"])
    ev = d["evidence"]
    live = [i for i in d["interviews"] if not i["duplicate"]]
    dims = {x["code"]: x for x in d["dimensions"]}
    byint = Counter(e["interview"] for e in ev)
    bydim = Counter(e["dim"] for e in ev)
    intbydim = defaultdict(set)
    for e in ev:
        intbydim[e["dim"]].add(e["interview"])
    minutos = sum(i.get("minutes") or 0 for i in live)
    m = {
        "live": live, "dims": dims, "byint": byint, "bydim": bydim,
        "intbydim": intbydim,
        "axname": {a["num"]: a["name"] for a in d["axes"]},
        "horas": f"{minutos // 60}h{minutos % 60:02d}",
        "n_tri": sum(1 for c, s in intbydim.items() if len(s) > 1),
        "n_div": sum(1 for e in ev if e["type"] == "divergencia" or e.get("alignment") == "divergente"),
    }
    hoje = date.today()
    stamp = f"{MESES[hoje.month - 1].capitalize()} de {hoje.year}"

    conteudo = {
        "visao": aba_visao(d, m), "corpus": aba_corpus(d, m),
        "codebook": aba_codebook(d, m), "evidencias": aba_evidencias(d, m),
        "cobertura": aba_cobertura(d, m), "divergencias": aba_divergencias(d, m),
        "integridade": aba_integridade(d, m),
    }
    pb = project_base.load(BASE)
    abas = list(ABAS) + ([("base", "Base do Produto 3")] if pb else [])

    nav = "".join(f'<button data-t="{k}" role="tab" aria-selected="false">{esc(v)}</button>'
                  for k, v in abas)
    secs = "".join(f'<section class="tab" id="tab-{k}" role="tabpanel" hidden><div class="wrap">'
                   f'{conteudo.get(k, "")}</div></section>' for k, _ in abas if k != "base")
    if pb:
        secs += ('<section class="tab" id="tab-base" role="tabpanel" hidden><div class="wrap">'
                 + project_base.HTML + "</div></section>")

    kpis = [
        (len(live), "sessões distintas"),
        (len(byint), "codificadas por completo"),
        (len(ev), "evidências rastreáveis"),
        (f"{len(bydim)}/55", "dimensões com evidência"),
        (m["n_tri"], "dimensões trianguladas"),
        (m["n_div"], "divergências preservadas"),
    ]
    kpi_html = "".join(f'<div class="kpi"><b>{esc(a)}</b><span>{esc(b)}</span></div>' for a, b in kpis)

    js_pb = project_base.JS if pb else ""
    pb_json = (f'<script type="application/json" id="pb">{json.dumps(pb, ensure_ascii=False)}</script>'
               if pb else "")

    body = f"""<header class="top"><div class="wrap">
  <h1>Repositório de Entrevistas de Maringá</h1>
  <p class="sub">{m['horas']} de escuta institucional em {len(live)} sessões, lidas contra as 55
  dimensões da metodologia. Todas codificadas: {len(ev)} evidências rastreáveis até o trecho que
  as sustenta, e os silêncios que continuam de pé.</p>
  <div class="kpis">{kpi_html}</div>
</div></header>
<nav class="tabs" role="tablist"><div class="in">{nav}</div></nav>
<main>{secs}</main>
<footer><div class="wrap">
  <p>Projeto CEPAL/IPPLAM, Maringá (PR). Camada anonimizada: nenhum nome, contato ou instituição
  nominal do participante entra aqui. Gerado por <span class="c">tools/build_site.py</span> a
  partir de <span class="c">codebook/dashboard.json</span> ({esc(d['generated'])}). {stamp}.</p>
</div></footer>
{pb_json}
<script type="application/json" id="ds">{json.dumps(d, ensure_ascii=False)}</script>
<script>{JS}
{js_pb}
</script>"""

    html = (f"<!doctype html><html lang=\"pt-BR\"><head><meta charset=\"utf-8\">"
            f"<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">"
            f"<title>Repositório de Entrevistas de Maringá</title>"
            f"<style>{CSS}</style></head><body>{body}</body></html>")

    OUT.write_text(html, encoding="utf-8")

    # Artifact: só a camada anonimizada, sem a base do projeto (que traz contatos).
    if pb:
        a_nav = "".join(f'<button data-t="{k}" role="tab" aria-selected="false">{esc(v)}</button>'
                        for k, v in ABAS)
        a_secs = "".join(f'<section class="tab" id="tab-{k}" role="tabpanel" hidden><div class="wrap">'
                         f'{conteudo.get(k, "")}</div></section>' for k, _ in ABAS)
        a_body = (body.replace(nav, a_nav).replace(secs, a_secs)
                      .replace(pb_json, "").replace(js_pb, ""))
    else:
        a_body = body
    OUT_ARTIFACT.parent.mkdir(exist_ok=True)
    OUT_ARTIFACT.write_text(f"<style>{CSS}</style>{a_body}", encoding="utf-8")

    senha = lock.senha_configurada(ROOT)
    publicada = lock.trancar(html, senha) if senha else html
    OUT_PUBLIC.parent.mkdir(exist_ok=True)
    OUT_PUBLIC.write_text(publicada, encoding="utf-8")

    print(f"public/index.html: {'CIFRADA com senha' if senha else 'EM CLARO — sem senha configurada'}")
    print(f"index.html: {len(html)//1024} KB · {len(abas)} abas · {len(ev)} evidências de "
          f"{len(byint)} sessões · {len(bydim)}/55 dimensões · {m['n_tri']} trianguladas · "
          f"{m['n_div']} divergências")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
