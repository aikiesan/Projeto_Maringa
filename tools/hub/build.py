# -*- coding: utf-8 -*-
"""Gera o Hub inteiro em hub_saida/, na raiz do projeto.

    python -m tools.hub.build

Tudo é derivado: codebook, bases do Produto 3, listagem da legislação e as
transcrições anonimizadas. Nenhum número é digitado à mão.
"""
import os, sys, csv, json, glob, shutil, io, zipfile, tempfile, contextlib, datetime, re
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dados as D
from base import CSS, pagina, hero, faixa_kpi
import paginas as P
import transcricoes as T

ROOT = Path(__file__).resolve().parents[2]
SAIDA = ROOT / "hub_saida"
ANON = ROOT / "saida_anonimizacao"
ANON_ZIP = ROOT / "anexos" / "Anexo_05_Transcricoes_Anonimizadas.zip"
BASE_URL = "https://aikiesan.github.io/Maringa/"
PAINEL = ROOT / "site" / "publico.html"
UP = ROOT



@contextlib.contextmanager
def _fonte_transcricoes():
    """Diretorio com os .docx anonimizados.

    Prefere `saida_anonimizacao/` quando existe (a saida corrente de
    `anonimizar_transcricoes.py`); senao extrai o Anexo 05 para um diretorio
    temporario que e apagado no fim — o acervo nao deve deixar copia solta.
    """
    if ANON.is_dir() and any(ANON.glob("*.docx")):
        yield ANON
        return
    if ANON_ZIP.exists():
        with tempfile.TemporaryDirectory(prefix="hub_transc_") as td:
            with zipfile.ZipFile(ANON_ZIP) as z:
                z.extractall(td)
            yield Path(td)
        return
    yield None




# A altura da barra do Hub muda com a largura da tela. As abas do painel sao
# sticky em top:0 e passariam por baixo dela; o deslocamento e MEDIDO no
# carregamento e a cada redimensionamento, porque um valor fixo erra em algum
# tamanho de tela e o sintoma (aba escondida atras da barra) so aparece rolando.
HUBBAR_JS = (
    "<script>(function(){"
    "function medir(){"
    "var b=document.querySelector('.hubbar');"
    "if(!b)return;"
    "document.documentElement.style.setProperty('--hubbar-h',"
    "Math.round(b.getBoundingClientRect().height)+'px');"
    "}"
    "addEventListener('resize',medir);"
    "addEventListener('DOMContentLoaded',medir);"
    "medir();"
    "})();</" "script>"
)

def _painel_documento(corpo: str) -> str:
    """Embrulha o painel num documento HTML de verdade, com o cabecalho do Hub.

    `site/publico.html` e corpo de Artifact: comeca em <style>, sem <!doctype>,
    <html>, <head>, <meta charset>, <title> nem lang. Servido pelo GitHub Pages
    funciona por acidente, porque o charset vem no cabecalho HTTP, mas aberto de
    qualquer outro lugar a acentuacao quebra inteira.

    O cabecalho e o MESMO de todas as paginas: vem de `cabecalho.py`. Como o
    painel nao carrega o `hub.css`, o CSS do cabecalho e os tokens de cor de que
    ele depende sao embutidos aqui. Sem os tokens, a barra ficaria sem cor e o
    modo escuro nao a alcancaria.
    """
    if corpo.lstrip()[:9].lower().startswith("<!doctype"):
        return corpo
    from base import NAV, CSS as CSS_HUB
    import cabecalho as CAB

    tokens = _tokens_de(CSS_HUB)

    estilo = ("<style>" + tokens + CAB.CSS +
              # as abas do painel sao sticky em top:0 e passariam por baixo da
              # barra; o deslocamento e medido em tempo de execucao
              "nav.tabs{top:var(--hubbar-h,58px)!important;z-index:20!important}"
              "</style>")
    cabeca = [
        "<!doctype html>",
        '<html lang="pt-BR">',
        "<head>",
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width,initial-scale=1">',
        "<title>Painel de evidências · Maringá em Ação pelo Clima</title>",
        '<meta name="description" content="As 494 evidências codificadas '
        'das 17 sessões, filtráveis por eixo, tipo, setor, sessão '
        'e dimensão.">',
        '<link rel="icon" href="marca/projeto.png" type="image/png">',
        CAB.JS_PRE,
        estilo,
        "</head>",
        "<body>",
    ]
    nl = chr(10)
    return (nl.join(cabeca) + nl + CAB.marcacao("painel.html", NAV) + nl
            + '<div id="conteudo">' + corpo + "</div>" + nl
            + CAB.JS_POS + nl + "</body>" + nl + "</html>" + nl)


def _tokens_de(css: str) -> str:
    """Extrai do hub.css apenas as declaracoes de token (:root e seus temas).

    O painel tem folha propria; trazer o hub.css inteiro brigaria com ela em
    seletores genericos (h2, p, table). So os tokens vem junto.
    """
    blocos = []
    for m in re.finditer(r"(@media[^{]*\{\s*)?(:root[^{]*\{[^}]*\})", css):
        if m.group(1):
            blocos.append(m.group(1) + m.group(2) + "}")
        else:
            blocos.append(m.group(2))
    return "".join(blocos)



def _conferir_css(css: str) -> None:
    """Nenhuma variavel de CSS pode ser usada sem estar definida.

    Declaracao que referencia variavel inexistente nao aplica, e nao avisa. O
    sintoma e sutil: a regra some, o elemento herda, e a pagina parece «quase
    certa». Ja aconteceu com `--card`, `--bg` e `--ink3`, que nunca existiram.
    """
    definidas = set(re.findall(r"(--[\w-]+)\s*:", css))
    usadas = set(re.findall(r"var\((--[\w-]+)\)", css))
    faltam = sorted(usadas - definidas)
    if faltam:
        raise SystemExit("CSS usa variaveis nao definidas: " + ", ".join(faltam))

    # Seletor orfao. Remover uma regra por regex pode deixar para tras o resto
    # do seletor anterior: `nav.menu{...}` virou `nav`, e o `nav` solto colou no
    # seletor seguinte, transformando `.hero-faixa` em `nav .hero-faixa`, que
    # nao casa com nada. A regra continua no arquivo, some da pagina, e o
    # sintoma foi texto branco sobre fundo transparente.
    sem_com = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    criticos = (".hero-faixa", ".hubbar", ".card", ".barra", ".p4-doc")
    for sel in criticos:
        achou = False
        for m in re.finditer(re.escape(sel) + r"[^{}]*\{", sem_com):
            antes = sem_com[:m.start()].rstrip()
            if not antes or antes[-1] in "}":
                achou = True
                break
        if not achou:
            raise SystemExit(
                f"CSS: a regra de {sel} nao comeca um bloco — provavel seletor "
                f"orfao colado antes dela. A regra existe no arquivo e nao "
                f"aplica na pagina.")



def _ancoras_aceitas():
    """Ancoras que passaram pelo criterio de selecao. So elas viram link.

    Le `produtos/P4_ancoras_revisao.csv`. A coluna `decisor` separa `humano` de
    `automatico`, e a pagina rotula a origem conforme ela.
    """
    sys.path.insert(0, str(ROOT))
    from tools.p4_revisao import aceitas
    return aceitas()


def _conferir_ancoras(html: str) -> int:
    """Todo link de ancora da pagina tem de resolver para evidencia existente.

    Tres invariantes, conferidos contra o codebook e contra o CSV de revisao: a
    evidencia existe; foi codificada com confianca alta; e esta marcada como
    aceita. Um link que erra o alvo afirma falsamente que a evidencia sustenta a
    afirmacao, e e o unico defeito desta pagina que nao se ve olhando.
    """
    ligs = re.findall(
        r'painel\.html#evidencias\?int=([^&"]+)&(?:amp;)?'
        r'dim=([^&"]+)&(?:amp;)?ts=([^"]+)', html)
    corpus, altas = set(), set()
    for arq in sorted(glob.glob(str(ROOT / "codebook" / "evidencias" / "ENT-*.csv"))):
        with open(arq, encoding="utf-8-sig", newline="") as f:
            for r in csv.DictReader(f):
                k = (r["interview"], r["dim"], r["ts"])
                corpus.add(k)
                if r["confidence"] == "alta":
                    altas.add(k)
    rev = ROOT / "produtos" / "P4_ancoras_revisao.csv"
    aceitas = set()
    if rev.exists():
        with rev.open(encoding="utf-8-sig", newline="") as f:
            aceitas = {(r["interview"], r["dim"], r["ts"])
                       for r in csv.DictReader(f) if r["decisao"] == "aceita"}
    problemas = []
    for l in ligs:
        k = tuple(l)
        if k not in corpus:
            problemas.append(f"{k}: evidencia inexistente")
        elif k not in altas:
            problemas.append(f"{k}: confianca nao e alta")
        elif aceitas and k not in aceitas:
            problemas.append(f"{k}: nao marcada como aceita no CSV de revisao")
    if problemas:
        raise SystemExit("ancoras invalidas na produto4.html: "
                         + chr(10) + "  ".join(problemas[:10]))
    return len(ligs)



def _res_kpi_ancoras() -> int:
    """Quantas afirmacoes da Secao 3 tem ancora aceita."""
    return len(_ancoras_aceitas())


def escreve(rel, txt):
    p = SAIDA / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(txt, encoding="utf-8")
    return p



def main():
    if SAIDA.exists():
        shutil.rmtree(SAIDA)
    SAIDA.mkdir(parents=True)

    m = D.metricas_corpus()
    c = D.comdema()
    orgs = D.organizacoes()
    leis = D.legislacao()
    ss = D.sessoes()
    ev = D.evidencias()

    # A pagina de dados e os arquivos que ela oferecia foram desativados em
    # 13/09/2026 a pedido. Removida a vitrine, os arquivos tambem saem: manter
    # `dados/*.csv` sem pagina que os liste nao os torna inacessiveis, so os
    # torna invisiveis — URL direta continua servindo.


    # ---------------------------------------------------------- páginas
    _conferir_css(CSS)
    escreve("hub.css", CSS)

    h_ini = hero(
        "Consultoria IPPLAM · CEPAL/ONU · Metodologia CCFLA",
        "Condições habilitantes ao financiamento climático urbano de Maringá",
        "Todo o material da avaliação, aberto e rastreável: a escuta institucional, "
        "a base documental, o mapeamento de atores e o arcabouço legal. "
        "<strong>cada afirmação ligada à evidência que a sustenta</strong>.")
    h_ini += faixa_kpi([
        (m["sessoes"], f"sessões de entrevista, {m['horas']} de escuta"),
        (m["evidencias"], "evidências rastreáveis até o trecho"),
        (f"{m['dimensoes_com_evidencia']}/{m['dimensoes_total']}",
         f"dimensões com evidência, {m['trianguladas']} trianguladas"),
        # o quarto numero era dos conselheiros, base do Produto 3, que saiu do
        # Hub em 13/09. Passou a ser a medida do produto corrente.
        (_res_kpi_ancoras(), "afirmações da Seção 3 ligadas à evidência"),
    ])
    escreve("index.html", pagina(
        "index.html", "Início",
        "Hub do projeto Maringá em Ação pelo Clima: evidências, conselhos, "
        "instituições, legislação e o Produto 04 na íntegra.",
        P.inicio(m, c, orgs, leis), hero=h_ini))

    sys.path.insert(0, str(ROOT))
    from tools import p4_base as PB
    escreve("projeto.html", pagina(
        "projeto.html", "O projeto",
        "O que é a consultoria IPPLAM–CEPAL sobre condições habilitantes ao "
        "financiamento climático urbano de Maringá, como a evidência foi "
        "produzida e sob que regras.",
        P.projeto(m, c, orgs, leis, PB.base()["subcategorias"]),
        hero=hero("O projeto", "Como esta avaliação foi feita",
                  "A metodologia, a unidade de registro, as regras declaradas e os "
                  "limites assumidos.")))

    # As paginas de conselhos e legislacao sairam em 13/09: eram de produto
# anterior, nao sao citadas no relatorio, e a de conselhos publicava 124
# nomes nominalmente — incoerente com a remocao do tipo institucional
# feita no mesmo dia para impedir o cruzamento pessoa x sessao.

    # ------------------------------------------------ Produto 04
    import produto4 as P4
    _dx = P4.DOCX
    _corpo_p4, _res_p4 = P4.pagina(
        m, _ancoras_aceitas(), PB.base()["subcategorias"],
        datetime.date.fromtimestamp(_dx.stat().st_mtime).strftime("%d/%m/%Y"),
        _dx.stat().st_size)
    _n_lig = _conferir_ancoras(_corpo_p4)
    escreve("produto4.html", pagina(
        "produto4.html", "Produto 04",
        "O Produto 04 da consultoria IPPLAM–CEPAL em versão web navegável, "
        "com a Matriz de Avaliação e cada afirmação da Seção 3 ligada à "
        "evidência que a sustenta.",
        _corpo_p4, P4.JS,
        hero=hero("Produto 04", "Síntese das consultas",
                  "Relatório parcial da consultoria sobre condições habilitantes ao "
                  "financiamento climático urbano de Maringá.")))
    # versao publica e editavel do relatorio, gerada pelo mesmo processo da
    # pagina: supressoes aplicadas e quadros nominais trocados pela contagem.
    from tools.p4_docx_publico import gerar as _gerar_docx
    _r = _gerar_docx(destino=SAIDA / "Produto_04_publico.docx")
    print(f"  Produto_04_publico.docx: {_r['supressoes']} supressões, "
          f"{_r['quadros']} quadros agregados, {_r['bytes'] // 1024} KB")
    print(f"  produto4: {_res_p4['afirmacoes']} afirmações, "
          f"{_res_p4['com_ancora']} com âncora, {_res_p4['sem_ancora']} sem "
          f"— {_n_lig} links conferidos contra o codebook")


    escreve("instituicoes.html", pagina(
        "instituicoes.html", "Instituições",
        f"As {len(orgs)} organizações mapeadas no Produto 3, por dimensão da "
        "metodologia CCFLA/CEPAL.",
        P.instituicoes(orgs), P.JS_BUSCA))


    # -------------------------------------------------- transcrições
    cabs = {}
    corpos = {}
    with _fonte_transcricoes() as origem:
        docx_transc = sorted(glob.glob(str(origem / "*.docx"))) if origem else []
        for f in docx_transc:
            cod, cab, corpo = T.converte(f)
            cabs[cod] = cab
            corpos[cod] = corpo
    if not corpos:
        print("AVISO: nenhuma transcricao encontrada — nem " + str(ANON)
              + " nem " + str(ANON_ZIP) + ". O indice sairá vazio.")

    por_cod = {s["code"]: s for s in ss}
    for cod, corpo in corpos.items():
        html_pg = pagina("transcricoes.html", cod,
                         f"Transcrição anonimizada da sessão {cod}.",
                         T.pagina_transcricao(cod, cabs[cod], corpo,
                                              por_cod.get(cod)))
        # a página vive num subdiretório: ajusta os caminhos relativos
        html_pg = html_pg.replace('href="hub.css"', 'href="../hub.css"')
        for h, _ in __import__("base").NAV:
            html_pg = html_pg.replace(f'href="{h}"', f'href="../{h}"')
        html_pg = html_pg.replace('href="../transcricoes.html">&larr;',
                                  'href="../transcricoes.html">&larr;')
        escreve(f"transcricoes/{cod}.html", html_pg)

    escreve("transcricoes.html", pagina(
        "transcricoes.html", "Transcrições",
        f"As {len(ss)} entrevistas na íntegra, em camada anonimizada.",
        T.indice(ss, cabs), P.JS_BUSCA))


    # -------------------------------------------------- marca
    md = SAIDA / "marca"
    md.mkdir()
    for nome in ("brisa.png", "onda.png", "cepal.png",
                 "projeto.png", "projeto-branco.png"):
        shutil.copy(ROOT / "assets" / "marca" / nome, md / nome)

    # -------------------------------------------------- painel existente
    if PAINEL.exists():
        escreve("painel.html", _painel_documento(PAINEL.read_text(encoding="utf-8")))

    # -------------------------------------------------- sitemap
    from base import NAV as _NAV
    _hoje = datetime.date.today().isoformat()
    _urls = [h for h, _ in _NAV] + [f"transcricoes/{c}.html" for c in sorted(corpos)]
    _xml = ['<?xml version="1.0" encoding="UTF-8"?>',
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in _urls:
        _xml.append(f"<url><loc>{BASE_URL}{u}</loc><lastmod>{_hoje}</lastmod></url>")
    _xml.append("</urlset>")
    escreve("sitemap.xml", chr(10).join(_xml))
    escreve("robots.txt", f"User-agent: *{chr(10)}Allow: /{chr(10)}"
                          f"Sitemap: {BASE_URL}sitemap.xml{chr(10)}")

    # relatório
    n = sum(1 for _ in SAIDA.rglob("*") if _.is_file())
    print(f"{n} arquivos em {SAIDA}")
    for p in sorted(SAIDA.rglob("*.html")):
        print(f"  {p.relative_to(SAIDA)}  {p.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
