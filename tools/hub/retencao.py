# -*- coding: utf-8 -*-
"""Quais sessoes entram na camada publica, e a medida que sustenta a decisao.

Em 14/09 mediu-se que 11 das 17 sessoes contem passagens em que o proprio
participante diz onde trabalha, junto de marca de primeira pessoa. Suprimir
todas destruiria o conteudo: publicar a transcricao integral e proteger o local
de trabalho de quem falou por uma hora sobre o proprio trabalho sao objetivos
incompativeis nessas sessoes. A decisao do projeto foi reter da camada publica
as que medem `limiar` passagens ou mais. As 17 continuam existindo como anexo
de entrega.

## Por que um CSV proprio, e nao uma coluna em interviews.csv

`interviews.csv` desagua na camada publica por `dados.sessoes()`, onde o
saneamento e campo a campo, a mao. Uma coluna nova vaza por padrao, e so nao
vaza se alguem lembrar de zera-la. Alem disso «nao publicada por
autoidentificacao de empregador» e da mesma familia dos rotulos de risco por
sessao que ja tiveram de ser arrancados, e que `varre_hub` hoje persegue.

## Por que 17 linhas e nao 6

Com 6 linhas e um default implicito «publica», uma sessao nova entraria
publicada sem ninguem ter decidido nada. `confere_cobertura` exige que o
conjunto de codigos seja exatamente o de `interviews.csv`.

## O que e digitado e o que e medido

Digitado e o ato de decisao: motivo, data, quem decidiu. Medido e
`n_passagens`, que `medir()` recalcula a partir do ACERVO e nao da saida
publicada, porque as sessoes retidas deixam de ter pagina para varrer.
"""
from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

ARQUIVO = ROOT / "codebook" / "retencao_publica.csv"
INTERVIEWS = ROOT / "codebook" / "interviews.csv"

CAMPOS = ("code", "publica", "termo", "criterio", "n_passagens", "limiar",
          "decidido_em", "decidido_por", "motivo")

# A janela em que a marca de primeira pessoa e a instituicao ainda se leem como
# uma coisa so. Foi medida, nao estimada: em 60 caracteres cabe a oracao, e
# acima disso o par passa a juntar frases que nao se referem uma a outra.
JANELA = 60

CRITERIO = ("mencoes do termo proprio a menos de 60 caracteres de marca de "
            "primeira pessoa, em fala de participante")

# Por que a medida e ancorada no TERMO declarado, e nao no gatilho de primeira
# pessoa. A primeira versao varria gatilhos («aqui no», «a gente do») e tomava
# como instituicao a primeira candidata na janela. O resultado era ruido: no
# ENT-009, sete das nove passagens eram «Olha», «Mas», «Yeah» e «Continua»,
# palavras capitalizadas por comeco de frase. E o numero que sustentava reter o
# ENT-008 contava dez ocorrencias de «meio ambiente» como substantivo comum.
#
# Ancorada no termo, a medida reproduz a medicao que fundamentou a decisao: o
# ENT-013 da 20 mencoes de «Defesa Civil» e 17 com primeira pessoa. O custo e
# que o termo proprio de cada sessao passa a ser declarado em vez de adivinhado,
# o que e ganho, porque adivinhar foi o defeito.
# «trabalho» e «trabalha» sairam desta lista na revisao de 14/09: o primeiro casa
# o substantivo («ha trabalho em conjunto») e o segundo casa a terceira pessoa
# («o orgao trabalha com»). Nenhum e marca de primeira pessoa, e ambos inflavam a
# medida. Quem diz «eu trabalho na Defesa Civil» ja e pego pelo «eu».
_PRIMEIRA = re.compile(
    r"\b(eu|n[óo]s|noss[oa]|a gente|meu|minha|aqui n[oa]|c[áa] n[oa]|sou|fui|"
    r"estou|estava|entrei)\b", re.IGNORECASE)
_FALANTE = re.compile(r"\[(participante[^\]]*|entrevistador[^\]]*)\]")


class RetencaoInvalida(RuntimeError):
    """A declaracao de retencao nao fecha com o codebook ou com a medida."""


def carregar(caminho: Path = ARQUIVO) -> dict[str, dict]:
    with open(caminho, encoding="utf-8-sig", newline="") as f:
        linhas = list(csv.DictReader(f))
    out = {}
    for r in linhas:
        r["publica"] = (r.get("publica") or "").strip().lower() == "true"
        r["n_passagens"] = int(r["n_passagens"])
        r["limiar"] = int(r["limiar"])
        out[r["code"].strip()] = r
    return out


def publicas(mapa: dict | None = None) -> set[str]:
    mapa = carregar() if mapa is None else mapa
    return {c for c, r in mapa.items() if r["publica"]}


def retidas(mapa: dict | None = None) -> set[str]:
    mapa = carregar() if mapa is None else mapa
    return {c for c, r in mapa.items() if not r["publica"]}


def confere_cobertura(codes, mapa: dict | None = None) -> None:
    """Toda sessao do codebook tem de ter uma decisao, e nenhuma a mais."""
    mapa = carregar() if mapa is None else mapa
    codes = set(codes)
    faltam, sobram = codes - set(mapa), set(mapa) - codes
    if faltam or sobram:
        raise RetencaoInvalida(
            f"retencao_publica.csv nao cobre o codebook. Sem decisao: "
            f"{sorted(faltam) or 'nenhuma'}. Decisao sem sessao: "
            f"{sorted(sobram) or 'nenhuma'}. Uma sessao sem decisao entraria "
            f"publicada por omissao.")


def confere_saida(dir_transcricoes: Path, mapa: dict | None = None) -> list[str]:
    """Achados: paginas de sessao retida que existem na saida.

    Um `continue` no gerador nao e trava. Esta funcao le a saida de verdade e
    devolve o que encontrou, para que o build e a varredura possam reprovar.
    """
    mapa = carregar() if mapa is None else mapa
    dir_transcricoes = Path(dir_transcricoes)
    if not dir_transcricoes.is_dir():
        return []
    presentes = {p.stem for p in dir_transcricoes.glob("*.html")}
    return sorted(presentes & retidas(mapa))


def _falas_de_participante(texto: str) -> list[str]:
    """Os trechos ditos por participante, descartados os do entrevistador.

    A pergunta do entrevistador tambem pode identificar o setor, e ja houve um
    corte declarado por isso. Mas a medida que sustenta a retencao e sobre o que
    o PARTICIPANTE diz de si: e disso que a decisao trata.
    """
    partes, quem, ini = [], None, 0
    for m in _FALANTE.finditer(texto):
        if quem and quem.startswith("participante"):
            partes.append(texto[ini:m.start()])
        quem, ini = m.group(1), m.end()
    if quem and quem.startswith("participante"):
        partes.append(texto[ini:])
    return partes


def medir(texto: str, termo: str) -> int:
    """Passagens em que o participante nomeia o proprio empregador.

    Uma passagem e uma ocorrencia de `termo` na fala do participante com marca
    de primeira pessoa a menos de `JANELA` caracteres, antes ou depois.

    Termo vazio mede zero, e e um valor legitimo: a sessao nao nomeia o proprio
    empregador em lugar nenhum. Uma retencao nesse caso se sustenta por outra
    razao, e a linha do CSV tem de dizer qual.
    """
    termo = (termo or "").strip()
    if not termo:
        return 0
    rx = re.compile(r"(?<![\wÀ-ÿ])" + re.escape(termo) + r"(?![\wÀ-ÿ])",
                    re.IGNORECASE)
    n = 0
    for parte in _falas_de_participante(texto):
        for m in rx.finditer(parte):
            janela = parte[max(0, m.start() - JANELA):m.end() + JANELA]
            if _PRIMEIRA.search(janela):
                n += 1
    return n


def medir_acervo(mapa: dict | None = None) -> dict[str, int]:
    """Roda `medir` sobre o acervo. Nao le `hub_saida/`: as retidas nao estao la."""
    import docx
    from tools.acervo import fonte_transcricoes, codigo
    mapa = carregar() if mapa is None else mapa
    out = {}
    with fonte_transcricoes() as origem:
        if origem is None:
            raise RetencaoInvalida(
                "acervo indisponivel: a medida nao pode ser conferida. Uma "
                "varredura que nao mediu nada nao esta limpa, esta cega.")
        for f in sorted(Path(origem).glob("*.docx")):
            texto = "\n".join(p.text for p in docx.Document(str(f)).paragraphs)
            code = codigo(f)
            out[code] = medir(texto, (mapa.get(code) or {}).get("termo", ""))
    return out


def confere_medida(medido: dict[str, int], mapa: dict | None = None) -> list[str]:
    """Achados: a declaracao divergiu do que se mede hoje.

    Tres casos. A medida declarada nao bate com a medida: a decisao foi tomada
    sobre outro material e precisa voltar a mesa. Sessao publicada que atinge o
    limiar: entrou no ar material que o criterio manda reter. Sessao retida
    abaixo do limiar: permitido, porque reter por outra razao e prerrogativa do
    projeto, mas exige motivo escrito.
    """
    mapa = carregar() if mapa is None else mapa
    achados = []
    for code, r in sorted(mapa.items()):
        n = medido.get(code)
        if n is None:
            achados.append(f"{code}: declarado mas ausente do acervo")
            continue
        if n != r["n_passagens"]:
            achados.append(
                f"{code}: declara {r['n_passagens']} passagens e o acervo mede "
                f"{n}. A decisao foi tomada sobre outro material.")
        if r["publica"] and n >= r["limiar"]:
            achados.append(
                f"{code}: publicada com {n} passagens, no limiar de "
                f"{r['limiar']} ou mais. O criterio manda reter.")
        if not r["publica"] and n < r["limiar"] and not (r.get("motivo") or "").strip():
            achados.append(f"{code}: retida abaixo do limiar e sem motivo escrito")
    return achados


def _codes_do_codebook() -> list[str]:
    with open(INTERVIEWS, encoding="utf-8-sig", newline="") as f:
        return [r["code"].strip() for r in csv.DictReader(f)
                if (r.get("duplicate") or "").strip() != "True"]


def main() -> int:
    mapa = carregar()
    confere_cobertura(_codes_do_codebook(), mapa)
    medido = medir_acervo(mapa)
    achados = confere_medida(medido, mapa)
    pub, ret = sorted(publicas(mapa)), sorted(retidas(mapa))
    print(f"{len(mapa)} sessoes · {len(pub)} publicadas · {len(ret)} retidas")
    for code in sorted(mapa):
        r = mapa[code]
        print(f"  {code:16} {'publica' if r['publica'] else 'RETIDA ':8} "
              f"{medido.get(code, '?'):>3} passagens")
    if achados:
        print("\nDIVERGENCIA ENTRE A DECISAO E O ACERVO:")
        for a in achados:
            print("  " + a)
        return 1
    print("\ndecisao confere com a medida do acervo")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
