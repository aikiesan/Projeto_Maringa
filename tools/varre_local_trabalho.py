# -*- coding: utf-8 -*-
"""Audita as transcrições publicadas em busca do local de trabalho do próprio
participante.

    python -m tools.varre_local_trabalho            # relatório
    python -m tools.varre_local_trabalho --csv      # + CSV para revisão

## O problema, e por que ele sobrou

Em 13/09 o tipo institucional saiu do cabeçalho de cada sessão, porque 13 dos 15
rótulos eram únicos de uma única sessão e, ao lado da lista nominal de pessoas
entrevistadas — que é entregável do termo de referência — funcionavam como
crachá.

Isso era necessário e **não é suficiente.** O corpo da transcrição continua
dizendo onde a pessoa trabalha, em primeira pessoa. A frase mais direta que esta
varredura encontrou identifica instituição, cidade e setor de atuação numa só
linha. O `tools/redacao.py` substitui a instituição própria da sessão quando ela
está no léxico e nas «próprias da sessão»; o que escapa é o que não estava
mapeado ali, e siglas ditas de improviso escapam com frequência.

## O que esta ferramenta faz, e o que ela não faz

Ela **levanta candidatos**, como o `p4_ancorar` faz com âncoras. Não decide. A
diferença entre «eu trabalho no X» (autoidentificação) e «os avisos emitidos
pelo X» (terceiro citado) não é decidível por padrão de texto: depende de quem
fala e de qual é a instituição da sessão, e a segunda informação, por desenho,
não está na camada pública.

Por isso a saída é uma lista para leitura, com:

- o falante rotulado, que separa participante de entrevistador;
- a expressão que disparou, e a instituição candidata;
- o contexto, para julgar;
- a marca de tempo, para achar na transcrição.

Quem decidir marca no CSV, e a supressão entra em `codebook/supressoes.csv` pelo
caminho já existente, com falha dura se deixar de casar.
"""
from __future__ import annotations

import argparse
import collections
import csv
import glob
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TRANSC = ROOT / "hub_saida" / "transcricoes"
SAIDA_CSV = ROOT / "anexos" / "revisao_local_trabalho.csv"

# Expressões em que alguém fala da instituição como a sua. A primeira pessoa é o
# sinal; o resto é contexto para leitura.
GATILHOS = [
    (r"eu\s+trabalho\s+(?:aqui\s+)?(?:n[oa]|com|para\s+[oa])\s+", "eu trabalho no/na"),
    (r"(?:eu\s+)?(?:sou|fui)\s+(?:d[oa]|servidor[a]?\s+d[oa]|"
     r"funcion[áa]ri[oa]\s+d[oa]|membro\s+d[oa])\s+", "sou/fui do/da"),
    (r"(?:eu\s+)?(?:estava|estou|est[ou]\s+)\s*(?:l[áa]\s+)?(?:n[oa])\s+", "estou/estava no/na"),
    (r"n[óo]s\s+(?:aqui\s+)?d[oa]\s+", "nós do/da"),
    (r"a\s+gente\s+(?:aqui\s+)?d[oa]\s+", "a gente do/da"),
    (r"(?:aqui|c[áa])\s+n[oa]\s+", "aqui no/na"),
    (r"(?:o|a)\s+noss[oa]\s+", "nosso/nossa"),
    (r"(?:meu|minha)\s+(?:trabalho|setor|equipe|diretoria|secretaria)\s+", "meu setor"),
    (r"(?:voc[êe]s|o\s+projeto\s+que\s+voc[êe]s)\s+(?:t[êe]m|tem)\s+com\s+[oa]\s+",
     "vocês têm com o/a"),
]

# Candidata a instituição: sigla de 3 letras ou mais, ou nome próprio composto.
INST = r"([A-Z]{3,8}|[A-ZÀ-Ý][\wÀ-ÿ]{2,}(?:\s+(?:d[aeo]s?\s+)?[A-ZÀ-Ý][\wÀ-ÿ]{2,}){0,3})"

# Topônimos, marcas de consumo, palavras que abrem frase. Não são local de
# trabalho e enchem o relatório de ruído.
RUIDO = {
    "BRASIL", "MARINGA", "MARINGÁ", "PARANA", "PARANÁ", "CIDADE", "PREFEITURA",
    "ESTADO", "MUNICIPIO", "MUNICÍPIO", "REGIAO", "REGIÃO", "PAIS", "PAÍS",
    "Brasil", "Maringá", "Paraná", "Cidade", "Prefeitura", "Estado", "Região",
    "Então", "Porque", "Quando", "Agora", "Depois", "Assim", "Ainda", "Mesmo",
    "Muito", "Aqui", "Gente", "Nossa", "Nosso", "Isso", "Esse", "Essa", "Para",
    "Como", "Todo", "Toda", "Mais", "Menos", "Sobre", "Talvez", "Enfim",
    "Toyota", "Shopping", "Gemini", "Office", "Himalaia", "Morumbi", "Uber",
    "Google", "Excel", "Word", "WhatsApp", "YouTube", "Instagram",
    "Mata Atlântica", "Amazonia", "Amazônia", "Cerrado", "Pantanal",
}



# Candidatos lidos e dispensados: o padrao disparou, a leitura mostrou que nao
# e local de trabalho. Ficam declarados para que a ferramenta possa REPROVAR
# quando aparecer algo novo, em vez de so listar e depender de alguem comparar
# com a memoria.
DISPENSADOS = {
    ("ENT-005", "Elninho"):
        "fenomeno El Nino, nao instituicao; o padrao casou por «nossa regiao»",
    ("ENT-009", "Parque do Ingá"):
        "parque publico da cidade; «a gente fez jardim de chuva aqui no» fala "
        "da cidade, nao do empregador do participante",
}

def _falante(txt: str, pos: int) -> str:
    """O rótulo de falante mais próximo antes da posição."""
    m = None
    for m in re.finditer(r"\[(participante[^\]]*|entrevistador[^\]]*)\]", txt[:pos]):
        pass
    return m.group(1) if m else "?"


def _marca(txt: str, pos: int) -> str:
    """A marca de tempo mais próxima antes da posição."""
    m = None
    for m in re.finditer(r"\b(\d{2}:\d{2}:\d{2})\b", txt[:pos]):
        pass
    return m.group(1) if m else ""


def varrer() -> list[dict]:
    achados = []
    for arq in sorted(glob.glob(str(TRANSC / "*.html"))):
        cod = Path(arq).stem
        bruto = Path(arq).read_text(encoding="utf-8")
        txt = " ".join(re.sub(r"<[^>]+>", " ", bruto).split())
        for pad, rot in GATILHOS:
            for m in re.finditer(pad + INST, txt):
                inst = m.group(1).strip()
                if inst in RUIDO or inst.upper() in RUIDO or len(inst) < 3:
                    continue
                achados.append({
                    "sessao": cod,
                    "ts": _marca(txt, m.start()),
                    "falante": _falante(txt, m.start()),
                    "gatilho": rot,
                    "instituicao": inst,
                    "contexto": txt[max(0, m.start() - 120):m.end() + 120],
                    "decisao": "",
                    "nota": "",
                })
    return achados


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--csv", action="store_true",
                    help="grava anexos/revisao_local_trabalho.csv para revisao")
    ap.add_argument("--so-participante", action="store_true",
                    help="mostra so o que o participante disse, nao o entrevistador")
    a = ap.parse_args()

    ach = varrer()
    if a.so_participante:
        ach = [x for x in ach if x["falante"].startswith("participante")]

    novos = [x for x in ach
             if x["falante"].startswith("participante")
             and (x["sessao"], x["instituicao"]) not in DISPENSADOS]

    print(f"candidatos: {len(ach)} em {len({x['sessao'] for x in ach})} sessoes")
    quem = collections.Counter(
        "participante" if x["falante"].startswith("participante") else "entrevistador"
        for x in ach)
    print(f"  ditos pelo participante: {quem['participante']}"
          f" | pelo entrevistador: {quem['entrevistador']}")
    print()
    por = collections.defaultdict(list)
    for x in ach:
        por[x["sessao"]].append(x)
    for cod in sorted(por):
        print(f"[{cod}]")
        for x in por[cod]:
            quemc = "PART" if x["falante"].startswith("participante") else "entr"
            print(f"  {quemc} {x['ts'] or '--:--:--'}  «{x['instituicao']}»"
                  f"  ({x['gatilho']})")
        print()

    if a.csv:
        SAIDA_CSV.parent.mkdir(parents=True, exist_ok=True)
        with SAIDA_CSV.open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(ach[0]))
            w.writeheader()
            w.writerows(ach)
        print(f"gravado: {SAIDA_CSV.relative_to(ROOT)}")
        print("  ATENCAO: fica FORA do git. O contexto traz trecho de transcricao.")

    if novos:
        print()
        print(f"{len(novos)} CANDIDATO(S) SEM TRATAMENTO NEM DISPENSA:")
        for x in novos:
            print(f"  [{x['sessao']}] {x['ts']} «{x['instituicao']}»"
                  f" ({x['gatilho']})")
        print("  Ou declare a supressao em codebook/supressoes.csv, ou acrescente")
        print("  a DISPENSADOS com o motivo da leitura. Nao publique antes.")
        return 1

    print()
    print(f"nenhum candidato pendente; {len(DISPENSADOS)} dispensado(s) por leitura.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
