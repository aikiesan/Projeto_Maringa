# -*- coding: utf-8 -*-
"""Supressao de trecho autoidentificador, aplicada no pipeline.

`tools/redacao.py` SUBSTITUI nome por rotulo e DETECTA cargo como residuo, mas
nao tem o conceito de **suprimir trecho**. Alguns trechos nao se resolvem por
substituicao: um vinculo familiar declarado, um voto, a presidencia nominal de
uma comissao, ou o nome de um agente publico dito ao lado de uma sessao que e
rotulada pelo cargo dele. Nesses, o que identifica nao e o nome — e a frase.

Este modulo aplica `codebook/supressoes.csv` a duas superficies:
  - as transcricoes anonimizadas (`anonimizar_transcricoes.py`);
  - o texto do Produto 4 na versao publica (`tools/hub/produto4.py`).

## Por que a ancora nao guarda o texto suprimido

Se o codebook versionado guardasse o trecho, o codebook passaria a ser o lugar
onde o material protegido vive — exatamente o que `anexos/cortes.csv` e, e por
isso ele esta fora do git (regra 5.7.3). Aqui a ancora e o CONTEXTO: um prefixo e
um sufixo curtos, que nao identificam ninguem, mais o `sha256` e o comprimento do
que sai. O aplicador casa pelo contexto e CONFERE o hash.

## Falha dura

Ancora que nao casa e protecao perdida em silencio. Toda falha levanta
`SupressaoNaoAplicada` e interrompe a geracao. O cenario que este modulo existe
para impedir e justamente o de regerar o material e publicar sem os cortes.
"""
from __future__ import annotations

import csv
import hashlib
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ARQUIVO = ROOT / "codebook" / "supressoes.csv"
MARCA = "(…)"

CAMPOS = ("fonte", "alvo", "paragrafo", "prefixo", "sufixo",
          "sha256", "n_chars", "motivo")


class SupressaoNaoAplicada(RuntimeError):
    """Uma supressao declarada nao pode ser aplicada. Nunca ignore."""


@dataclass(frozen=True)
class Supressao:
    fonte: str          # `transcricao` ou `produto4`
    alvo: str           # ENT-XXX, ou Produto_4
    paragrafo: int
    prefixo: str
    sufixo: str
    sha256: str
    n_chars: int
    motivo: str

    def chave(self):
        return (self.fonte, self.alvo, self.paragrafo)


def sha(texto: str) -> str:
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()


def carregar(caminho: Path = ARQUIVO) -> list[Supressao]:
    if not caminho.exists():
        return []
    out = []
    with caminho.open(encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f):
            out.append(Supressao(
                fonte=r["fonte"].strip(), alvo=r["alvo"].strip(),
                paragrafo=int(r["paragrafo"]), prefixo=r["prefixo"],
                sufixo=r["sufixo"], sha256=r["sha256"].strip(),
                n_chars=int(r["n_chars"]), motivo=r["motivo"]))
    return out


def gravar(sups: list[Supressao], caminho: Path = ARQUIVO) -> None:
    with caminho.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CAMPOS)
        w.writeheader()
        for s in sups:
            w.writerow({c: getattr(s, c) for c in CAMPOS})


# O contexto e casado progressivamente: primeiro inteiro, depois encurtado. A
# razao e concreta — o mesmo paragrafo aparece como texto puro e como HTML com
# <strong>, e um prefixo longo atravessa a etiqueta. Encurtar NAO afrouxa a
# verificacao: quem garante que o trecho certo saiu e o sha256, nao o contexto.
_RECUOS = (None, 14, 8, 4)


def _casar(texto: str, s: Supressao):
    for r in _RECUOS:
        pre = s.prefixo if r is None else s.prefixo[-r:]
        suf = s.sufixo if r is None else s.sufixo[:r]
        if not pre or not suf:
            continue
        de = 0
        while True:
            i = texto.find(pre, de)
            if i < 0:
                break
            ini = i + len(pre)
            j = texto.find(suf, ini)
            if j < 0:
                break
            if sha(texto[ini:j]) == s.sha256:
                return ini, j
            de = i + 1
    return None


def aplicar_em(texto: str, s: Supressao) -> str:
    """Remove o trecho entre `prefixo` e `sufixo`, conferindo o hash."""
    achado = _casar(texto, s)
    if achado is None:
        raise SupressaoNaoAplicada(
            f"{s.alvo} §{s.paragrafo}: o trecho declarado não foi encontrado "
            f"({s.n_chars} caracteres, sha {s.sha256[:12]}…). O material mudou — "
            f"reveja a supressão antes de publicar. Proteção NÃO aplicada.")
    ini, j = achado
    return texto[:ini] + MARCA + texto[j:]


def aplicar(paragrafos: dict[int, str], fonte: str, alvo: str,
            sups: list[Supressao] | None = None) -> tuple[dict[int, str], int]:
    """Aplica todas as supressoes de (fonte, alvo). Devolve (paragrafos, n)."""
    sups = carregar() if sups is None else sups
    minhas = [s for s in sups if s.fonte == fonte and s.alvo == alvo]
    out, n = dict(paragrafos), 0
    for s in minhas:
        if s.paragrafo not in out:
            raise SupressaoNaoAplicada(
                f"{alvo} §{s.paragrafo}: parágrafo não existe no material "
                f"({len(out)} parágrafos). O documento mudou.")
        out[s.paragrafo] = aplicar_em(out[s.paragrafo], s)
        n += 1
    return out, n


def nova(fonte: str, alvo: str, paragrafo: int, texto: str,
         trecho: str, motivo: str, ctx: int = 26) -> Supressao:
    """Cria a declaracao a partir do texto e do trecho a remover.

    O prefixo e o sufixo sao recortes curtos do entorno — contexto, nao o
    material protegido. O trecho em si nunca e gravado: fica o `sha256`.
    """
    i = texto.find(trecho)
    if i < 0:
        raise SupressaoNaoAplicada(
            f"{alvo} §{paragrafo}: o trecho a suprimir não está no parágrafo")
    return Supressao(fonte=fonte, alvo=alvo, paragrafo=paragrafo,
                     prefixo=texto[max(0, i - ctx):i],
                     sufixo=texto[i + len(trecho):i + len(trecho) + ctx],
                     sha256=sha(trecho), n_chars=len(trecho), motivo=motivo)


def aplicar_em_turnos(corpo: list[dict], code: str,
                      sups: list[Supressao] | None = None) -> tuple[list[dict], int]:
    """Aplica as supressoes de uma sessao aos turnos de `varrer_turnos`.

    `corpo` e a lista de dicts `{idx, ts, rotulo, texto}`. A juncao e pelo `idx`,
    que e o mesmo numero de paragrafo que a relacao de cortes usa.

    Falha dura se uma supressao declarada nao casar: ancora que nao casa e
    protecao perdida em silencio, e o cenario que este modulo existe para
    impedir e justamente o de regerar as transcricoes e publicar sem os cortes.
    """
    sups = carregar() if sups is None else sups
    minhas = [s for s in sups if s.fonte == "transcricao" and s.alvo == code]
    if not minhas:
        return corpo, 0
    por_idx = {t["idx"]: t for t in corpo}
    for s in minhas:
        t = por_idx.get(s.paragrafo)
        if t is None:
            raise SupressaoNaoAplicada(
                f"{code} §{s.paragrafo}: turno não existe nesta transcrição "
                f"({len(corpo)} turnos). O material mudou — a proteção declarada "
                f"NÃO foi aplicada.")
        t["texto"] = aplicar_em(t["texto"], s)
    return corpo, len(minhas)
