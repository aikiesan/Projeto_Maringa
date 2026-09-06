"""
Leitura das transcrições .docx do acervo.

Formato observado: parágrafos soltos, onde uma linha `HH:MM:SS` isolada marca o
tempo dos turnos seguintes e cada turno é `Falante: texto`.

Não grava nada e não sai da memória — o texto bruto contém nomes e nunca deve
ser escrito na camada de análise.
"""

from __future__ import annotations

import html
import re
import unicodedata
import zipfile
from dataclasses import dataclass
from pathlib import Path

TS_RE = re.compile(r"^(\d{1,2}:\d{2}:\d{2})$")
TURN_RE = re.compile(r"^([^:]{2,60}):\s*(.*)$")


@dataclass
class Turn:
    idx: int
    ts: str
    speaker: str
    text: str


def paragraphs(path: str | Path) -> list[str]:
    xml = zipfile.ZipFile(path).read("word/document.xml").decode("utf-8")
    out = []
    for para in xml.split("</w:p>"):
        t = "".join(re.findall(r"<w:t[^>]*>(.*?)</w:t>", para, re.S))
        t = html.unescape(t).strip()
        if t:
            out.append(t)
    return out


def turns(path: str | Path) -> list[Turn]:
    """Turnos da transcrição.

    Tudo que vem antes da primeira marca de tempo é cabeçalho (data e título da
    reunião) e é descartado — senão uma linha como «Reunião em 2 de set. às 12:30»
    é lida como falante por causa dos dois-pontos.
    """
    ts = "00:00:00"
    out: list[Turn] = []
    comecou = False
    for p in paragraphs(path):
        m = TS_RE.match(p)
        if m:
            ts = m.group(1)
            comecou = True
            continue
        if not comecou:
            continue
        m = TURN_RE.match(p)
        if m:
            out.append(Turn(len(out), ts, m.group(1).strip(), m.group(2).strip()))
        elif out:                      # continuação do turno anterior
            out[-1].text += " " + p
    return out


def fold(s: str) -> str:
    s = unicodedata.normalize("NFKD", s or "")
    return "".join(c for c in s if not unicodedata.combining(c)).lower()


def stats(ts_turns: list[Turn], interviewers: set[str]) -> dict:
    total = sum(len(t.text) for t in ts_turns)
    part = sum(len(t.text) for t in ts_turns if t.speaker not in interviewers)
    def secs(t: str) -> int:
        h, m, s = (int(x) for x in t.split(":"))
        return h * 3600 + m * 60 + s

    first = ts_turns[0].ts if ts_turns else "00:00:00"
    last = ts_turns[-1].ts if ts_turns else "00:00:00"
    return {
        "turns": len(ts_turns),
        "chars": total,
        "participant_share": round(100 * part / total) if total else 0,
        "first_ts": first,
        "last_ts": last,
        # duração efetiva do registro: do primeiro ao último carimbo
        "minutes_span": round((secs(last) - secs(first)) / 60),
        "speakers": sorted({t.speaker for t in ts_turns}),
    }
