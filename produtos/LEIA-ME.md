# Produtos gerados

Os arquivos desta pasta são **derivados**, não fonte. Saem de contagem sobre
`codebook/` e do texto do Produto 04, e são reproduzíveis por comando. Editar um
deles à mão é trabalho perdido na próxima geração — a correção vai no codebook ou
na ferramenta.

| Arquivo | Como regerar |
|---|---|
| `P4_matriz_v2.md` | `python -m tools.p4_base` alimenta a tabela; ver a ferramenta |
| `P4_ancoras_secao3.csv` | `python -m tools.p4_ancorar --docx "Produto 4.docx" --csv produtos/P4_ancoras_secao3.csv` |

## P4_matriz_v2.md

A Matriz de Avaliação atualizada que o TdR exige (Produto 1, §2.2). Todos os
números saem de `tools/p4_base.py`.

O rótulo de maturidade de cada subcategoria é a **moda** da distribuição de
evidências. Não é a média nem a mediana, e a diferença não é cosmética: a escala
é ordinal e a distribuição é bimodal em oito das treze subcategorias. A 1.2 tem
28 evidências em «inexistente» e 18 em «em_implementacao»; a média cai em 1,54 e
produziria «Formalizado», estágio que apenas 2 das 52 evidências sustentam.

A coluna *perfil* declara essa forma. Ela é o achado, não um detalhe estatístico:
duas concentrações afastadas na escala não descrevem um estágio intermediário,
descrevem condição que existe numa frente e não existe noutra.

## P4_ancoras_secao3.csv

Âncoras **candidatas** para as 93 afirmações da Seção 3, três por afirmação, com
sessão, dimensão e marca de tempo. O TdR pede repositório auditável, com origem e
trecho; a Seção 3 hoje é narrativa corrida, sem uma única referência.

Estas âncoras não estão validadas. Sobreposição léxica acha candidato, não prova
que a evidência sustenta a afirmação — a aceitação de cada uma é humana. A coluna
`score` ordena, não decide: 34 afirmações têm candidato forte (≥0,30), 51 médio e
8 fracas, que precisam de leitura antes de virar citação.
