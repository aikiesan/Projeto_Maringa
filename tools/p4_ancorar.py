"""
Ancoragem da Seção 3 do Produto 04 nas evidências codificadas.

    python -m tools.p4_ancorar --docx "Produto 4.docx"
    python -m tools.p4_ancorar --docx ... --csv saida.csv --top 5

O TdR pede repositório auditável, com origem e trecho. A Seção 3 hoje é narrativa
corrida: nenhuma das 94 afirmações cita sessão ou marca de tempo. Esta ferramenta
não reescreve a narrativa — propõe, para cada afirmação, as evidências do **mesmo
setor** que mais se sobrepõem a ela, com código, dimensão e carimbo de tempo.

A decisão de aceitar cada âncora é humana. O que a ferramenta garante é que a
âncora proposta vem do setor certo e que o caminho afirmação → evidência → sessão
→ marca de tempo fecha; o que ela não faz é julgar se a evidência de fato sustenta
a afirmação. Sobreposição léxica acha candidato, não prova.
"""

from __future__ import annotations

import argparse
import csv
import html
import re
import sys
import unicodedata
import zipfile
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from tools import redacao as R                                   # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
CB = ROOT / "codebook"
VAULT = ROOT / "vault"

# Subseção da Seção 3 → setores do registro que a sustentam.
SETOR_DA_SECAO = {
    "Setor Público": {"Publico", "Especial"},
    "Setor Privado": {"Privado"},
    "Academia": {"Academia"},
    "Sociedade Civil": {"Sociedade Civil"},
}

VAZIAS = set("""a o e de da do das dos em no na nos nas para por com sem sob sobre
que se como mais menos muito pouco ja nao sim ser estar ter haver fazer todo toda
todos todas outro outra um uma uns umas este esta isso esse essa aquilo seu sua
seus suas ao aos as os pelo pela pelos pelas entre ate desde apos antes durante
onde quando quem qual quais cujo porque pois entao assim tambem so apenas ainda
maior menor grande pequeno novo nova primeiro segundo ha e' sao foi era sera
ha tem tem-se pode deve precisa falta existe""".split())


def dobrar(s: str) -> str:
    s = unicodedata.normalize("NFKD", str(s or ""))
    return "".join(c for c in s if not unicodedata.combining(c)).lower()


def conteudo(texto: str) -> set[str]:
    """Palavras de conteúdo, sem acento, com pelo menos 4 letras."""
    return {t for t in re.findall(r"[a-z]{4,}", dobrar(texto)) if t not in VAZIAS}


def paragrafos(path: Path) -> list[tuple[str, str]]:
    xml = zipfile.ZipFile(path).read("word/document.xml").decode("utf-8")
    out = []
    for p in re.findall(r"<w:p(?:\s[^>]*)?>.*?</w:p>", xml, re.S):
        t = html.unescape("".join(re.findall(r"<w:t(?:\s[^>]*)?>(.*?)</w:t>", p, re.S))).strip()
        st = re.search(r'<w:pStyle w:val="([^"]+)"', p)
        out.append((st.group(1) if st else "", t))
    return out


def afirmacoes(path: Path) -> list[dict]:
    """As afirmações em lista da Seção 3, com a subseção e o setor a que pertencem."""
    paras = paragrafos(path)
    inicio = next((i for i, (st, t) in enumerate(paras)
                   if st.startswith("Ttulo1") and "ANÁLISE E RESUMO" in t), None)
    if inicio is None:
        raise SystemExit("Seção 3 (ANÁLISE E RESUMO...) não encontrada no documento")

    out, setor, sub = [], None, None
    for st, t in paras[inicio + 1:]:
        if st.startswith("Ttulo1"):
            break
        if st.startswith("Ttulo2"):
            setor, sub = t, None
        elif st.startswith("Ttulo3"):
            sub = t
        elif st.startswith("PargrafodaLista") and t and setor:
            # «Riscos e Vulnerabilidades Identificados:» é chamada da lista que vem
            # a seguir, não afirmação — ancorá-la produziria uma âncora para um
            # título, e o item real ficaria sem a sua.
            chamada = t.endswith(":") and len(conteudo(t)) <= 4
            out.append({"n": len(out) + 1, "setor": setor, "subsecao": sub or "",
                        "texto": t, "chamada": chamada})
    return out


def regras_da_narrativa() -> list[R.Regra]:
    """Regras para redigir o texto da própria narrativa do Produto 04.

    A Seção 3 nomeia participantes — «a figura do prefeito, Silvio Barros» — e a
    ancoragem emparelha cada afirmação com o código da sessão. Uma coisa ao lado
    da outra entrega ENT-015, que é justamente a sessão da liderança do Executivo.
    O artefato de auditoria não pode reintroduzir o que o corpus já protegeu.

    Sem `vault/`, não há dicionário determinístico: a ferramenta avisa e segue,
    porque a ancoragem continua útil — mas o CSV não deve ser versionado assim.
    """
    def ler(nome: str) -> list[dict]:
        caminho = VAULT / nome
        if not caminho.exists():
            return []
        with caminho.open(encoding="utf-8-sig", newline="") as f:
            return list(csv.DictReader(f))

    pessoas, terceiros = ler("pessoas.csv"), ler("terceiros.csv")
    apelidos = {dobrar(r["nome"]): [a for a in (r.get("apelidos") or "").split("|") if a]
                for r in ler("apelidos.csv")}
    if not pessoas:
        print("AVISO: vault/pessoas.csv ausente — a coluna «afirmacao» sai como está "
              "no documento, com nomes. Não versione o CSV assim.", file=sys.stderr)
        return []

    regras = []
    for r in pessoas:
        regras += R.regras_pessoa(r["nome"], "[participante]",
                                  apelidos.get(dobrar(r["nome"]), ()), "base")[0]
    for r in terceiros:
        apes = [r["nome"]] + [a for a in (r.get("apelidos") or "").split("|") if a]
        regras += R.regras_pessoa(r["nome"], "[terceiro]", apes, "terceiro")[0]
    return regras + R.regras_contato()


def evidencias() -> list[dict]:
    setor = {}
    with (CB / "interviews.csv").open(encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f):
            setor[r["code"]] = r["sector"]
    dims = {}
    with (CB / "dimensions.csv").open(encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f):
            dims[r["code"]] = r
    out = []
    for p in sorted((CB / "evidencias").glob("ENT-*.csv")):
        with p.open(encoding="utf-8-sig", newline="") as f:
            for r in csv.DictReader(f):
                r["setor"] = setor.get(r["interview"], "")
                d = dims.get(r["dim"], {})
                r["dim_nome"] = d.get("name", "")
                r["subcat"] = d.get("subcat", "")
                r["_toks"] = conteudo(" ".join((r["excerpt"], r["paraphrase"],
                                                r["keywords"].replace("|", " "),
                                                r["dim_nome"])))
                out.append(r)
    return out


def ancorar(afirm: list[dict], ev: list[dict], top: int,
            regras: list[R.Regra] | None = None) -> list[dict]:
    por_setor = defaultdict(list)
    for e in ev:
        por_setor[e["setor"]].append(e)

    linhas = []
    for a in afirm:
        if a.get("chamada"):
            continue
        alvo = conteudo(a["texto"])
        pool = [e for s in SETOR_DA_SECAO.get(a["setor"], set()) for e in por_setor[s]]
        pontuados = []
        for e in pool:
            comum = alvo & e["_toks"]
            if not comum:
                continue
            # sobreposição normalizada pelo tamanho da afirmação: evidência longa
            # não pode ganhar só por ser longa
            pontuados.append((len(comum) / max(len(alvo), 1), sorted(comum), e))
        pontuados.sort(key=lambda x: -x[0])
        # uma sessão pode ter várias evidências no mesmo carimbo, em dimensões
        # diferentes; como âncora elas são a mesma passagem
        vistos, unicos = set(), []
        for score, comum, e in pontuados:
            chave = (e["interview"], e["ts"])
            if chave in vistos:
                continue
            vistos.add(chave)
            unicos.append((score, comum, e))
        for score, comum, e in unicos[:top] or [(0.0, [], None)]:
            linhas.append({
                "n": a["n"], "setor": a["setor"], "subsecao": a["subsecao"],
                "afirmacao": R.aplicar(a["texto"], regras)[0] if regras else a["texto"],
                "score": round(score, 3),
                "interview": e["interview"] if e else "",
                "ts": e["ts"] if e else "",
                "dim": e["dim"] if e else "",
                "dim_nome": e["dim_nome"] if e else "",
                "maturity": e["maturity"] if e else "",
                "confidence": e["confidence"] if e else "",
                "termos": "|".join(comum[:8]),
                "paraphrase": e["paraphrase"] if e else "",
            })
    return linhas


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--docx", required=True, help="Produto 04 .docx")
    ap.add_argument("--csv", help="grava as âncoras candidatas")
    ap.add_argument("--top", type=int, default=3)
    ap.add_argument("--min-score", type=float, default=0.0)
    args = ap.parse_args()

    afirm = afirmacoes(Path(args.docx))
    ev = evidencias()
    regras = regras_da_narrativa()
    linhas = [l for l in ancorar(afirm, ev, args.top, regras)
              if l["score"] >= args.min_score]

    por_afirm = defaultdict(list)
    for l in linhas:
        por_afirm[l["n"]].append(l)
    sem = [a for a in afirm if not any(x["interview"] for x in por_afirm[a["n"]])]

    reais = [a for a in afirm if not a.get("chamada")]
    sem = [a for a in reais if not any(x["interview"] for x in por_afirm[a["n"]])]
    print(f"{len(afirm)} parágrafos na Seção 3 · {len(reais)} afirmações ancoráveis "
          f"({len(afirm) - len(reais)} chamadas de lista) · {len(ev)} evidências")
    print(f"{len(reais) - len(sem)} com candidato · {len(sem)} sem nenhum candidato\n")
    for a in reais:
        c = [x for x in por_afirm[a["n"]] if x["interview"]]
        marca = "  " if c else "!!"
        print(f"{marca} [{a['n']:>2}] {a['texto'][:74]}")
        for x in c:
            print(f"        {x['score']:.2f}  {x['interview']:<16} {x['ts']}  "
                  f"dim {x['dim']:<6} {x['dim_nome'][:40]}")
    if args.csv:
        with open(args.csv, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(linhas[0]))
            w.writeheader()
            w.writerows(linhas)
        print(f"\ngravado: {args.csv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
