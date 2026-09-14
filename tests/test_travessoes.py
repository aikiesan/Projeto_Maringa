"""
Testes da reescrita de travessões (`tools.p4_travessoes`).

Texto sintético. O que se verifica são as três regras e, sobretudo, que a
ferramenta **reprova** quando sobra travessão: entregar o texto meio tratado é
pior do que não tratar.
"""

import os
import sys
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tools import p4_travessoes as T                            # noqa: E402

D = T.TRAVESSAO


class _Run:
    def __init__(self, texto):
        self.text = texto


class _Par:
    def __init__(self, *textos):
        self.runs = [_Run(t) for t in textos]

    @property
    def text(self):
        return "".join(r.text for r in self.runs)

    def add_run(self, texto):
        self.runs.append(_Run(texto))
        return self.runs[-1]


class TestRegras(unittest.TestCase):
    def test_titulo_de_anexo_vira_dois_pontos(self):
        self.assertEqual(T.reescrever(f"Anexo 01 {D} Instrumentais de entrevista"),
                         "Anexo 01: Instrumentais de entrevista")

    def test_aposto_vira_parenteses(self):
        self.assertEqual(
            T.reescrever(f"Das 494 evidências, 206 {D} 42% {D} classificam a condição"),
            "Das 494 evidências, 206 (42%) classificam a condição")

    def test_aposto_que_fecha_antes_de_virgula(self):
        """«… se aplica —, enquanto» não pode virar «…),,»."""
        saida = T.reescrever(
            f"de mais de uma sessão {D} situação em que se aplica {D}, enquanto 53")
        self.assertEqual(saida,
                         "de mais de uma sessão (situação em que se aplica), enquanto 53")
        self.assertNotIn(",,", saida)

    def test_aposto_com_parenteses_dentro_vira_virgulas(self):
        """Parêntese dentro de parêntese é pior do que o travessão."""
        saida = T.reescrever(
            f"sem fonte oral {D} 1.1.2 (alinhamento) e 3.3.2 (títulos) {D}, todas de")
        self.assertNotIn("((", saida)
        self.assertNotIn("))", saida)
        self.assertNotIn(",,", saida)
        self.assertIn("sem fonte oral, 1.1.2 (alinhamento) e 3.3.2 (títulos), todas de",
                      saida)

    def test_coordenacao_vira_virgula(self):
        """Regressão: a versão anterior capturava um caractere e «mas» virava «m»."""
        for conj in ("mas", "e", "ou"):
            with self.subTest(conj=conj):
                saida = T.reescrever(f"existem instrumentos formalizados {D} {conj} "
                                     f"quase nada atravessa disso.")
                self.assertIn(f"formalizados, {conj} quase", saida)

    def test_explicacao_vira_dois_pontos(self):
        saida = T.reescrever(f"é matéria de verificação documental {D} PPA, LDO, LOA.")
        self.assertIn("documental: PPA", saida)

    def test_dois_isolados_no_mesmo_paragrafo_nao_viram_par(self):
        """§333 tem dois travessões que não são um par.

        O que separa os casos é o ponto final dentro do segmento, e não o
        tamanho: um aposto não atravessa fim de frase.
        """
        texto = (f"existem instrumentos formalizados {D} mas quase nada atravessa. "
                 f"Isso aparece de forma convergente {D} por divulgação insuficiente.")
        saida = T.reescrever(texto)
        self.assertNotIn("(", saida)
        self.assertIn("formalizados, mas quase", saida)
        self.assertIn("convergente: por divulgação", saida)

    def test_idempotente(self):
        texto = f"Anexo 02 {D} Termo de Consentimento"
        self.assertEqual(T.reescrever(T.reescrever(texto)), T.reescrever(texto))

    def test_texto_sem_travessao_fica_intacto(self):
        texto = "Uma frase comum, com vírgula e ponto."
        self.assertEqual(T.reescrever(texto), texto)


class TestPontuacaoResultante(unittest.TestCase):
    """Nenhuma das regras pode produzir pontuação quebrada."""

    CASOS = [
        f"A organização por setor {D} poder público, academia e sociedade civil {D} "
        f"reproduz a estrutura.",
        f"Este capítulo explicita essa passagem {D} o que a evidência determina.",
        f"Anexo 06 {D} Painel público de acompanhamento.",
        f"a unidade adotada {D} a evidência, e não a resposta {D} é o que permite.",
    ]

    def test_sem_pontuacao_duplicada(self):
        for texto in self.CASOS:
            with self.subTest(texto=texto[:40]):
                saida = T.reescrever(texto)
                for ruim in (",,", "::", " ,", " :", "((", "))", "( ", " )", D):
                    self.assertNotIn(ruim, saida, ruim)


class TestEscritaNoDoc(unittest.TestCase):
    def test_runs_fora_da_mudanca_ficam_intactos(self):
        """O negrito que abre a afirmação vive num run próprio."""
        par = _Par("3.1.1. ", f"Das 494 evidências, 206 {D} 42% {D} classificam",
                   " a condição.")
        T._escrever_preservando_runs(par, T.reescrever(par.text))
        self.assertEqual(par.runs[0].text, "3.1.1. ")
        self.assertEqual(par.runs[2].text, " a condição.")
        self.assertIn("(42%)", par.text)
        self.assertNotIn(D, par.text)

    def test_texto_final_e_o_esperado(self):
        par = _Par("Anexo 03 ", f"{D} Protocolo de Registro")
        esperado = T.reescrever(par.text)
        T._escrever_preservando_runs(par, esperado)
        self.assertEqual(par.text, esperado)


class TestTrava(unittest.TestCase):
    def test_sobra_de_travessao_aborta(self):
        """Se uma regra deixar de pegar um caso, a geração tem de parar.

        Sem esta trava, a ferramenta entregaria um .docx meio tratado, que é o
        pior dos resultados: parece tratado e não está.
        """
        class _DocFalso:
            def __init__(self, pars):
                self.paragraphs = pars

        # travessao colado, que nenhuma das tres regras alcanca
        doc = _DocFalso([_Par(f"texto{D}colado sem espacos")])
        with self.assertRaises(SystemExit) as caso:
            T.aplicar_no_doc(doc)
        self.assertIn("sobraram", str(caso.exception))

    def test_documento_tratavel_passa_e_conta(self):
        class _DocFalso:
            def __init__(self, pars):
                self.paragraphs = pars

        doc = _DocFalso([_Par(f"Anexo 01 {D} Instrumentais"),
                         _Par("sem travessão aqui"),
                         _Par(f"206 {D} 42% {D} classificam")])
        r = T.aplicar_no_doc(doc)
        self.assertEqual(r["antes"], 3)
        self.assertEqual(r["depois"], 0)
        self.assertEqual(r["paragrafos"], 2)


class TestRelacaoDeCortes(unittest.TestCase):
    """A relação de cortes descreve o que saiu, e não pode descrever errado."""

    def sup(self, substituto):
        from tools import supressoes as S
        texto = "[participante 1]: eu trabalho aqui no Instituto Fictício, faz anos."
        return S.nova("transcricao", "ENT-999", 0, texto,
                      " aqui no Instituto Fictício", "local de trabalho",
                      substituto=substituto)

    def test_efeito_declarado_por_supressao(self):
        from tools import supressoes as S
        from tools.relacao_cortes import _efeito
        self.assertEqual(_efeito(self.sup(S.MARCA)), "corte marcado com (…)")
        self.assertEqual(_efeito(self.sup("")), "remoção sem marca")
        self.assertEqual(_efeito(self.sup("no órgão")), "substituição")

    def test_marca_de_tempo_e_a_anterior_ao_paragrafo(self):
        from tools.relacao_cortes import _marca_tempo
        pars = ["00:04:35", "um turno", "00:12:51", "outro turno", "o turno do corte"]
        self.assertEqual(_marca_tempo(pars, 4), "00:12:51")
        self.assertEqual(_marca_tempo(pars, 1), "00:04:35")
        self.assertEqual(_marca_tempo(["sem marca", "nada"], 1), "")


if __name__ == "__main__":
    unittest.main(verbosity=2)
