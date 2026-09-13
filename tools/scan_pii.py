# -*- coding: utf-8 -*-
"""Varredura de identificadores na saida aberta. Sai com codigo != 0 se achar algo."""
import re, sys, csv, unicodedata, argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lista_pessoas import carregar_todas, ListaIndisponivel  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]

_ap = argparse.ArgumentParser(description=__doc__)
_ap.add_argument("--alvo", default=str(ROOT / "site" / "publico.html"),
                 help="HTML da camada aberta a varrer")
_args = _ap.parse_args()
ALVO = Path(_args.alvo)

if not ALVO.exists():
    print(f"alvo inexistente: {ALVO}")
    sys.exit(2)
h = ALVO.read_text(encoding="utf-8")
achados = []

PADROES = {
    "e-mail": r"[\w.+-]+@[\w-]+\.(?:com|br|org|gov|net|edu)[\w.]*",
    "telefone": r"(?<![\d/:.-])\b\(?\d{2}\)?[\s.-]?9?\d{4}[\s.-]\d{4}\b",
    "CPF": r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b",
    "CNPJ": r"\b\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}\b",
    "tratamento": r"\b(?:Sr\.|Sra\.|Dr\.|Dra\.)\s+[A-ZÁÉÍÓÚÂÊÔÃÕÇ]",
    "risco": r"risco residual de reidentifica|no nível de direção|Sessão com assessoria|\bEspecial\b",
}
for rotulo, pat in PADROES.items():
    for m in re.finditer(pat, h):
        achados.append((rotulo, h[max(0, m.start() - 60):m.end() + 40].replace("\n", " ")))

# nomes proprios da base de participantes. Falha de carga e ACHADO, nao aviso:
# varrer sem a lista e sair 0 seria declarar limpo o que nao foi olhado.
try:
    nomes = set()
    for _completo in carregar_todas(ROOT):
        for tok in _completo.split():
            if len(tok) > 3 and tok[0].isupper():
                nomes.add(tok)
    print(f"lista de participantes: {len(nomes)} tokens distintivos")
    for nome in sorted(nomes):
        for m in re.finditer(r"(?<![\wÀ-ÿ])" + re.escape(nome) + r"(?![\wÀ-ÿ])", h):
            achados.append(("nome:" + nome, h[max(0, m.start() - 60):m.end() + 40].replace("\n", " ")))
except ListaIndisponivel as e:
    achados.append(("IMPOSSIVEL VARRER - lista de nomes nao carregou", str(e)))

if achados:
    print(f"{len(achados)} ACHADO(S) — a saida NAO pode ser publicada:")
    for rotulo, ctx in achados[:40]:
        print(f"  [{rotulo}] ...{ctx[:120]}...")
    sys.exit(1)
print("varredura limpa: nenhum identificador encontrado na saida aberta")
