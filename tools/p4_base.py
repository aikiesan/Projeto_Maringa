"""
Base determinística do Produto 04 — os números da matriz saem de cálculo.

    python -m tools.p4_base            # painel no terminal
    python -m tools.p4_base --json     # mesmo conteúdo, para consumo por script

Tudo aqui é contagem sobre `codebook/`: nada é lido por julgamento, nada é
estimado. É o que sustenta a quantificação das consultas, a matriz de avaliação
v2 e a seção de lacunas exigidas pelo TdR (Produto 1, §2.2).

A escala de maturidade do METODOLOGIA.md §4 vira ordinal aqui para permitir média
e mediana por subcategoria. `sem_evidencia` e `nao_aplicavel` ficam fora do
cálculo: a primeira é pendência de reinquirição, a segunda é inaplicabilidade —
nenhuma das duas é um estágio baixo de maturidade, e tratá-las como zero
rebaixaria artificialmente a subcategoria.
"""

from __future__ import annotations

import argparse
import csv
import json
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CB = ROOT / "codebook"

ESCALA = {"inexistente": 0, "em_elaboracao": 1, "formalizado": 2, "regulamentado": 3,
          "em_implementacao": 4, "monitorado": 5, "efetivo": 6}
FORA = {"sem_evidencia", "nao_aplicavel"}
ROTULO = {0: "Inexistente", 1: "Em elaboração", 2: "Formalizado", 3: "Regulamentado",
          4: "Em implementação", 5: "Monitorado", 6: "Efetivo"}
RANK = {"Muito alta": 4, "Alta": 3, "Média": 2, "Baixa": 1}

# O registro usa «Especial» para as três sessões de nível de direção (ENT-008,
# ENT-012, ENT-015), separadas por risco residual de reidentificação. No relatório
# elas são poder público, como a narrativa do Produto 04 já as trata.
SETOR_RELATORIO = {"Especial": "Publico"}


def ler(nome: str) -> list[dict]:
    with (CB / nome).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def evidencias() -> list[dict]:
    out = []
    for p in sorted((CB / "evidencias").glob("ENT-*.csv")):
        with p.open(encoding="utf-8-sig", newline="") as f:
            out.extend(csv.DictReader(f))
    return out


def hhmm(minutos: int) -> str:
    return f"{minutos // 60}h{minutos % 60:02d}"


def base() -> dict:
    ev = evidencias()
    dims = {d["code"]: d for d in ler("dimensions.csv")}
    ses = [s for s in ler("interviews.csv") if s["duplicate"] == "False"]

    # ── quantificação das consultas ────────────────────────────────────────
    minutos = sum(int(s["minutes"] or 0) for s in ses)
    consultas = {
        "sessoes": len(ses),
        "atores": sum(int(s["n_participants"] or 0) for s in ses),
        "minutos": minutos,
        "duracao": hhmm(minutos),
        "turnos": sum(int(s["turns"] or 0) for s in ses),
        "caracteres": sum(int(s["chars"] or 0) for s in ses),
        "evidencias": len(ev),
        "com_tcle": sum(1 for s in ses if s["tcle"] == "True"),
        "sem_tcle": sorted(s["code"] for s in ses if s["tcle"] != "True"),
        "por_setor": dict(Counter(SETOR_RELATORIO.get(s["sector"], s["sector"])
                                  for s in ses)),
        "atores_por_setor": {
            k: sum(int(s["n_participants"] or 0) for s in ses
                   if SETOR_RELATORIO.get(s["sector"], s["sector"]) == k)
            for k in sorted({SETOR_RELATORIO.get(s["sector"], s["sector"]) for s in ses})},
        "participacao_media": round(statistics.mean(
            int(s["participant_share"] or 0) for s in ses)),
        "periodo": (min(s["date"] for s in ses), max(s["date"] for s in ses)),
    }

    # ── cobertura dimensional ──────────────────────────────────────────────
    por_dim = defaultdict(list)
    for e in ev:
        por_dim[e["dim"]].append(e)
    sem_ev = sorted(c for c in dims if c not in por_dim)
    cobertura = {
        "dimensoes_total": len(dims),
        "dimensoes_com_evidencia": len(por_dim),
        "sem_evidencia": [{"code": c, "nome": dims[c]["name"],
                           "prioridade": dims[c]["priority"],
                           "subcat": dims[c]["subcat_name"]} for c in sem_ev],
        "trianguladas": sum(1 for c, l in por_dim.items()
                            if len({x["interview"] for x in l}) > 1),
        "fonte_unica": sum(1 for c, l in por_dim.items()
                           if len({x["interview"] for x in l}) == 1),
        "divergencias": sum(1 for e in ev if e["alignment"] == "divergente"),
    }
    for pri in RANK:
        alvo = [c for c, d in dims.items() if d["priority"] == pri]
        cobertura[f"prioridade_{pri.lower().replace(' ', '_')}"] = {
            "dimensoes": len(alvo),
            "com_evidencia": sum(1 for c in alvo if c in por_dim),
            "evidencias": sum(len(por_dim.get(c, [])) for c in alvo),
        }

    # ── matriz v2: insumo por subcategoria ─────────────────────────────────
    subs = {}
    for code, d in dims.items():
        s = subs.setdefault(d["subcat"], {
            "subcat": d["subcat"], "nome": d["subcat_name"],
            "eixo": d["axis"], "eixo_nome": d["axis_name"],
            "dimensoes": [], "evidencias": [],
        })
        s["dimensoes"].append(code)
        s["evidencias"].extend(por_dim.get(code, []))

    for s in subs.values():
        e = s["evidencias"]
        notas = [ESCALA[x["maturity"]] for x in e
                 if x["maturity"] in ESCALA and x["maturity"] not in FORA]
        s["n_dimensoes"] = len(s["dimensoes"])
        s["n_cobertas"] = sum(1 for c in s["dimensoes"] if c in por_dim)
        s["n_evidencias"] = len(e)
        s["n_sessoes"] = len({x["interview"] for x in e})
        s["sessoes"] = sorted({x["interview"] for x in e})
        s["maturidades"] = dict(Counter(x["maturity"] for x in e))
        s["tipos"] = dict(Counter(x["type"] for x in e))
        s["confianca"] = dict(Counter(x["confidence"] for x in e))
        s["divergencias"] = sum(1 for x in e if x["alignment"] == "divergente")
        s["prioridade_max"] = max((RANK.get(dims[c]["priority"], 0)
                                   for c in s["dimensoes"]), default=0)
        if notas:
            # O rótulo sai da MODA, não de média nem de mediana. A escala é ordinal e
            # a distribuição é tipicamente bimodal: 1.2 tem 28 evidências em
            # «inexistente» e 18 em «em_implementacao», e a média dessas duas pontas
            # cai em 1,54 — «Formalizado» —, estágio que só 2 das 52 evidências
            # sustentam. A média descreveria um estado que o corpus não registra.
            dist = Counter(notas)
            moda = max(dist, key=lambda v: (dist[v], -v))
            s["maturidade_media"] = round(statistics.mean(notas), 2)
            s["maturidade_mediana"] = statistics.median(notas)
            s["maturidade_moda"] = moda
            s["maturidade_rotulo"] = ROTULO[moda]
            s["dispersao"] = round(statistics.pstdev(notas), 2) if len(notas) > 1 else 0.0
            s["share_inexistente"] = round(100 * dist.get(0, 0) / len(notas))
            # Duas concentrações afastadas na escala não descrevem estágio
            # intermediário: descrevem condição que existe numa frente e não existe
            # noutra. Isso é achado, e o relatório precisa dizê-lo em vez de mediar.
            top = dist.most_common(2)
            s["perfil"] = ("bimodal" if len(top) > 1
                           and top[1][1] >= 0.25 * len(notas)
                           and abs(top[0][0] - top[1][0]) >= 2
                           else "concentrado" if s["dispersao"] < 1.2 else "disperso")
            s["perfil_polos"] = ([ROTULO[top[0][0]], ROTULO[top[1][0]]]
                                 if s["perfil"] == "bimodal" else [])
        else:
            s["maturidade_media"] = s["maturidade_mediana"] = s["maturidade_moda"] = None
            s["maturidade_rotulo"] = "Sem evidência"
            s["dispersao"] = s["share_inexistente"] = None
            s["perfil"] = "sem evidência"
            s["perfil_polos"] = []
        del s["evidencias"]

    # ── maturidade por setor ───────────────────────────────────────────────
    setor_de = {s["code"]: SETOR_RELATORIO.get(s["sector"], s["sector"]) for s in ses}
    por_setor = defaultdict(list)
    for e in ev:
        m = e["maturity"]
        if m in ESCALA and m not in FORA:
            por_setor[setor_de.get(e["interview"], "?")].append(ESCALA[m])
    def perfil_setor(v: list[int]) -> dict:
        dist = Counter(v)
        moda = max(dist, key=lambda x: (dist[x], -x))
        return {"n": len(v), "media": round(statistics.mean(v), 2),
                "rotulo": ROTULO[moda],
                "share_inexistente": round(100 * dist.get(0, 0) / len(v))}
    setores = {k: perfil_setor(v) for k, v in sorted(por_setor.items())}

    return {"consultas": consultas, "cobertura": cobertura,
            "subcategorias": [subs[k] for k in sorted(subs)], "setores": setores}


def painel(b: dict) -> None:
    c, cv = b["consultas"], b["cobertura"]
    print("═" * 78)
    print("PRODUTO 04 — BASE DETERMINÍSTICA")
    print("═" * 78)
    print(f"\nCONSULTAS  {c['sessoes']} sessões · {c['atores']} atores · "
          f"{c['duracao']} · {c['turnos']:,} turnos · {c['evidencias']} evidências"
          .replace(",", "."))
    print(f"           período {c['periodo'][0]} a {c['periodo'][1]} · "
          f"fala do participante {c['participacao_media']}% do registro")
    print(f"           TCLE localizado em {c['com_tcle']}/{c['sessoes']}"
          f" — sem: {', '.join(c['sem_tcle'])}")
    print("           setores: " + " · ".join(
        f"{k} {v} sessões/{c['atores_por_setor'][k]} atores"
        for k, v in sorted(c["por_setor"].items())))

    print(f"\nCOBERTURA  {cv['dimensoes_com_evidencia']}/{cv['dimensoes_total']} dimensões "
          f"com evidência · {cv['trianguladas']} trianguladas · "
          f"{cv['fonte_unica']} de fonte única · {cv['divergencias']} divergências")
    for pri in ("Muito alta", "Alta", "Média", "Baixa"):
        k = f"prioridade_{pri.lower().replace(' ', '_')}"
        d = cv[k]
        print(f"           {pri:<11} {d['com_evidencia']:>2}/{d['dimensoes']:<2} dimensões · "
              f"{d['evidencias']:>3} evidências")

    print(f"\nLACUNAS    {len(cv['sem_evidencia'])} dimensões sem nenhuma evidência:")
    for d in cv["sem_evidencia"]:
        print(f"           {d['code']:<7} {d['prioridade']:<11} {d['nome'][:52]}")

    print("\nMATRIZ v2 — insumo por subcategoria")
    print(f"  {'':<6} {'':<44} {'dim':>6} {'ev':>4} {'ses':>4} {'méd':>5} "
          f"{'%inex':>6}  {'maturidade (moda)':<19} perfil")
    for s in b["subcategorias"]:
        polos = f" [{' / '.join(s['perfil_polos'])}]" if s["perfil_polos"] else ""
        print(f"  {s['subcat']:<6} {s['nome'][:44]:<44} "
              f"{s['n_cobertas']}/{s['n_dimensoes']:<4} {s['n_evidencias']:>4} "
              f"{s['n_sessoes']:>4} {str(s['maturidade_media'] or '—'):>5} "
              f"{str(s['share_inexistente']) + '%' if s['share_inexistente'] is not None else '—':>6}"
              f"  {s['maturidade_rotulo']:<19} {s['perfil']}{polos}")

    print("\nMATURIDADE POR SETOR  (o que cada grupo de atores enxerga)")
    for k, v in b["setores"].items():
        print(f"  {k:<18} n={v['n']:>3}  média {v['media']:>4}  "
              f"{v['share_inexistente']:>3}% inexistente  moda {v['rotulo']}")
    print()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    b = base()
    if args.json:
        json.dump(b, sys.stdout, ensure_ascii=False, indent=2)
    else:
        painel(b)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
