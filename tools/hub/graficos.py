# -*- coding: utf-8 -*-
"""Graficos descritivos do Hub. HTML e CSS puros, sem biblioteca e sem SVG.

Regra que governa este modulo: **o grafico mostra a contagem, nao a leitura da
contagem.** A legenda diz o que se ve — «206 das 494 evidencias registram a
condicao como inexistente» — e nao o que isso significaria. A interpretacao,
quando existir, e do relatorio, assinada, e nao da figura.

Cada figura carrega:
  - titulo e legenda factual;
  - rotulo de valor visivel em toda marca (a paleta clara reprova o piso de
    contraste de 3:1 em duas series, e o rotulo e o alivio exigido);
  - uma tabela com os numeros, em <details>, que e a versao acessivel e
    tambem o substituto do download que a pagina de dados oferecia;
  - `title` por marca, que e o tooltip possivel sem JavaScript.

A paleta categorica vem de `base.py` e NAO se altera aqui: foi validada nos dois
modos (pior par adjacente DeltaE 9.2 protan/deutan, 27.6 visao normal).
"""
from __future__ import annotations

import html


def E(s) -> str:
    return html.escape(str(s if s is not None else ""))


def _pct(v, tot):
    return (100.0 * v / tot) if tot else 0.0


def tabela(colunas: list[str], linhas: list[tuple]) -> str:
    """Tabela dos numeros que a figura mostra. Sempre presente."""
    th = "".join(f"<th>{E(c)}</th>" for c in colunas)
    tr = "".join(
        "<tr>" + "".join(
            f'<td class="n">{E(c)}</td>' if isinstance(c, (int, float))
            else f"<td>{E(c)}</td>" for c in ln) + "</tr>"
        for ln in linhas)
    return (f'<details class="numeros"><summary>ver os números</summary>'
            f'<div class="rolo"><table><thead><tr>{th}</tr></thead>'
            f"<tbody>{tr}</tbody></table></div></details>")


def figura(titulo: str, grafico: str, legenda_txt: str = "",
           numeros: str = "", id_: str = "") -> str:
    """Envolve um grafico com titulo, legenda factual e a tabela de numeros."""
    ident = f' id="{E(id_)}"' if id_ else ""
    cap = (f'<figcaption class="leg">{legenda_txt}</figcaption>'
           if legenda_txt else "")
    return (f'<figure class="fig"{ident}>'
            f'<h3 class="fig-t">{E(titulo)}</h3>'
            f"{grafico}{cap}{numeros}</figure>")


def barras(itens, cor="var(--s1)", maximo=None, sufixo="", total=None):
    """Barras horizontais. `itens` e [(rotulo, valor)].

    Com `total`, acrescenta a fracao ao rotulo de valor — e leitura direta da
    propria contagem, nao inferencia.
    """
    vals = [v for _, v in itens]
    m = maximo or max(vals, default=1) or 1
    linhas = []
    for rot, val in itens:
        p = 100.0 * val / m
        extra = f' <span class="frac">{_pct(val, total):.0f}%</span>' if total else ""
        dica = f"{rot}: {val}" + (f" ({_pct(val, total):.1f}% de {total})" if total else "")
        linhas.append(
            f'<div class="barra" title="{E(dica)}">'
            f'<span class="rot">{rot}</span>'
            f'<span class="trilho"><i class="fill" style="width:{p:.1f}%;'
            f'background:{cor}"></i></span>'
            f'<span class="val">{val}{sufixo}{extra}</span></div>')
    return '<div class="barras">' + "".join(linhas) + "</div>"


def pares(itens, series, cores):
    """Duas contagens lado a lado por linha — `itens` e [(rotulo, a, b)].

    Usado para «tem evidencia / nao tem»: as duas metades somam o universo, e ver
    as duas e o ponto. Barra empilhada de dois segmentos, com folga de 2px.
    """
    out = []
    for rot, a, b in itens:
        tot = (a + b) or 1
        segs = []
        for v, nome, cor in ((a, series[0], cores[0]), (b, series[1], cores[1])):
            if not v:
                continue
            p = 100.0 * v / tot
            txt = str(v) if p >= 12 else ""
            segs.append(f'<i style="flex:0 0 {p:.2f}%;background:{cor}" '
                        f'title="{E(nome)}: {v} de {tot}">{txt}</i>')
        out.append(f'<div class="linha-ano" title="{E(rot)}: {a} de {tot}">'
                   f'<span class="ano">{E(rot)}</span>'
                   f'<span class="pilha">{"".join(segs)}</span>'
                   f'<span class="tot">{tot}</span></div>')
    return '<div class="empilhada">' + "".join(out) + "</div>"


def multiplos(blocos, cor="var(--s1)", maximo=None):
    """Pequenos multiplos: varios graficos de barras na MESMA escala.

    A escala comum e o que torna os paineis comparaveis; sem ela, cada painel
    mentiria sobre a sua propria altura. `blocos` e [(titulo, [(rot, val)])].
    """
    m = maximo or max((v for _, its in blocos for _, v in its), default=1) or 1
    cels = []
    for tit, its in blocos:
        tot = sum(v for _, v in its)
        cels.append(f'<div class="mult-cel"><h4>{E(tit)} '
                    f'<span class="mut">{tot}</span></h4>'
                    f"{barras(its, cor, maximo=m)}</div>")
    return f'<div class="multiplos">{"".join(cels)}</div>'
