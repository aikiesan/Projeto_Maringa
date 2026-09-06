"""
Gera o `index.html` do GitHub Pages a partir de `site/template.html` e do
`codebook/dashboard.json`.

    python -m tools.build_site

O template é a página do painel (layout, CSS e JS). Este script injeta os dados
atuais e aplica as correções de texto e de comportamento que dependem do estado
da codificação. Cada substituição é verificada: se o template mudar de forma
incompatível, o build falha em vez de gerar uma página silenciosamente errada.
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from tools import lock  # noqa: E402
from tools import project_base  # noqa: E402
from database import codebook as cb  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "site" / "template.html"
DATA = ROOT / "codebook" / "dashboard.json"
BASE = ROOT / "data"          # base de mapeamento do Produto 3
OUT = ROOT / "index.html"
OUT_PUBLIC = ROOT / "public" / "index.html"   # diretório de saída para hospedagem

MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho",
         "agosto", "setembro", "outubro", "novembro", "dezembro"]


def sub1(html: str, old: str, new: str, label: str) -> str:
    n = html.count(old)
    if n != 1:
        raise SystemExit(f"build_site: '{label}' encontrado {n}x no template (esperado 1)")
    return html.replace(old, new)


def diagnostico(d: dict) -> str:
    """Seção «Diagnóstico da cobertura», gerada a partir do estado atual do acervo."""
    dims = {x["code"]: x for x in d["dimensions"]}
    live = [i for i in d["interviews"] if not i["duplicate"]]
    tocadas = {c for v in d["triage"].values() for c, n in v.items() if n > 0}
    com_ev = {e["dim"] for e in d["evidence"]}
    mudas = sorted(set(dims) - tocadas - com_ev)
    criticas = [c for c in mudas if dims[c]["rank"] == 4]

    ouvidas: dict[str, int] = {}
    for i in live:
        for t in (i.get("institution_type") or "—").split("; "):
            ouvidas[t] = ouvidas.get(t, 0) + 1

    ausentes = {k: v for k, v in cb.MISSING_INSTITUTIONS.items()
                if not any(cb._fold(k.split(" (")[0][:12]) in cb._fold(o) for o in ouvidas)}

    li_ok = "\n".join(
        f'        <li>{t}{f" <em>({n} sessões)</em>" if n > 1 else ""}</li>'
        for t, n in sorted(ouvidas.items(), key=lambda x: (-x[1], x[0])))
    li_no = "\n".join(
        f'        <li><strong>{k}</strong> <em>→ '
        + ", ".join(f'{c} {dims[c]["name"].lower()}' for c in v if c in dims)
        + "</em></li>" for k, v in ausentes.items())

    lista_criticas = ", ".join(
        f'<span class="c">{c}</span> {dims[c]["name"].lower()}' for c in criticas) or "nenhuma"

    return f"""<section>
  <p class="eyebrow">Diagnóstico da cobertura</p>
  <div class="col">
    <h2>Os silêncios têm um endereço institucional</h2>
    <p>{len(mudas)} das 55 dimensões atravessaram as {len(live)} sessões sem uma única menção na
    pré-triagem e sem evidência codificada — {len(criticas)} delas com prioridade «Muito alta»:
    {lista_criticas}. Não é coincidência: são as dimensões cuja fonte primária, segundo a
    própria Matriz 1, são órgãos que não aparecem nos registros de entrevista.</p>
  </div>

  <div class="two">
    <div class="card ok">
      <div class="t">Com registro de entrevista · {len(live)} sessões</div>
      <ul>
{li_ok}
      </ul>
    </div>
    <div class="card no">
      <div class="t">Sem registro — e fonte primária de dimensão prioritária</div>
      <ul>
{li_no}
      </ul>
    </div>
  </div>

  <div class="note alert">
    <h3>O que isso significa para o diagnóstico</h3>
    <p>O eixo <strong>Orçamento e Finanças</strong> concentra 25 das 55 dimensões e é onde a
    metodologia atribuiu mais prioridade «Muito alta» — e é o eixo cuja fonte primária segue
    ausente. As menções financeiras que aparecem no corpus vêm de quem <em>usa</em> o orçamento,
    não de quem o <em>monta</em>. Isso não invalida a evidência coletada; delimita o que ela pode
    sustentar.</p>
    <p>Duas saídas: sessões adicionais com fazenda/planejamento, planejamento urbano e
    procuradoria cobririam a maior parte do vazio; ou essas dimensões são sustentadas por
    evidência documental na Matriz 2 (PPA, LDO, LOA, QDD, relatórios de execução), que não
    depende de entrevista.</p>
  </div>
</section>

"""


def integridade(d: dict) -> str:
    """Seção «Integridade», gerada a partir do estado atual do acervo."""
    live = [i for i in d["interviews"] if not i["duplicate"]]
    dup = [i for i in d["interviews"] if i["duplicate"]]
    sem_tcle = [i["code"] for i in live if not i["tcle"]]
    conjuntas = [i["code"] for i in live if (i.get("n_participants") or 1) > 1]
    cod = lambda xs: ", ".join(f'<span class="c">{x}</span>' for x in xs)  # noqa: E731

    linhas = []
    if sem_tcle:
        linhas.append(f"""        <tr>
          <td><span class="pill crit">Sem TCLE</span></td>
          <td>{len(sem_tcle)} de {len(live)} sessões sem termo assinado localizado na pasta
              de termos: {cod(sem_tcle)}.</td>
          <td>Aparecem na matriz, mas não devem alimentar o diagnóstico até o termo ser
              localizado. O campo <span class="c">tcle</span> nunca é marcado por inferência.</td>
        </tr>""")
    linhas.append(f"""        <tr>
          <td><span class="pill warn">Fora da Lista</span></td>
          <td>Em <span class="c">ENT-009</span> e <span class="c">ENT-017-ENT-018</span> há falante
              que não consta da Lista de Entrevistas.</td>
          <td>O casamento falante × participante ficou manual nesses dois casos; o tipo de
              instituição foi atribuído por conferência, não pelo cruzamento automático.</td>
        </tr>""")
    if conjuntas:
        linhas.append(f"""        <tr>
          <td><span class="pill warn">Sessões conjuntas</span></td>
          <td>{cod(conjuntas)} reúnem dois participantes na mesma sessão.</td>
          <td>Contadas como uma sessão. A codificação separa por falante na leitura — a
              diarização automática não separa: em <span class="c">ENT-001-ENT-002</span> ela
              atribui todos os turnos a um único nome.</td>
        </tr>""")
    linhas.append(f"""        <tr>
          <td><span class="pill acc">Corrigido</span></td>
          <td>A duplicata registrada em 01/09 entre <span class="c">ENT-011</span> e
              <span class="c">ENT-012</span> <strong>não se confirma</strong>: no acervo atual
              a pasta ENT-011 contém a sessão conjunta
              <span class="c">ENT-010-ENT-011</span> e <span class="c">ENT-012</span> tem
              registro próprio, com md5 distinto.</td>
          <td>Nenhuma duplicata no acervo atual{" (" + cod([i["code"] for i in dup]) + ")" if dup else ""}.
              O total é {len(live)} sessões distintas.</td>
        </tr>""")
    linhas.append("""        <tr>
          <td><span class="pill warn">Reidentificação</span></td>
          <td>Instituições singulares — órgão ambiental, liderança do Executivo, Legislativo —
              são identificáveis pelo próprio rótulo genérico.</td>
          <td>Risco residual assumido e registrado. A proteção vale contra leitura casual, não
              contra quem conhece a estrutura da prefeitura.</td>
        </tr>""")

    return f"""<section>
  <p class="eyebrow">Integridade</p>
  <div class="col">
    <h2>As ressalvas que acompanham estes números</h2>
    <p>Levantadas por <span class="c">tools/ingest_registros.py</span>, que confere cada registro
    contra a Lista de Entrevistas e a pasta de termos assinados, e detecta duplicata por md5 do
    texto da transcrição — não por nome de pasta.</p>
  </div>
  <div class="scroll">
    <table>
      <thead><tr><th>Item</th><th>Situação</th><th>Como está tratado aqui</th></tr></thead>
      <tbody>
{chr(10).join(linhas)}
      </tbody>
    </table>
  </div>
</section>
"""


def main() -> int:
    html = TEMPLATE.read_text(encoding="utf-8")
    d = json.loads(DATA.read_text(encoding="utf-8"))

    ev = d["evidence"]
    coded = sorted({e["interview"] for e in ev})
    dims_cov = {e["dim"] for e in ev}
    live = [i for i in d["interviews"] if not i["duplicate"]]
    by_int = Counter(e["interview"] for e in ev)
    tri = sorted({c for c in dims_cov
                  if len({e["interview"] for e in ev if e["dim"] == c}) > 1})
    div = [e for e in ev if e.get("alignment") == "divergente" or e["type"] == "divergencia"]
    codigos = sum(len(i["code"].split("-")) // 2 for i in live)
    minutos = sum(i.get("minutes") or 0 for i in live)
    horas = f"{minutos // 60}h{minutos % 60:02d}"
    setores = sorted({i.get("sector") for i in live if i.get("sector")})
    hoje = date.today()
    stamp = f"{MESES[hoje.month - 1].capitalize()} de {hoje.year}"

    # ---------------------------------------------------------------- dados
    html = re.sub(
        r'(<script type="application/json" id="ds">).*?(</script>)',
        lambda m: m.group(1) + json.dumps(d, ensure_ascii=False) + m.group(2),
        html, count=1, flags=re.S)

    # ------------------------------------------------------------------ JS
    html = sub1(html,
        'contradicao:"Contradição",',
        'contradicao:"Contradição",divergencia:"Divergência",',
        "rótulo de tipo divergência")

    html = sub1(html,
        '[D.evidence.length, "evidências codificadas (1 sessão)"],',
        '[D.evidence.length, "evidências codificadas<br>(" + CODED.length + " de " '
        '+ NI + " sessões)"],',
        "KPI de evidências")

    html = sub1(html,
        'const NI = live.length;',
        'const NI = live.length;\n'
        'const CODED = [...new Set(D.evidence.map(e => e.interview))].sort();\n'
        'const EVBYINT = Object.fromEntries(CODED.map(c => '
        '[c, D.evidence.filter(e => e.interview === c).length]));',
        "constantes de sessões codificadas")

    # cartão de evidência: mostrar a que entrevista pertence
    html = sub1(html,
        '<span class="pill neu">${esc(e.dim)}</span>',
        '<span class="pill acc">${esc(e.interview)}</span>\n'
        '      <span class="pill neu">${esc(e.dim)}</span>',
        "pill da entrevista no cartão de evidência")

    # filtro por entrevista, ao lado dos filtros de eixo e tipo
    html = sub1(html,
        '  const sep = document.createElement("span");\n'
        '  sep.className = "lbl"; sep.style.marginLeft = "8px"; sep.textContent = "Tipo";',
        '  const sepI = document.createElement("span");\n'
        '  sepI.className = "lbl"; sepI.style.marginLeft = "8px"; sepI.textContent = "Sessão";\n'
        '  box.appendChild(sepI);\n'
        '  const inBtns = CODED.map(c => mk(c + " (" + EVBYINT[c] + ")", b => {\n'
        '    evInt = evInt === c ? "" : c; sync(); renderEv();\n'
        '  }));\n'
        '  const sep = document.createElement("span");\n'
        '  sep.className = "lbl"; sep.style.marginLeft = "8px"; sep.textContent = "Tipo";',
        "chips de sessão")

    html = sub1(html, 'let evAxis = 0, evType = "";',
                'let evAxis = 0, evType = "", evInt = "";', "estado do filtro")

    html = sub1(html,
        '    tyBtns.forEach((b, k) => b.setAttribute("aria-pressed",',
        '    inBtns.forEach((b, k) => b.setAttribute("aria-pressed",\n'
        '      evInt === CODED[k] ? "true" : "false"));\n'
        '    tyBtns.forEach((b, k) => b.setAttribute("aria-pressed",',
        "sincronização dos chips de sessão")

    html = sub1(html,
        'return (!evAxis || (d && d.axis === evAxis)) && (!evType || e.type === evType);',
        'return (!evAxis || (d && d.axis === evAxis)) && (!evType || e.type === evType)\n'
        '      && (!evInt || e.interview === evInt);',
        "filtro por sessão")

    # tipos disponíveis nos chips: incluir divergência
    html = sub1(html,
        'const tyBtns = ["lacuna", "declaracao", "percepcao", "oportunidade"].map(t =>',
        'const TYPES = ["lacuna", "declaracao", "percepcao", "oportunidade", "divergencia"];\n'
        '  const tyBtns = TYPES.map(t =>',
        "lista de tipos")
    html = sub1(html,
        'evType === ["lacuna", "declaracao", "percepcao", "oportunidade"][k] ? "true" : "false"));',
        'evType === TYPES[k] ? "true" : "false"));',
        "sincronização dos chips de tipo")

    # ---------------------------------------------------------------- texto
    html = sub1(html,
        "Onze horas e meia de escuta institucional, lidas contra as 55 dimensões da metodologia. "
        "Onde o corpus fala, onde ele silencia — e por quê.",
        f"{horas} de escuta institucional em {len(live)} sessões, lidas contra as 55 dimensões da "
        f"metodologia. {len(coded)} já codificadas, {len(ev)} evidências rastreáveis até o trecho "
        f"que as sustenta — e os silêncios que continuam de pé.",
        "linha de apoio do cabeçalho")

    html = sub1(html, '[NI, "sessões distintas<br>(em 16 códigos)"],',
                f'[NI, "sessões distintas<br>(em {codigos} códigos)"],',
                "KPI de sessões")

    html = sub1(html,
        "A barra conta entrevistas, não menções — quatorze é o máximo.",
        f"A barra conta entrevistas, não menções — {len(live)} é o máximo.",
        "legenda da cobertura")

    html = sub1(html, "<h2>Quatorze sessões, quatro setores</h2>",
                f"<h2>{len(live)} sessões, {len(setores)} setores</h2>",
                "título da seção do corpus")

    html = sub1(html,
        '<h2>O que a codificação produz, em concreto</h2>',
        '<h2>Evidência codificada, sessão a sessão</h2>',
        "título da seção de evidências")

    lista = ", ".join(f"{c} ({by_int[c]})" for c in coded)
    html = sub1(html,
        '<p>Até aqui uma sessão foi codificada por completo — <span class="c">ENT-003</span>, '
        'órgão ambiental municipal — e ela rendeu <strong>30 evidências em 23 das 55 dimensões</strong>, '
        'atravessando os quatro eixos. É a amostra do que sai do processo quando ele roda: trecho '
        'anonimizado com marca de tempo, dimensão, tipo, maturidade e confiança.</p>',
        f'<p>{len(coded)} sessões codificadas por completo — {lista} — somando '
        f'<strong>{len(ev)} evidências em {len(dims_cov)} das 55 dimensões</strong>, nos quatro eixos. '
        f'Cada evidência é um trecho anonimizado com marca de tempo, uma dimensão, um tipo, a '
        f'maturidade que revela e a confiança que merece. Filtre por sessão para ler uma entrevista '
        f'inteira, ou por dimensão para confrontar o que duas fontes dizem sobre a mesma condição.</p>'
        f'<p><strong>{len(tri)} dimensões já têm evidência de mais de uma sessão</strong> — é onde a '
        f'triangulação começa a valer, e onde as divergências aparecem.</p>',
        "abertura da seção de evidências")

    html = sub1(html,
        '<p>Gerado por <span class="c">tools/export_dashboard.py</span> a partir de '
        '<span class="c">codebook/dashboard.json</span>. Setembro de 2026.</p>',
        f'<p>Gerado por <span class="c">tools/build_site.py</span> a partir de '
        f'<span class="c">codebook/dashboard.json</span> ({d["generated"]}). {stamp}.</p>',
        "rodapé")

    # A seção de diagnóstico da cobertura é regerada por inteiro: as listas de
    # instituições ouvidas e ausentes mudam a cada nova sessão do acervo.
    ini = html.find('<section>\n  <p class="eyebrow">Diagnóstico da cobertura</p>')
    fim = html.find('<section>\n  <p class="eyebrow">Evidência codificada</p>')
    if ini < 0 or fim < 0 or fim <= ini:
        raise SystemExit("build_site: não localizei a seção de diagnóstico da cobertura")
    html = html[:ini] + diagnostico(d) + html[fim:]

    # seção de integridade, também regerada
    ini = html.find('<section>\n  <p class="eyebrow">Integridade</p>')
    if ini < 0:
        raise SystemExit("build_site: não localizei a seção de integridade")
    fim = html.find("\n</main>", ini)
    html = html[:ini] + integridade(d) + html[fim:]

    # nota de impacto na seção de diagnóstico da cobertura
    nota = (
        '  <div class="note">\n'
        '    <h3>O que a codificação já mudou neste quadro</h3>\n'
        f'    <p>As sete dimensões silenciosas acima vêm da pré-triagem por palavra-chave sobre as '
        f'quatorze transcrições. A codificação é mais fina que a triagem, e já corrigiu parte do '
        f'quadro: <span class="c">ENT-001-ENT-002</span>, na secretaria de governo, produziu a '
        f'primeira evidência do corpus sobre <strong>2.2.1 orçamento verde</strong> — negativa, e '
        f'vinda de quem estava na reunião de elaboração do orçamento de 2027 — e também sobre '
        f'<strong>2.1.3 fundos climáticos internacionais</strong>. Nenhuma das duas havia sido '
        f'alcançada por palavra-chave.</p>\n'
        f'    <p>Continuam sem qualquer evidência codificada, entre as de prioridade «Muito alta»: '
        f'<span class="c">2.2.2</span> rastreamento de gastos climáticos, <span class="c">2.3.2</span> '
        f'uso do FUNDEMA e <span class="c">3.1.3</span> inventário municipal de GEE. As três dependem '
        f'de fontes que seguem ausentes do acervo — Fazenda, conselho gestor do fundo e órgão '
        f'ambiental estadual —, o que reforça a leitura institucional acima em vez de contradizê-la.</p>\n'
        '  </div>\n'
    )
    html = sub1(html,
        '</section>\n\n<section>\n  <p class="eyebrow">Evidência codificada</p>',
        nota + '</section>\n\n<section>\n  <p class="eyebrow">Evidência codificada</p>',
        "nota de impacto")

    # Variante para publicar como Artifact — sem doctype/head/body (o serviço
    # embrulha o conteúdo) e SEM a base do projeto: o artefato é compartilhável,
    # então leva só a camada anonimizada, nunca os pontos focais nominais.
    inner = html.split("<body>", 1)[1].rsplit("</body>", 1)[0].strip()
    (ROOT / "site" / "artifact.html").write_text(inner, encoding="utf-8")

    # ------------------------------------------- base do projeto (Produto 3)
    pb = project_base.load(BASE)
    if pb:
        html = sub1(html, '<script type="application/json" id="ds">',
                    '<script type="application/json" id="pb">'
                    + json.dumps(pb, ensure_ascii=False)
                    + '</script>\n<script type="application/json" id="ds">',
                    "payload da base do projeto")
        html = sub1(html, "\n</main>", project_base.HTML + "\n</main>",
                    "seções da base do projeto")
        html = sub1(html, "renderEv();\nrenderHeat();",
                    "renderEv();\nrenderHeat();\n" + project_base.JS,
                    "scripts da base do projeto")

    OUT.write_text(html, encoding="utf-8")

    # A saída publicada vai cifrada quando há senha configurada (PAINEL_SENHA ou
    # o arquivo .senha). O index.html local fica em claro — é o seu disco.
    senha = lock.senha_configurada(ROOT)
    publicada = lock.trancar(html, senha) if senha else html
    OUT_PUBLIC.parent.mkdir(exist_ok=True)
    OUT_PUBLIC.write_text(publicada, encoding="utf-8")

    print(f"public/index.html: {'CIFRADA com senha' if senha else 'EM CLARO — sem senha configurada'}")
    print(f"{OUT.relative_to(ROOT)}: {len(html) // 1024} KB · {len(ev)} evidências "
          f"de {len(coded)} sessões · {len(dims_cov)}/{len(d['dimensions'])} dimensões com evidência "
          f"· {len(tri)} trianguladas · {len(div)} divergência(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
