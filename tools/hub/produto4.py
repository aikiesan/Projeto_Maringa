# -*- coding: utf-8 -*-
"""O Produto 04 como pagina do Hub, gerado a partir do `.docx`.

Nao ha texto recopiado a mao: o documento e lido de `anexos/Produto_4.docx` a
cada build. Se o relatorio mudar, a pagina muda junto — e se o arquivo errado for
apontado, a conversao aborta (ver `guarda`).

O que esta pagina acrescenta ao documento e uma coisa so, e e a razao de ela
existir: **cada afirmacao da Secao 3 fica ligada a evidencia que a sustenta.**
Afirmacao cuja ancora foi aceita na revisao humana vira link para o painel
filtrado naquele ponto; afirmacao sem ancora aceita fica sem link, marcada e
contada. Ausencia de evidencia e resultado, inclusive sobre o proprio texto.

Armadilhas do documento, todas tratadas aqui:
  - o capitulo 4 usa `Ttulo3` onde semanticamente seria `Ttulo2`, de modo que
    mapear estilo para nivel produz hierarquia quebrada;
  - ha um `Ttulo1` vazio e um `PargrafodaLista` vazio;
  - a numeracao «3.», «4.» vem da numeracao automatica do Word e NAO esta no
    texto — os capitulos sao numerados por posicao;
  - as 8 tabelas nao aparecem em `d.paragraphs`: vivem em `body`, intercaladas,
    e sao lidas na ordem do corpo;
  - o sumario do Word e um `sdt` e e descartado: a pagina tem o seu proprio.
"""
from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOCX = ROOT / "anexos" / "Produto_4.docx"

# a mesma trava de tools/p4_ancorar, pela mesma razao: existe uma copia de 328
# paragrafos, sem o capitulo 4, as Consideracoes Finais e os Anexos, e ela e mais
# nova no disco.
PARAGRAFOS_ESPERADOS = 367
ULTIMO_TITULO = "Nota sobre a anonimização das transcrições (Anexo 05)"
TITULO_SECAO3 = "ANÁLISE E RESUMO"
TITULO_CAP4 = "RELAÇÃO COM O PLANO DE AÇÃO"


def E(s) -> str:
    return html.escape(str(s if s is not None else ""))


def _slug(s: str) -> str:
    s = re.sub(r"[^\w\s-]", "", s.lower(), flags=re.U)
    return re.sub(r"[\s_-]+", "-", s).strip("-")[:60] or "sec"


class Bloco:
    """Um elemento do corpo, ja classificado."""

    __slots__ = ("tipo", "estilo", "texto", "html", "idx", "sid")

    def __init__(self, tipo, estilo="", texto="", html_="", idx=-1):
        self.tipo, self.estilo, self.texto, self.html, self.idx = \
            tipo, estilo, texto, html_, idx


def guarda(doc, caminho: Path) -> None:
    n = len(doc.paragraphs)
    titulos = [p.text.strip() for p in doc.paragraphs
               if p.style.name.startswith("Heading") and p.text.strip()]
    ultimo = titulos[-1] if titulos else ""
    if n != PARAGRAFOS_ESPERADOS or ultimo != ULTIMO_TITULO:
        linhas = [
            "DOCX ERRADO: " + str(caminho),
            "  paragrafos: %d (esperado %d)" % (n, PARAGRAFOS_ESPERADOS),
            "  ultimo titulo: %r" % (ultimo,),
            "  esperado:      %r" % (ULTIMO_TITULO,),
            "  A fonte e anexos/Produto_4.docx. A copia de 328 paragrafos nao tem",
            "  o capitulo 4, as Consideracoes Finais nem os Anexos.",
        ]
        raise SystemExit(chr(10).join(linhas))


def _runs_html(par) -> str:
    """Texto do paragrafo com negrito e italico preservados."""
    out = []
    for r in par.runs:
        t = E(r.text)
        if not t:
            continue
        if r.bold:
            t = f"<strong>{t}</strong>"
        if r.italic:
            t = f"<em>{t}</em>"
        out.append(t)
    return "".join(out) or E(par.text)


# Quadros nominais do documento. Cada um lista pessoas com nome, instituicao e,
# em dois deles, cargo. O Quadro 02 e a chave de reidentificacao do corpus
# inteiro: nome + instituicao + cargo dos entrevistados, ao lado de um Hub em que
# cada sessao e rotulada por setor e tipo institucional — o cruzamento e imediato.
# Na versao publica eles sao substituidos pela CONTAGEM que sustentam, derivada do
# codebook. O numero que o quadro provava continua na pagina; a lista nominal,
# nao. O documento completo segue sendo a entrega a coordenacao, por outro canal.
CABECALHOS_NOMINAIS = ("nome", "entrevistado", "entrevistado(a)", "participante")


def _e_nominal(tab) -> bool:
    if not tab.rows:
        return False
    prim = [c.text.strip().lower() for c in tab.rows[0].cells]
    return any(h in CABECALHOS_NOMINAIS for h in prim)


def _tabela_html(tab) -> str:
    if _e_nominal(tab):
        n = max(0, len(tab.rows) - 1)
        cols = [c.text.strip() for c in tab.rows[0].cells if c.text.strip()]
        outras = ", ".join(c.lower() for c in cols
                           if c.lower() not in CABECALHOS_NOMINAIS and c != "#")
        return (f'<div class="quadro-suprimido">'
                f'<p><strong>Quadro nominal suprimido na versão pública.</strong> '
                f'{n} pessoas, com {E(outras)}. As entrevistas foram concedidas sob '
                f'termo de consentimento que garante confidencialidade: publicar a '
                f'lista nominal ao lado do corpus identificaria os participantes de '
                f'cada sessão. A lista existe no documento entregue à coordenação.</p>'
                f'</div>')
    linhas = []
    for i, row in enumerate(tab.rows):
        tag = "th" if i == 0 else "td"
        cels = "".join(f"<{tag}>{E(c.text.strip())}</{tag}>" for c in row.cells)
        linhas.append(f"<tr>{cels}</tr>")
    corpo = "".join(linhas)
    return (f'<div class="rolo"><table class="quadro">'
            f"<tbody>{corpo}</tbody></table></div>")


def ler(caminho: Path = DOCX, suprimir: bool = True) -> list[Bloco]:
    """Blocos do documento, na ordem do corpo — paragrafos e tabelas.

    Com `suprimir`, aplica `codebook/supressoes.csv` ao texto e ao HTML de cada
    paragrafo. Se uma supressao declarada nao casar, a leitura FALHA: publicar o
    documento sem um corte declarado e pior do que nao publicar.
    """
    import docx
    from docx.table import Table
    from docx.text.paragraph import Paragraph

    doc = docx.Document(str(caminho))
    guarda(doc, caminho)

    blocos, i = [], 0
    for filho in doc.element.body.iterchildren():
        tag = filho.tag.split("}")[-1]
        if tag == "p":
            par = Paragraph(filho, doc)
            estilo = par.style.name
            texto = par.text.strip()
            blocos.append(Bloco("p", estilo, texto, _runs_html(par), i))
            i += 1
        elif tag == "tbl":
            blocos.append(Bloco("tbl", "", "", _tabela_html(Table(filho, doc))))
        # `sdt` (sumario do Word) e `sectPr` sao descartados de proposito

    if suprimir:
        _suprimir(blocos)
    return blocos


def _suprimir(blocos: list[Bloco]) -> int:
    import sys
    sys.path.insert(0, str(ROOT))
    from tools.supressoes import carregar, aplicar_em
    por_idx = {b.idx: b for b in blocos if b.tipo == "p"}
    n = 0
    for sup in carregar():
        if sup.fonte != "produto4":
            continue
        b = por_idx.get(sup.paragrafo)
        if b is None:
            raise SystemExit(f"supressao declarada para §{sup.paragrafo}, "
                             f"que nao existe no documento")
        b.texto = aplicar_em(b.texto, sup)
        b.html = aplicar_em(b.html, sup)
        n += 1
    return n


# --------------------------------------------------------------- estrutura

def estrutura(blocos: list[Bloco]) -> list[dict]:
    """Capitulos, na ordem, com nivel corrigido.

    O nivel vem da POSICAO, nao do estilo. No capitulo 4 o autor usou `Ttulo3`
    para o que e, semanticamente, subsecao de primeiro nivel — mapear estilo a
    nivel ali produziria um h4 orfao sob um h2.
    """
    caps, atual, dentro_cap4 = [], None, False
    for b in blocos:
        if b.tipo == "p" and b.estilo == "Heading 1" and b.texto:
            dentro_cap4 = TITULO_CAP4 in b.texto
            atual = {"titulo": b.texto, "n": len(caps) + 1, "blocos": [],
                     "id": f"cap-{len(caps) + 1}-{_slug(b.texto)}",
                     "secao3": TITULO_SECAO3 in b.texto, "subs": []}
            caps.append(atual)
            continue
        if atual is None:
            continue          # capa e sumario, antes do primeiro capitulo
        if b.tipo == "p" and b.estilo in ("Heading 2", "Heading 3") and b.texto:
            nivel = 2 if (b.estilo == "Heading 2" or dentro_cap4) else 3
            sid = f"{atual['id']}--{_slug(b.texto)}"
            atual["subs"].append({"titulo": b.texto, "nivel": nivel, "id": sid})
            b.sid = sid
        atual["blocos"].append(b)
    return caps


def sumario(caps: list[dict]) -> str:
    itens = []
    for c in caps:
        subs = "".join(
            f'<li class="n{s["nivel"]}"><a href="#{E(s["id"])}">{E(s["titulo"])}</a></li>'
            for s in c["subs"])
        itens.append(f'<li class="n1"><a href="#{E(c["id"])}">'
                     f'<span class="cn">{c["n"]}</span>{E(c["titulo"])}</a></li>'
                     + (f"<li><ul>{subs}</ul></li>" if subs else ""))
    return f'<nav class="sumario" aria-label="Sumário do Produto 04"><ul>{"".join(itens)}</ul></nav>'


# ------------------------------------------------------------------ render

def _link_ancora(r: dict) -> str:
    """Link para o painel filtrado no ponto exato da evidencia.

    Por FILTRO e nao por fragmento: (sessao, dimensao, marca de tempo) nao e
    chave — 32 triplas do corpus tem mais de uma evidencia. Filtrar mostra todas
    as daquele ponto, que e a resposta correta, e nao depende da paginacao.
    """
    alvo = (f'painel.html#evidencias?int={r["interview"]}'
            f'&dim={r["dim"]}&ts={r["ts"]}')
    titulo = (f'{r["interview"]} · {r["ts"]} · dimensão {r["dim"]}: '
              f'{r["dim_nome"]}')
    return (f'<a class="anc" href="{E(alvo)}" title="{E(titulo)}">'
            f'<span class="mono">{E(r["interview"])}</span>'
            f'<span class="anc-ts mono">{E(r["ts"])}</span>'
            f'<span class="anc-dim mono">{E(r["dim"])}</span></a>')


ROTULO = {
    "humano": ("âncora revisada", "Âncora conferida por leitura humana."),
    "automatico": ("âncora por critério automático",
                   "Selecionada por critério declarado: confiança alta, peso "
                   "informacional dos termos compartilhados e margem sobre a "
                   "segunda candidata. Não passou por leitura humana."),
}


def _afirmacao(b: Bloco, n: int, aceitas: dict) -> str:
    """Uma afirmacao da Secao 3, com ou sem ancora aceita.

    O rotulo declara QUEM decidiu. Uma ancora escolhida por criterio automatico
    nao e uma ancora validada, e a pagina nao pode dizer que e: a procedencia da
    afirmacao e o que esta publicacao oferece.
    """
    rs = aceitas.get(str(n), [])
    if rs:
        origem = rs[0].get("decisor") or "automatico"
        rot, dica = ROTULO.get(origem, ROTULO["automatico"])
        links = "".join(_link_ancora(r) for r in rs)
        return (f'<li class="af com origem-{E(origem)}" id="af-{n}">'
                f'<span class="af-n">{n}</span>{b.html}'
                f'<span class="ancs"><span class="origem" title="{E(dica)}">'
                f'{E(rot)}</span>{links}</span></li>')
    return (f'<li class="af sem" id="af-{n}">'
            f'<span class="af-n">{n}</span>{b.html}'
            f'<span class="sem-anc" title="Nenhuma candidata satisfez o critério '
            f'de seleção para esta afirmação">sem âncora</span></li>')


def corpo_capitulo(cap: dict, afirm_n: dict, aceitas: dict) -> str:
    """HTML de um capitulo. `afirm_n` mapeia id(bloco) -> numero da afirmacao."""
    out, lista_aberta = [], False

    def fecha():
        nonlocal lista_aberta
        if lista_aberta:
            out.append("</ul>")
            lista_aberta = False

    for b in cap["blocos"]:
        if b.tipo == "tbl":
            fecha()
            out.append(b.html)
            continue
        if not b.texto:
            continue
        est = b.estilo
        if est in ("Heading 2", "Heading 3"):
            fecha()
            nivel = next((s["nivel"] for s in cap["subs"] if s["id"] == b.sid), 3)
            tag = "h3" if nivel == 2 else "h4"
            out.append(f'<{tag} id="{E(b.sid)}">{b.html}</{tag}>')
        elif est == "Quote":
            fecha()
            out.append(f"<blockquote>{b.html}</blockquote>")
        elif est == "Tabela":
            fecha()
            out.append(f'<p class="quadro-leg">{b.html}</p>')
        elif est == "List Paragraph":
            if not lista_aberta:
                out.append('<ul class="afs">')
                lista_aberta = True
            n = afirm_n.get(id(b))
            out.append(_afirmacao(b, n, aceitas) if n
                       else f"<li>{b.html}</li>")
        else:
            fecha()
            out.append(f"<p>{b.html}</p>")
    fecha()
    return "".join(out)


def numerar_afirmacoes(caps: list[dict]) -> tuple[dict, int, int]:
    """Mapeia cada `List Paragraph` da Secao 3 ao numero que `p4_ancorar` usa.

    A numeracao TEM de ser a mesma, senao a afirmacao recebe a ancora de outra.
    Ela e reproduzida aqui pela mesma regra — ordem dos paragrafos de lista nao
    vazios dentro da Secao 3 — e conferida contra o proprio `p4_ancorar`, que le
    o arquivo por outro caminho (regex sobre o XML). Se as duas divergirem, a
    construcao para.
    """
    cap3 = next((c for c in caps if c["secao3"]), None)
    if cap3 is None:
        raise SystemExit("Secao 3 (ANALISE E RESUMO...) nao encontrada no docx")
    lista = [b for b in cap3["blocos"]
             if b.tipo == "p" and b.estilo == "List Paragraph" and b.texto]

    import sys
    sys.path.insert(0, str(ROOT))
    from tools import p4_ancorar as PA
    af = PA.afirmacoes(DOCX)
    # `p4_ancorar` le o arquivo cru; os blocos daqui ja passaram pelas
    # supressoes. Para comparar, aplica-se a mesma supressao ao outro lado.
    from tools.supressoes import carregar, aplicar_em, SupressaoNaoAplicada
    sups = [x for x in carregar() if x.fonte == "produto4"]
    textos_pa = []
    for a in af:
        t = a["texto"]
        for x in sups:
            try:
                t = aplicar_em(t, x)
            except SupressaoNaoAplicada:
                pass          # esta supressao e de outro paragrafo
        textos_pa.append(t)
    if textos_pa != [b.texto for b in lista]:
        raise SystemExit(
            "As afirmacoes da Secao 3 divergem entre os dois extratores "
            "(python-docx x regex do XML). A numeracao das ancoras nao pode ser "
            "confiada — corrija antes de publicar.")

    mapa, chamadas = {}, 0
    for a, b in zip(af, lista):
        if a["chamada"]:
            chamadas += 1
            continue        # chamada de lista, nao afirmacao: nao recebe ancora
        mapa[id(b)] = a["n"]
    return mapa, len(af) - chamadas, chamadas


# ------------------------------------------------------------------ matriz

def matriz(sub: list[dict]) -> str:
    """A Matriz de Avaliacao que o TdR exige (Produto 1, §2.2).

    Vem de `tools.p4_base`, a mesma fonte de `produtos/P4_matriz_v2.md` — a
    pagina nao le o markdown ja gerado, le o dado.

    A maturidade e por MODA, nao por media, e a coluna «perfil» diz por que:
    a distribuicao e bimodal na maioria das subcategorias, e nessas uma media
    aponta um estagio que quase nenhuma evidencia sustenta.
    """
    linhas = []
    for s in sub:
        polos = " / ".join(s.get("perfil_polos") or [])
        perfil = s["perfil"] + (f": {polos}" if polos else "")
        barra = (f'<span class="mini"><i style="width:{s["share_inexistente"]}%"></i></span>')
        linhas.append(
            f'<tr><td class="mono">{E(s["subcat"])}</td>'
            f'<td>{E(s["nome"])}</td>'
            f'<td class="n">{s["n_cobertas"]}/{s["n_dimensoes"]}</td>'
            f'<td class="n">{s["n_evidencias"]}</td>'
            f'<td class="n">{s["n_sessoes"]}</td>'
            f'<td><b>{E(s["maturidade_rotulo"])}</b></td>'
            f'<td class="n">{barra}{s["share_inexistente"]}%</td>'
            f'<td class="perfil">{E(perfil)}</td></tr>')
    bim = sum(1 for s in sub if s["perfil"] == "bimodal")
    return (
        '<div class="rolo"><table class="matriz"><thead><tr>'
        "<th>#</th><th>Subcategoria</th><th>Dim.</th><th>Evid.</th>"
        "<th>Sessões</th><th>Maturidade</th><th>% inexistente</th><th>Perfil</th>"
        f'</tr></thead><tbody>{"".join(linhas)}</tbody></table></div>'
        f'<p class="leg">As {len(sub)} subcategorias avaliadas. <b>Dim.</b> é quantas '
        f"dimensões da subcategoria receberam evidência, sobre o total. "
        f"<b>Maturidade</b> é a <em>moda</em>, isto é, o estágio mais registrado, não a "
        f"média: em {bim} das {len(sub)} subcategorias a distribuição é bimodal, e "
        f"nessas a média aponta um estágio intermediário que quase nenhuma evidência "
        f"sustenta. A coluna <b>perfil</b> declara a forma da distribuição e, quando "
        f"bimodal, os dois polos.</p>")


# ------------------------------------------------------------------ pagina

def pagina(m: dict, aceitas: dict, sub: list[dict], data_docx: str,
           bytes_docx: int) -> tuple[str, dict]:
    """Corpo da pagina do Produto 04. Devolve (html, resumo)."""
    blocos = ler()
    caps = estrutura(blocos)
    afirm_n, n_af, _ = numerar_afirmacoes(caps)

    com = sum(1 for n in afirm_n.values() if str(n) in aceitas)
    sem = n_af - com
    resumo = {"afirmacoes": n_af, "com_ancora": com, "sem_ancora": sem}

    secs = []
    for c in caps:
        marca = ""
        if c["secao3"]:
            ns = [n for n in afirm_n.values()]
            c_com = sum(1 for n in ns if str(n) in aceitas)
            marca = (f'<p class="contador"><b>{len(ns) - c_com} de {len(ns)}</b> '
                     f'afirmações desta seção ficaram <b>sem âncora</b>: nenhuma '
                     f'evidência do corpus satisfez o critério de seleção para '
                     f'elas. '
                     f'<button type="button" id="so-sem" aria-pressed="false">'
                     f'mostrar só essas</button></p>')
        secs.append(f'<section class="cap" id="{E(c["id"])}">'
                    f'<h2><span class="cn">{c["n"]}</span>{E(c["titulo"])}</h2>'
                    f"{marca}{corpo_capitulo(c, afirm_n, aceitas)}</section>")

    kpis = [(str(n_af), "afirmações na Seção 3"),
            (str(com), "com âncora de evidência"),
            (str(sem), "sem âncora"),
            (str(len(sub)), "subcategorias na matriz")]
    faixa = "".join(f'<div><b>{v}</b><span>{r}</span></div>' for v, r in kpis)

    aviso = (
        '<div class="nota"><p><strong>Como as âncoras foram escolhidas.</strong> '
        'Para cada afirmação da Seção 3, três candidatas foram levantadas por '
        'sobreposição de vocabulário com as ' + str(494) + ' evidências, e uma '
        'foi escolhida, ou nenhuma, por critério declarado: a evidência precisa '
        'ter sido codificada com <em>confiança alta</em>; a afirmação precisa '
        'afirmar algo (chamada de lista não ancora); os termos em comum precisam '
        'somar peso informacional suficiente, medido pela raridade de cada termo '
        'no próprio corpus; e a melhor candidata precisa vencer a segunda por '
        'margem. Empate não decide, e por isso não escolhe.</p>'
        '<p>O critério é conservador de propósito: ele recusa mais do que aceita, '
        'e erra para o lado de deixar sem âncora. Âncora errada afirmaria '
        'falsamente que a evidência existe; âncora ausente apenas mostra o que '
        'não foi possível estabelecer.</p>'
        '<p><strong>Seleção automática não é validação.</strong> As âncoras desta '
        'página trazem o rótulo <span class="origem">âncora por critério '
        'automático</span>; quando passarem por leitura, passam a trazer '
        '<span class="origem">âncora revisada</span>. O critério completo está em '
        '<code>tools/p4_selecao.py</code> e cada decisão, com seu motivo, em '
        '<code>produtos/P4_ancoras_revisao.csv</code>.</p></div>'
        if com else
        '<div class="nota alerta"><p><strong>Nenhuma âncora selecionada.</strong> '
        'A Seção 3 aparece sem ligações para o painel.</p></div>')

    return (f"""
<div class="p4-kpi">{faixa}</div>

<div class="nota">
  <p><strong>Como ler esta página.</strong> É o Produto 04 na íntegra, gerado a
  partir do documento entregue, e nada foi reescrito aqui. O que a versão web
  acrescenta está na Seção 3: cada afirmação recebe um número e, quando há âncora
  de evidência, links que abrem o painel filtrado no ponto exato: sessão,
  dimensão e marca de tempo. Afirmação sem âncora validada fica
  <span class="sem-anc exemplo">assim</span>, sem link e contada no topo da seção.</p>
</div>

{aviso}

<div class="p4-baixar">
  <a class="botao" href="Produto_04_publico.docx" download>Baixar em Word (.docx)</a>
  <span class="mut sm">Versão de {E(data_docx)}, editável. Nela os quatro quadros
  nominais de participantes aparecem como contagem: a lista de pessoas mobilizadas
  e entrevistadas é entregável do termo de referência e segue para a coordenação,
  mas publicá-la ao lado das transcrições identificaria quem falou em cada
  sessão.</span>
</div>

<div class="p4">
  <aside class="p4-sum">
    <details open><summary>Sumário</summary>{sumario(caps)}</details>
  </aside>
  <div class="p4-doc">{"".join(secs)}</div>
</div>

<h2 id="matriz">Matriz de Avaliação</h2>
{matriz(sub)}
""", resumo)


JS = """
<script>
(function () {
  var b = document.getElementById("so-sem");
  if (b) b.addEventListener("click", function () {
    var on = b.getAttribute("aria-pressed") !== "true";
    b.setAttribute("aria-pressed", on ? "true" : "false");
    b.textContent = on ? "mostrar todas" : "mostrar só essas";
    document.querySelectorAll("li.af.com").forEach(function (li) {
      li.hidden = on;
    });
  });
  // sumario: destaca a secao corrente
  var alvos = document.querySelectorAll(".p4-doc section.cap[id], .p4-doc h3[id]");
  var links = {};
  document.querySelectorAll(".p4-sum a").forEach(function (a) {
    links[a.getAttribute("href").slice(1)] = a;
  });
  if (!("IntersectionObserver" in window) || !alvos.length) return;
  var io = new IntersectionObserver(function (ents) {
    ents.forEach(function (e) {
      var a = links[e.target.id];
      if (a) a.classList.toggle("aqui", e.isIntersecting);
    });
  }, {rootMargin: "-72px 0px -70% 0px"});
  alvos.forEach(function (t) { io.observe(t); });
})();
</script>
"""
