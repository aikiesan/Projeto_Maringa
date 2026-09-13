# -*- coding: utf-8 -*-
"""Fluxo de aceitacao humana das ancoras da Secao 3 do Produto 4.

    python -m tools.p4_revisao              # gera/atualiza o CSV de revisao
    python -m tools.p4_revisao --pagina     # gera tambem a pagina local de revisao

`tools/p4_ancorar` ordena por `score`; nao decide. Sobreposicao lexica acha
candidato, nao prova que a evidencia sustenta a afirmacao. Este modulo mantem
`produtos/P4_ancoras_revisao.csv`, onde cada candidata recebe uma decisao humana,
e e esse arquivo — nao o de candidatas — que a pagina do Produto 4 cita.

Invariante: rodar de novo NUNCA apaga decisao ja tomada. A juncao e por
(n, interview, dim, ts); candidata que sumiu do CSV de candidatas e mantida com a
marca `orfa`, para nao perder o julgamento em silencio.
"""
from __future__ import annotations

import argparse
import csv
import html
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CANDIDATAS = ROOT / "produtos" / "P4_ancoras_secao3.csv"
REVISAO = ROOT / "produtos" / "P4_ancoras_revisao.csv"
PAGINA = ROOT / "revisao_ancoras.html"

DECISOES = ("", "aceita", "rejeitada", "substituida")
EXTRA = ("decisao", "ancora_substituta", "nota", "orfa")


def _ler(p: Path) -> list[dict]:
    if not p.exists():
        return []
    with p.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def chave(r: dict) -> tuple:
    return (r.get("n", ""), r.get("interview", ""), r.get("dim", ""), r.get("ts", ""))


def montar() -> tuple[list[dict], dict]:
    cand = _ler(CANDIDATAS)
    if not cand:
        raise SystemExit(f"sem candidatas: {CANDIDATAS} nao existe ou esta vazio")
    antes = {chave(r): r for r in _ler(REVISAO)}

    saida, colunas = [], list(cand[0]) + list(EXTRA)
    for r in cand:
        novo = {c: r.get(c, "") for c in cand[0]}
        velho = antes.get(chave(r), {})
        for c in EXTRA:
            novo[c] = velho.get(c, "") or ""
        novo["orfa"] = ""
        d = novo["decisao"].strip().lower()
        if d and d not in DECISOES:
            raise SystemExit(f"decisao invalida {d!r} em {chave(r)} — use {DECISOES[1:]}")
        novo["decisao"] = d
        saida.append(novo)

    vivas = {chave(r) for r in cand}
    orfas = 0
    for k, v in antes.items():
        if k not in vivas and (v.get("decisao") or "").strip():
            v = {c: v.get(c, "") for c in colunas}
            v["orfa"] = "sim"
            saida.append(v)
            orfas += 1

    por_n = {}
    for r in saida:
        por_n.setdefault(r["n"], []).append(r)
    resumo = {
        "candidatas": len(cand),
        "afirmacoes": len(por_n),
        "aceitas": sum(1 for r in saida if r["decisao"] == "aceita"),
        "rejeitadas": sum(1 for r in saida if r["decisao"] == "rejeitada"),
        "substituidas": sum(1 for r in saida if r["decisao"] == "substituida"),
        "sem_decisao": sum(1 for r in saida if not r["decisao"]),
        "orfas": orfas,
    }
    resumo["afirmacoes_com_ancora"] = sum(
        1 for rs in por_n.values() if any(r["decisao"] == "aceita" for r in rs))
    resumo["afirmacoes_sem_ancora"] = resumo["afirmacoes"] - resumo["afirmacoes_com_ancora"]
    return saida, resumo


def gravar(linhas: list[dict]) -> None:
    cols = list(linhas[0])
    with REVISAO.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(linhas)


def aceitas() -> dict[str, list[dict]]:
    """Ancoras aceitas, por numero de afirmacao. A pagina do Produto 4 usa SO isto."""
    out: dict[str, list[dict]] = {}
    for r in _ler(REVISAO):
        if (r.get("decisao") or "").strip().lower() == "aceita" and not r.get("orfa"):
            out.setdefault(r["n"], []).append(r)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pagina", action="store_true",
                    help="gera tambem revisao_ancoras.html, para revisar no navegador")
    a = ap.parse_args()

    linhas, resumo = montar()
    gravar(linhas)
    print(f"{REVISAO.relative_to(ROOT)}: {len(linhas)} linhas")
    for k in ("afirmacoes", "candidatas", "aceitas", "rejeitadas", "substituidas",
              "sem_decisao", "orfas", "afirmacoes_com_ancora", "afirmacoes_sem_ancora"):
        print(f"  {k:24} {resumo[k]}")
    if resumo["orfas"]:
        print("  ATENCAO: ha decisoes orfas — a candidata sumiu do CSV de candidatas.")

    if a.pagina:
        from tools import p4_revisao_pagina as PG
        vivas = [r for r in linhas if not r.get("orfa")]
        PAGINA.write_text(PG.render(vivas, list(linhas[0]), resumo), encoding="utf-8")
        print(f"pagina: {PAGINA}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
