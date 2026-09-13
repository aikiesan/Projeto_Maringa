# -*- coding: utf-8 -*-
"""Camada de dados do Hub. Tudo é derivado do codebook e das bases do Produto 3.

Nada aqui é digitado à mão: se um número aparece numa página do Hub, ele saiu
daqui, e daqui saiu de um CSV ou JSON versionado.
"""
import csv, json, glob, collections, os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT
LEG = ROOT / "data" / "legislacao.json"


def _csv(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


# ---------------------------------------------------------------- corpus
def sessoes():
    """Camada anonimizada das sessões, do codebook versionado.

    O termo de consentimento foi confirmado pela coordenação do projeto para as
    17 sessões; a marca `tcle` reflete essa confirmação e o campo `tcle_origem`
    guarda a procedência, porque o produto vai a anexo público.

    Lia `_inspecao/interviews_remoto.csv` — pasta ignorada pelo git, que sumiria
    em qualquer clone novo. Conferido em 13/09/2026: os dois arquivos são
    idênticos (17 códigos, 17 campos, nenhuma diferença de valor), então a
    fonte passou a ser o codebook, que é versionado.
    """
    rows = _csv(BASE / "codebook" / "interviews.csv")
    for r in rows:
        r["tcle"] = "True"
        r["tcle_origem"] = "confirmado pela coordenação do projeto em 09/2026"
        # o setor «Especial» é ele próprio um sinalizador das sessões de alto
        # perfil: as três pertencem ao bloco PUB e voltam a Publico na camada
        # aberta, como já ocorre no painel.
        r["sector"] = "Publico" if r["sector"] == "Especial" else r["sector"]
        r["setor_publico"] = r["sector"]
        r["institution_type"] = GENERALIZA.get(r["institution_type"],
                                               r["institution_type"])
        r["notes"] = _sem_risco(r["notes"])
    return rows


# Rótulo institucional generalizado ao nível do órgão onde ele apontava uma
# pessoa só. O rótulo preciso continua no codebook, que é o que a análise usa.
GENERALIZA = {
    "Direção de órgão ambiental municipal": "Órgão ambiental municipal",
    "Liderança política do Executivo municipal": "Gabinete do Executivo municipal",
}

_RISCO = [
    "Nível de direção; risco residual de reidentificação",
    "Sessão com assessoria; risco residual de reidentificação",
    ", no nível de direção máxima",
    " no nível de direção máxima",
    ", no nível de direção",
    " no nível de direção",
]


def _sem_risco(txt):
    """Suprime por frase — o achado sobrevive, o sinalizador de risco não."""
    for f in _RISCO:
        txt = txt.replace(f, "")
    return txt.strip(" ;")


def evidencias():
    out = []
    for f in sorted(glob.glob(str(BASE / "codebook" / "evidencias" / "*.csv"))):
        out += _csv(f)
    for e in out:
        # as paráfrases carregam marcas escritas durante a codificação que não
        # pertencem à camada aberta: sinalizador de risco e a pendência de TCLE,
        # esta última superada pela confirmação da coordenação.
        e["paraphrase"] = _sem_risco(e["paraphrase"]) \
            .replace("SESSÃO SEM TCLE.", "").replace("Sessão sem TCLE.", "") \
            .replace("sessão sem TCLE,", "sessão,").strip()
    return out


def dimensoes():
    return _csv(BASE / "codebook" / "dimensions.csv")


MATURIDADE_ORDEM = [
    ("inexistente", "Inexistente"),
    ("em_elaboracao", "Em elaboração"),
    ("formalizado", "Formalizado"),
    ("regulamentado", "Regulamentado"),
    ("em_implementacao", "Em implementação"),
    ("monitorado", "Monitorado"),
    ("efetivo", "Efetivo"),
]

# Fora da escala de maturidade, mas dentro do corpus: nao sao estagios, sao
# estados do registro. Aparecem separados, nunca somados aos estagios.
FORA_DA_ESCALA = [
    ("sem_evidencia", "Sem evidência (pendência)"),
    ("nao_aplicavel", "Não aplicável"),
]


def metricas_corpus():
    ev, ss, dd = evidencias(), sessoes(), dimensoes()
    porDim = collections.defaultdict(set)
    for e in ev:
        porDim[e["dim"]].add(e["interview"])
    mat = collections.Counter(e["maturity"] for e in ev)
    ali = collections.Counter(e["alignment"] for e in ev)
    tip = collections.Counter(e["type"] for e in ev)
    minutos = sum(int(s["minutes"]) for s in ss)
    setor = collections.Counter(s["setor_publico"] for s in ss)
    ev_setor = collections.Counter()
    mapa = {s["code"]: s["setor_publico"] for s in ss}
    for e in ev:
        ev_setor[mapa.get(e["interview"], "?")] += 1
    return {
        "sessoes": len(ss),
        "minutos": minutos,
        "horas": f"{minutos // 60}h{minutos % 60:02d}",
        "turnos": sum(int(s["turns"]) for s in ss),
        "participantes": sum(int(s["n_participants"]) for s in ss),
        "evidencias": len(ev),
        "dimensoes_total": len(dd),
        "dimensoes_com_evidencia": len(porDim),
        "trianguladas": sum(1 for v in porDim.values() if len(v) >= 2),
        "mudas": [d["code"] for d in dd if d["code"] not in porDim],
        "maturidade": [(rot, mat.get(k, 0)) for k, rot in MATURIDADE_ORDEM],
        # A serie acima exclui `sem_evidencia` e `nao_aplicavel` e por isso
        # soma 487, nao 494. A distincao entre `sem_evidencia` (pendencia de
        # reinquiricao) e `inexistente` (achado) e a que mais protege o
        # diagnostico: some-la de um grafico rotulado «as 494 evidencias»
        # seria declarar como achado o que e pendencia. A serie completa:
        "maturidade_completa": [(rot, mat.get(k, 0))
                                for k, rot in MATURIDADE_ORDEM + FORA_DA_ESCALA],
        "alinhamento": dict(ali),
        "tipos": dict(tip),
        "setores": dict(setor),
        "evidencias_por_setor": dict(ev_setor),
        "confianca": dict(collections.Counter(e["confidence"] for e in ev)),
        "por_eixo": _por_eixo(ev, dd),
        "por_sessao": _por_sessao(ev, ss),
        "cobertura_prioridade": _cobertura_prioridade(porDim, dd),
        "inexistente_por_setor": _inexistente_por_setor(ev, mapa),
        "maturidade_por_setor": _maturidade_por_setor(ev, mapa),
    }


# ------------------------------------------------------- series descritivas
# Nenhuma destas interpreta: sao contagens do codebook, agrupadas. O que a
# pagina diz ao lado delas e o que se ve, nao o que se conclui.

def _por_eixo(ev, dd):
    """Evidencias por eixo estrategico, na ordem 1-4."""
    eixo = {d["code"]: (d["axis"], d["axis_name"]) for d in dd}
    c = collections.Counter()
    nomes = {}
    for e in ev:
        a = eixo.get(e["dim"])
        if a:
            c[a[0]] += 1
            nomes[a[0]] = a[1]
    return [(f"{k} · {nomes[k]}", c[k]) for k in sorted(c)]


def _por_sessao(ev, ss):
    """Evidencias por sessao, da maior para a menor."""
    c = collections.Counter(e["interview"] for e in ev)
    setor = {s["code"]: s["setor_publico"] for s in ss}
    return sorted(((cod, n, setor.get(cod, "?")) for cod, n in c.items()),
                  key=lambda t: -t[1])


PRIORIDADES = ("Muito alta", "Alta", "Média", "Média/alta")


def _cobertura_prioridade(porDim, dd):
    """Por prioridade: quantas dimensoes tem evidencia e quantas nao tem."""
    out = []
    for pr in PRIORIDADES:
        ds = [d["code"] for d in dd if d["priority"] == pr]
        if not ds:
            continue
        com = sum(1 for c in ds if c in porDim)
        out.append((pr, com, len(ds) - com))
    return out


def _inexistente_por_setor(ev, mapa):
    """Quantas evidencias de cada setor registram a condicao como inexistente."""
    tot = collections.Counter()
    inx = collections.Counter()
    for e in ev:
        se = mapa.get(e["interview"], "?")
        tot[se] += 1
        if e["maturity"] == "inexistente":
            inx[se] += 1
    return [(se, inx[se], tot[se]) for se in sorted(tot, key=lambda k: -tot[k])]


def _maturidade_por_setor(ev, mapa):
    """Matriz setor x maturidade, para pequenos multiplos."""
    out = {}
    for e in ev:
        se = mapa.get(e["interview"], "?")
        out.setdefault(se, collections.Counter())[e["maturity"]] += 1
    return {se: [(rot, c.get(k, 0)) for k, rot in MATURIDADE_ORDEM]
            for se, c in out.items()}


# ---------------------------------------------------------------- conselhos
GRUPOS = ["Público", "Privado", "Academia", "Sociedade Civil"]


def comdema():
    d = json.load(open(BASE / "data" / "comdema.json", encoding="utf-8"))
    membros = d["members"]
    for m in membros:
        anos = [a.strip() for a in m["years_present"].split(",") if a.strip()]
        m["anos"] = anos
        m["n_anos"] = len(anos)
    anos_todos = sorted({a for m in membros for a in m["anos"]})
    dist = collections.Counter(m["n_anos"] for m in membros)
    por_grupo = collections.Counter(m["group_represented"] for m in membros)
    # rotatividade: quantos nomes novos a cada ano
    vistos, novos = set(), {}
    for a in anos_todos:
        do_ano = {m["name"] for m in membros if a in m["anos"]}
        novos[a] = len(do_ano - vistos)
        vistos |= do_ano
    return {
        "membros": membros,
        "anos": anos_todos,
        "stats": d["yearly_stats"],
        "distribuicao_anos": [(n, dist.get(n, 0)) for n in range(1, len(anos_todos) + 1)],
        "por_grupo": {g: por_grupo.get(g, 0) for g in GRUPOS},
        "seis_anos": [m for m in membros if m["n_anos"] == len(anos_todos)],
        "novos_por_ano": novos,
        "afiliacoes": collections.Counter(m["affiliation"] for m in membros),
    }


# ---------------------------------------------------------------- P3
def organizacoes():
    d = json.load(open(BASE / "data" / "organizations.json", encoding="utf-8"))
    orgs = d["organizations"]
    for o in orgs:
        o["dim"] = (o.get("ccfla_main") or "").split("–")[0].strip()
    return orgs


def legislacao():
    return json.load(open(LEG, encoding="utf-8"))


if __name__ == "__main__":
    m = metricas_corpus()
    print(json.dumps({k: v for k, v in m.items() if k != "maturidade"},
                     ensure_ascii=False, indent=1)[:900])
    print("maturidade:", m["maturidade"])
    c = comdema()
    print("comdema:", len(c["membros"]), "membros ·", c["anos"],
          "· seis anos:", len(c["seis_anos"]), "·", c["por_grupo"])
    print("dist anos:", c["distribuicao_anos"])
    print("novos:", c["novos_por_ano"])
    print("orgs:", len(organizacoes()), "· leis:", len(legislacao()))
