"""
Carrega no banco a codificação de uma entrevista a partir do CSV versionado.

    python -m tools.load_evidence ENT-003          # carrega
    python -m tools.load_evidence ENT-003 --dry    # só valida e mostra
    python -m tools.load_evidence --all

O CSV em `codebook/evidencias/ENT-XXX.csv` é a fonte de verdade; o banco é
derivado dele. Recarregar é idempotente: apaga as evidências daquela
entrevista e regrava.

RECONSTRUÍDO em 06/09/2026.
"""

from __future__ import annotations

import argparse
import csv
import os
import sys
from pathlib import Path

import psycopg

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from database import codebook as cb  # noqa: E402

EVID_DIR = Path(__file__).resolve().parent.parent / "codebook" / "evidencias"

FIELDS = ["interview", "dim", "question", "type", "excerpt", "paraphrase",
          "ts", "keywords", "maturity", "alignment", "confidence"]


def read_csv(code: str) -> list[dict]:
    path = EVID_DIR / f"{code}.csv"
    if not path.exists():
        raise SystemExit(f"não encontrado: {path}")
    with path.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        r["keywords"] = [k for k in (r.get("keywords") or "").split("|") if k]
    return rows


def validate(rows: list[dict], code: str) -> list[str]:
    dims = cb.dimension_index()
    qids = {q["id"] for q in cb.questions()}
    mat = {m for m, _ in cb.MATURITY}
    problems = []
    for n, r in enumerate(rows, start=2):
        if r.get("interview") != code:
            problems.append(f"linha {n}: interview '{r.get('interview')}' ≠ {code}")
        if r.get("dim") not in dims:
            problems.append(f"linha {n}: dimensão '{r.get('dim')}' inexistente")
        if r.get("question") and r["question"] not in qids:
            problems.append(f"linha {n}: pergunta '{r['question']}' inexistente")
        if r.get("type") not in cb.EVIDENCE_TYPES:
            problems.append(f"linha {n}: tipo '{r.get('type')}' inválido")
        if r.get("maturity") not in mat:
            problems.append(f"linha {n}: maturidade '{r.get('maturity')}' inválida")
        if r.get("alignment") and r["alignment"] not in cb.ALIGNMENT:
            problems.append(f"linha {n}: alinhamento '{r['alignment']}' inválido")
        if r.get("confidence") and r["confidence"] not in cb.CONFIDENCE:
            problems.append(f"linha {n}: confiança '{r['confidence']}' inválida")
        if not (r.get("excerpt") or "").strip():
            problems.append(f"linha {n}: trecho vazio")
        # rede de segurança contra PII: o trecho já deve chegar anonimizado
        for marker in ("@", "Sr.", "Sra.", "telefone"):
            if marker in (r.get("excerpt") or ""):
                problems.append(f"linha {n}: possível identificador no trecho ('{marker}')")
    return problems


def load(conn: psycopg.Connection, code: str, rows: list[dict]) -> int:
    with conn.cursor() as cur:
        cur.execute("SELECT 1 FROM interviews WHERE code=%s", (code,))
        if not cur.fetchone():
            raise SystemExit(f"entrevista {code} não está em `interviews` — rode a migração antes.")
        cur.execute("DELETE FROM evidence WHERE interview_code=%s", (code,))
        for r in rows:
            cur.execute(
                """INSERT INTO evidence (interview_code, dimension, question_id, ev_type,
                       excerpt_anon, paraphrase, ts, keywords, maturity, alignment,
                       confidence, source_file)
                   VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                (code, r["dim"], r.get("question") or None, r["type"], r["excerpt"],
                 r.get("paraphrase") or None, r.get("ts") or None, r["keywords"],
                 r["maturity"], r.get("alignment") or None,
                 r.get("confidence") or "media", f"codebook/evidencias/{code}.csv"))
    conn.commit()
    return len(rows)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("codes", nargs="*", help="códigos ENT (ex.: ENT-003)")
    ap.add_argument("--all", action="store_true", help="todos os CSV de codebook/evidencias/")
    ap.add_argument("--dry", action="store_true", help="valida sem gravar")
    args = ap.parse_args()

    codes = args.codes
    if args.all:
        codes = sorted(p.stem for p in EVID_DIR.glob("ENT-*.csv"))
    if not codes:
        ap.error("informe ao menos um código ou use --all")

    total, bad = 0, 0
    conn = None if args.dry else (
        psycopg.connect(os.environ["DATABASE_URL"]) if os.environ.get("DATABASE_URL")
        else psycopg.connect())
    try:
        for code in codes:
            rows = read_csv(code)
            problems = validate(rows, code)
            for p in problems:
                print(f"  ! {code}: {p}")
            bad += len(problems)
            if problems:
                print(f"{code}: {len(problems)} problema(s) — não carregado.")
                continue
            if args.dry:
                dims = len({r['dim'] for r in rows})
                print(f"{code}: {len(rows)} evidências em {dims} dimensões — OK")
            else:
                n = load(conn, code, rows)
                print(f"{code}: {n} evidências carregadas")
            total += len(rows)
    finally:
        if conn:
            conn.close()
    print(f"\ntotal: {total} evidências, {bad} problema(s).")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
