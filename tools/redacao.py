"""
Motor de redação das transcrições — substituição determinística e varredura de risco.

Módulo puro: não lê acervo, não escreve arquivo, não conhece o vault. Tudo que
precisa chega por parâmetro. É o que `tests/test_redacao.py` importa, e é o que
permite testar a anonimização sem nenhum dado real.

A orquestração (ler o acervo, montar o dicionário, gravar o anexo) vive em
`tools/anonimizar_transcricoes.py`.

Duas invariantes governam o desenho:

1. **Ordem das regras é correção, não estilo.** Contato antes de pessoa: uma regra
   de primeiro nome aplicada a «joana.alves@exemplo.org» produziria
   «[participante].alves@exemplo.org» — uma redação parcial que *parece* redigida,
   que é o pior resultado possível.
2. **Placeholder gravado é inerte.** Depois de escrever «[instituto de planejamento]»,
   uma regra posterior de «planejamento» não pode reescrever por dentro. Por isso
   `aplicar` troca cada acerto por um sentinela e só restaura no fim.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field
from typing import Iterable, Sequence

# Ordem de aplicação. Índice na tupla = prioridade; dentro de cada categoria,
# literal mais longo primeiro.
CATEGORIAS = ("contato", "documento", "url", "reuniao",
              "pessoa", "equipe", "instituicao", "endereco")

# Partículas que nunca viram regra sozinhas.
PARTICULAS = {"da", "de", "do", "das", "dos", "e", "di", "du", "del", "van", "von"}

# Palavras portuguesas que também são nome próprio. Um token solto destes não
# gera regra — o custo de redigir «a rosa dos ventos» é maior que o de deixar o
# sobrenome para a varredura de resíduos.
COMUNS = {
    "vera", "sol", "luz", "rosa", "neves", "campos", "prado", "serra", "silva",
    "santos", "costa", "lima", "cruz", "pereira", "ribeiro", "duarte", "franco",
    "leao", "leão", "rego", "sene", "matos", "moura", "nunes", "paz", "pinto",
    "ramos", "rocha", "salles", "sales", "teles", "telles", "viana", "vieira",
    "maringa", "maringá", "parana", "paraná", "brasil", "junior", "júnior",
    "filho", "neto", "primo", "amor", "bela", "belo", "boa", "bom", "graca",
    "graça", "gloria", "glória", "ceu", "céu", "mar", "rio", "vale", "monte",
}

# Palavras portuguesas frequentes que aparecem capitalizadas por começarem frase.
# Não são resíduo: sinalizá-las afoga a revisão humana em ruído, que é a forma
# mais eficaz de fazer com que ninguém leia o `revisar.csv`.
COMUM_PT = {
    "entao", "nao", "mas", "uhum", "voce", "voces", "sim", "isso", "porque", "aham",
    "olha", "bom", "boa", "ele", "ela", "eles", "elas", "obrigado", "obrigada",
    "acho", "como", "perfeito", "agora", "tem", "nos", "muito", "que", "tudo",
    "exatamente", "yeah", "aqui", "ali", "la", "entendi", "certo", "claro", "opa",
    "oi", "ola", "tchau", "sei", "acha", "sabe", "veja", "vamos", "vou", "foi",
    "era", "esse", "essa", "este", "esta", "isto", "aquele", "aquela", "quando",
    "quem", "qual", "quais", "onde", "para", "por", "com", "sem", "uma", "dois",
    "duas", "tres", "hoje", "ontem", "amanha", "sempre", "nunca", "ainda", "ja",
    "tambem", "so", "ate", "depois", "antes", "durante", "desde", "pois", "logo",
    "assim", "talvez", "quase", "bastante", "pouco", "mais", "menos", "melhor",
    "pior", "grande", "pequeno", "primeiro", "segundo", "terceiro", "ultimo",
    "legal", "otimo", "beleza", "pronto", "vai", "vem", "fazer", "ter", "ser",
    "estar", "dar", "ver", "dizer", "falar", "pode", "deve", "precisa", "gente",
    "coisa", "caso", "ponto", "parte", "forma", "modo", "vez", "ano", "anos",
    "dia", "dias", "mes", "meses", "hora", "horas", "tempo", "agenda", "reuniao",
    "projeto", "projetos", "plano", "planos", "area", "areas", "obra", "obras",
    "agua", "aguas", "clima", "cidade", "cidades", "bairro", "bairros", "rua",
    "ruas", "praca", "parque", "parques", "meio", "ambiente", "ambiental",
    "sustentabilidade", "desenvolvimento", "gestao", "politica", "politicas",
    "publico", "publica", "privado", "privada", "social", "tecnico", "tecnica",
    "banco", "bancos", "fundo", "fundos", "recurso", "recursos", "verba",
    "orcamento", "imposto", "taxa", "lei", "leis", "decreto", "norma", "projeto",
    "defesa", "civil", "saude", "educacao", "cultura", "esporte", "transporte",
    "energia", "residuo", "residuos", "lixo", "esgoto", "drenagem", "arvore",
    "arvores", "verde", "risco", "riscos", "impacto", "impactos", "dado", "dados",
    "sistema", "sistemas", "rede", "redes", "conselho", "camara", "prefeitura",
    "secretaria", "instituto", "universidade", "empresa", "associacao", "sindicato",
    "ok", "um", "meu", "minha", "seu", "sua", "nosso", "nossa", "deus", "sao",
    "santa", "santo", "rio", "norte", "sul", "leste", "oeste", "centro", "google",
    "whatsapp", "excel", "word", "powerpoint", "zoom", "teams", "pdf", "email",
}

_SENTINELA = "\x00%d\x00"
_SENT_RE = re.compile(r"\x00(\d+)\x00")

# Vogais acentuadas equivalentes, para casar grafia de ASR que perde acento.
_EQUIV = {
    "a": "aáàâãä", "e": "eéèêë", "i": "iíìîï", "o": "oóòôõö",
    "u": "uúùûü", "c": "cç", "n": "nñ",
}


@dataclass(frozen=True)
class Regra:
    """Uma substituição a aplicar. `literal` é o texto de origem, usado para ordenar."""
    padrao: re.Pattern
    substituto: str
    categoria: str
    origem: str          # lista | vault | lexico | regex | manual
    literal: str

    def __post_init__(self) -> None:
        if self.categoria not in CATEGORIAS:
            raise ValueError(f"categoria desconhecida: {self.categoria}")


@dataclass
class Substituicao:
    turno: int
    ts: str
    categoria: str
    origem: str
    achado: str
    substituto: str


@dataclass
class Residuo:
    turno: int
    ts: str
    token: str
    contexto: str
    risco: str           # alto | medio | baixo
    motivo: str


def dobrar(s: str) -> str:
    """Minúscula sem acento. Mesma semântica de `tools.transcript.fold`."""
    s = unicodedata.normalize("NFKD", str(s or ""))
    return "".join(c for c in s if not unicodedata.combining(c)).strip().lower()


def padrao_tolerante(s: str) -> str:
    """Texto literal → regex que casa a mesma palavra com ou sem acento.

    «José» vira algo que casa «José», «Jose», «JOSÉ». Espaço casa qualquer
    espaçamento, porque a transcrição automática quebra linha em lugar arbitrário.
    """
    out = []
    for ch in s:
        base = dobrar(ch)
        if base in _EQUIV:
            classe = _EQUIV[base]
            out.append(f"[{classe}{classe.upper()}]")
        elif ch.isspace():
            out.append(r"\s+")
        elif ch.isalpha():
            # letra sem equivalente acentuado: as duas caixas, senão «Cid» não
            # casa «CID» — a grafia em caixa alta é comum na transcrição automática
            out.append(f"[{base}{base.upper()}]")
        else:
            out.append(re.escape(ch))
    return "".join(out)


def variantes_nome(nome: str, apelidos: Iterable[str] = ()) -> list[str]:
    """Formas pelas quais um nome aparece na fala.

    «Joana Ribeiro Alves» → nome completo, primeiro+último, último, primeiro.
    Tokens soltos passam pelas guardas de `_token_seguro`; os barrados são
    devolvidos pelo chamador via `regras_pessoa`, para revisão humana.
    """
    partes = [p for p in re.split(r"\s+", nome.strip()) if p]
    uteis = [p for p in partes if dobrar(p) not in PARTICULAS]
    out: list[str] = []

    def push(v: str) -> None:
        if v and v not in out:
            out.append(v)

    if len(partes) > 1:
        push(" ".join(partes))
    if len(uteis) > 2:
        push(f"{uteis[0]} {uteis[-1]}")
    for a in apelidos:
        push(a.strip())
    for i in range(len(uteis) - 1):
        push(f"{uteis[i]} {uteis[i + 1]}")      # pares adjacentes: «Ana Paula»
    for t in uteis:
        push(t)                                  # tokens soltos, filtrados adiante
    return out


def _token_seguro(tok: str) -> bool:
    """Um token solto só vira regra se for improvável como palavra comum."""
    d = dobrar(tok)
    return len(d) >= 4 and d not in PARTICULAS and d not in COMUNS


def regras_pessoa(nome: str, substituto: str, apelidos: Iterable[str] = (),
                  origem: str = "vault") -> tuple[list[Regra], list[str]]:
    """Regras para um nome. Devolve (regras, variantes suprimidas).

    Multi-token casa sem distinguir caixa nem acento. Token solto casa
    **respeitando a caixa** — «Alves» é nome, «alves» quase nunca é.
    """
    regras, suprimidas = [], []
    explicitos = {dobrar(a) for a in apelidos}
    for v in variantes_nome(nome, apelidos):
        solto = len(v.split()) == 1
        if solto and dobrar(v) not in explicitos and not _token_seguro(v):
            suprimidas.append(v)
            continue
        # Token solto exige inicial maiúscula (ou caixa alta inteira): «Alves» é
        # nome, «alves» quase nunca é. Nome com mais de um token dispensa a guarda.
        guarda = r"(?=[A-ZÀ-Ý])" if solto else ""
        pat = re.compile(rf"(?<![\w]){guarda}{padrao_tolerante(v)}(?![\w])")
        regras.append(Regra(pat, substituto, "pessoa", origem, v))
    return regras, suprimidas


def regras_instituicao(entradas: Sequence[dict], proprias: set[str]) -> list[Regra]:
    """Regras institucionais, filtradas pelo escopo do §3 da metodologia.

    `entradas` são linhas de `codebook/anonimizacao_lexico.csv`:
    `termo,tipo,substituto,escopo,nota`.

      * `sempre`  — sempre redige
      * `proprio` — redige só quando o termo está em `proprias`, isto é, quando é
        a instituição do próprio participante naquela sessão
      * `nunca`   — nunca redige (terceiro de caráter público: órgão estadual,
        contrato publicado, lei). Some da lista de regras e entra na allowlist.
    """
    out = []
    for e in entradas:
        escopo = (e.get("escopo") or "sempre").strip()
        if escopo == "nunca":
            continue
        if escopo == "proprio" and dobrar(e["termo"]) not in proprias:
            continue
        termo = e["termo"].strip()
        sub = (e.get("substituto") or "").strip()
        if not termo or not sub:
            continue
        # Sigla curta exige caixa alta: sem isso «IAM» casaria o verbo «iam», e
        # «CAU» casaria «cau-». Nome por extenso não precisa da guarda.
        sigla = termo.isupper() and len(termo) <= 6
        guarda = r"(?=[A-ZÀ-Ý])" if sigla else ""
        pat = re.compile(rf"(?<![\w]){guarda}{padrao_tolerante(termo)}(?![\w])")
        out.append(Regra(pat, sub, "instituicao", "lexico", termo))
    return out


def regras_contato() -> list[Regra]:
    """Identificadores diretos. Aplicadas antes de qualquer regra de nome."""
    def r(pat: str, sub: str, cat: str, flags: int = 0) -> Regra:
        return Regra(re.compile(pat, flags), sub, cat, "regex", pat)

    return [
        r(r"\b[\w.+-]+@[\w-]+\.[\w.]+\b", "[e-mail]", "contato"),
        r(r"\b\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}\b", "[CNPJ]", "documento"),
        r(r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b", "[CPF]", "documento"),
        r(r"\b\d{5}-?\d{3}\b(?=\s*(?:CEP|$|[,.]))", "[CEP]", "documento"),
        r(r"(?:\+55\s*)?\(?\d{2}\)?\s*9?\d{4}[-\s]?\d{4}\b", "[telefone]", "contato"),
        r(r"\bhttps?://\S+", "[link]", "url"),
        r(r"\b(?:meet\.google\.com|tel\.meet)/[\w?=-]+", "[link de reunião]", "reuniao"),
        r(r"\bPIN:?\s*[\d\s]{6,}#?", "[PIN]", "reuniao", re.IGNORECASE),
        r(r"\b(?:Rua|Av\.?|Avenida|Travessa|Alameda|Praça)\s+"
          r"[A-ZÀ-Ý][\wÀ-ÿ]*(?:\s+(?:d[aeo]s?\s+)?[A-ZÀ-Ý][\wÀ-ÿ]*)*,?\s*n?º?\s*\d+",
          "[endereço]", "endereco"),
    ]


def ordenar(regras: Sequence[Regra]) -> list[Regra]:
    """Categoria na ordem de CATEGORIAS; dentro dela, literal mais longo primeiro."""
    return sorted(regras, key=lambda x: (CATEGORIAS.index(x.categoria), -len(x.literal)))


def aplicar(texto: str, regras: Sequence[Regra]) -> tuple[str, list[tuple[Regra, str]]]:
    """Aplica as regras em ordem, protegendo o que já foi substituído.

    Cada substituição vira um sentinela `\\x00n\\x00` — invisível para as regras
    seguintes — e só volta a ser texto no fim. Sem isso, «[instituto de
    planejamento]» seria reescrito por uma regra de «planejamento».
    """
    guardado: list[str] = []
    achados: list[tuple[Regra, str]] = []
    for regra in ordenar(regras):
        def troca(m: re.Match) -> str:
            achados.append((regra, m.group(0)))
            guardado.append(regra.substituto)
            return _SENTINELA % (len(guardado) - 1)
        texto = regra.padrao.sub(troca, texto)
    return _SENT_RE.sub(lambda m: guardado[int(m.group(1))], texto), achados


_TOKEN_RE = re.compile(r"\b[A-ZÀ-Ý][\wÀ-ÿ'’-]{2,}\b|\b[A-Z]{2,6}\b")
_CARGO_RE = re.compile(
    r"\b(?:o|a|senhor|senhora|sr|sra|doutor|doutora|dr|dra|professor|professora|"
    r"secretári[oa]|diretor|diretora|presidente|gerente|coordenador|coordenadora|"
    r"vereador|vereadora|prefeito|prefeita|engenheir[oa]|arquitet[oa])\s*\.?\s*$",
    re.IGNORECASE)
_COMPOSTO_RE = re.compile(r"\b[A-ZÀ-Ý][\wÀ-ÿ]+\s+(?:d[aeo]s?\s+)?[A-ZÀ-Ý][\wÀ-ÿ]+\b")


def residuos(texto: str, permitidos: set[str], turno: int = 0, ts: str = "") -> list[Residuo]:
    """Tokens capitalizados que sobraram e não estão na allowlist.

    Gradua o risco, mas **não descarta nada** — nem token em início de frase.
    Ruído em `revisar.csv` é barato; nome perdido em anexo público não é.
    """
    limpo = _SENT_RE.sub(" ", texto)
    # o que já está dentro de [colchetes] é nosso, não é resíduo
    vaos = [(m.start(), m.end()) for m in re.finditer(r"\[[^\]]*\]", limpo)]

    out: list[Residuo] = []
    for m in _TOKEN_RE.finditer(limpo):
        if any(a <= m.start() < b for a, b in vaos):
            continue
        tok = m.group(0)
        if dobrar(tok) in permitidos or dobrar(tok) in COMUM_PT:
            continue
        antes = limpo[max(0, m.start() - 40):m.start()]
        if tok.isupper() and len(tok) <= 6:
            risco, motivo = "alto", "sigla fora da allowlist"
        elif _CARGO_RE.search(antes):
            risco, motivo = "alto", "precedido de tratamento ou cargo"
        elif _COMPOSTO_RE.match(limpo[m.start():]):
            risco, motivo = "alto", "sequência de capitalizadas (possível nome composto)"
        elif antes.rstrip().endswith((".", "!", "?")) or not antes.strip():
            risco, motivo = "baixo", "início de frase"
        else:
            risco, motivo = "medio", "capitalizada no meio da frase"
        ctx = limpo[max(0, m.start() - 60):m.end() + 60].replace("\n", " ")
        out.append(Residuo(turno, ts, tok, ctx, risco, motivo))
    return out


def varrer_turnos(turnos: Sequence, regras: Sequence[Regra], permitidos: set[str],
                  rotulos: dict[str, str]) -> tuple[list[dict], list[Substituicao], list[Residuo]]:
    """Passa o corpo inteiro da sessão: rotula falante, redige texto, colhe resíduos.

    `turnos` são `tools.transcript.Turn`; `rotulos` mapeia falante → «[participante]».
    Devolve turnos já anonimizados como dicionários prontos para o escritor.
    """
    regras = ordenar(regras)
    saida, subs, res = [], [], []
    for t in turnos:
        rot = rotulos.get(t.speaker)
        if rot is None:
            continue                      # falante descartado (aviso do ASR)
        texto, achados = aplicar(t.text, regras)
        for regra, achado in achados:
            subs.append(Substituicao(t.idx, t.ts, regra.categoria, regra.origem,
                                     achado, regra.substituto))
        res.extend(residuos(texto, permitidos, t.idx, t.ts))
        saida.append({"idx": t.idx, "ts": t.ts, "rotulo": rot, "texto": texto})
    return saida, subs, res
