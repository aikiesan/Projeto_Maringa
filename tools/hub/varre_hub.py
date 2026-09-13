# -*- coding: utf-8 -*-
"""Varredura de identificadores no Hub inteiro, antes de publicar.

Sai com código != 0 se achar qualquer coisa. É o portão: nada vai ao ar sem
passar por aqui.

A base de conselheiros é a exceção declarada — composição de conselho municipal
é ato público, publicada em portaria, e aparece nominalmente por decisão do
projeto. Esses nomes são permitidos SOMENTE nas páginas de conselhos e no CSV
correspondente; em qualquer outra página do Hub eles são achado.
"""
import re, sys, csv, glob, os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lista_pessoas import carregar_todas, ListaIndisponivel  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
SAIDA = ROOT / "hub_saida"
PERMITE_CONSELHEIRO = {"conselhos.html"}

PADROES = {
    "e-mail": r"[\w.+-]+@[\w-]+\.(?:com|br|org|gov|net|edu)[\w.]*",
    "telefone": r"(?<![\d/:.-])\b\(?\d{2}\)?[\s.-]?9\d{4}[\s.-]\d{4}\b",
    "CPF": r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b",
    "CNPJ": r"\b\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}\b",
    "rotulo de risco": r"risco residual de reidentifica|no nível de direção|"
                       r"Sessão com assessoria",
    "setor Especial": r"\bEspecial\b",
}

# Tokens que também são nome próprio mas aparecem legitimamente: topônimos,
# nomes de órgão, e palavras portuguesas comuns. Um token destes sozinho não
# gera achado — o custo de acusar «Defesa Civil» é maior que o de deixar o
# sobrenome para a conferência por nome completo.
AMBIGUOS = {
    "Civil", "Defesa", "Paulo", "Dias", "Jardim", "Franco", "Cruz", "Castro",
    "Braun", "Lee", "Barros", "Leão", "Leao", "Sene", "Rego", "Soares", "Telles",
    "Nacional", "Estadual", "Municipal", "Santos", "Costa", "Campos", "Ribeiro",
    "Verde", "Ambiental", "Urbano", "Livre", "Norte", "Grande", "Alto", "Bom",
    # logradouros e predios publicos citados no Produto 4. Sao endereco e local
    # de evento, nao pessoa — «Avenida Colombo», «Auditorio Helio Moreira»,
    # «Rua Padre Severino», bairro «Sao Pedro». A conferencia por nome COMPLETO
    # continua valendo para todos eles; o que se dispensa e o token sozinho.
    "Colombo", "Moreira", "Severino", "Pedro",
}

# nomes de participantes e convidados — nunca podem aparecer em página nenhuma
nomes_participantes = set()     # tokens distintivos
nomes_completos = set()         # nomes inteiros, sempre achado
# Falha dura, de propósito: uma varredura que não carregou a lista não está
# limpa, está cega — e sairia 0 sem ter procurado nada. Ver tools/lista_pessoas.py.
try:
    _lista = carregar_todas(ROOT)
except ListaIndisponivel as e:
    print("IMPOSSIVEL VARRER - a lista de participantes nao carregou:")
    print(f"  {e}")
    print("  Sem ela esta varredura nao procura nome nenhum. "
          "O Hub NAO pode ser publicado.")
    sys.exit(2)

for limpo in _lista:
    if len(limpo.split()) >= 2:
        nomes_completos.add(limpo)
    for tok in limpo.split():
        if len(tok) > 3 and tok[0].isupper() and tok not in AMBIGUOS:
            nomes_participantes.add(tok)
print(f"lista de participantes: {len(_lista)} nomes, "
      f"{len(nomes_completos)} completos, {len(nomes_participantes)} tokens distintivos")

# nomes de conselheiro — permitidos só nas páginas de conselho
# A fonte e `data/comdema.json`, o dado versionado — NAO a saida gerada. Lia-se
# `hub_saida/dados/comdema.csv`, mas essa pagina de downloads foi desativada em
# 13/09: se a lista viesse da saida, remover o arquivo esvaziaria o conjunto em
# silencio e a varredura pararia de checar vazamento de nome de conselheiro,
# ainda saindo 0.
import json as _json

nomes_conselheiro = set()
_cm = ROOT / "data" / "comdema.json"
_membros = []
if _cm.exists():
    _membros = _json.loads(_cm.read_text(encoding="utf-8")).get("members", [])
if not _membros:
    print("IMPOSSIVEL VARRER - data/comdema.json ausente ou vazio:", _cm)
    print("  Sem ele a varredura nao detecta nome de conselheiro fora de lugar.")
    sys.exit(2)
for _mb in _membros:
    for tok in (_mb.get("name") or "").split():
        if len(tok) > 3 and tok[0].isupper() and tok not in AMBIGUOS:
            nomes_conselheiro.add(tok)
print(f"conselheiros: {len(_membros)} registros, {len(nomes_conselheiro)} tokens")

so_participante = nomes_participantes - nomes_conselheiro

# nomes completos de conselheiro, para casar por primeiro+último token — a
# grafia difere entre as bases («Sidnei Telles» × «Sidnei Telles Filho»)
_cons_chaves = set()
for _mb in _membros:
    t = [x.lower() for x in (_mb.get("name") or "").split() if len(x) > 3]
    if t:
        _cons_chaves.add((t[0], t[-1]))
        _cons_chaves.add((t[0], t[1] if len(t) > 1 else t[0]))


def _e_conselheiro(nome):
    t = [x.lower() for x in nome.split() if len(x) > 3]
    if not t:
        return False
    return (t[0], t[-1]) in _cons_chaves or (t[0], t[1] if len(t) > 1 else t[0]) in _cons_chaves

achados = []
for p in sorted(SAIDA.rglob("*")):
    if not p.is_file() or p.suffix not in (".html", ".csv", ".json", ".css"):
        continue
    rel = str(p.relative_to(SAIDA)).replace(os.sep, "/")
    if rel == "painel.html":
        continue  # já auditado pelo tools/scan_pii.py na geração
    txt = p.read_text(encoding="utf-8", errors="replace")

    for rotulo, pat in PADROES.items():
        # a página de transcrições EXPLICA o risco residual; explicar não é vazar
        # explicar o risco residual nao e vaza-lo: a pagina de transcricoes e a
        # Nota sobre a anonimizacao (Anexo 05), dentro do Produto 4, descrevem a
        # limitacao declarada do protocolo. Sao o lugar onde isso deve aparecer.
        if rotulo == "rotulo de risco" and rel in ("transcricoes.html",
                                                   "produto4.html"):
            continue
        for m in re.finditer(pat, txt):
            achados.append((rel, rotulo, txt[max(0, m.start() - 60):m.end() + 40]))

    for nome in sorted(nomes_completos):
        if nome not in txt:
            continue
        # parte das pessoas do acervo também é conselheiro: nas duas páginas de
        # conselho o nome é conteúdo publicado por decisão do projeto, não vazamento
        if rel in PERMITE_CONSELHEIRO and _e_conselheiro(nome):
            continue
        i = txt.index(nome)
        achados.append((rel, "nome completo:" + nome, txt[max(0, i - 60):i + 80]))

    for nome in sorted(so_participante):
        for m in re.finditer(r"(?<![\wÀ-ÿ])" + re.escape(nome) + r"(?![\wÀ-ÿ])", txt):
            achados.append((rel, "participante:" + nome,
                            txt[max(0, m.start() - 60):m.end() + 40]))

    if rel not in PERMITE_CONSELHEIRO:
        for nome in sorted(nomes_conselheiro):
            for m in re.finditer(r"(?<![\wÀ-ÿ])" + re.escape(nome) + r"(?![\wÀ-ÿ])", txt):
                achados.append((rel, "conselheiro fora de lugar:" + nome,
                                txt[max(0, m.start() - 60):m.end() + 40]))

if achados:
    print(f"{len(achados)} ACHADO(S) — o Hub NÃO pode ser publicado\n")
    vistos = {}
    for rel, rotulo, ctx in achados:
        vistos.setdefault((rel, rotulo), ctx)
    for (rel, rotulo), ctx in list(vistos.items())[:60]:
        print(f"  [{rel}] {rotulo}\n      …{ctx[:130].strip()}…")
    print(f"\n  ({len(vistos)} combinações distintas)")
    sys.exit(1)

print(f"varredura limpa — {sum(1 for _ in SAIDA.rglob('*') if _.is_file())} arquivos, "
      f"nenhum identificador fora de lugar")
print(f"  nomes de participante verificados: {len(so_participante)}")
print(f"  nomes de conselheiro (permitidos só em {', '.join(sorted(PERMITE_CONSELHEIRO))}): "
      f"{len(nomes_conselheiro)}")
