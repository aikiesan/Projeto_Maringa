# -*- coding: utf-8 -*-
"""As afirmações da Seção 3 que ficaram sem âncora, para revisão humana.

    python -m tools.p4_pendentes              # relatório em markdown
    python -m tools.p4_pendentes --pagina     # + página local para decidir

A seleção automática (`tools.p4_selecao`) é conservadora: erra para o lado de
deixar sem âncora. Logo, entre as 53 sem âncora há dois tipos muito diferentes
de caso, e confundi-los desperdiça leitura:

- **afirmação que o corpus sustenta e o método não viu**, geralmente porque a
  afirmação e a evidência dizem a mesma coisa com vocabulário diferente. É aqui
  que a revisão humana rende;
- **afirmação que o corpus de fato não sustenta**, e então a ausência é achado
  do diagnóstico, não falha do método. Confirmar isso também é resultado.

A ordem de revisão abaixo reflete essa diferença: começa pelo que tem mais
chance de ser recuperável.

| Prioridade | Grupo | Por quê |
|---|---|---|
| 1 | empate entre candidatas | o método achou duas boas e se recusou a escolher; a leitura resolve em segundos |
| 2 | peso entre 15 e 18 | passou perto do corte; provável falso negativo |
| 3 | peso entre 12 e 15 | zona cinzenta |
| 4 | peso abaixo de 12 | provável ausência real; confirmar é o resultado |
| 5 | chamada de lista | só confirmar que não deve ancorar |
"""
from __future__ import annotations

import argparse
import collections
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from tools.p4_selecao import (frequencia_documental, avaliar,  # noqa: E402
                              decidir, e_chamada)

REVISAO = ROOT / "produtos" / "P4_ancoras_revisao.csv"
RELATORIO = ROOT / "P4_afirmacoes_sem_ancora.md"
PAGINA = ROOT / "revisao_pendentes.html"


def prioridade(motivo: str, peso: float) -> tuple[int, str]:
    if motivo.startswith("empate"):
        return 1, "Empate entre candidatas"
    if motivo.startswith("chamada"):
        return 5, "Chamada de lista"
    if peso >= 15:
        return 2, "Passou perto do corte (peso 15 a 18)"
    if peso >= 12:
        return 3, "Zona cinzenta (peso 12 a 15)"
    return 4, "Peso baixo (abaixo de 12)"


def levantar(peso_min: float = 18.0, margem: float = 2.0):
    with REVISAO.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    df, n = frequencia_documental()
    avaliar(rows, df, n, 0.10)
    porN: dict = {}
    for r in rows:
        porN.setdefault(r["n"], []).append(r)
    res = decidir(porN, peso_min, margem)

    pend = []
    for num, d in res.items():
        if d["escolhida"]:
            continue
        cands = sorted(porN[num], key=lambda r: -r["_peso"])
        melhor = max((r["_peso"] for r in cands
                      if r["confidence"] == "alta"), default=0.0)
        p, rot = prioridade(d["motivo"], melhor)
        pend.append({"n": num, "motivo": d["motivo"], "peso": melhor,
                     "prioridade": p, "grupo": rot, "cands": cands,
                     "setor": cands[0]["setor"], "subsecao": cands[0]["subsecao"],
                     "afirmacao": cands[0]["afirmacao"]})
    pend.sort(key=lambda x: (x["prioridade"], -x["peso"], int(x["n"])))
    return pend, porN


def markdown(pend: list[dict]) -> str:
    total = len(pend)
    grupos = collections.Counter(p["grupo"] for p in pend)
    out = [
        "# Afirmações da Seção 3 sem âncora de evidência",
        "",
        f"**{total} das 93 afirmações** não receberam âncora na seleção "
        "automática. Este arquivo existe para que a revisão humana decida caso a "
        "caso, e está ordenado por onde a leitura rende mais.",
        "",
        "A seleção automática é conservadora de propósito: ela recusa mais do que "
        "aceita. Logo, estar nesta lista **não** significa que a afirmação não "
        "tenha sustentação. Significa que o método não conseguiu estabelecê-la "
        "com o critério declarado. Os dois desfechos possíveis da revisão são "
        "igualmente úteis: encontrar a evidência que o método não viu, ou "
        "confirmar que ela não existe, e nesse caso a ausência é achado.",
        "",
        "## Como decidir",
        "",
        "Para cada afirmação estão as três candidatas levantadas, com a paráfrase "
        "da evidência, que é o que se cita. Se alguma sustentar a afirmação, "
        "anote o código; se nenhuma sustentar, a afirmação fica sem âncora e isso "
        "é o resultado. Depois, marque na página `revisao_pendentes.html` ou "
        "direto em `produtos/P4_ancoras_revisao.csv`, mudando `decisao` para "
        "`aceita` e `decisor` para `humano`. A seleção automática nunca "
        "sobrescreve decisão humana.",
        "",
        "## Resumo",
        "",
        "| Prioridade | Grupo | Afirmações |",
        "|---|---|---:|",
    ]
    vistos = []
    for p in pend:
        if (p["prioridade"], p["grupo"]) not in vistos:
            vistos.append((p["prioridade"], p["grupo"]))
    for pr, g in sorted(vistos):
        out.append(f"| {pr} | {g} | {grupos[g]} |")
    out.append("")

    grupo_atual = None
    for p in pend:
        if p["grupo"] != grupo_atual:
            grupo_atual = p["grupo"]
            out += ["", f"## {p['prioridade']}. {grupo_atual}", ""]
            out.append(_nota_do_grupo(p["prioridade"]))
            out.append("")
        out += [
            f"### Afirmação {p['n']}, {p['setor']}",
            "",
            f"*{p['subsecao']}*",
            "",
            f"> {p['afirmacao']}",
            "",
            f"Motivo da recusa: **{p['motivo']}**",
            "",
            "| | Sessão | Marca | Dimensão | Maturidade | Conf. | Peso |",
            "|---|---|---|---|---|---|---:|",
        ]
        for i, c in enumerate(p["cands"], 1):
            out.append(f"| {i} | `{c['interview']}` | `{c['ts']}` | "
                       f"`{c['dim']}` {c['dim_nome']} | {c['maturity']} | "
                       f"{c['confidence']} | {c['_peso']:.1f} |")
        out.append("")
        for i, c in enumerate(p["cands"], 1):
            out.append(f"{i}. {c['paraphrase']}")
        out.append("")
    return "\n".join(out)


def _nota_do_grupo(p: int) -> str:
    return {
        1: "O método encontrou duas candidatas com peso semelhante e se recusou "
           "a escolher, porque escolher no empate inventaria precisão. A leitura "
           "resolve depressa: basta dizer qual das duas.",
        2: "Ficaram logo abaixo do corte. São as mais prováveis de serem "
           "falsos negativos do método.",
        3: "Zona cinzenta: o vocabulário em comum existe, mas é pouco "
           "distintivo. Pode ser sustentação real com vocabulário divergente.",
        4: "Pouca sobreposição de vocabulário específico. A hipótese mais "
           "provável é que o corpus realmente não sustente a afirmação, e "
           "confirmar isso é resultado do diagnóstico, não trabalho perdido.",
        5: "Não afirmam nada: anunciam a lista que vem a seguir. Só confirmar "
           "que não devem receber âncora.",
    }.get(p, "")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pagina", action="store_true",
                    help="gera tambem revisao_pendentes.html")
    a = ap.parse_args()

    pend, porN = levantar()
    RELATORIO.write_text(markdown(pend), encoding="utf-8")
    print(f"{RELATORIO.name}: {len(pend)} afirmacoes sem ancora")
    grupos = collections.Counter((p["prioridade"], p["grupo"]) for p in pend)
    for (pr, g), q in sorted(grupos.items()):
        print(f"  {pr}. {g:36} {q:3}")

    if a.pagina:
        from tools import p4_revisao_pagina as PG
        nums = {p["n"] for p in pend}
        linhas = [r for rs in porN.values() for r in rs if r["n"] in nums]
        for r in linhas:
            for k in list(r):
                if k.startswith("_"):
                    del r[k]
        cols = [c for c in linhas[0] if not c.startswith("_")]
        resumo = {"afirmacoes": len(nums)}
        PAGINA.write_text(PG.render(linhas, cols, resumo), encoding="utf-8")
        print(f"pagina: {PAGINA}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
