"""
Codebook analítico do projeto CEPAL/IPPLAM — Maringá.

Metodologia: *Assessing Subnational Enabling Framework Conditions for Urban
Climate Finance* (CCFLA / Urban-Act, 2024), priorizada para Maringá no Produto 2.

Fonte de verdade: os CSV em `codebook/`. Este módulo apenas os carrega, valida
e expõe as estruturas derivadas (índices, léxico, rank de prioridade).

RECONSTRUÍDO em 06/09/2026 a partir do `dashboard.json` embutido no artefato
"Repositório de Entrevistas de Maringá" (versão de 01/09/2026). Os dados
(dimensões, perguntas, crosswalk, léxico) são idênticos ao original; a forma
do módulo foi reescrita.
"""

from __future__ import annotations

import csv
import unicodedata
from functools import lru_cache
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parent.parent
CODEBOOK_DIR = ROOT / "codebook"

# ---------------------------------------------------------------- eixos

AXES: dict[int, dict[str, str]] = {
    1: {"name": "Política Climática", "short": "Política climática", "en": "Climate Policy (CP)"},
    2: {"name": "Orçamento e Finanças", "short": "Orçamento e finanças", "en": "Budget and Finance (BF)"},
    3: {"name": "Dados Climáticos", "short": "Dados climáticos", "en": "Climate Data (CD)"},
    4: {"name": "Coordenação Vertical e Horizontal", "short": "Coordenação",
        "en": "Vertical and Horizontal Coordination (VHC)"},
}

SUBCATEGORIES: dict[str, dict] = {
    "1.1": {"axis": 1, "name": "Políticas subnacionais de mudança do clima"},
    "1.2": {"axis": 1, "name": "Implementação da ação climática subnacional"},
    "2.1": {"axis": 2, "name": "Fontes subnacionais de recursos para ação climática urbana"},
    "2.2": {"axis": 2, "name": "Orçamento verde subnacional"},
    "2.3": {"axis": 2, "name": "Mobilização de receitas subnacionais"},
    "2.4": {"axis": 2, "name": "Mobilização de finanças privadas"},
    "2.5": {"axis": 2, "name": "Capacidade de crédito, endividamento e acesso a mercado de capitais"},
    "2.6": {"axis": 2, "name": "Cofinanciamento e finanças inovadoras"},
    "3.1": {"axis": 3, "name": "Reporte de dados climáticos no nível subnacional"},
    "3.2": {"axis": 3, "name": "Disponibilidade de dados climáticos e parcerias de análise"},
    "4.1": {"axis": 4, "name": "Coordenação entre níveis de governo"},
    "4.2": {"axis": 4, "name": "Participação pública e engajamento de atores"},
    "4.3": {"axis": 4, "name": "Cooperação subnacional e aprendizagem entre pares"},
}

BLOCKS = {
    "PUB": "Setor público",
    "PRI": "Setor privado",
    "ACA": "Academia",
    "SOC": "Sociedade civil",
}

# ------------------------------------------------------- escalas de registro

MATURITY = [
    ("sem_evidencia", "A entrevista não produziu informação sobre a condição"),
    ("nao_aplicavel", "A dimensão não se aplica àquele ator"),
    ("inexistente", "Há evidência positiva de que a condição não existe"),
    ("em_elaboracao", "Está sendo construída, sem resultado ainda"),
    ("formalizado", "Existe em norma, sem regulamentação"),
    ("regulamentado", "Regulamentado, ainda não plenamente operante"),
    ("em_implementacao", "Opera, com limitações declaradas"),
    ("monitorado", "Opera com acompanhamento sistemático"),
    ("efetivo", "Opera, é monitorada e produz resultado verificável"),
]
MATURITY_ORDER = {k: i for i, (k, _) in enumerate(MATURITY)}

EVIDENCE_TYPES = {
    "declaracao": "Fato afirmado sobre a instituição",
    "percepcao": "Avaliação do participante",
    "lacuna": "Ausência declarada ou constatada",
    "divergencia": "Conflito com outra fonte",
    "oportunidade": "Caminho apontado",
    "documento_indicado": "Pista para a Matriz 2 (evidência documental)",
}

ALIGNMENT = ("convergente", "complementar", "divergente", "isolada")
CONFIDENCE = ("alta", "media", "baixa")

PRIORITY_RANKS = {
    "muito alta": 4,
    "alta": 3,
    "media/alta": 3,
    "media": 2,
    "baixa": 1,
}


def _fold(s: str) -> str:
    """Minúsculas sem acento — para casar 'Média', 'media' e 'MÉDIA'."""
    s = unicodedata.normalize("NFKD", str(s or ""))
    return "".join(c for c in s if not unicodedata.combining(c)).strip().lower()


def priority_rank(priority: str) -> int:
    """Converte o rótulo de prioridade do Produto 2 em ordinal 1..4.

    Tolerante a acento, caixa e à variante 'Média/alta'. Desconhecido → 0.
    """
    return PRIORITY_RANKS.get(_fold(priority).replace(" ", ""), 0) or \
        PRIORITY_RANKS.get(_fold(priority), 0)


# ------------------------------------------------------------ carregamento

def _read(name: str) -> list[dict]:
    with (CODEBOOK_DIR / name).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


@lru_cache(maxsize=1)
def dimensions() -> list[dict]:
    out = []
    for r in _read("dimensions.csv"):
        r["axis"] = int(r["axis"])
        r["rank"] = int(r["rank"]) if r.get("rank") else priority_rank(r["priority"])
        r["keywords"] = [k for k in (r.get("keywords") or "").split("|") if k]
        out.append(r)
    return out


@lru_cache(maxsize=1)
def dimension_index() -> dict[str, dict]:
    return {d["code"]: d for d in dimensions()}


@lru_cache(maxsize=1)
def questions() -> list[dict]:
    return _read("questions.csv")


@lru_cache(maxsize=1)
def question_dimension() -> list[dict]:
    """Crosswalk pergunta × dimensão: relation ∈ {D, I}."""
    return _read("question_dimension.csv")


@lru_cache(maxsize=1)
def interviews() -> list[dict]:
    """Camada anonimizada autoritativa. Nunca contém PII."""
    out = []
    for r in _read("interviews.csv"):
        r["duplicate"] = str(r.get("duplicate", "")).lower() in ("true", "1", "sim")
        r["tcle"] = str(r.get("tcle", "")).lower() in ("true", "1", "sim")
        for k in ("n_participants", "minutes", "turns", "chars",
                  "participant_share", "n_dim_candidates", "n_hits"):
            if r.get(k):
                r[k] = int(float(r[k]))
        out.append(r)
    return out


def active_interviews() -> list[dict]:
    """Sessões distintas — exclui os códigos marcados como duplicata."""
    return [i for i in interviews() if not i["duplicate"]]


@lru_cache(maxsize=1)
def lexicon() -> dict[str, list[str]]:
    """Léxico de triagem: dimensão → palavras-chave (forma sem acento)."""
    return {d["code"]: [_fold(k) for k in d["keywords"]] for d in dimensions()}


def institution_types() -> list[str]:
    """Tipos genéricos de instituição presentes na camada anonimizada."""
    return sorted({i["institution_type"] for i in interviews() if i.get("institution_type")})


# Órgãos sem registro de entrevista que são fonte primária de dimensão
# prioritária (achado de cobertura do painel, 01/09/2026).
MISSING_INSTITUTIONS = {
    "Fazenda e Planejamento": ["2.2.1", "2.2.2", "2.2.3", "2.3.4"],
    "Planejamento urbano (IPPLAM)": ["3.1.1", "3.2.5", "2.1.4"],
    "Obras públicas": ["2.1.4"],
    "Urbanismo e habitação": ["3.2.4"],
    "Procuradoria": ["2.1.3"],
    "Limpeza urbana e mobilidade": ["2.1.6"],
    "Órgão ambiental estadual": ["1.1.2", "1.1.6"],
    "Conselho municipal de meio ambiente (COMDEMA)": ["4.2.3"],
    "Universidade pública": ["3.2.1"],
}


# ------------------------------------------------------------- validação

def validate() -> list[str]:
    """Checagens de integridade do codebook. Devolve a lista de problemas."""
    problems: list[str] = []
    dims = dimension_index()

    for d in dimensions():
        if d["subcat"] not in SUBCATEGORIES:
            problems.append(f"dimensão {d['code']}: subcategoria {d['subcat']} desconhecida")
        if d["rank"] == 0:
            problems.append(f"dimensão {d['code']}: prioridade '{d['priority']}' sem rank")
        if not d["keywords"]:
            problems.append(f"dimensão {d['code']}: sem palavras-chave")

    qids = {q["id"] for q in questions()}
    linked_q, linked_d = set(), set()
    for link in question_dimension():
        if link["question_id"] not in qids:
            problems.append(f"crosswalk: pergunta {link['question_id']} inexistente")
        if link["dimension_code"] not in dims:
            problems.append(f"crosswalk: dimensão {link['dimension_code']} inexistente")
        if link["relation"] not in ("D", "I"):
            problems.append(f"crosswalk {link['question_id']}: relação '{link['relation']}' inválida")
        linked_q.add(link["question_id"])
        linked_d.add(link["dimension_code"])

    for q in sorted(qids - linked_q):
        problems.append(f"pergunta {q}: sem nenhuma marcação D/I (lacuna conhecida do Produto 2)")
    for c in sorted(set(dims) - linked_d):
        problems.append(f"dimensão {c}: nenhuma pergunta aponta para ela "
                        f"(prioridade {dims[c]['priority']})")
    return problems


def summary() -> dict:
    ints = active_interviews()
    return {
        "eixos": len(AXES),
        "subcategorias": len(SUBCATEGORIES),
        "dimensoes": len(dimensions()),
        "perguntas": len(questions()),
        "vinculos_crosswalk": len(question_dimension()),
        "palavras_chave": sum(len(d["keywords"]) for d in dimensions()),
        "sessoes_distintas": len(ints),
        "codigos_ent": len(interviews()),
        "minutos": sum(i.get("minutes") or 0 for i in ints),
    }


if __name__ == "__main__":
    for k, v in summary().items():
        print(f"{k:>22}: {v}")
    print()
    probs = validate()
    print(f"{len(probs)} apontamento(s) de integridade:")
    for p in probs:
        print(" -", p)
