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

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "site" / "template.html"
DATA = ROOT / "codebook" / "dashboard.json"
OUT = ROOT / "index.html"

MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho",
         "agosto", "setembro", "outubro", "novembro", "dezembro"]


def sub1(html: str, old: str, new: str, label: str) -> str:
    n = html.count(old)
    if n != 1:
        raise SystemExit(f"build_site: '{label}' encontrado {n}x no template (esperado 1)")
    return html.replace(old, new)


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
        f"Onze horas e meia de escuta institucional, lidas contra as 55 dimensões da metodologia. "
        f"{len(coded)} sessões já codificadas, {len(ev)} evidências rastreáveis até o trecho que as "
        f"sustenta — e os silêncios que continuam de pé.",
        "linha de apoio do cabeçalho")

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

    OUT.write_text(html, encoding="utf-8")

    # variante para publicar como Artifact: sem doctype/head/body — o serviço
    # embrulha o conteúdo por conta própria.
    inner = html.split("<body>", 1)[1]
    inner = inner.rsplit("</body>", 1)[0].strip()
    (ROOT / "site" / "artifact.html").write_text(inner, encoding="utf-8")

    print(f"{OUT.relative_to(ROOT)}: {len(html) // 1024} KB · {len(ev)} evidências "
          f"de {len(coded)} sessões · {len(dims_cov)}/{len(d['dimensions'])} dimensões com evidência "
          f"· {len(tri)} trianguladas · {len(div)} divergência(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
