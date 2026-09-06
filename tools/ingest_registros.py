"""
Passo 1 do protocolo: conferir os registros de entrevista contra o Anexo 03.

    python -m tools.ingest_registros --acervo "A:\\Projeto_Maringa\\DRIVE_FILES"
    python -m tools.ingest_registros --acervo ... --commit

Varre o acervo, casa os falantes de cada transcrição com a Lista de Entrevistas,
mede a sessão e separa em dois destinos:

  * `codebook/interviews.csv` — camada anonimizada, versionada em git.
    Código, setor, tipo genérico de instituição, bloco, data, TCLE, métricas.
  * `vault/participants.csv`  — identificação (nome, instituição nominal, termo).
    NUNCA versionado; é a carga de `participants_vault` no banco local.

Sem `--commit` o comando apenas confere e mostra; nada é escrito.

Duplicatas são detectadas por md5 do texto da transcrição, não por nome de
arquivo — duas pastas com o mesmo conteúdo são uma sessão só.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from tools.transcript import paragraphs, turns  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT_INTERVIEWS = ROOT / "codebook" / "interviews.csv"
OUT_VAULT = ROOT / "vault" / "participants.csv"

# A equipe que conduz as entrevistas é identificada por padrão, não por lista de
# nomes no código: é quem aparece em mais de duas sessões e não consta da Lista de
# Entrevistas. Isso evita gravar nomes no repositório e sobrevive a troca de equipe.
MIN_SESSOES_EQUIPE = 3

MESES = {"jan": 1, "fev": 2, "mar": 3, "abr": 4, "mai": 5, "jun": 6,
         "jul": 7, "ago": 8, "set": 9, "out": 10, "nov": 11, "dez": 12}

BLOCO = {"Publico": "PUB", "Privado": "PRI",
         "Academia": "ACA", "Sociedade Civil": "SOC", "Especial": "PUB"}

# O setor é gravado sem acento: é o domínio `sector_t` do banco e o rótulo que o
# painel usa para colorir. A Lista escreve "Público"; aqui vira "Publico".
SETOR_CANONICO = {"publico": "Publico", "privado": "Privado", "academia": "Academia",
                  "sociedade civil": "Sociedade Civil", "especial": "Especial"}

# Instituição nominal (como está na Lista) → tipo genérico publicável.
# É a tradução que protege a identificação sem esvaziar a matriz dimensão × ator.
TIPO_GENERICO = [
    ("secretaria de governo", "Secretaria municipal de governo"),
    ("presidente do instituto ambiental", "Direção de órgão ambiental municipal"),
    ("instituto ambiental", "Órgão ambiental municipal"),
    ("seinfra", "Secretaria municipal de infraestrutura"),
    ("defesa civil", "Órgão municipal de proteção e defesa civil"),
    ("camara de vereadores", "Poder Legislativo municipal"),
    ("câmara de vereadores", "Poder Legislativo municipal"),
    ("prefeito", "Liderança política do Executivo municipal"),
    ("instituto de arquitetos", "Entidade profissional de arquitetura e urbanismo"),
    ("conselho de arquitetura", "Conselho profissional de arquitetura e urbanismo"),
    ("universidade livre do meio ambiente", "Organização técnica ambiental"),
    ("unilivre", "Organização técnica ambiental"),
    ("unicesumar", "Universidade privada"),
    ("cooperacao internacional", "Escritório de cooperação internacional de universidade pública"),
    ("cooperação internacional", "Escritório de cooperação internacional de universidade pública"),
    ("uem", "Universidade pública"),
    ("brde", "Banco público de desenvolvimento regional"),
    ("codem", "Conselho de desenvolvimento econômico"),
    ("trevo", "Empresa de mercado de carbono"),
    ("transresíduos", "Empresa de gestão de resíduos"),
    ("alianza", "Empresa de gestão de resíduos"),
]


def fold(s: str) -> str:
    s = unicodedata.normalize("NFKD", str(s or ""))
    return "".join(c for c in s if not unicodedata.combining(c)).strip().lower()


def tipo_generico(inst: str) -> str:
    f = fold(inst)
    for chave, tipo in TIPO_GENERICO:
        if fold(chave) in f:
            return tipo
    return ""


def parse_data(linha: str) -> str:
    """'ago. 7, 2026' → '2026-08-07'."""
    t = fold(linha).replace(".", "").replace(",", "")
    partes = t.split()
    if len(partes) >= 3 and partes[0][:3] in MESES:
        try:
            return f"{int(partes[2]):04d}-{MESES[partes[0][:3]]:02d}-{int(partes[1]):02d}"
        except ValueError:
            pass
    return ""


def ler_lista(acervo: Path) -> list[dict]:
    import openpyxl
    hits = list(acervo.rglob("Lista de Entrevistas.xlsx"))
    if not hits:
        raise SystemExit(f"Lista de Entrevistas.xlsx não encontrada em {acervo}")
    ws = openpyxl.load_workbook(hits[0], data_only=True)["PESSOAS"]
    pessoas, primeiro = [], True
    for row in ws.iter_rows(values_only=True):
        if primeiro:
            primeiro = False
            continue
        if not row[1]:
            continue
        pessoas.append({"nome": str(row[1]).strip(), "email": str(row[2] or "").strip(),
                        "telefone": str(row[3] or "").strip(), "inst": str(row[4] or "").strip(),
                        "setor": str(row[5] or "").strip()})
    return pessoas


def termos_assinados(acervo: Path) -> list[set[str]]:
    """Nomes nos termos assinados, como conjuntos de tokens."""
    out = []
    for p in acervo.rglob("Assinados/*.pdf"):
        nome = p.stem
        for corte in ("Termo de Consentimento_", "_assinado"):
            nome = nome.replace(corte, "")
        out.append({t for t in fold(nome).split() if len(t) > 2})
    return out


def tem_termo(nome: str, assinados: list[set[str]]) -> bool:
    """Casa o nome com um termo assinado.

    Exige dois tokens em comum. Quando a transcrição traz só o primeiro nome
    («Everson»), aceita se ele identificar um único termo — se houver mais de um,
    fica sem casar, e o aviso pede conferência manual.
    """
    toks = {t for t in fold(nome).split() if len(t) > 2}
    if not toks:
        return False
    if any(len(toks & a) >= 2 for a in assinados):
        return True
    if len(toks) == 1:
        return sum(1 for a in assinados if toks & a) == 1
    return False


def casar(nome_falante: str, pessoas: list[dict]) -> dict | None:
    toks = {t for t in fold(nome_falante).split() if len(t) > 2}
    melhor, score_max = None, 0
    for p in pessoas:
        score = len(toks & {t for t in fold(p["nome"]).split() if len(t) > 2})
        if score > score_max:
            melhor, score_max = p, score
    return melhor


def identificar_equipe(transcricoes: list[Path], pessoas: list[dict]) -> set[str]:
    """Falantes recorrentes que não constam da Lista: a equipe da consultoria."""
    presenca: dict[str, int] = {}
    for path in transcricoes:
        for s in {t.speaker for t in turns(path)}:
            if s.startswith("A transcrição"):
                continue
            presenca[fold(s)] = presenca.get(fold(s), 0) + 1
    return {s for s, n in presenca.items()
            if n >= MIN_SESSOES_EQUIPE and casar(s, pessoas) is None}


def processar(acervo: Path) -> tuple[list[dict], list[dict], list[str]]:
    pessoas = ler_lista(acervo)
    assinados = termos_assinados(acervo)
    transcricoes = sorted(acervo.rglob("*_Transcrição.docx"))
    entrevistadores = identificar_equipe(transcricoes, pessoas)
    avisos: list[str] = []
    sessoes, vault, hashes = [], [], {}

    for path in transcricoes:
        code = path.name.replace("_Transcrição.docx", "")
        texto = "\n".join(paragraphs(path))
        h = hashlib.md5(texto.encode("utf-8")).hexdigest()
        tt = turns(path)

        if h in hashes:
            avisos.append(f"{code}: conteúdo idêntico a {hashes[h]} — registrado como duplicata")
            sessoes.append({"code": code, "canonical": hashes[h], "duplicate": True,
                            "status": "Duplicata"})
            continue
        hashes[h] = code

        falas: dict[str, int] = {}
        for t in tt:
            if t.speaker.startswith("A transcrição"):
                continue
            falas[t.speaker] = falas.get(t.speaker, 0) + len(t.text)
        participantes = [s for s in falas if fold(s) not in entrevistadores]
        total = sum(falas.values())
        part = sum(falas[s] for s in participantes)

        casados = [(s, casar(s, pessoas)) for s in participantes]
        setores = {c["setor"] for _, c in casados if c and c["setor"]}
        tipos = [tipo_generico(c["inst"]) for _, c in casados if c]
        tipos = [t for t in tipos if t]
        for s, c in casados:
            if c is None:
                avisos.append(f"{code}: falante «{s}» não consta da Lista de Entrevistas")

        secs = lambda t: sum(int(x) * f for x, f in zip(t.split(":"), (3600, 60, 1)))  # noqa: E731
        minutos = round((secs(tt[-1].ts) - secs(tt[0].ts)) / 60) if tt else 0
        setores = {SETOR_CANONICO.get(fold(x), x) for x in setores}
        setor = sorted(setores)[0] if len(setores) == 1 else ("; ".join(sorted(setores)) or "")
        if len(setores) > 1:
            avisos.append(f"{code}: participantes de setores distintos ({setor}) — codificar por falante")

        assinado = [tem_termo(c["nome"], assinados) if c else tem_termo(s, assinados)
                    for s, c in casados]
        tcle = bool(assinado) and all(assinado)
        if not tcle:
            faltam = [s for s, ok in zip([s for s, _ in casados], assinado) if not ok]
            avisos.append(f"{code}: termo assinado não localizado para {', '.join(faltam)}")

        sessoes.append({
            "code": code, "canonical": code, "duplicate": False, "sector": setor,
            "institution_type": "; ".join(dict.fromkeys(tipos)),
            "block": BLOCO.get(setor, ""), "date": parse_data(paragraphs(path)[0]),
            "n_participants": len(participantes), "tcle": tcle, "status": "Transcrita",
            "minutes": minutos, "turns": len(tt), "chars": total,
            "participant_share": round(100 * part / total) if total else 0,
        })
        for s, c in casados:
            vault.append({"interview_code": code, "falante_transcricao": s,
                          "nome": c["nome"] if c else "", "instituicao": c["inst"] if c else "",
                          "email": c["email"] if c else "", "telefone": c["telefone"] if c else "",
                          "setor": c["setor"] if c else "",
                          "casado_por": "lista" if c else "MANUAL"})
    return sessoes, vault, avisos


def preservar(sessoes: list[dict]) -> list[dict]:
    """Mantém `status` (Codificada) e a triagem já medida do arquivo anterior."""
    if not OUT_INTERVIEWS.exists():
        return sessoes
    antigo = {r["code"]: r for r in csv.DictReader(OUT_INTERVIEWS.open(encoding="utf-8-sig"))}
    for s in sessoes:
        a = antigo.get(s["code"])
        if not a:
            continue
        if a.get("status") == "Codificada":
            s["status"] = "Codificada"
        # campos curados à mão: só são preenchidos pelo arquivo anterior quando o
        # casamento automático não conseguiu determiná-los (participante fora da Lista)
        for campo in ("sector", "institution_type", "block"):
            if not s.get(campo) and a.get(campo):
                s[campo] = a[campo]
        for campo in ("n_dim_candidates", "n_hits", "notes"):
            if a.get(campo):
                s.setdefault(campo, a[campo])
    return sessoes


COLS = ["code", "canonical", "duplicate", "sector", "institution_type", "block", "date",
        "n_participants", "tcle", "status", "minutes", "turns", "chars",
        "participant_share", "n_dim_candidates", "n_hits", "notes"]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--acervo", required=True, help="pasta do acervo (DRIVE_FILES)")
    ap.add_argument("--commit", action="store_true", help="grava os arquivos")
    args = ap.parse_args()

    sessoes, vault, avisos = processar(Path(args.acervo))
    sessoes = preservar(sessoes)

    vivas = [s for s in sessoes if not s["duplicate"]]
    print(f"{len(sessoes)} registros · {len(vivas)} sessões distintas · "
          f"{sum(s.get('minutes') or 0 for s in vivas)} min · "
          f"{sum(s.get('turns') or 0 for s in vivas)} turnos\n")
    for s in sessoes:
        print(f"  {s['code']:<18} {s.get('sector',''):<16} {s.get('institution_type','')[:52]}")
    if avisos:
        print(f"\n{len(avisos)} apontamento(s):")
        for a in avisos:
            print("  !", a)

    if not args.commit:
        print("\n(nada gravado — use --commit)")
        return 0

    OUT_INTERVIEWS.parent.mkdir(parents=True, exist_ok=True)
    with OUT_INTERVIEWS.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLS, extrasaction="ignore")
        w.writeheader()
        w.writerows(sessoes)
    OUT_VAULT.parent.mkdir(parents=True, exist_ok=True)
    with OUT_VAULT.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(vault[0]))
        w.writeheader()
        w.writerows(vault)
    print(f"\ngravado: {OUT_INTERVIEWS.relative_to(ROOT)} e {OUT_VAULT.relative_to(ROOT)} "
          f"(vault fora do git)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
