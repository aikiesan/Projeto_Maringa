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

# 2. rotulo institucional: nao ha mais o que generalizar.
#
# As duas trocas que suavizavam «Direção de órgão ambiental municipal» e
# «Liderança política do Executivo municipal» alcancavam o campo
# institution_type em dois lugares — o JSON e a celula da tabela do corpus.
# A coluna saiu de build_site.py e o campo sai do JSON logo abaixo, entao
# generalizar o rotulo antes de apaga-lo seria trabalho morto — e a trava de
# minimo deste script falharia, como deve falhar quando uma troca perde o
# objeto.

# tipo institucional fora da camada aberta.
#
# 13 dos 15 rotulos sao unicos de uma unica sessao: «Secretaria municipal de
# governo», «Banco publico de desenvolvimento regional», «Gabinete do Executivo
# municipal». A lista nominal de pessoas mobilizadas e entrevistadas e
# entregavel do termo de referencia; com ela ao lado, o rotulo deixa de ser
# generico e passa a funcionar como cracha, ligando pessoa a sessao e, por
# tabela, a cada trecho que ela disse. O setor permanece: sao quatro valores
# para 17 sessoes.
troca(r'"institution_type": "[^"]*", ', '', 17,
      "tipo institucional fora do JSON")
troca(r'\$\{esc\(i\.sector \|\| ""\)\} · \$\{esc\(i\.institution_type \|\| ""\)\}',
      '${esc(i.sector || "")}', 1,
      "tipo institucional fora do rodape do card")

# data da sessao fora da camada aberta.
#
# Mesma mecanica do cracha acima, por outro caminho. Agendas de gabinete, de
# diretoria e de conselho sao publicas: com a data ao lado do setor e da
# duracao, quem conhece a estrutura do municipio estreita a uma ou duas pessoas
# o conjunto de quem pode ter falado naquela manha. E a data nao responde nada
# sobre o conteudo — as 17 sessoes cabem numa janela de quatro semanas e nenhuma
# leitura do painel depende de saber em qual delas. Sai das duas superficies: o
# JSON embutido e a coluna da tabela do corpus. A pagina de transcricoes faz a
# mesma remocao, em tools/hub/transcricoes.py.
troca(r'"date": "\d{4}-\d{2}-\d{2}", ', '', 17, "data fora do JSON")
troca(r'(</span></td><td>[^<]*</td>)<td class="num">\d\d/\d\d</td>', r'\1', 17,
      "coluna Data fora da tabela do corpus")
troca(r'<th>Setor</th><th>Data</th>', '<th>Setor</th>', 1,
      "cabecalho Data fora da tabela do corpus")

# o rotulo tambem vaza pela nota de uma sessao, que e texto livre e escapa das
# regras acima porque nao esta no campo institution_type.
troca(r' ?Poder Legislativo municipal\.', '', 1,
      "rotulo na nota de sessao (ENT-012)")

# 3. frases de risco suprimidas das notas — por frase, nao por nota inteira
troca(r'Nível de direção; risco residual de reidentificação', '', 1, "nota ENT-008")
troca(r'Sessão com assessoria; risco residual de reidentificação', '', 1, "nota ENT-015")
troca(r',? ?no nível de direção máxima', '', 1, "parafrase: nivel de direcao maxima")
troca(r',? ?no nível de direção', '', 1, "parafrase: nivel de direcao")



# 4. TCLE — nada a sanear.
#
# As 17 sessoes tem Termo de Consentimento Livre e Esclarecido assinado e
# arquivado no acervo do projeto. A marcacao de pendencia que existia em
# ENT-009, ENT-012, ENT-014 e ENT-016 era artefato de organizacao de arquivos,
# ja sanado no codebook. Nao ha marca a remover na camada publica.

open(SAIDA, "w", encoding="utf-8").write(h)
print(f"{SAIDA}: {len(h)//1024} KB")
for rot, n in aplicadas:
    print(f"  {n:3d}  {rot}")
