"""
Aplica o schema analítico e carrega o codebook no PostgreSQL. Idempotente.

    python -m database.migrate            # aplica schema + carrega codebook
    python -m database.migrate --check    # só valida o codebook, não toca no banco

Conexão por DATABASE_URL (ou PGHOST/PGPORT/PGUSER/PGPASSWORD/PGDATABASE).

RECONSTRUÍDO em 06/09/2026. Valida contra PostgreSQL 16.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

import psycopg

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from database import codebook as cb  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SCHEMA = ROOT / "database" / "schema_v2.sql"


def connect() -> psycopg.Connection:
    dsn = os.environ.get("DATABASE_URL")
    return psycopg.connect(dsn) if dsn else psycopg.connect()


def apply_schema(conn: psycopg.Connection) -> None:
    conn.execute(SCHEMA.read_text(encoding="utf-8"))
    print(f"schema aplicado: {SCHEMA.name}")


def load_codebook(conn: psycopg.Connection) -> None:
    with conn.cursor() as cur:
        for num, a in cb.AXES.items():
            cur.execute(
                """INSERT INTO axes (num, name, short_name, name_en) VALUES (%s,%s,%s,%s)
                   ON CONFLICT (num) DO UPDATE SET
                     name=EXCLUDED.name, short_name=EXCLUDED.short_name, name_en=EXCLUDED.name_en""",
                (num, a["name"], a["short"], a["en"]))

        for code, s in cb.SUBCATEGORIES.items():
            cur.execute(
                """INSERT INTO subcategories (code, axis, name) VALUES (%s,%s,%s)
                   ON CONFLICT (code) DO UPDATE SET axis=EXCLUDED.axis, name=EXCLUDED.name""",
                (code, s["axis"], s["name"]))

        for d in cb.dimensions():
            cur.execute(
                """INSERT INTO dimensions (code, axis, subcat, name, priority, rank, keywords)
                   VALUES (%s,%s,%s,%s,%s,%s,%s)
                   ON CONFLICT (code) DO UPDATE SET
                     axis=EXCLUDED.axis, subcat=EXCLUDED.subcat, name=EXCLUDED.name,
                     priority=EXCLUDED.priority, rank=EXCLUDED.rank, keywords=EXCLUDED.keywords""",
                (d["code"], d["axis"], d["subcat"], d["name"], d["priority"],
                 d["rank"] or cb.priority_rank(d["priority"]), d["keywords"]))

        for q in cb.questions():
            cur.execute(
                """INSERT INTO questions (id, block, text) VALUES (%s,%s,%s)
                   ON CONFLICT (id) DO UPDATE SET block=EXCLUDED.block, text=EXCLUDED.text""",
                (q["id"], q["block"], q["text"]))

        cur.execute("DELETE FROM question_dimension")
        for link in cb.question_dimension():
            cur.execute(
                """INSERT INTO question_dimension (question_id, dimension, relation)
                   VALUES (%s,%s,%s) ON CONFLICT DO NOTHING""",
                (link["question_id"], link["dimension_code"], link["relation"]))

        for i in cb.interviews():
            cur.execute(
                """INSERT INTO interviews (code, canonical, is_duplicate, sector, institution_type,
                       block, interview_date, n_participants, tcle_signed, status, minutes, turns,
                       chars, participant_share, notes)
                   VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                   ON CONFLICT (code) DO UPDATE SET
                     canonical=EXCLUDED.canonical, is_duplicate=EXCLUDED.is_duplicate,
                     sector=EXCLUDED.sector, institution_type=EXCLUDED.institution_type,
                     block=EXCLUDED.block, interview_date=EXCLUDED.interview_date,
                     n_participants=EXCLUDED.n_participants, tcle_signed=EXCLUDED.tcle_signed,
                     status=EXCLUDED.status, minutes=EXCLUDED.minutes, turns=EXCLUDED.turns,
                     chars=EXCLUDED.chars, participant_share=EXCLUDED.participant_share,
                     notes=EXCLUDED.notes""",
                (i["code"], i.get("canonical") or i["code"], i["duplicate"], i.get("sector") or None,
                 i.get("institution_type") or None, i.get("block") or None,
                 i.get("date") or None, i.get("n_participants") or 1, i["tcle"],
                 i.get("status") or None, i.get("minutes") or None, i.get("turns") or None,
                 i.get("chars") or None, i.get("participant_share") or None,
                 i.get("notes") or None))
    conn.commit()
    s = cb.summary()
    print(f"codebook carregado: {s['dimensoes']} dimensões, {s['perguntas']} perguntas, "
          f"{s['vinculos_crosswalk']} vínculos, {s['codigos_ent']} códigos ENT "
          f"({s['sessoes_distintas']} sessões distintas)")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="só valida o codebook")
    args = ap.parse_args()

    problems = cb.validate()
    if args.check:
        for p in problems:
            print(" -", p)
        print(f"{len(problems)} apontamento(s).")
        return 0

    with connect() as conn:
        apply_schema(conn)
        load_codebook(conn)
    if problems:
        print(f"\n{len(problems)} apontamento(s) de integridade conhecidos "
              f"(veja `python -m database.migrate --check`).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
