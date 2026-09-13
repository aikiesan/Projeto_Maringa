# -*- coding: utf-8 -*-
"""A página «O projeto»: o que é a consultoria e sob que regras a evidência
foi produzida.

Página **descritiva**. Ela diz o que foi feito e sob que regra, não o que os
dados significam. Conclusão é do Produto 04, assinada, e é lá que ela deve ser
lida. Aqui não há tese: há procedimento.

Nenhum número é digitado: todos vêm das métricas e do `p4_base`.
"""
from __future__ import annotations

import html

E = html.escape


def render(m: dict, c: dict, orgs: list, leis: list, sub: list) -> str:
    bimodais = sum(1 for x in sub if x["perfil"] == "bimodal")
    divergentes = m["alinhamento"].get("divergente", 0)
    return f"""
<h2>A consultoria</h2>

<p>Este Hub e o material que ele abre pertencem a uma consultoria técnica
contratada pelo <strong>IPPLAM</strong> (Instituto de Pesquisa e Planejamento
Urbano de Maringá), no âmbito da cooperação com a <strong>CEPAL/ONU</strong>, e
executada pela Brisa Soluções Ambientais. O objeto são as <em>condições
habilitantes ao financiamento climático urbano</em> de Maringá.</p>

<p><strong>Condição habilitante</strong> é um termo técnico, e vale fixá-lo: não é
um projeto nem uma obra. É o arranjo que precisa existir <em>antes</em>, para que
o financiamento climático seja possível. Uma política com meta declarada. Um
orçamento que permita identificar o gasto climático. Um inventário de emissões.
Uma instância que coordene secretarias. A avaliação verifica, condição por
condição, se ela existe, em que estágio está, e com que evidência se pode afirmar
isso.</p>

<h2>A metodologia</h2>

<p>A referência é <em>Assessing Subnational Enabling Framework Conditions for
Urban Climate Finance</em> (CCFLA / Urban-Act, 2024), adaptada e priorizada para
Maringá no Produto 2 desta consultoria. Ela organiza
{m['dimensoes_total']} dimensões em quatro eixos (política climática; orçamento e
finanças; dados climáticos; coordenação vertical e horizontal), agrupadas em
{len(sub)} subcategorias.</p>

<div class="grade g2">
  <div class="card"><h3>{m['dimensoes_total']} dimensões</h3>
    <p class="sm">Cada uma é uma condição habilitante específica, com prioridade
    atribuída na adaptação para Maringá.</p></div>
  <div class="card"><h3>{len(sub)} subcategorias</h3>
    <p class="sm">O agrupamento entre eixo e dimensão. É neste nível que a Matriz
    de Avaliação do Produto 04 reporta.</p></div>
  <div class="card"><h3>{m['sessoes']} sessões</h3>
    <p class="sm">{m['participantes']} participantes, {m['horas']} de escuta,
    {m['turnos']:n} turnos de fala transcritos.</p></div>
  <div class="card"><h3>{m['evidencias']} evidências</h3>
    <p class="sm">Codificadas uma a uma a partir das transcrições, cada qual
    vinculada a exatamente uma dimensão.</p></div>
</div>

<h2>A unidade de registro</h2>

<p>A unidade não é a entrevista, nem a resposta a uma pergunta: é a
<strong>evidência</strong>. Uma evidência é um trecho anonimizado, com marca de
tempo, vinculado a uma dimensão e classificado por tipo, maturidade, alinhamento e
confiança. Um mesmo trecho pode gerar duas evidências, em dimensões diferentes.
A paráfrase é o juízo analítico de quem codificou, e é o que se cita; o trecho
fica como lastro, conferível na transcrição.</p>

<div class="grade g2">
  <div class="card"><h3>Maturidade</h3>
    <p class="sm">Em que estágio a condição está: inexistente, em elaboração,
    formalizado, regulamentado, em implementação, monitorado, efetivo. Há ainda
    <em>sem evidência</em>, que marca pendência de reinquirição e <strong>não</strong>
    se confunde com <em>inexistente</em>: a primeira diz que não se perguntou o
    bastante; a segunda, que se constatou a ausência.</p></div>
  <div class="card"><h3>Alinhamento</h3>
    <p class="sm">Convergente, complementar, isolada ou divergente, conforme o que
    as demais sessões dizem sobre o mesmo ponto.</p></div>
  <div class="card"><h3>Tipo</h3>
    <p class="sm">Declaração, percepção, lacuna, divergência, oportunidade ou
    documento indicado.</p></div>
  <div class="card"><h3>Confiança</h3>
    <p class="sm">Baixa quando o participante remete a outro órgão, quando a
    formulação partiu do entrevistador e foi apenas confirmada, ou quando o trecho
    é ambíguo.</p></div>
</div>

<h2>As regras declaradas</h2>

<div class="grade g2">
  <div class="card"><h3>Ausência de evidência é resultado</h3>
    <p class="sm">Uma dimensão que atravessa o corpus sem evidência é registrada
    como tal, não preenchida por inferência. {len(m['mudas'])} das
    {m['dimensoes_total']} dimensões não receberam evidência oral.</p></div>
  <div class="card"><h3>Divergência não se resolve</h3>
    <p class="sm">As {divergentes} evidências divergentes são preservadas como
    divergentes, nunca resolvidas por predominância de setor. São o material da
    validação participativa.</p></div>
  <div class="card"><h3>Tudo é derivado</h3>
    <p class="sm">Todo número destas páginas saiu de uma ferramenta que leu um
    arquivo versionado. Corrigir um número significa corrigir a fonte, nunca a
    página.</p></div>
  <div class="card"><h3>Moda, não média</h3>
    <p class="sm">A Matriz reporta a maturidade pela moda, isto é, o estágio mais
    registrado. Em {bimodais} das {len(sub)} subcategorias a distribuição é
    bimodal, e nessas a média apontaria um estágio intermediário que quase nenhuma
    evidência sustenta.</p></div>
</div>

<h2>O que a anonimização protege, e o que não protege</h2>

<p>As entrevistas foram concedidas sob termo de consentimento que garante
confidencialidade. Não aparecem em página alguma deste Hub: nome de participante
ou de entrevistador, cargo específico, a instituição nominal do próprio
entrevistado, contato ou qualquer identificador direto. Cada sessão é identificada
por código, setor e tipo institucional genérico.</p>

<p>Aparecem nominalmente, por serem informação pública: órgãos de fato
(SEMOP, IPPLAM, Defesa Civil), leis e instrumentos, contratos publicados,
concessionárias e órgãos estaduais.</p>

<div class="nota">
  <p><strong>Risco residual, declarado.</strong> Maringá tem um único órgão
  ambiental municipal: o rótulo genérico já identifica a instituição. A
  anonimização protege contra a leitura casual, não contra quem conhece a
  estrutura da prefeitura. Em três sessões o que identifica não é o nome, e sim o
  cargo; nelas os trechos autoidentificadores foram suprimidos e aparecem como
  <code>(&hellip;)</code>. Cada corte está registrado em relação própria, que não
  integra esta publicação.</p>
</div>

<div class="nota">
  <p><strong>Conselheiro é exceção declarada.</strong> A composição de conselho
  municipal é ato público, publicada em portaria. Por isso os
  {len(c['membros'])} conselheiros do COMDEMA aparecem nominalmente, mas apenas
  na página de conselhos. Em qualquer outra página, nome de conselheiro seria
  falha, e a varredura que precede cada publicação trata assim.</p>
</div>

<h2>Quem executa</h2>

<p><strong>Brisa Soluções Ambientais</strong>, para o <strong>IPPLAM</strong>, no
âmbito da cooperação com a <strong>CEPAL/ONU</strong>. A sistematização analítica
e a codificação do corpus foram conduzidas por Lucas Nakamura Cerejo, arquiteto e
urbanista, pós-doutorando no NIPE/CP2b da Unicamp.</p>
"""
