"""
Testes do motor de redação (`tools.redacao`).

Tudo roda contra uma transcrição sintética construída aqui dentro, com nomes e
instituições fictícios. **Nenhum dado real do acervo entra em `tests/`** — é a
mesma regra que governa o resto do projeto.
"""

import os
import re
import sys
import unittest
import zipfile
from tempfile import TemporaryDirectory

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tools import redacao as R                                  # noqa: E402
from tools.transcript import turns                              # noqa: E402
from tools import supressoes as S                               # noqa: E402

PESSOA = "Joana Ribeiro Alves"
EMAIL = "joana.alves@exemplo.org"
FONE = "(44) 99999-0000"

LEXICO = [
    {"termo": "Instituto Fictício de Planejamento", "tipo": "nominal",
     "substituto": "[instituto de planejamento]", "escopo": "proprio", "nota": ""},
    {"termo": "IFP", "tipo": "acronimo",
     "substituto": "[instituto de planejamento]", "escopo": "proprio", "nota": ""},
    {"termo": "Sanefic", "tipo": "nominal",
     "substituto": "[companhia de saneamento]", "escopo": "sempre", "nota": ""},
    {"termo": "BNDES", "tipo": "acronimo",
     "substituto": "", "escopo": "nunca", "nota": "§3 terceiro público"},
]

PERMITIDOS = {R.dobrar(x) for x in
              ("Maringá", "Paraná", "Brasil", "BNDES", "Plano", "Diretor", "Agosto")}


def regras_base(proprias=("instituto fictício de planejamento", "ifp")):
    regras, _ = R.regras_pessoa(PESSOA, "[participante]")
    return (regras + R.regras_contato()
            + R.regras_instituicao(LEXICO, {R.dobrar(p) for p in proprias}))


class TestVariantes(unittest.TestCase):
    def test_gera_formas_esperadas(self):
        v = R.variantes_nome(PESSOA)
        self.assertIn("Joana Ribeiro Alves", v)
        self.assertIn("Joana Alves", v)
        self.assertIn("Joana", v)

    def test_particula_nao_vira_variante_solta(self):
        v = R.variantes_nome("Maria da Conceição Souza")
        self.assertNotIn("da", v)

    def test_token_comum_e_suprimido_e_relatado(self):
        _, supr = R.regras_pessoa("Carlos Silva", "[participante]")
        self.assertIn("Silva", supr)          # sobrenome comum não vira regra solta
        self.assertNotIn("Carlos", supr)


class TestSubstituicao(unittest.TestCase):
    def test_nome_completo_e_parciais(self):
        for entrada in ("Joana Ribeiro Alves", "Joana Alves", "Joana", "Alves"):
            saida, _ = R.aplicar(f"conversei com {entrada} ontem", regras_base())
            self.assertEqual(saida, "conversei com [participante] ontem", entrada)

    def test_tolerante_a_acento(self):
        regras, _ = R.regras_pessoa("José Antônio Pereira", "[participante]")
        saida, _ = R.aplicar("o Jose Antonio Pereira falou", regras)
        self.assertEqual(saida, "o [participante] falou")

    def test_caixa_alta_do_asr(self):
        """Regressão: «Cid» tem de casar «CID» — a transcrição automática grita siglas."""
        regras, _ = R.regras_pessoa("Cid Fictício", "[entrevistador]", apelidos=("Cid",))
        for grafia in ("Cid", "CID", "Cíd"):
            saida, _ = R.aplicar(f"passei pro {grafia} ontem", regras)
            self.assertEqual(saida, "passei pro [entrevistador] ontem", grafia)

    def test_token_solto_exige_maiuscula(self):
        """«alves» minúsculo no meio da frase não é nome — não pode ser redigido."""
        saida, _ = R.aplicar("ele alves pela janela", regras_base())
        self.assertEqual(saida, "ele alves pela janela")

    def test_apelido_curto_passa_pela_guarda(self):
        """Apelido explícito e curado vence a guarda de tamanho mínimo."""
        regras, _ = R.regras_pessoa("Ana Fictícia", "[participante]", apelidos=("Ana",))
        saida, _ = R.aplicar("a Ana comentou", regras)
        self.assertEqual(saida, "a [participante] comentou")

    def test_contato_antes_de_nome(self):
        """Regressão: e-mail tem de cair inteiro, não virar [participante].alves@…"""
        saida, _ = R.aplicar(f"manda pra {EMAIL}", regras_base())
        self.assertEqual(saida, "manda pra [e-mail]")
        self.assertNotIn("alves", saida)

    def test_identificadores(self):
        casos = {
            FONE: "[telefone]",
            "123.456.789-00": "[CPF]",
            "43.807.298/0001-59": "[CNPJ]",
            "https://exemplo.org/x": "[link]",
            "PIN: 227 064 004 7433#": "[PIN]",
        }
        for entrada, esperado in casos.items():
            saida, _ = R.aplicar(f"anota {entrada} ai", regras_base())
            self.assertIn(esperado, saida, entrada)

    def test_placeholder_nao_e_reescrito(self):
        """«[instituto de planejamento]» não pode ser tocado por uma regra de 'planejamento'."""
        extra = R.Regra(re.compile(r"planejamento", re.IGNORECASE), "[X]",
                        "instituicao", "manual", "planejamento")
        saida, _ = R.aplicar("trabalho no Instituto Fictício de Planejamento",
                             regras_base() + [extra])
        self.assertEqual(saida, "trabalho no [instituto de planejamento]")

    def test_escopo_proprio(self):
        texto = "o IFP cuida disso"
        propria, _ = R.aplicar(texto, regras_base())
        self.assertEqual(propria, "o [instituto de planejamento] cuida disso")
        alheia, _ = R.aplicar(texto, regras_base(proprias=()))
        self.assertEqual(alheia, texto)       # instituição de outra sessão fica nominal

    def test_escopo_sempre_e_nunca(self):
        saida, _ = R.aplicar("a Sanefic e o BNDES financiam", regras_base())
        self.assertIn("[companhia de saneamento]", saida)
        self.assertIn("BNDES", saida)         # §3: terceiro público permanece nominal


class TestResiduos(unittest.TestCase):
    def test_sinaliza_desconhecido_e_ignora_allowlist(self):
        achados = R.residuos("fomos a Curitiba discutir com Maringá", PERMITIDOS)
        tokens = {r.token for r in achados}
        self.assertIn("Curitiba", tokens)
        self.assertNotIn("Maringá", tokens)

    def test_nao_sinaliza_dentro_de_placeholder(self):
        achados = R.residuos("o [instituto de planejamento] respondeu", PERMITIDOS)
        self.assertEqual([r.token for r in achados], [])

    def test_sigla_e_risco_alto(self):
        achados = R.residuos("mandaram pro CREA ontem", PERMITIDOS)
        self.assertEqual([r.risco for r in achados if r.token == "CREA"], ["alto"])

    def test_cargo_eleva_risco(self):
        achados = R.residuos("falei com o secretário Fulaninho sobre isso", PERMITIDOS)
        alto = [r.token for r in achados if r.risco == "alto"]
        self.assertIn("Fulaninho", alto)


class TestVarreduraReversa(unittest.TestCase):
    """A verificação final tem de reprovar texto mal redigido — golden negative."""

    def test_detecta_vazamento_plantado(self):
        vazou = f"o {PESSOA} disse que sim"
        self.assertIn(R.dobrar("Alves"), R.dobrar(vazou))
        limpo, _ = R.aplicar(vazou, regras_base())
        self.assertNotIn(R.dobrar("alves"), R.dobrar(limpo))
        self.assertNotIn(R.dobrar("joana"), R.dobrar(limpo))


def _docx_sintetico(caminho):
    """Escreve um .docx mínimo no formato que `tools.transcript` lê."""
    paras = ["ago. 7, 2026", "Entrevista fictícia - Transcrição", "00:04:35",
             f"Cid Fictício: bom dia, {PESSOA}",
             f"{PESSOA}: bom dia, meu e-mail é {EMAIL}",
             "00:12:51",
             f"{PESSOA}: aqui no Instituto Fictício de Planejamento a gente cuida disso"]
    corpo = "".join(f"<w:p><w:r><w:t>{p}</w:t></w:r></w:p>" for p in paras)
    doc = ('<?xml version="1.0"?><w:document '
           'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
           f"<w:body>{corpo}</w:body></w:document>")
    with zipfile.ZipFile(caminho, "w") as z:
        z.writestr("word/document.xml", doc)


class TestIntegracao(unittest.TestCase):
    def test_ponta_a_ponta(self):
        with TemporaryDirectory() as tmp:
            caminho = os.path.join(tmp, "ENT-999_Transcrição.docx")
            _docx_sintetico(caminho)
            tt = turns(caminho)
            rotulos = {"Cid Fictício": "[entrevistador]", PESSOA: "[participante]"}
            saida, subs, res = R.varrer_turnos(tt, regras_base(), PERMITIDOS, rotulos)

            self.assertEqual([t["ts"] for t in saida],
                             ["00:04:35", "00:04:35", "00:12:51"])
            texto = " ".join(t["texto"] for t in saida)
            self.assertNotIn("Joana", texto)
            self.assertNotIn("exemplo.org", texto)
            self.assertIn("[instituto de planejamento]", texto)
            self.assertTrue(subs)
            self.assertEqual({t["rotulo"] for t in saida},
                             {"[entrevistador]", "[participante]"})

    def test_timestamps_preservados(self):
        with TemporaryDirectory() as tmp:
            caminho = os.path.join(tmp, "ENT-999_Transcrição.docx")
            _docx_sintetico(caminho)
            originais = {t.ts for t in turns(caminho)}
            rotulos = {"Cid Fictício": "[entrevistador]", PESSOA: "[participante]"}
            saida, _, _ = R.varrer_turnos(turns(caminho), regras_base(),
                                          PERMITIDOS, rotulos)
            self.assertEqual({t["ts"] for t in saida}, originais)




# --------------------------------------------------------------- supressão
class TestSupressao(unittest.TestCase):
    """Supressão de trecho autoidentificador (`tools.supressoes`).

    Dados sintéticos, como o resto do arquivo. O que se verifica é o que a
    proteção promete: o trecho sai, a marca entra, o resto do turno sobrevive,
    e uma âncora que não casa **reprova** em vez de passar em silêncio.
    """

    TEXTO = ("[participante 1]: Eu presidi a comissão de meio ambiente da Câmara "
             "em 2019, e por isso conheço o processo.")
    TRECHO = "Eu presidi a comissão de meio ambiente da Câmara em 2019, e "

    def nova(self, **kw):
        campos = dict(fonte="transcricao", alvo="ENT-999", paragrafo=7,
                      texto=self.TEXTO, trecho=self.TRECHO,
                      motivo="presidencia nominal de comissao identifica a pessoa")
        campos.update(kw)
        return S.nova(**campos)

    def test_trecho_sai_e_marca_entra(self):
        sup = self.nova()
        saida = S.aplicar_em(self.TEXTO, sup)
        self.assertNotIn("presidi a comissão", saida)
        self.assertNotIn("2019", saida)
        self.assertIn(S.MARCA, saida)

    def test_resto_do_turno_sobrevive(self):
        saida = S.aplicar_em(self.TEXTO, self.nova())
        self.assertTrue(saida.startswith("[participante 1]: "))
        self.assertIn("conheço o processo", saida)

    def test_declaracao_nao_guarda_o_texto_suprimido(self):
        """O codebook é versionado: o material protegido não pode morar nele."""
        sup = self.nova()
        serializado = " ".join(str(getattr(sup, c)) for c in S.CAMPOS)
        self.assertNotIn("presidi", serializado)
        self.assertNotIn("Câmara", serializado)
        self.assertEqual(sup.n_chars, len(self.TRECHO))

    def test_ancora_que_nao_casa_reprova(self):
        """O cenário que o módulo existe para impedir: regerar e publicar sem o
        corte, sem ninguém perceber."""
        sup = self.nova()
        outro = self.TEXTO.replace("comissão", "subcomissão")
        with self.assertRaises(S.SupressaoNaoAplicada):
            S.aplicar_em(outro, sup)

    def test_trecho_alterado_reprova_mesmo_com_contexto_intacto(self):
        sup = self.nova()
        adulterado = self.TEXTO.replace("2019", "2020")
        with self.assertRaises(S.SupressaoNaoAplicada):
            S.aplicar_em(adulterado, sup)

    def test_aplica_nos_turnos_pelo_indice(self):
        sup = self.nova()
        corpo = [{"idx": 6, "ts": "00:00:10", "rotulo": "[participante 1]",
                  "texto": "Turno anterior, intacto."},
                 {"idx": 7, "ts": "00:00:20", "rotulo": "[participante 1]",
                  "texto": self.TEXTO}]
        saida, n = S.aplicar_em_turnos(corpo, "ENT-999", [sup])
        self.assertEqual(n, 1)
        self.assertEqual(saida[0]["texto"], "Turno anterior, intacto.")
        self.assertIn(S.MARCA, saida[1]["texto"])
        self.assertEqual(saida[1]["ts"], "00:00:20")

    def test_turno_ausente_reprova(self):
        sup = self.nova(paragrafo=999)
        corpo = [{"idx": 7, "ts": "00:00:20", "rotulo": "[participante 1]",
                  "texto": self.TEXTO}]
        with self.assertRaises(S.SupressaoNaoAplicada):
            S.aplicar_em_turnos(corpo, "ENT-999", [sup])

    def test_sessao_sem_supressao_passa_intacta(self):
        corpo = [{"idx": 7, "ts": "00:00:20", "rotulo": "[participante 1]",
                  "texto": self.TEXTO}]
        saida, n = S.aplicar_em_turnos(corpo, "ENT-000", [self.nova()])
        self.assertEqual(n, 0)
        self.assertEqual(saida[0]["texto"], self.TEXTO)


if __name__ == "__main__":
    unittest.main(verbosity=2)
