"""
Passo 8 do protocolo: gerar as transcrições anonimizadas para anexar ao Produto 04.

    python -m tools.anonimizar_transcricoes --acervo "A:\\Projeto_Maringa\\DRIVE_FILES"
    python -m tools.anonimizar_transcricoes --acervo ... --commit
    python -m tools.anonimizar_transcricoes --acervo ... --commit --incluir-sem-tcle

Lê as transcrições do acervo, rotula os falantes, redige o texto e grava um anexo
por sessão **fora do git**, junto com o relatório e a planilha de revisão humana.

Sem `--commit` o comando apenas confere e mostra; nada é escrito.

O que entra no repositório é só o método: `tools/redacao.py` (motor),
`codebook/anonimizacao_lexico.csv` (instituições) e
`codebook/anonimizacao_permitidos.csv` (allowlist). O dicionário de pessoas vive
em `vault/pessoas.csv`, que o `.gitignore` cobre, e a saída em
`saida_anonimizacao/`, idem.

A ferramenta é deliberadamente incapaz de declarar sucesso enquanto houver
resíduo de risco alto pendente (código de saída 3) ou nome vazado na saída
(código 2). Revisão humana do `revisar.csv` é parte do procedimento, não enfeite.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import re
import sys
import unicodedata
from collections import Counter
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from tools import redacao as R
from tools import supressoes as SUP                        # noqa: E402
from tools.transcript import turns                    # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
LEXICO = ROOT / "codebook" / "anonimizacao_lexico.csv"
PERMITIDOS = ROOT / "codebook" / "anonimizacao_permitidos.csv"
INTERVIEWS = ROOT / "codebook" / "interviews.csv"
EVID = ROOT / "codebook" / "evidencias"
PESSOAS = ROOT / "vault" / "pessoas.csv"
APELIDOS = ROOT / "vault" / "apelidos.csv"
TERCEIROS = ROOT / "vault" / "terceiros.csv"
SAIDA = ROOT / "saida_anonimizacao"

MIN_SESSOES_EQUIPE = 3
DESCARTE_RE = re.compile(r"^A transcrição")

SETOR_ROTULO = {"Publico": "Público", "Privado": "Privado", "Academia": "Academia",
                "Sociedade Civil": "Sociedade Civil", "Especial": "Público"}

CABECALHO = """> Transcrição automática revisada e anonimizada. Nomes de pessoas e a instituição do
> próprio participante foram substituídos por rótulos entre colchetes. As marcas de
> tempo `HH:MM:SS` são as do registro original e ancoram as evidências codificadas no
> Produto 04. Organizações terceiras de caráter público — órgãos estaduais e federais,
> contratos publicados, leis — permanecem nominais, conforme §3 da metodologia."""

NOTA_DIARIZACAO = """>
> **Sessão conjunta.** A transcrição automática atribuiu todos os turnos dos
> participantes a um único falante — os participantes não estão separados na
> diarização. A atribuição por falante registrada nas evidências codificadas foi feita
> por leitura e não é reproduzível na transcrição integral."""


def fold(s: str) -> str:
    return R.dobrar(s)


def ler_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def tokens(nome: str) -> set[str]:
    return {t for t in fold(nome).split() if len(t) > 2}


def casar(falante: str, pessoas: list[dict]) -> tuple[dict | None, bool]:
    """Casa um falante com uma pessoa da base. Devolve (pessoa, ambíguo).

    Mais rígido que o `casar` de `ingest_registros`: exige dois tokens em comum,
    ou um único token que identifique **uma só** pessoa. Empate é ambiguidade
    declarada, não escolha silenciosa por ordem de lista — aqui o erro monta o
    dicionário de nomes errado, que é falha de anonimização.
    """
    toks = tokens(falante)
    if not toks:
        return None, False
    fortes = [p for p in pessoas if len(toks & tokens(p["nome"])) >= 2]
    if len(fortes) == 1:
        return fortes[0], False
    if len(fortes) > 1:
        return fortes[0], True
    fracos = [p for p in pessoas if toks & tokens(p["nome"])]
    if len(fracos) == 1:
        return fracos[0], False
    return None, len(fracos) > 1


def identificar_equipe(transcricoes: list[Path], pessoas: list[dict]) -> set[str]:
    """Falantes recorrentes que não constam da base: a equipe da consultoria.

    Mesmo critério de `ingest_registros.identificar_equipe` — identificação por
    padrão, não por lista de nomes no código, para não gravar nome no repositório
    e sobreviver a troca de equipe.
    """
    presenca: Counter[str] = Counter()
    for path in transcricoes:
        for s in {t.speaker for t in turns(path)}:
            if DESCARTE_RE.match(s):
                continue
            presenca[fold(s)] += 1
    return {s for s, n in presenca.items()
            if n >= MIN_SESSOES_EQUIPE and casar(s, pessoas)[0] is None}


def proprias_da_sessao(participantes: list[dict], lexico: list[dict]) -> set[str]:
    """Termos do léxico que são a instituição do próprio participante.

    É o que liga `escopo=proprio` à sessão: o IPPLAM vira
    «[instituto de planejamento]» na entrevista de quem trabalha lá, e continua
    IPPLAM quando outro participante o cita de fora — exatamente o que o corpus
    codificado já faz.
    """
    insts = " ".join(p.get("instituicao", "") for p in participantes)
    f = fold(insts)
    out: set[str] = set()
    for e in lexico:
        if (e.get("escopo") or "").strip() != "proprio":
            continue
        termo, nota = fold(e["termo"]), fold(e.get("nota", ""))
        if (termo and termo in f) or (nota and nota in f):
            out.add(termo)
    # um acerto puxa todos os termos do mesmo grupo (sigla + nominal)
    grupos = {fold(e.get("nota", "")) for e in lexico
              if fold(e["termo"]) in out and e.get("nota")}
    for e in lexico:
        if (e.get("escopo") or "").strip() == "proprio" and fold(e.get("nota", "")) in grupos:
            out.add(fold(e["termo"]))
    return out


def guardar_allowlist(permitidos: set[str], pessoas: list[dict], equipe: set[str]) -> None:
    """A allowlist não pode conter nome de participante.

    Sem esta guarda, a allowlist vira o lugar óbvio para silenciar um alerta
    inconveniente na véspera da entrega.
    """
    nomes: set[str] = set()
    for p in pessoas:
        nomes |= tokens(p["nome"])
    for e in equipe:
        nomes |= tokens(e)
    colisao = permitidos & nomes
    if colisao:
        raise SystemExit(
            "ERRO: a allowlist contém tokens que são nome de pessoa: "
            + ", ".join(sorted(colisao))
            + "\nRemova de codebook/anonimizacao_permitidos.csv antes de continuar.")


def plano_de_rotulos(turnos, equipe: set[str], pessoas: list[dict],
                     n_esperado: int) -> tuple[dict[str, str], list[dict], list[str]]:
    """Falante → rótulo, na ordem da primeira aparição. Devolve também avisos."""
    vistos: list[str] = []
    for t in turnos:
        if DESCARTE_RE.match(t.speaker):
            continue
        if t.speaker not in vistos:
            vistos.append(t.speaker)

    entrevistadores = [s for s in vistos if fold(s) in equipe]
    participantes = [s for s in vistos if fold(s) not in equipe]

    rotulos = {s: "[entrevistador]" for s in entrevistadores}
    if len(participantes) == 1:
        rotulos[participantes[0]] = "[participante]"
    else:
        for i, s in enumerate(participantes):
            rotulos[s] = f"[participante {chr(ord('A') + i)}]"

    avisos: list[str] = []
    casados: list[dict] = []
    for s in participantes:
        p, ambiguo = casar(s, pessoas)
        if ambiguo:
            avisos.append(f"falante «{s}» casa com mais de uma pessoa da base — conferir")
        if p is None:
            avisos.append(f"falante «{s}» não consta da base de pessoas — "
                          f"sem dicionário determinístico de nome para esta sessão")
            casados.append({"nome": s, "instituicao": "", "papel": "desconhecido"})
        else:
            casados.append(p)

    if len(participantes) != n_esperado:
        avisos.append(f"a diarização separa {len(participantes)} participante(s), "
                      f"mas o registro anota {n_esperado}")
    return rotulos, casados, avisos


def montar_regras(casados: list[dict], pessoas: list[dict], equipe: set[str],
                  lexico: list[dict], rotulos: dict[str, str],
                  apelidos: dict[str, list[str]] | None = None,
                  terceiros: list[dict] | None = None) -> tuple[list, list[str]]:
    """Dicionário determinístico da sessão.

    Redige **todos** os nomes da base, não só os desta sessão: os entrevistadores
    citam participantes de outras entrevistas dentro da fala, e o nome de um
    participante de ENT-001 aparecendo em ENT-003 identifica igual.
    """
    regras, suprimidas = [], []
    apelidos = apelidos or {}
    proprios = {fold(c["nome"]) for c in casados}

    def emitir(nome: str, rotulo: str, origem: str) -> None:
        r, sup = R.regras_pessoa(nome, rotulo, apelidos.get(fold(nome), ()), origem)
        regras.extend(r)
        suprimidas.extend(sup)

    for falante, rot in rotulos.items():
        emitir(falante, rot, "falante")
    for p in pessoas:
        emitir(p["nome"], "[participante]" if fold(p["nome"]) in proprios else "[terceiro]",
               "base")
    for nome in equipe:
        emitir(nome, "[entrevistador]", "equipe")
    for t in (terceiros or []):
        # a lista de terceiros é curada à mão: o próprio nome entra como forma
        # explícita, vencendo a guarda de palavra comum — quem a escreveu decidiu
        # que «Silva» ali é vocativo, não a planta
        apes = [t["nome"]] + [a for a in (t.get("apelidos") or "").split("|") if a]
        r, sup = R.regras_pessoa(t["nome"], "[terceiro]", apes, "terceiro")
        regras.extend(r)
        suprimidas.extend(sup)

    regras += R.regras_contato()
    regras += R.regras_instituicao(lexico, proprias_da_sessao(casados, lexico))
    return regras, sorted(set(suprimidas))


def escrever_md(code: str, meta: dict, corpo: list[dict], agregada: bool) -> str:
    setor = SETOR_ROTULO.get(meta.get("sector", ""), meta.get("sector", ""))
    d = meta.get("date", "")
    data_br = f"{d[8:10]}/{d[5:7]}/{d[0:4]}" if len(d) == 10 else d
    primeiro = corpo[0]["ts"] if corpo else "00:00:00"
    ultimo = corpo[-1]["ts"] if corpo else "00:00:00"
    tcle = "assinado e arquivado" if meta.get("tcle") == "True" else "não localizado"

    linhas = [f"# Entrevista {code} — transcrição anonimizada", "",
              "| Campo | Valor |", "|---|---|",
              f"| Código | {code} |",
              f"| Setor | {setor} |",
              f"| Tipo de instituição | {meta.get('institution_type', '')} |",
              f"| Data | {data_br} |",
              f"| Duração do registro | {meta.get('minutes', '')} min "
              f"({primeiro} – {ultimo}) |",
              f"| Participantes | {meta.get('n_participants', '')} |",
              f"| TCLE | {tcle} |",
              f"| Turnos | {len(corpo)} |", "",
              CABECALHO + (NOTA_DIARIZACAO if agregada else ""), "", "---", ""]

    ts_atual = None
    for t in corpo:
        if t["ts"] != ts_atual:
            ts_atual = t["ts"]
            linhas += ["", f"`{ts_atual}`", ""]
        linhas.append(f"**{t['rotulo']}** — {t['texto']}")
        linhas.append("")
    return "\n".join(linhas).rstrip() + "\n"


def verificar_saida(textos: dict[str, str], pessoas: list[dict], equipe: set[str],
                    apelidos: dict[str, list[str]] | None = None,
                    terceiros: list[dict] | None = None) -> list[str]:
    """Varredura reversa: nenhum nome, e-mail ou telefone da base pode ter sobrado.

    Busca literal em texto dobrado, **sem regex e sem reaproveitar nada do motor**
    — é um caminho de código deliberadamente diferente, para que um erro em
    `redacao.py` não consiga se esconder atrás da própria lógica.
    """
    alvos: list[tuple[str, str]] = []
    for p in pessoas:
        for tok in tokens(p["nome"]):
            if len(tok) >= 5 and fold(tok) not in R.COMUNS:
                alvos.append((tok, p["nome"]))
    for e in equipe:
        for tok in tokens(e):
            if len(tok) >= 5:
                alvos.append((tok, e))
    for nome, apes in (apelidos or {}).items():
        for a in apes:
            if len(fold(a)) >= 5:
                alvos.append((fold(a), nome))
    for t in (terceiros or []):
        for v in [t["nome"]] + [a for a in (t.get("apelidos") or "").split("|") if a]:
            if len(fold(v)) >= 5:
                alvos.append((fold(v), t["nome"]))

    falhas = []
    for code, texto in textos.items():
        # palavra inteira, não substring: «América» contém «erica» e não é vazamento
        presentes = set(re.findall(r"[\wÀ-ÿ]+", fold(texto)))
        # token que também é palavra comum só conta capitalizado: «silva» é planta,
        # «Silva» é sobrenome — a mesma distinção que a redação faz
        capitalizados = {fold(t) for t in re.findall(r"(?<![\w])[A-ZÀ-Ý][\wÀ-ÿ]+", texto)}
        for tok, origem in alvos:
            achou = tok in capitalizados if tok in R.COMUNS else tok in presentes
            if achou:
                falhas.append(f"{code}: «{tok}» (de «{origem}») sobrou na saída")
        # sequência com cara de telefone no texto corrido, não dígitos concatenados
        for m in re.finditer(r"(?<!\d)(?:\+?55[\s-]*)?\(?\d{2}\)?[\s-]*9?\d{4}[\s-]?\d{4}(?!\d)",
                             texto):
            falhas.append(f"{code}: «{m.group(0).strip()}» tem forma de telefone "
                          f"e não foi redigido")
            break
    return falhas


def verificar_ancoras(textos: dict[str, str]) -> list[str]:
    """Toda marca de tempo citada pelas evidências tem de existir no anexo.

    `ts` não é único por linha de evidência — várias evidências compartilham o
    mesmo carimbo —, então a checagem é de subconjunto, não de junção 1:1.
    """
    falhas = []
    for code, texto in textos.items():
        arq = EVID / f"{code}.csv"
        if not arq.exists():
            continue
        presentes = set(re.findall(r"`(\d{2}:\d{2}:\d{2})`", texto))
        querem = {r["ts"] for r in ler_csv(arq) if r.get("ts")}
        faltam = querem - presentes
        if faltam:
            falhas.append(f"{code}: {len(faltam)} marca(s) de tempo das evidências "
                          f"ausentes do anexo: {', '.join(sorted(faltam)[:5])}")
    return falhas


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--acervo", required=True, help="pasta do acervo (DRIVE_FILES)")
    ap.add_argument("--saida", default=str(SAIDA), help="pasta de saída")
    ap.add_argument("--pessoas", default=str(PESSOAS), help="dicionário de nomes (vault)")
    ap.add_argument("--code", nargs="*", help="restringe a sessões")
    ap.add_argument("--commit", action="store_true", help="grava os arquivos")
    ap.add_argument("--incluir-sem-tcle", action="store_true",
                    help="gera as sessões sem TCLE em _quarentena/")
    ap.add_argument("--forcar", nargs="*", default=[],
                    help="libera sessão sem vínculo com a base de pessoas")
    ap.add_argument("--entrevistador", action="append", default=[],
                    help="força um nome como equipe (repetível)")
    ap.add_argument("--aceitar-residuos", action="store_true",
                    help="não falha com resíduo de risco alto pendente")
    ap.add_argument("--sem-verificacao", action="store_true")
    args = ap.parse_args()

    acervo, saida = Path(args.acervo), Path(args.saida)
    lexico = ler_csv(LEXICO)
    permitidos = {fold(r["termo"]) for r in ler_csv(PERMITIDOS)}
    permitidos |= {fold(e["termo"]) for e in lexico
                   if (e.get("escopo") or "").strip() == "nunca"}
    registro = {r["code"]: r for r in ler_csv(INTERVIEWS)}
    pessoas = ler_csv(Path(args.pessoas))
    apelidos = {fold(r["nome"]): [a for a in (r.get("apelidos") or "").split("|") if a]
                for r in ler_csv(APELIDOS)}
    terceiros = ler_csv(TERCEIROS)
    if not pessoas:
        print(f"AVISO: {args.pessoas} não encontrado — sem dicionário determinístico "
              f"de nomes. A anonimização fica dependente da varredura de resíduos.",
              file=sys.stderr)

    transcricoes = sorted(acervo.rglob("*_Transcrição.docx"))
    if not transcricoes:
        raise SystemExit(f"nenhuma transcrição encontrada em {acervo}")

    equipe = identificar_equipe(transcricoes, pessoas)
    equipe |= {fold(x) for x in args.entrevistador}
    guardar_allowlist(permitidos, pessoas, equipe)

    print(f"{len(transcricoes)} transcrição(ões) · equipe detectada: "
          f"{', '.join(sorted(equipe)) or '(nenhuma)'}\n")

    textos: dict[str, str] = {}
    retidas: dict[str, str] = {}
    resumo, revisar, avisos_gerais = [], [], []

    for path in transcricoes:
        code = path.name.replace("_Transcrição.docx", "")
        if args.code and code not in args.code:
            continue
        meta = registro.get(code, {})
        tt = turns(path)
        n_esp = int(meta.get("n_participants") or 1)
        rotulos, casados, avisos = plano_de_rotulos(tt, equipe, pessoas, n_esp)
        regras, suprimidas = montar_regras(casados, pessoas, equipe, lexico,
                                           rotulos, apelidos, terceiros)
        corpo, subs, res = R.varrer_turnos(tt, regras, permitidos, rotulos)

        # Supressao de trecho, DEPOIS da substituicao e ANTES da serializacao.
        # A posicao importa: aqui a ancora casa contra texto ja redigido (o nome
        # dentro do trecho ja e [participante]), o `idx` do turno e o mesmo
        # numero de paragrafo que a relacao de cortes usa, o (…) entra no .md e
        # passa de graca por verificar_saida/verificar_ancoras, e o trecho some
        # do revisar.csv — que e a intencao.
        corpo, n_cortes = SUP.aplicar_em_turnos(corpo, code)

        agregada = len([s for s in rotulos.values() if "participante" in s]) < n_esp
        tcle_ok = meta.get("tcle") == "True"
        sem_base = any("não consta da base" in a for a in avisos)
        publicavel = tcle_ok and not (sem_base and code not in args.forcar)

        md = escrever_md(code, meta, corpo, agregada)
        (textos if publicavel else retidas)[code] = md

        cat = Counter(s.categoria for s in subs)
        risco = Counter(r.risco for r in res)
        resumo.append({
            "code": code, "turnos": len(corpo), "chars": sum(len(t["texto"]) for t in corpo),
            "subs_pessoa": cat["pessoa"], "subs_instituicao": cat["instituicao"],
            "subs_contato": cat["contato"] + cat["documento"] + cat["url"] + cat["reuniao"],
            "residuos_alto": risco["alto"], "residuos_medio": risco["medio"],
            "residuos_baixo": risco["baixo"], "cortes": n_cortes,
            "tcle": meta.get("tcle", ""),
            "publicavel": publicavel,
        })
        for r in res:
            revisar.append({"code": code, "turno": r.turno, "ts": r.ts, "token": r.token,
                            "risco": r.risco, "motivo": r.motivo, "contexto": r.contexto})
        for a in avisos:
            avisos_gerais.append(f"{code}: {a}")
        for s in suprimidas:
            if len(s) > 2:
                avisos_gerais.append(f"{code}: variante «{s}» suprimida (palavra comum) "
                                     f"— confirmar manualmente")

        marca = "  " if publicavel else "!!"
        print(f"{marca} {code:<18} {len(corpo):>4} turnos · "
              f"{cat['pessoa']:>3} nomes · {cat['instituicao']:>3} inst · "
              f"{cat['contato'] + cat['documento']:>2} contatos · "
              f"resíduos alto={risco['alto']:>3} médio={risco['medio']:>4}"
              f"{'' if publicavel else '  ← RETIDA'}")

    if avisos_gerais:
        print(f"\n{len(avisos_gerais)} apontamento(s):")
        for a in avisos_gerais[:20]:
            print("  !", a)
        if len(avisos_gerais) > 20:
            print(f"  … e mais {len(avisos_gerais) - 20}")

    falhas = []
    if not args.sem_verificacao:
        falhas = verificar_saida({**textos, **retidas}, pessoas, equipe,
                                 apelidos, terceiros)
        falhas += verificar_ancoras(textos)
        print(f"\nverificação: {'FALHOU — ' + str(len(falhas)) + ' problema(s)' if falhas else 'limpa'}")
        for f in falhas[:15]:
            print("  ✗", f)

    alto = sum(r["residuos_alto"] for r in resumo)
    if not args.commit:
        print(f"\n(nada gravado — use --commit) · {alto} resíduo(s) de risco alto")
        return 2 if falhas else 0

    if falhas:
        print("\nnada gravado: a verificação reprovou.", file=sys.stderr)
        return 2

    saida.mkdir(parents=True, exist_ok=True)
    for code, md in textos.items():
        (saida / f"{code}.md").write_text(md, encoding="utf-8")
    if retidas:
        q = saida / "_quarentena"
        q.mkdir(exist_ok=True)
        if args.incluir_sem_tcle:
            for code, md in retidas.items():
                cab = ("> ⚠️ **SESSÃO RETIDA — NÃO ANEXAR AO PRODUTO 04.**\n"
                       "> TCLE não localizado ou participante sem vínculo com a base.\n\n")
                (q / f"NAO-PUBLICAR_{code}.md").write_text(cab + md, encoding="utf-8")

    with (saida / "revisar.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["code", "turno", "ts", "token", "risco",
                                          "motivo", "contexto"])
        w.writeheader()
        w.writerows(sorted(revisar, key=lambda r: ({"alto": 0, "medio": 1, "baixo": 2}[r["risco"]],
                                                   r["code"], r["turno"])))
    with (saida / "resumo.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(resumo[0]))
        w.writeheader()
        w.writerows(resumo)

    manifesto = [f"Anonimização das transcrições — Projeto Maringá em Ação pelo Clima",
                 f"gerado em {date.today().isoformat()}",
                 f"léxico sha256 {hashlib.sha256(LEXICO.read_bytes()).hexdigest()[:16]}",
                 f"allowlist sha256 {hashlib.sha256(PERMITIDOS.read_bytes()).hexdigest()[:16]}", ""]
    for code in sorted(textos):
        h = hashlib.sha256((saida / f"{code}.md").read_bytes()).hexdigest()
        manifesto.append(f"{h}  {code}.md")
    for code in sorted(retidas):
        manifesto.append(f"{'RETIDA — não publicar':<64}  {code}")
    (saida / "MANIFESTO.txt").write_text("\n".join(manifesto) + "\n", encoding="utf-8")

    relatorio = [f"# Relatório de anonimização", "",
                 "> **Material de trabalho — não anexar e não versionar.** Este relatório e "
                 "o `revisar.csv` citam nomes e trechos do texto original; vivem em "
                 "`saida_anonimizacao/`, que o `.gitignore` cobre.", "",
                 f"Gerado em {date.today().isoformat()}. "
                 f"{len(textos)} sessão(ões) publicável(is), {len(retidas)} retida(s).", "",
                 "## Resumo por sessão", "",
                 "| Sessão | Turnos | Nomes | Instituições | Contatos | Resíduo alto | Publicável |",
                 "|---|---:|---:|---:|---:|---:|---|"]
    for r in resumo:
        relatorio.append(f"| {r['code']} | {r['turnos']} | {r['subs_pessoa']} | "
                         f"{r['subs_instituicao']} | {r['subs_contato']} | "
                         f"{r['residuos_alto']} | {'sim' if r['publicavel'] else '**não**'} |")
    if retidas:
        relatorio += ["", "## Sessões retidas", "",
                      "Não entram no anexo público. TCLE não localizado, ou participante "
                      "sem vínculo com a base de pessoas — sem dicionário determinístico "
                      "de nomes, a redação depende apenas da varredura de resíduos.", ""]
        relatorio += [f"- `{c}`" for c in sorted(retidas)]
    if avisos_gerais:
        relatorio += ["", "## Apontamentos", ""] + [f"- {a}" for a in avisos_gerais]
    relatorio += ["", "## Revisão humana pendente", "",
                  f"`revisar.csv` traz {len(revisar)} token(s) capitalizado(s) que "
                  f"sobraram, dos quais **{alto} de risco alto**. O anexo não deve ser "
                  f"entregue antes de percorrer os de risco alto.", ""]
    (saida / "relatorio_anonimizacao.md").write_text("\n".join(relatorio) + "\n",
                                                     encoding="utf-8")

    print(f"\ngravado em {saida} · {len(textos)} anexo(s) · {len(retidas)} retida(s)")
    if alto and not args.aceitar_residuos:
        print(f"\n{alto} resíduo(s) de risco alto pendentes — percorra "
              f"{saida / 'revisar.csv'} antes de anexar.", file=sys.stderr)
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
