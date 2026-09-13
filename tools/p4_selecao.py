# -*- coding: utf-8 -*-
"""Seleção automática de âncoras para a Seção 3 do Produto 4.

    python -m tools.p4_selecao            # relatório, não grava
    python -m tools.p4_selecao --gravar   # grava as decisões no CSV de revisão

## O que este módulo NÃO é

Não é validação humana. `produtos/P4_ancoras_revisao.csv` distingue as duas
coisas na coluna `decisor`: `humano` para o que Lucas marcou, `automatico` para o
que saiu daqui. A página do Produto 4 rotula a origem da âncora conforme essa
coluna — dizer «validada» sobre uma decisão de máquina seria mentir sobre a
procedência, e a procedência é o que esta consultoria vende.

## Por que o score sozinho não serve

Lido contra o material, o `score` de sobreposição léxica erra nos dois sentidos:

- Falso positivo. A afirmação 14 — «Esforços em Andamento: a prefeitura está
  realizando investimentos significativos para superar essa lacuna, incluindo:» —
  tem score 0,333 e não afirma coisa alguma: é chamada da lista que vem a seguir.
  Casou por «andamento», «lacuna» e «prefeitura», que aparecem em quase todo o
  corpus.
- Falso negativo. A afirmação 44, sobre equidade territorial, tem score 0,182 e
  é sustentada de fato por uma recomendação de equidade territorial do agente
  financeiro. O score é baixo porque o vocabulário das duas é diferente.

O remédio é pesar os termos: um termo que aparece em quase toda evidência não
distingue nada. Aqui isso é medido, não estimado — a frequência documental é
calculada sobre as 494 evidências do corpus.

## O critério, declarado

Uma candidata é aceita quando TODAS as condições valem:

1. `confidence == alta`. Confiança não discrimina sozinha — 251 das 279
   candidatas são altas —, mas exclui o que a codificação já marcou como
   incerto, e essa exclusão é barata.
2. A afirmação **afirma alguma coisa**. Texto terminado em `:` é chamada de
   lista: não tem o que ancorar, e ancorá-lo produz uma âncora para um título.
3. Peso informacional mínimo: a soma do peso IDF dos termos compartilhados
   atinge `--peso-min`, hoje **18**. É isto que separa «pirapó, ivaí, unilivre»
   de «prefeitura, gestão, dados».

   O valor foi calibrado por leitura, não por gosto. Em 12, das seis aceitas
   mais fracas três não sustentavam a afirmação — a pior casava «bombeiros,
   corpo, defesa» de uma proposta de reforma do IAM com uma evidência que
   elogia a resposta a evento extremo. Em 18, das sete mais fracas seis
   sustentam. O preço é recusar casamentos bons de vocabulário divergente,
   como a afirmação 44 sobre equidade territorial. O erro foi empurrado para
   o lado de deixar sem âncora, que é o lado certo: âncora errada afirma
   falsamente que a evidência existe; âncora ausente apenas mostra o que não
   foi possível estabelecer.
4. Ao menos um termo compartilhado **distintivo** (presente em menos de
   `--df-max` das evidências).
5. Margem sobre a segunda colocada: se a melhor e a segunda empatam dentro de
   `--margem`, nenhuma é aceita. Empate significa que o método não escolheu —
   e escolher no empate é inventar precisão.

Afirmação que não satisfaz fica **sem âncora**, e isso é resultado exibido, não
falha escondida: é a regra 5.2 aplicada ao próprio texto do produto.
"""
from __future__ import annotations

import argparse
import collections
import csv
import glob
import math
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REVISAO = ROOT / "produtos" / "P4_ancoras_revisao.csv"
EVID = ROOT / "codebook" / "evidencias"

# uma decisao humana NUNCA e sobrescrita por esta ferramenta
DECISOR_AUTO = "automatico"
DECISOR_HUMANO = "humano"


def dobrar(s: str) -> str:
    s = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


def termos(texto: str) -> set[str]:
    return set(re.findall(r"[a-z]{4,}", dobrar(texto)))


def frequencia_documental() -> tuple[dict[str, int], int]:
    """Em quantas das 494 evidências cada termo aparece.

    A base é o corpus inteiro, não as candidatas: é o corpus que define o que é
    vocabulário comum neste projeto. «climatica» é rara no português geral e
    banal aqui.
    """
    df: collections.Counter = collections.Counter()
    n = 0
    for arq in sorted(glob.glob(str(EVID / "ENT-*.csv"))):
        with open(arq, encoding="utf-8-sig", newline="") as f:
            for r in csv.DictReader(f):
                n += 1
                juntos = " ".join((r.get("excerpt") or "", r.get("paraphrase") or "",
                                   r.get("keywords") or ""))
                df.update(termos(juntos))
    return dict(df), n


def peso(t: str, df: dict[str, int], n: int) -> float:
    """IDF suavizado. Termo em toda evidência pesa ~0; termo raro pesa alto."""
    return math.log((n + 1) / (df.get(t, 0) + 1))


def e_chamada(texto: str) -> bool:
    """Chamada de lista: anuncia o que vem a seguir, não afirma nada."""
    t = (texto or "").strip()
    return t.endswith(":") or t.endswith(": ")


def avaliar(rows: list[dict], df: dict, n: int, df_max: float) -> list[dict]:
    """Acrescenta a cada candidata as medidas que a decisao usa."""
    limite = df_max * n
    for r in rows:
        ts = [t for t in (r.get("termos") or "").split("|") if t]
        r["_termos"] = ts
        r["_peso"] = round(sum(peso(t, df, n) for t in ts), 3)
        r["_distintivos"] = [t for t in ts if df.get(t, 0) < limite]
        r["_score"] = float(r.get("score") or 0)
    return rows


def decidir(porN: dict, peso_min: float, margem: float) -> dict:
    """Para cada afirmacao, escolhe uma candidata ou nenhuma."""
    fora = {}
    for num, rs in porN.items():
        elegiveis = [r for r in rs
                     if r["confidence"] == "alta" and not e_chamada(r["afirmacao"])]
        if not elegiveis:
            motivo = ("chamada de lista" if rs and e_chamada(rs[0]["afirmacao"])
                      else "nenhuma candidata com confiança alta")
            fora[num] = {"escolhida": None, "motivo": motivo}
            continue
        elegiveis.sort(key=lambda r: (-r["_peso"], -r["_score"]))
        melhor = elegiveis[0]
        segunda = elegiveis[1] if len(elegiveis) > 1 else None

        if melhor["_peso"] < peso_min:
            fora[num] = {"escolhida": None,
                         "motivo": f"peso informacional {melhor['_peso']:.1f} "
                                   f"< {peso_min}"}
            continue
        if not melhor["_distintivos"]:
            fora[num] = {"escolhida": None,
                         "motivo": "nenhum termo compartilhado é distintivo"}
            continue
        if segunda and (melhor["_peso"] - segunda["_peso"]) < margem:
            fora[num] = {"escolhida": None,
                         "motivo": f"empate: {melhor['_peso']:.1f} vs "
                                   f"{segunda['_peso']:.1f} (margem < {margem})"}
            continue
        fora[num] = {"escolhida": melhor, "motivo": ""}
    return fora


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--peso-min", type=float, default=18.0,
                    help="soma minima de IDF dos termos compartilhados")
    ap.add_argument("--df-max", type=float, default=0.10,
                    help="termo presente em mais desta fracao das evidencias "
                         "nao conta como distintivo")
    ap.add_argument("--margem", type=float, default=2.0,
                    help="vantagem minima da melhor sobre a segunda")
    ap.add_argument("--gravar", action="store_true",
                    help="grava as decisoes no CSV de revisao")
    ap.add_argument("--mostrar", type=int, default=0,
                    help="imprime N aceitas e N recusadas, para conferencia")
    a = ap.parse_args()

    with REVISAO.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    cols = list(rows[0])

    df, n = frequencia_documental()
    print(f"frequencia documental sobre {n} evidencias, {len(df)} termos distintos")
    avaliar(rows, df, n, a.df_max)

    porN: dict = {}
    for r in rows:
        porN.setdefault(r["n"], []).append(r)
    res = decidir(porN, a.peso_min, a.margem)

    aceitas = {num: d["escolhida"] for num, d in res.items() if d["escolhida"]}
    print(f"\nafirmacoes: {len(porN)}")
    print(f"  com ancora selecionada: {len(aceitas)}")
    print(f"  sem ancora:             {len(porN) - len(aceitas)}")
    motivos = collections.Counter(d["motivo"].split(":")[0].split(" <")[0]
                                  for d in res.values() if not d["escolhida"])
    for m, q in motivos.most_common():
        print(f"      {q:3}  {m}")

    if a.mostrar:
        for rotulo, cond in (("ACEITAS", True), ("RECUSADAS", False)):
            sel = [(k, v) for k, v in res.items() if bool(v["escolhida"]) is cond]
            sel.sort(key=lambda kv: -(kv[1]["escolhida"]["_peso"] if cond else 0))
            print(f"\n{'=' * 70}\n{rotulo} — amostra\n{'=' * 70}")
            for num, d in sel[:a.mostrar]:
                r = d["escolhida"] or porN[num][0]
                print(f"\n[{num}] peso={r['_peso']} score={r['_score']} "
                      f"distintivos={r['_distintivos']}")
                if not cond:
                    print(f"  RECUSA: {d['motivo']}")
                print(f"  AFIRMA: {r['afirmacao'][:165]}")
                print(f"  EVID  : {r['interview']} {r['ts']} dim {r['dim']}")
                print(f"  PARAFR: {r['paraphrase'][:165]}")

    if a.gravar:
        for r in rows:
            if (r.get("decisor") or "") == DECISOR_HUMANO:
                continue          # decisao humana nunca e sobrescrita
            esc = aceitas.get(r["n"])
            igual = esc is not None and (r["interview"], r["dim"], r["ts"]) == \
                (esc["interview"], esc["dim"], esc["ts"])
            r["decisao"] = "aceita" if igual else "rejeitada"
            r["decisor"] = DECISOR_AUTO
            r["criterio"] = (f"peso={r['_peso']} idf; distintivos="
                             f"{'|'.join(r['_distintivos'])}" if igual
                             else res[r["n"]]["motivo"])
        for c in ("decisor", "criterio"):
            if c not in cols:
                cols.append(c)
        with REVISAO.open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
            w.writeheader()
            w.writerows(rows)
        print(f"\ngravado: {REVISAO.relative_to(ROOT)}")
    else:
        print("\n(nada gravado — use --gravar)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
