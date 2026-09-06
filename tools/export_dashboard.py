"""
Gera `codebook/dashboard.json` — o retrato do corpus consumido pelo painel.

    python -m tools.export_dashboard

Fonte: os CSV de `codebook/`. A pré-triagem (`triage`) é preservada da versão
anterior do arquivo, porque depende das transcrições e só muda quando
`tools.triage` é rodado de novo sobre elas.
"""

from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from database import codebook as cb  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "codebook" / "dashboard.json"
EVID = ROOT / "codebook" / "evidencias"


def load_evidence() -> list[dict]:
    import csv
    rows = []
    for path in sorted(EVID.glob("ENT-*.csv")):
        with path.open(encoding="utf-8-sig", newline="") as f:
            for r in csv.DictReader(f):
                rows.append({
                    "interview": r["interview"], "dim": r["dim"],
                    "question": r.get("question") or None, "type": r["type"],
                    "excerpt": r["excerpt"], "paraphrase": r.get("paraphrase") or "",
                    "ts": r.get("ts") or "",
                    "keywords": [k for k in (r.get("keywords") or "").split("|") if k],
                    "maturity": r["maturity"], "alignment": r.get("alignment") or None,
                    "confidence": r.get("confidence") or "media",
                })
    return rows


def load_triage() -> dict:
    """Matriz entrevista × dimensão, de `codebook/triage_matrix.csv`.

    Gerada por `python -m tools.triage --all`. Se o arquivo não existir, cai para
    a triagem embutida na versão anterior do dashboard.
    """
    import csv
    path = ROOT / "codebook" / "triage_matrix.csv"
    if path.exists():
        out: dict[str, dict[str, int]] = {}
        with path.open(encoding="utf-8-sig", newline="") as f:
            for r in csv.DictReader(f):
                out.setdefault(r["interview"], {})[r["dimension_code"]] = int(r["hits"])
        return out
    if OUT.exists():
        try:
            return json.loads(OUT.read_text(encoding="utf-8")).get("triage", {})
        except json.JSONDecodeError:
            pass
    return {}


def build() -> dict:
    return {
        "generated": date.today().isoformat(),
        "axes": [{"num": n, "name": a["name"], "short": a["short"], "name_en": a["en"]}
                 for n, a in cb.AXES.items()],
        "subcategories": [{"code": c, "axis": s["axis"], "name": s["name"]}
                          for c, s in cb.SUBCATEGORIES.items()],
        "dimensions": [{"code": d["code"], "axis": d["axis"], "axis_name": d["axis_name"],
                        "subcat": d["subcat"], "subcat_name": d["subcat_name"],
                        "name": d["name"], "priority": d["priority"], "rank": d["rank"],
                        "keywords": d["keywords"]} for d in cb.dimensions()],
        "questions": [{"id": q["id"], "block": q["block"], "text": q["text"],
                       "dims": [f"{l['dimension_code']}:{l['relation']}"
                                for l in cb.question_dimension() if l["question_id"] == q["id"]]}
                      for q in cb.questions()],
        "interviews": [{"code": i["code"], "canonical": i.get("canonical") or i["code"],
                        "duplicate": i["duplicate"], "sector": i.get("sector"),
                        "institution_type": i.get("institution_type"), "block": i.get("block"),
                        "date": i.get("date"), "n_participants": i.get("n_participants") or 1,
                        "tcle": i["tcle"], "status": i.get("status"),
                        "notes": i.get("notes") or "", "minutes": i.get("minutes"),
                        "turns": i.get("turns"), "chars": i.get("chars"),
                        "participant_share": i.get("participant_share"),
                        "n_dim_candidates": i.get("n_dim_candidates"),
                        "n_hits": i.get("n_hits")} for i in cb.interviews()],
        "triage": load_triage(),
        "evidence": load_evidence(),
    }


if __name__ == "__main__":
    d = build()
    OUT.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    coded = sorted({e["interview"] for e in d["evidence"]})
    print(f"{OUT.relative_to(ROOT)}: {len(d['dimensions'])} dimensões, "
          f"{len(d['interviews'])} códigos ENT, {len(d['evidence'])} evidências "
          f"({len(coded)} sessões codificadas: {', '.join(coded)})")
