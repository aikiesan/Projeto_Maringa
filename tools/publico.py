# -*- coding: utf-8 -*-
"""Saneia site/artifact.html para a camada aberta do painel (GitHub Pages).

Deriva da saida interna; nao duplica conteudo. Cada transformacao e explicita e
contada, e o script FALHA se qualquer uma delas nao encontrar o que esperava.
"""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENTRADA = str(ROOT / "site" / "artifact.html")
SAIDA = str(ROOT / "site" / "publico.html")

h = open(ENTRADA, encoding="utf-8").read()
aplicadas = []


def troca(padrao, novo, minimo=1, rotulo=""):
    global h
    h, n = re.subn(padrao, novo, h)
    aplicadas.append((rotulo or padrao[:48], n))
    if n < minimo:
        sys.exit(f"FALHOU: '{rotulo or padrao}' esperava >= {minimo}, aplicou {n}")


# 1. setor Especial extinto — as tres sessoes sao do bloco PUB
troca(r'"sector": "Especial"', '"sector": "Publico"', 3, "sector Especial -> Publico (JSON)")
troca(r'<td>Especial</td>', '<td>Publico</td>', 3, "celula Especial -> Publico")

# card do setor: funde Especial em Publico e remove o card proprio
troca(r'<div class="card"><h3 style="margin-top:0">Publico</h3><p class="mut"([^>]*)>4 sessões · 124 evidências</p>',
      r'<div class="card"><h3 style="margin-top:0">Publico</h3><p class="mut"\1>7 sessões · 226 evidências</p>',
      1, "card Publico recalculado")
troca(r'<div class="card"><h3 style="margin-top:0">Especial</h3><p class="mut"[^>]*>3 sessões · 102 evidências</p></div>',
      '', 1, "card Especial removido")

# 2. rotulo institucional generalizado ao nivel do orgao
troca(r'Direção de órgão ambiental municipal', 'Órgão ambiental municipal', 2,
      "ENT-008: direcao -> orgao")
troca(r'Liderança política do Executivo municipal', 'Gabinete do Executivo municipal', 2,
      "ENT-015: lideranca -> gabinete")

# 3. frases de risco suprimidas das notas — por frase, nao por nota inteira
troca(r'Nível de direção; risco residual de reidentificação', '', 1, "nota ENT-008")
troca(r'Sessão com assessoria; risco residual de reidentificação', '', 1, "nota ENT-015")
troca(r',? ?no nível de direção máxima', '', 1, "parafrase: nivel de direcao maxima")
troca(r',? ?no nível de direção', '', 1, "parafrase: nivel de direcao")

# 4. TCLE — NAO alterado.
#
# A coordenacao comunicou em 09/09/2026 que ha termo assinado para as 17 sessoes.
# A conferencia do acervo em A:\ nao sustenta isso: a pasta Termos Entrevistas\
# Assinados traz 18 PDFs, e neles NAO estao ENT-009, ENT-012, ENT-014 e ENT-016 —
# exatamente as quatro sessoes marcadas "tcle": false no codebook.
#
# Ausencia de evidencia e resultado, nao falha: enquanto os arquivos assinados nao
# forem localizados e conferidos, o painel continua dizendo o que o acervo mostra.
# Trocar a marca aqui produziria uma pagina publica afirmando algo que o projeto
# nao consegue demonstrar — e as marcas «SESSÃO SEM TCLE» seguem gravadas em 40+
# parafrases de evidencia, o que deixaria a pagina em contradicao consigo mesma.

open(SAIDA, "w", encoding="utf-8").write(h)
print(f"{SAIDA}: {len(h)//1024} KB")
for rot, n in aplicadas:
    print(f"  {n:3d}  {rot}")
