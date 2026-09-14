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
          "sha256", "n_chars", "substituto", "motivo")


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
    # O que entra no lugar do trecho, LITERAL. Para cortar marcando, escreve-se
    # a propria marca `(…)` na coluna; vazio significa remover sem por nada.
    #
    # A coluna ser literal e deliberado. Antes, vazio significava «corta e
    # marca», e entao nao havia como expressar «remove o marcador e nao poe
    # nada» — que e o tratamento certo quando o que identifica e o marcador de
    # primeira pessoa e nao o conteudo. «nos aqui da Defesa Civil, a gente
    # tomou» com substituto «a Defesa Civil tomou» deixa a frase inteira e
    # retira a atribuicao da sessao ao orgao.
    substituto: str
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
                n_chars=int(r["n_chars"]),
                substituto=r.get("substituto") or "",
                motivo=r["motivo"]))
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
    """Acha o trecho declarado, pelo contexto, conferindo o sha256.

    Prefixo ou sufixo vazios sao legitimos e significam borda: um trecho no fim
    do paragrafo nao tem o que vir depois dele. Exigir os dois nao vazios fazia
    esses casos nunca casarem, e o sintoma era uma supressao declarada que a
    geracao recusava aplicar — pior do que nao ter declarado.
    """
    for r in _RECUOS:
        pre = s.prefixo if r is None else s.prefixo[-r:]
        suf = s.sufixo if r is None else s.sufixo[:r]
        if not s.prefixo and not s.sufixo:
            return None            # sem contexto algum nao ha como localizar
        de = 0
        while True:
            if pre:
                i = texto.find(pre, de)
                if i < 0:
                    break
                ini = i + len(pre)
            else:
                i, ini = 0, 0      # trecho no inicio do paragrafo
            if suf:
                j = texto.find(suf, ini)
                if j < 0:
                    break
            else:
                j = len(texto)     # trecho no fim do paragrafo
            if sha(texto[ini:j]) == s.sha256:
                return ini, j
            if not pre:
                break
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
    return texto[:ini] + s.substituto + texto[j:]


def aplicar_em_paragrafo(par, s: Supressao) -> bool:
    """Aplica a supressao DENTRO de um paragrafo, preservando os runs.

    `par` e um paragrafo do python-docx, mas este modulo nao importa `docx`: o
    que se exige do objeto e `.text` (a concatenacao dos runs), `.runs` (cada um
    com `.text` gravavel) e `.add_run`. O duck type e deliberado — a regra de
    supressao mora aqui, e nao no gerador de .docx.

    Reescrever `par.text` inteiro seria mais simples e destruiria a formatacao: a
    maioria dos paragrafos das transcricoes tem mais de um run, e na Secao 3 do
    Produto 4 o rotulo que abre a afirmacao e negrito. Por isso o intervalo e
    casado contra o texto concatenado e so os runs atravessados sao reescritos.

    Devolve True se aplicou, False se a ancora nao casou.
    """
    achado = _casar(par.text, s)
    if achado is None:
        return False
    ini, fim = achado
    if not par.runs:                       # paragrafo sem run, caso defensivo
        par.add_run(aplicar_em(par.text, s))
        return True
    pos, primeiro = 0, True
    for r in par.runs:
        a, b = pos, pos + len(r.text)
        pos = b
        if b <= ini or a >= fim:
            continue
        antes = r.text[:max(0, ini - a)]
        depois = r.text[max(0, fim - a):] if fim - a < len(r.text) else ""
        # O substituto entra uma vez so, no primeiro run atravessado. Ele e
        # LITERAL: antes daqui saia `MARCA` fixo, e as cinco supressoes cujo
        # substituto e outra coisa produziam arquivo divergente da pagina.
        r.text = antes + (s.substituto if primeiro else "") + depois
        primeiro = False
    return True


def _ja_aplicada(texto: str, s: Supressao) -> bool:
    """Diz se o tratamento declarado ja esta neste paragrafo.

    Com substituto nao vazio a prova e direta: o substituto esta la. Com
    substituto VAZIO nao ha o que procurar — a remocao nao deixa marca — e
    procurar `MARCA` daria negativo sempre, fazendo a geracao falhar sobre
    material que ja estava correto. A prova positiva nesse caso e que o prefixo
    e o sufixo ficaram ADJACENTES, isto e, que o que havia entre eles saiu.

    Se o trecho ainda estiver no paragrafo, prefixo e sufixo nao sao adjacentes
    e esta funcao devolve False, que e o comportamento que o modulo inteiro
    existe para garantir.
    """
    if s.substituto:
        return s.substituto in texto
    for r in _RECUOS:
        pre = s.prefixo if r is None else s.prefixo[-r:]
        suf = s.sufixo if r is None else s.sufixo[:r]
        if not pre and not suf:
            continue
        if not pre:
            if texto.startswith(suf):
                return True
        elif not suf:
            if texto.endswith(pre):
                return True
        elif pre + suf in texto:
            return True
    return False


def _decidir(texto: str, s: Supressao) -> str:
    """O unico lugar onde se decide o que fazer com uma supressao.

    Devolve `aplicar`, `ja` ou `falha`. Existe para que a pagina e o .docx de
    entrega nao tenham duas copias da regra: a equivalencia entre as duas saidas
    passa a ser estrutural, e nao disciplina de quem edita.
    """
    if _casar(texto, s) is not None:
        return "aplicar"
    if _ja_aplicada(texto, s):
        return "ja"
    return "falha"


def _falha(alvo: str, s: Supressao) -> SupressaoNaoAplicada:
    return SupressaoNaoAplicada(
        f"{alvo} §{s.paragrafo}: a ancora nao casa e o tratamento declarado "
        f"nao esta no paragrafo. {s.n_chars} caracteres, sha "
        f"{s.sha256[:12]}…. Protecao NAO aplicada.")


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
         trecho: str, motivo: str, substituto: str = "",
         ctx: int = 26) -> Supressao:
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
                     sha256=sha(trecho), n_chars=len(trecho),
                     substituto=substituto, motivo=motivo)


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


def aplicar_tolerante(paragrafos: list[str], fonte: str, alvo: str,
                      sups: list[Supressao] | None = None) -> tuple[list[str], int, int]:
    """Aplica as supressoes a uma lista de paragrafos, tolerando as ja aplicadas.

    Serve a camada publicada do Hub. As transcricoes que ela recebe vem do
    Anexo 05, que **ja passou** pelo pipeline: os sete cortes originais estao
    dentro dele, escritos como `(…)`. Exigir que essas ancoras casem de novo
    faria a geracao falhar sempre.

    A tolerancia e estreita de proposito: se a ancora nao casa, o paragrafo tem
    de conter o substituto declarado — a prova de que o tratamento ja esta la.
    Fora desses dois casos, levanta. Ancora que nao casa e nao esta aplicada e
    protecao perdida em silencio, que e o que este modulo existe para impedir.

    Devolve (paragrafos, aplicadas, ja_estavam).
    """
    sups = carregar() if sups is None else sups
    minhas = [x for x in sups if x.fonte == fonte and x.alvo == alvo]
    out = list(paragrafos)
    novas = ja = 0
    for x in minhas:
        if x.paragrafo >= len(out):
            raise SupressaoNaoAplicada(
                f"{alvo} §{x.paragrafo}: paragrafo nao existe ({len(out)} no "
                f"material). O material mudou e a protecao NAO foi aplicada.")
        alvo_txt = out[x.paragrafo]
        caso = _decidir(alvo_txt, x)
        if caso == "aplicar":
            out[x.paragrafo] = aplicar_em(alvo_txt, x)
            novas += 1
        elif caso == "ja":
            ja += 1
        else:
            raise _falha(alvo, x)
    return out, novas, ja


def aplicar_em_evidencias(evidencias, sups: list[Supressao] | None = None) -> int:
    """Aplica as supressoes de `fonte=evidencia` aos trechos do painel.

    A terceira superficie. As duas primeiras eram a transcricao e o Produto 4;
    o campo `excerpt` de `codebook/evidencias/` e publicado no painel e nao
    passava por aqui. O efeito era um corte valer numa superficie e nao na
    outra: em ENT-003 a transcricao perdia «aqui no orgao ambiental municipal»
    e o painel republicava a frase inteira.

    `evidencias` e a lista de dicts com `interview` e `excerpt`, na ordem em que
    o painel a le. O `paragrafo` da declaracao e o indice da evidencia DENTRO da
    sessao, nessa mesma ordem. Se a ordem mudar, `_casar` nao acha o trecho e a
    geracao falha, que e o comportamento certo: e o material que mudou.
    """
    sups = carregar() if sups is None else sups
    minhas = [s for s in sups if s.fonte == "evidencia"]
    if not minhas:
        return 0
    por_sessao: dict[str, list] = {}
    for e in evidencias:
        por_sessao.setdefault(e["interview"], []).append(e)
    n = 0
    for s in minhas:
        fila = por_sessao.get(s.alvo, [])
        if s.paragrafo >= len(fila):
            raise SupressaoNaoAplicada(
                f"{s.alvo} evidencia #{s.paragrafo}: nao existe ({len(fila)} na "
                f"sessao). O codebook mudou e a protecao NAO foi aplicada.")
        ev = fila[s.paragrafo]
        caso = _decidir(ev.get("excerpt") or "", s)
        if caso == "aplicar":
            ev["excerpt"] = aplicar_em(ev["excerpt"], s)
            n += 1
        elif caso != "ja":
            raise _falha(s.alvo + " evidencia", s)
    return n


def aplicar_em_doc(paragrafos, fonte: str, alvo: str,
                   sups: list[Supressao] | None = None) -> tuple[int, int]:
    """Aplica as supressoes aos paragrafos de um .docx, preservando os runs.

    `paragrafos` e `doc.paragraphs`, na ordem CRUA: sao esses os indices que
    `codebook/supressoes.csv` declara, porque a pagina tambem os le antes de
    descartar os vazios (`tools/hub/transcricoes.py`). Indexar sobre a lista ja
    filtrada deslocaria todas as declaracoes.

    Mesma decisao de `aplicar_tolerante`, pelo mesmo `_decidir`. Devolve
    (aplicadas, ja_estavam).
    """
    sups = carregar() if sups is None else sups
    minhas = [x for x in sups if x.fonte == fonte and x.alvo == alvo]
    novas = ja = 0
    for x in minhas:
        if x.paragrafo >= len(paragrafos):
            raise SupressaoNaoAplicada(
                f"{alvo} §{x.paragrafo}: paragrafo nao existe ({len(paragrafos)} "
                f"no material). O material mudou e a protecao NAO foi aplicada.")
        par = paragrafos[x.paragrafo]
        caso = _decidir(par.text, x)
        if caso == "aplicar":
            aplicar_em_paragrafo(par, x)
            novas += 1
        elif caso == "ja":
            ja += 1
        else:
            raise _falha(alvo, x)
    return novas, ja
