# -*- coding: utf-8 -*-
"""Gera o Hub inteiro em hub_saida/, na raiz do projeto.

    python -m tools.hub.build

Tudo é derivado: codebook, bases do Produto 3, listagem da legislação e as
transcrições anonimizadas. Nenhum número é digitado à mão.
"""
import os, sys, csv, json, glob, shutil, io, zipfile, tempfile, contextlib, datetime
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



def _painel_documento(corpo: str) -> str:
    """Embrulha o painel num documento HTML de verdade.

    `site/publico.html` e corpo de Artifact: comeca em <style>, sem <!doctype>,
    <html>, <head>, <meta charset>, <title> nem lang. Servido pelo GitHub Pages
    funciona por acidente — o charset vem no cabecalho HTTP —, mas aberto de
    qualquer outro lugar a acentuacao quebra inteira, e sem <title> e sem lang a
    pagina reprova acessibilidade. O conteudo NAO e alterado; so ganha a casca.
    """
    if corpo.lstrip()[:9].lower().startswith("<!doctype"):
        return corpo
    cabeca = [
        "<!doctype html>",
        '<html lang="pt-BR">',
        "<head>",
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width,initial-scale=1">',
        "<title>Painel de evidencias &mdash; Maringa em Acao pelo Clima</title>",
        '<meta name="description" content="As 494 evidencias codificadas das '
        '17 sessoes, filtraveis por eixo, tipo, setor, sessao e dimensao.">',
        "</head>",
        "<body>",
    ]
    nl = chr(10)
    return nl.join(cabeca) + nl + corpo + nl + "</body>" + nl + "</html>" + nl



def _ancoras_aceitas():
    """Ancoras que passaram pela revisao humana. So elas viram link.

    Le `produtos/P4_ancoras_revisao.csv`. Enquanto ninguem revisar, o dicionario
    vem vazio e a pagina mostra todas as afirmacoes como «sem ancora validada» —
    que e a verdade, nao um defeito.
    """
    sys.path.insert(0, str(ROOT))
    from tools.p4_revisao import aceitas
    return aceitas()



def _conferir_css(css: str) -> None:
    """Nenhuma variavel de CSS pode ser usada sem estar definida.

    Declaracao que referencia variavel inexistente nao aplica — e nao avisa. O
    sintoma e sutil: a regra some, o elemento herda, e a pagina parece «quase
    certa». Ja aconteceu com `--card`, `--bg` e `--ink3`, que nunca existiram.
    """
    import re
    definidas = set(re.findall(r"(--[\w-]+)\s*:", css))
    usadas = set(re.findall(r"var\((--[\w-]+)\)", css))
    faltam = sorted(usadas - definidas)
    if faltam:
        raise SystemExit("CSS usa variaveis nao definidas: " + ", ".join(faltam))


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
        "a base documental, o mapeamento de atores e o arcabouço legal — "
        "<strong>cada afirmação ligada à evidência que a sustenta</strong>.")
    h_ini += faixa_kpi([
        (m["sessoes"], f"sessões de entrevista, {m['horas']} de escuta"),
        (m["evidencias"], "evidências rastreáveis até o trecho"),
        (f"{m['dimensoes_com_evidencia']}/{m['dimensoes_total']}",
         f"dimensões com evidência, {m['trianguladas']} trianguladas"),
        (len(c["membros"]), "conselheiros mapeados em seis anos"),
    ])
    escreve("index.html", pagina(
        "index.html", "Início",
        "Hub do projeto Maringá em Ação pelo Clima: evidências, conselhos, "
        "instituições, legislação e o Produto 04 na íntegra.",
        P.inicio(m, c, orgs, leis), hero=h_ini))

    # ------------------------------------------------ Produto 04
    import produto4 as P4
    from tools import p4_base as PB
    _dx = P4.DOCX
    _corpo_p4, _res_p4 = P4.pagina(
        m, _ancoras_aceitas(), PB.base()["subcategorias"],
        datetime.date.fromtimestamp(_dx.stat().st_mtime).strftime("%d/%m/%Y"),
        _dx.stat().st_size)
    escreve("produto4.html", pagina(
        "produto4.html", "Produto 04",
        "O Produto 04 da consultoria IPPLAM-CEPAL em versao web navegavel, com a "
        "Matriz de Avaliacao e as afirmacoes ligadas a evidencia que as sustenta.",
        _corpo_p4, P4.JS,
        hero=hero("Produto 04", "Síntese das consultas",
                  "Relatório parcial da consultoria sobre condições habilitantes ao "
                  "financiamento climático urbano de Maringá.")))
    # o .docx NAO e publicado: contem os quadros nominais de participantes
    print(f"  produto4: {_res_p4['afirmacoes']} afirmações, "
          f"{_res_p4['com_ancora']} com âncora, {_res_p4['sem_ancora']} sem")

    escreve("conselhos.html", pagina(
        "conselhos.html", "Conselhos",
        f"Os {len(c['membros'])} conselheiros do COMDEMA entre 2021 e 2026, "
        "com análise de continuidade e composição por grupo.",
        P.conselhos(c), P.JS_BUSCA))

    escreve("instituicoes.html", pagina(
        "instituicoes.html", "Instituições",
        f"As {len(orgs)} organizações mapeadas no Produto 3, por dimensão da "
        "metodologia CCFLA/CEPAL.",
        P.instituicoes(orgs), P.JS_BUSCA))

    escreve("legislacao.html", pagina(
        "legislacao.html", "Legislação",
        f"As {len(leis)} normas municipais do arcabouço climático de Maringá.",
        P.legislacao_pg(leis), P.JS_BUSCA))

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
    for nome in ("brisa.png", "onda.png", "cepal.png"):
        shutil.copy(ROOT / "assets" / "marca" / nome, md / nome)

    # -------------------------------------------------- painel existente
    if PAINEL.exists():
        escreve("painel.html", _painel_documento(PAINEL.read_text(encoding="utf-8")))

    # relatório
    n = sum(1 for _ in SAIDA.rglob("*") if _.is_file())
    print(f"{n} arquivos em {SAIDA}")
    for p in sorted(SAIDA.rglob("*.html")):
        print(f"  {p.relative_to(SAIDA)}  {p.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
