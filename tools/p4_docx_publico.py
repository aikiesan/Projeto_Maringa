# -*- coding: utf-8 -*-
"""Gera a versão pública e editável do Produto 04, em `.docx`.

    python -m tools.p4_docx_publico

Por que existe uma segunda versão do arquivo. O `.docx` entregue à coordenação
traz quatro quadros nominais: as pessoas mobilizadas no evento de lançamento, as
entrevistadas (com nome, instituição **e cargo**), as convidadas que não
participaram e as que se ofereceram para o questionário. A lista nominal é
entregável previsto no termo de referência, e continua sendo entregue.

O que não pode circular junto com ela é a ligação entre pessoa e sessão. O Hub
publica as 17 transcrições identificadas por código; a lista nominal ao lado,
num arquivo baixável, reconstrói o vínculo em minutos. É o mesmo motivo pelo
qual o tipo institucional saiu das páginas: 13 dos 15 rótulos eram únicos de uma
única sessão.

Esta versão, então:

- aplica as supressões declaradas em `codebook/supressoes.csv`, como a página;
- substitui cada quadro nominal pela contagem que ele sustentava, derivada do
  codebook, com nota dizendo que a lista existe e por que não está ali;
- preserva o resto do documento intacto, inclusive a formatação, porque é para
  ser editado.

O arquivo completo, com os quadros, segue por outro canal para IPPLAM e CEPAL.
"""
from __future__ import annotations

import collections
import csv
import glob
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

ORIGEM = ROOT / "anexos" / "Produto_4.docx"
DESTINO = ROOT / "hub_saida" / "Produto_04_publico.docx"

CABECALHOS_NOMINAIS = ("nome", "entrevistado", "entrevistado(a)", "participante")


def _setores_do_codebook() -> collections.Counter:
    c: collections.Counter = collections.Counter()
    with (ROOT / "codebook" / "interviews.csv").open(
            encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f):
            s = (r.get("sector") or "").strip()
            # «Especial» e o sinalizador das tres sessoes de alto perfil; elas
            # pertencem ao bloco publico e voltam a ele na camada aberta. Sem
            # normalizar, «Publico» e «Público» virariam duas chaves.
            c[{"Especial": "Público", "Publico": "Público"}.get(s, s)] += 1
    return c


def _e_nominal(tab) -> bool:
    if not tab.rows:
        return False
    prim = [c.text.strip().lower() for c in tab.rows[0].cells]
    return any(h in CABECALHOS_NOMINAIS for h in prim)


def _texto_agregado(tab, setores) -> str:
    n = max(0, len(tab.rows) - 1)
    cols = [c.text.strip() for c in tab.rows[0].cells if c.text.strip()]
    outras = ", ".join(c.lower() for c in cols
                       if c.lower() not in CABECALHOS_NOMINAIS and c != "#")
    comp = ""
    # A composicao por setor descreve as SESSOES DE ENTREVISTA, e so vale para o
    # quadro dos entrevistados. Colada no quadro dos voluntarios do evento de
    # lancamento, afirmaria sobre 14 pessoas um numero apurado sobre outras 17.
    # O quadro se identifica pelo proprio cabecalho, nao pelo tamanho.
    if any(h.lower().startswith("entrevistado") for h in cols):
        comp = " Composição por setor: " + "; ".join(
            f"{k} {v}" for k, v in sorted(setores.items(), key=lambda kv: -kv[1])) + "."
    return (f"[Quadro nominal suprimido nesta versão pública: {n} pessoas, "
            f"com {outras}.{comp} As entrevistas foram concedidas sob termo de "
            f"consentimento que garante confidencialidade; publicar a lista "
            f"nominal ao lado do corpus identificaria os participantes de cada "
            f"sessão. A lista consta da versão entregue à coordenação.]")


def _limpa_paragrafo(par, texto: str) -> None:
    """Deixa o parágrafo com `texto`, preservando o formato do primeiro run."""
    if not par.runs:
        par.add_run(texto)
        return
    par.runs[0].text = texto
    for r in par.runs[1:]:
        r.text = ""


def _aplicar_supressao(par, sup) -> bool:
    """Aplica uma supressão mexendo só nos runs que o trecho atravessa.

    Reescrever o parágrafo inteiro seria mais simples e perderia o negrito do
    rótulo que abre cada afirmação da Seção 3. O mapa de deslocamentos existe
    para preservá-lo.
    """
    from tools.supressoes import _casar, MARCA
    achado = _casar(par.text, sup)
    if achado is None:
        return False
    ini, fim = achado
    pos, primeiro = 0, True
    for r in par.runs:
        a, b = pos, pos + len(r.text)
        pos = b
        if b <= ini or a >= fim:
            continue
        antes = r.text[:max(0, ini - a)]
        depois = r.text[max(0, fim - a):] if fim - a < len(r.text) else ""
        r.text = antes + (MARCA if primeiro else "") + depois
        primeiro = False
    return True


def gerar(origem: Path = ORIGEM, destino: Path = DESTINO) -> dict:
    import docx
    sys.path.insert(0, str(ROOT / "tools" / "hub"))
    import produto4 as P4
    from tools.supressoes import carregar

    doc = docx.Document(str(origem))
    P4.guarda(doc, origem)            # a mesma trava: 367 paragrafos, ultimo titulo

    # supressoes declaradas
    sups = [s for s in carregar() if s.fonte == "produto4"]
    pars = doc.paragraphs
    aplicadas, falhas = 0, []
    for s in sups:
        if s.paragrafo >= len(pars):
            falhas.append(f"§{s.paragrafo} fora do intervalo")
            continue
        if _aplicar_supressao(pars[s.paragrafo], s):
            aplicadas += 1
        else:
            falhas.append(f"§{s.paragrafo} nao casou")
    if falhas:
        raise SystemExit("supressoes nao aplicadas no .docx publico: "
                         + "; ".join(falhas)
                         + ". Publicar sem um corte declarado e pior do que nao "
                           "publicar.")

    # quadros nominais -> contagem
    setores = _setores_do_codebook()
    quadros = 0
    for tab in doc.tables:
        if not _e_nominal(tab):
            continue
        texto = _texto_agregado(tab, setores)
        # esvazia todas as celulas e escreve o agregado na primeira
        for i, row in enumerate(tab.rows):
            for j, cel in enumerate(row.cells):
                for k, par in enumerate(cel.paragraphs):
                    _limpa_paragrafo(par, texto if (i == 0 and j == 0 and k == 0)
                                     else "")
        quadros += 1

    destino.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(destino))
    return {"supressoes": aplicadas, "quadros": quadros,
            "paragrafos": len(doc.paragraphs), "tabelas": len(doc.tables),
            "bytes": destino.stat().st_size}


def main() -> int:
    r = gerar()
    print(f"{DESTINO.relative_to(ROOT)}")
    for k, v in r.items():
        print(f"  {k:14} {v}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
