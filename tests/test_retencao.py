"""
Testes da retenção de sessões da camada pública (`tools.hub.retencao`).

Dados sintéticos, com instituições fictícias. **Nenhum dado real do acervo entra
em `tests/`** — mesma regra que governa `tests/test_redacao.py`.

Cada teste aqui é um teste negativo: o que se verifica não é que a trava deixa
passar o que deve passar, e sim que ela **reprova** o que não pode passar. Uma
trava sem teste negativo é uma trava que pode não existir, e isso já aconteceu
neste projeto.
"""

import os
import sys
import unittest
from tempfile import TemporaryDirectory
from pathlib import Path

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tools.hub import retencao as RT                            # noqa: E402
from tools.hub import transcricoes as T                         # noqa: E402

CRIT = "criterio sintetico"


def linha(code, publica, termo="", n=0, limiar=3, motivo=""):
    return {"code": code, "publica": publica, "termo": termo,
            "criterio": CRIT, "n_passagens": n, "limiar": limiar,
            "decidido_em": "2026-09-14", "decidido_por": "teste",
            "motivo": motivo}


def mapa(*linhas):
    return {x["code"]: x for x in linhas}


class TestMedida(unittest.TestCase):
    """A medida é ancorada no termo declarado, não adivinhada no texto."""

    FALA = ("[participante 1]: eu trabalho aqui no Instituto Fictício há seis "
            "anos. [entrevistador]: e o Instituto Fictício participa do "
            "conselho? [participante 1]: participa, sim.")

    def test_conta_so_a_fala_do_participante(self):
        """A menção do entrevistador não sustenta a decisão sobre o participante."""
        self.assertEqual(RT.medir(self.FALA, "Instituto Fictício"), 1)

    def test_termo_vazio_mede_zero(self):
        self.assertEqual(RT.medir(self.FALA, ""), 0)
        self.assertEqual(RT.medir(self.FALA, "   "), 0)

    def test_sem_marca_de_primeira_pessoa_nao_conta(self):
        """Citar a instituição não é dizer que se trabalha nela."""
        texto = ("[participante 1]: o Instituto Fictício publicou o relatório "
                 "no ano passado, e o documento está no portal da transparência.")
        self.assertEqual(RT.medir(texto, "Instituto Fictício"), 0)

    def test_nao_conta_palavra_dentro_de_outra(self):
        texto = "[participante 1]: eu trabalho no IFPR, que não é o IFP."
        self.assertEqual(RT.medir(texto, "IFP"), 1)

    def test_janela_nao_atravessa_turno(self):
        """Marca de 1ª pessoa num turno não identifica instituição de outro.

        Medir sobre a fala concatenada faria a janela de 60 caracteres pular a
        fronteira entre dois turnos e contar passagens que não existem.
        """
        texto = ("[participante 1]: eu comecei em 2019 e foi difícil no começo, "
                 "sinceramente, tudo muito devagar por causa do orçamento curto."
                 "[participante 2]: o Instituto Fictício respondeu o ofício.")
        self.assertEqual(RT.medir(texto, "Instituto Fictício"), 0)


class TestCobertura(unittest.TestCase):
    def test_sessao_sem_decisao_reprova(self):
        """Sem esta trava, uma sessão nova entraria publicada por omissão."""
        m = mapa(linha("ENT-901", True))
        with self.assertRaises(RT.RetencaoInvalida):
            RT.confere_cobertura(["ENT-901", "ENT-902"], m)

    def test_decisao_sem_sessao_reprova(self):
        m = mapa(linha("ENT-901", True), linha("ENT-999", False, motivo="x"))
        with self.assertRaises(RT.RetencaoInvalida):
            RT.confere_cobertura(["ENT-901"], m)

    def test_cobertura_exata_passa(self):
        m = mapa(linha("ENT-901", True))
        self.assertIsNone(RT.confere_cobertura(["ENT-901"], m))


class TestSaida(unittest.TestCase):
    """O gerador prova que não escreveu, lendo a saída de verdade."""

    def test_pagina_de_sessao_retida_na_saida_e_achado(self):
        m = mapa(linha("ENT-901", True), linha("ENT-999", False, motivo="x"))
        with TemporaryDirectory() as td:
            d = Path(td)
            (d / "ENT-901.html").write_text("ok", encoding="utf-8")
            (d / "ENT-999.html").write_text("não devia estar aqui", encoding="utf-8")
            self.assertEqual(RT.confere_saida(d, m), ["ENT-999"])

    def test_saida_so_com_publicadas_passa(self):
        m = mapa(linha("ENT-901", True), linha("ENT-999", False, motivo="x"))
        with TemporaryDirectory() as td:
            d = Path(td)
            (d / "ENT-901.html").write_text("ok", encoding="utf-8")
            self.assertEqual(RT.confere_saida(d, m), [])


class TestMedidaContraDecisao(unittest.TestCase):
    def test_publicada_no_limiar_reprova(self):
        m = mapa(linha("ENT-901", True, "Instituto Fictício", n=4))
        achados = RT.confere_medida({"ENT-901": 4}, m)
        self.assertTrue(any("criterio manda reter" in a for a in achados))

    def test_retida_no_limiar_passa(self):
        m = mapa(linha("ENT-901", False, "Instituto Fictício", n=4))
        self.assertEqual(RT.confere_medida({"ENT-901": 4}, m), [])

    def test_numero_declarado_divergente_reprova(self):
        """A decisão teria sido tomada sobre outro material."""
        m = mapa(linha("ENT-901", False, "Instituto Fictício", n=9, motivo="x"))
        achados = RT.confere_medida({"ENT-901": 2}, m)
        self.assertTrue(any("outro material" in a for a in achados))

    def test_retida_abaixo_do_limiar_exige_motivo(self):
        sem = mapa(linha("ENT-901", False, n=0))
        self.assertTrue(RT.confere_medida({"ENT-901": 0}, sem))
        com = mapa(linha("ENT-901", False, n=0, motivo="regra 5.6"))
        self.assertEqual(RT.confere_medida({"ENT-901": 0}, com), [])


class TestIndice(unittest.TestCase):
    """O índice lista as 17 e não linka o que não existe."""

    SESSOES = [
        {"code": "ENT-901", "setor_publico": "Publico", "date": "2026-08-01",
         "minutes": "60", "n_participants": "1"},
        {"code": "ENT-999", "setor_publico": "Academia", "date": "2026-08-02",
         "minutes": "30", "n_participants": "2"},
    ]

    def html(self):
        return T.indice(self.SESSOES, {}, publicadas={"ENT-901"})

    def test_retida_sai_sem_link(self):
        h = self.html()
        self.assertNotIn('href="transcricoes/ENT-999.html"', h)
        self.assertIn('href="transcricoes/ENT-901.html"', h)

    def test_retida_continua_listada_e_marcada(self):
        h = self.html()
        self.assertIn("ENT-999", h)
        self.assertIn(T.MARCA_RETIDA, h)

    def test_marca_e_generica_na_linha_da_sessao(self):
        """O método pode ser declarado; o motivo POR SESSÃO, não.

        A nota da página explica o critério em geral, e isso é o que se espera
        de método declarado. O que não pode aparecer é a linha de uma sessão
        dizendo por que ela saiu: seria repor por outro caminho o rótulo por
        sessão que deixou a camada pública em 13/09.
        """
        import re
        h = self.html()
        linha = re.search(r"<tr[^>]*>(?:(?!</tr>).)*ENT-999.*?</tr>", h, re.S)
        self.assertIsNotNone(linha, "linha da sessão retida não encontrada")
        celula = linha.group(0)
        self.assertIn(T.MARCA_RETIDA, celula)
        for proibido in ("empregador", "autoidentifica", "limiar", "passagens"):
            self.assertNotIn(proibido, celula, proibido)

    def test_pagina_nao_traz_motivo_declarado_no_codebook(self):
        """Os motivos do CSV nomeiam órgão e regra. Nenhum pode vazar."""
        h = self.html()
        for r in RT.carregar().values():
            motivo = (r.get("motivo") or "").strip()
            if motivo:
                self.assertNotIn(motivo, h, r["code"])
            termo = (r.get("termo") or "").strip()
            if termo:
                self.assertNotIn(termo, h, r["code"])


class TestDispensaOrfa(unittest.TestCase):
    def test_dispensa_sem_candidato_correspondente_reprova(self):
        from tools import varre_local_trabalho as V
        orfas = V.dispensas_orfas([])
        self.assertEqual(len(orfas), len(V.DISPENSADOS))

    def test_dispensa_com_candidato_vivo_passa(self):
        from tools import varre_local_trabalho as V
        vivos = [{"sessao": s, "instituicao": i} for (s, i) in V.DISPENSADOS]
        self.assertEqual(V.dispensas_orfas(vivos), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
