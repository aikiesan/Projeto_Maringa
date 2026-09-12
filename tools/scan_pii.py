# -*- coding: utf-8 -*-
"""Varredura de identificadores na saida aberta. Sai com codigo != 0 se achar algo."""
import re, sys, csv, unicodedata

ALVO = "/home/claude/painel/index.html"
LISTA = "/mnt/user-data/uploads/Projeto_Maringa/DRIVE_FILES/drive-download-20260906T102534Z-1-001/Lista de Entrevistas.xlsx"

h = open(ALVO, encoding="utf-8").read()
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

# nomes proprios da base de participantes
try:
    import openpyxl
    wb = openpyxl.load_workbook(LISTA, data_only=True)
    nomes = set()
    for r in wb["PESSOAS"].iter_rows(min_row=2, values_only=True):
        if r and r[1] and isinstance(r[1], str):
            for tok in r[1].split():
                if len(tok) > 3 and tok[0].isupper():
                    nomes.add(tok)
    for nome in sorted(nomes):
        for m in re.finditer(r"(?<![\wÀ-ÿ])" + re.escape(nome) + r"(?![\wÀ-ÿ])", h):
            achados.append(("nome:" + nome, h[max(0, m.start() - 60):m.end() + 40].replace("\n", " ")))
except Exception as e:
    achados.append(("ERRO ao carregar a lista de nomes", str(e)))

if achados:
    print(f"{len(achados)} ACHADO(S) — a saida NAO pode ser publicada:")
    for rotulo, ctx in achados[:40]:
        print(f"  [{rotulo}] ...{ctx[:120]}...")
    sys.exit(1)
print("varredura limpa: nenhum identificador encontrado na saida aberta")
