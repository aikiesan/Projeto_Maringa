"""
Pré-triagem por palavras-chave sobre a transcrição.

    python -m tools.triage ENT-003 --md
    python -m tools.triage ENT-001-ENT-002 --dim 2.2.1

Varre a transcrição, agrupa os turnos candidatos por dimensão e devolve marca de
tempo, falante e a palavra que disparou o vínculo.

A triagem NÃO codifica nada: produz o roteiro de leitura e a trilha de auditoria
de por que aquele trecho foi olhado. Falsos positivos são esperados e descartados
na leitura (passo 3 do protocolo).

A saída contém nomes de falantes — é material de trabalho do codificador, nunca
entra na camada de análise nem no repositório.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from database import codebook as cb          # noqa: E402
from tools.transcript import fold, turns     # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
TRANSCRIPTS = ROOT / "transcricoes"


def find_transcript(code: str) -> Path:
    for pat in (f"{code}.docx", f"{code}_Transcrição.docx", f"{code}.txt"):
        hits = list(TRANSCRIPTS.rglob(pat))
        if hits:
            return hits[0]
    hits = list(TRANSCRIPTS.rglob(f"*{code}*"))
    if hits:
        return hits[0]
    raise SystemExit(f"transcrição de {code} não encontrada em {TRANSCRIPTS}")


def scan(code: str, only_dim: str | None = None) -> dict[str, list]:
    path = find_transcript(code)
    tt = turns(path)
    lex = cb.lexicon()
    if only_dim:
        lex = {only_dim: lex[only_dim]}
    # palavra inteira, tolerante a acento
    pats = {d: [(k, re.compile(rf"(?<!\w){re.escape(k)}(?!\w)")) for k in kws]
            for d, kws in lex.items()}

    found: dict[str, list] = {}
    for t in tt:
        folded = fold(t.text)
        for dim, kps in pats.items():
            hit = [k for k, p in kps if p.search(folded)]
            if hit:
                found.setdefault(dim, []).append((t, hit))
    return found


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("code")
    ap.add_argument("--md", action="store_true", help="saída em markdown, com os trechos")
    ap.add_argument("--dim", help="restringe a uma dimensão")
    ap.add_argument("--min", type=int, default=1, help="mínimo de ocorrências para listar")
    args = ap.parse_args()

    found = scan(args.code, args.dim)
    dims = cb.dimension_index()
    order = sorted(found, key=lambda d: (-dims[d]["rank"], -len(found[d]), d))

    n_hits = sum(len(v) for v in found.values())
    print(f"# Triagem {args.code}\n")
    print(f"{len(found)} dimensões candidatas · {n_hits} ocorrências\n")

    for dim in order:
        rows = found[dim]
        if len(rows) < args.min:
            continue
        d = dims[dim]
        print(f"## {dim} · {d['name']}  ({d['priority']}, {len(rows)} ocorrências)")
        if not args.md:
            print()
            continue
        for t, kws in rows:
            txt = t.text if len(t.text) <= 400 else t.text[:400] + "…"
            print(f"- `{t.ts}` **{t.speaker}** _[{', '.join(kws)}]_\n  > {txt}")
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
