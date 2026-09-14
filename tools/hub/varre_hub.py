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
# A pagina de conselhos saiu do Hub em 13/09. O conjunto fica vazio de
# proposito: sem excecao, nome de conselheiro passa a ser achado em QUALQUER
# pagina, que e a regra mais forte e a que agora vale.
PERMITE_CONSELHEIRO: set[str] = set()
# O mapeamento institucional do Produto 3 DESCREVE organizacoes com as mesmas
# expressoes («Orgao ambiental municipal: licenciamento...», «Universidade
# publica»). Ali e conteudo, nao rotulo de sessao: a pagina nao diz quem foi
# entrevistado, so quem foi mapeado. A excecao vale apenas para ela.
PERMITE_ROTULO = {"instituicoes.html"}

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


# Rotulos de tipo institucional que sao UNICOS de uma sessao. Com a lista
# nominal de pessoas mobilizadas e entrevistadas, que e entregavel do termo de
# referencia, um rotulo unico deixa de ser generico: ele identifica a sessao e,
# por tabela, quem falou. 13 dos 15 rotulos do codebook sao unicos.
# Os nao unicos ficam de fora daqui porque tambem sao descricao legitima de
# organizacao em outras paginas (o mapeamento do Produto 3 descreve o IAM como
# «Orgao ambiental municipal», e ali isso e conteudo, nao rotulo de sessao).
import collections as _col

_rotulos = _col.Counter()
_inter = ROOT / "codebook" / "interviews.csv"
if _inter.exists():
    with _inter.open(encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f):
            t = (r.get("institution_type") or "").strip()
            if t:
                _rotulos[t] += 1
rotulos_unicos = {t for t, q in _rotulos.items() if q == 1}
# Os rotulos GENERALIZADOS tambem entram: sao eles que chegavam a pagina, e
# vigiar so o valor cru do codebook deixaria passar exatamente o que era
# publicado. Descobri isso porque o teste negativo nao acusou o rotulo
# injetado.
rotulos_unicos |= {"Gabinete do Executivo municipal",
                   "Direção de órgão ambiental municipal",
                   "Liderança política do Executivo municipal"}
print(f"rotulos de sessao unicos vigiados: {len(rotulos_unicos)}")



def _texto_docx(caminho):
    """Todo o texto de um .docx: paragrafos e celulas de tabela."""
    try:
        import docx
    except ImportError:
        print(f"IMPOSSIVEL VARRER {caminho.name}: python-docx ausente.")
        sys.exit(2)
    d = docx.Document(str(caminho))
    partes = [par.text for par in d.paragraphs]
    for t in d.tables:
        for row in t.rows:
            partes += [c.text for c in row.cells]
    return chr(10).join(partes)


achados = []
for p in sorted(SAIDA.rglob("*")):
    if not p.is_file() or p.suffix not in (".html", ".csv", ".json", ".css",
                                           ".docx", ".txt", ".xml"):
        continue
    rel = str(p.relative_to(SAIDA)).replace(os.sep, "/")
    if rel == "painel.html":
        continue  # já auditado pelo tools/scan_pii.py na geração
    if p.suffix == ".docx":
        # ponto cego ate 13/09: a varredura so lia texto puro, e um .docx no
        # hub_saida passava inteiro pelo portao. O mesmo valia para imagem, que
        # continua fora do alcance — por isso as capturas de tela estao no
        # .gitignore em vez de dependerem daqui.
        txt = _texto_docx(p)
    else:
        txt = p.read_text(encoding="utf-8", errors="replace")

    for rotulo, pat in PADROES.items():
        # a página de transcrições EXPLICA o risco residual; explicar não é vazar
        # explicar o risco residual nao e vaza-lo: a pagina de transcricoes e a
        # Nota sobre a anonimizacao (Anexo 05), dentro do Produto 4, descrevem a
        # limitacao declarada do protocolo. Sao o lugar onde isso deve aparecer.
        if rotulo == "rotulo de risco" and rel in ("transcricoes.html",
                                                   "produto4.html",
                                                   "Produto_04_publico.docx"):
            continue
        # A capa do relatorio traz o endereco e o CNPJ da executora. E dado
        # institucional de empresa, publico por definicao, e nao identificador
        # de participante — que e o que este padrao existe para pegar.
        if rotulo == "CNPJ" and rel == "Produto_04_publico.docx":
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

    for rot in (sorted(rotulos_unicos) if rel not in PERMITE_ROTULO else ()):
        if rot in txt:
            i = txt.index(rot)
            achados.append((rel, "rotulo de sessao:" + rot,
                            txt[max(0, i - 60):i + 90]))

    if rel not in PERMITE_CONSELHEIRO:
        for nome in sorted(nomes_conselheiro):
            for m in re.finditer(r"(?<![\wÀ-ÿ])" + re.escape(nome) + r"(?![\wÀ-ÿ])", txt):
                achados.append((rel, "conselheiro fora de lugar:" + nome,
                                txt[max(0, m.start() - 60):m.end() + 40]))

# ---------------------------------------------------------------- retencao
# O portao le `codebook/retencao_publica.csv` por conta propria, e nao confia no
# gerador. Pega os dois casos que o `continue` do build nao pega: alguem mexeu
# no laco, e `hub_saida/` velho que nao foi limpo antes de publicar.
from tools.hub import retencao as _R                                # noqa: E402

for _cod in _R.confere_saida(SAIDA / "transcricoes"):
    achados.append((f"transcricoes/{_cod}.html", "sessao retida publicada",
                    "autoidentificacao de empregador; ver codebook/retencao_publica.csv"))

_retidas = _R.retidas()
for _p in sorted(SAIDA.rglob("*")):
    if not _p.is_file() or _p.suffix.lower() not in (".html", ".xml", ".css", ".json"):
        continue
    _t = _p.read_text(encoding="utf-8", errors="ignore")
    for _cod in sorted(_retidas):
        if f"transcricoes/{_cod}.html" in _t:
            achados.append((str(_p.relative_to(SAIDA)).replace("\\", "/"),
                            "link para sessao retida:" + _cod,
                            "a pagina nao existe e o link nao pode existir"))

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
print(f"  nomes de conselheiro (proibidos em toda página): "
      f"{len(nomes_conselheiro)}")
