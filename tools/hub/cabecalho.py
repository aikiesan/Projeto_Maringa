# -*- coding: utf-8 -*-
"""O cabeçalho do Hub: uma implementação só, usada por todas as páginas.

Existe por uma razão concreta. O painel de evidências não é gerado como as
outras páginas: ele é corpo de Artifact, com folha de estilo própria que já
define `.top` e `.wrap` para outra coisa, e não carrega o `hub.css`. Quando a
navegação foi acrescentada a ele, virou uma segunda barra, parecida mas não
igual: cores fixas em vez de tokens, sem botão de tema, sem link de pulo. Quem
navegasse entre as páginas via a barra mudar de comportamento no meio do
caminho, e no modo escuro o painel ficava com cabeçalho claro.

Aqui a marcação e o CSS são produzidos por **uma função só** e entregues por
dois caminhos: as páginas do Hub recebem o CSS no `hub.css`, e o painel recebe
o mesmo bloco embutido, junto com os tokens de cor de que ele precisa por não
carregar a folha comum. Mudar o cabeçalho passa a ser mudar um arquivo.

As classes são `hubbar*` justamente para não colidirem com o `.top` e o `.wrap`
que o painel já tem.
"""
from __future__ import annotations

ALTURA_REF = 58      # altura tipica; o valor real e medido em tempo de execucao


def marcacao(arquivo: str, nav) -> str:
    """Markup do cabeçalho. `arquivo` marca o item corrente."""
    itens = "".join(
        '<a href="' + h + '"'
        + (' aria-current="page"' if h == arquivo else "")
        + ">" + r + "</a>"
        for h, r in nav)
    return (
        '<a class="pular" href="#conteudo">Pular para o conteúdo</a>'
        '<header class="hubbar"><div class="hubbar-in">'
        '<a class="hubbar-marca" href="index.html">'
        '<img class="marca-clara" src="marca/projeto.png"'
        ' alt="Maringá em Ação pelo Clima">'
        '<img class="marca-escura" src="marca/projeto-branco.png" alt="">'
        "</a>"
        '<nav class="hubbar-menu" aria-label="Navegação do Hub">' + itens + "</nav>"
        '<button class="hubbar-tema" type="button" id="tema"'
        ' aria-label="Alternar tema claro e escuro"'
        ' title="Alternar tema claro e escuro">'
        '<span aria-hidden="true">◐</span></button>'
        "</div></header>")


CSS = """
/* ---- cabeçalho: uma implementação para todas as páginas ------------- */
.pular{position:absolute; left:-9999px; top:0; z-index:99; padding:10px 16px;
  background:var(--floresta); color:var(--sobre-marca); border-radius:0 0 8px 0}
.pular:focus{left:0}
.hubbar{position:sticky; top:0; z-index:60; background:var(--surface);
  border-bottom:2px solid var(--grid); box-shadow:0 1px 0 var(--ring);
  backdrop-filter:saturate(1.6) blur(8px)}
.hubbar-in{max-width:var(--max); margin:0 auto; padding:9px 22px;
  display:flex; gap:16px; align-items:center}
.hubbar-marca{display:flex; align-items:center; text-decoration:none;
  flex:0 0 auto}
.hubbar-marca img{height:34px; width:auto; display:block}
/* Duas imagens, uma visível por vez. A marca do projeto é colorida sobre claro
   e branca sobre escuro; um filtro CSS não daria conta, porque o símbolo tem
   três cores e inverter todas destruiria a marca. */
.hubbar-marca .marca-escura{display:none}
@media (prefers-color-scheme:dark){
  :root:not([data-theme="light"]) .hubbar-marca .marca-clara{display:none}
  :root:not([data-theme="light"]) .hubbar-marca .marca-escura{display:block}
}
:root[data-theme="dark"] .hubbar-marca .marca-clara{display:none}
:root[data-theme="dark"] .hubbar-marca .marca-escura{display:block}
:root[data-theme="light"] .hubbar-marca .marca-clara{display:block}
:root[data-theme="light"] .hubbar-marca .marca-escura{display:none}
/* O menu tem de PARECER um controle, não um rodapé de texto: trilho com fundo
   e contorno, e o item corrente preenchido com a cor da marca. */
.hubbar-menu{display:flex; flex-wrap:wrap; gap:2px; margin-left:auto;
  padding:3px; background:var(--plane); border:1px solid var(--grid);
  border-radius:11px; max-width:100%}
.hubbar-menu a{flex:0 0 auto; text-decoration:none; color:var(--ink2);
  font-size:13.5px; font-weight:560; padding:7px 13px; border-radius:8px;
  white-space:nowrap; transition:background .12s, color .12s}
.hubbar-menu a:hover{background:var(--realce); color:var(--floresta)}
.hubbar-menu a[aria-current="page"]{background:var(--floresta);
  color:var(--sobre-marca); font-weight:700}
.hubbar-menu a[aria-current="page"]:hover{background:var(--floresta-2)}
.hubbar-tema{flex:0 0 auto; font:inherit; font-size:15px; line-height:1;
  cursor:pointer; background:transparent; color:var(--ink2);
  border:1px solid var(--grid); border-radius:8px; padding:7px 10px}
.hubbar-tema:hover{background:var(--realce); color:var(--ink)}
:focus-visible{outline:2px solid var(--s1); outline-offset:2px}
/* Em tela estreita, oito itens em várias fileiras comeriam meia tela. Vira uma
   fileira que rola, com a barra de rolagem escondida porque ela sozinha custava
   23px de altura do cabeçalho. */
@media (max-width:760px){
  .hubbar-in{padding:8px 14px; gap:10px}
  .hubbar-marca img{height:28px}
  .hubbar-menu{flex-wrap:nowrap; overflow-x:auto; scrollbar-width:none;
    -webkit-overflow-scrolling:touch}
  .hubbar-menu::-webkit-scrollbar{display:none}
}
@media print{.hubbar,.pular{display:none!important}}
"""


# Lido antes da primeira pintura, senão a página pisca clara e vira escura.
# Em try/catch porque o acesso ao localStorage pode lançar: janela privada,
# dados de site bloqueados, captura de miniatura.
JS_PRE = (
    "<script>(function(){try{var t=localStorage.getItem('tema');"
    "if(t==='claro'||t==='escuro')document.documentElement.setAttribute("
    "'data-theme',t==='claro'?'light':'dark');}catch(e){}})();</" "script>")

# O toggle de tema e a medicao da altura da barra. A altura muda com a largura
# da tela, e quem precisa do deslocamento (as abas do painel, que sao sticky em
# top:0) le `--hubbar-h`. Chutar um valor fixo erra em algum tamanho, e o
# sintoma, aba escondida atras da barra, so aparece rolando.
JS_POS = (
    "<script>(function(){"
    "var b=document.getElementById('tema');"
    "var raiz=document.documentElement;"
    "function atual(){var t=raiz.getAttribute('data-theme');"
    "return t||(matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light');}"
    "function rotula(){if(b)b.setAttribute('aria-pressed',"
    "atual()==='dark'?'true':'false');}"
    "rotula();"
    "if(b)b.addEventListener('click',function(){"
    "var novo=atual()==='dark'?'light':'dark';"
    "raiz.setAttribute('data-theme',novo);"
    "try{localStorage.setItem('tema',novo==='dark'?'escuro':'claro');}catch(e){}"
    "rotula();});"
    "function medir(){var h=document.querySelector('.hubbar');if(!h)return;"
    "raiz.style.setProperty('--hubbar-h',"
    "Math.round(h.getBoundingClientRect().height)+'px');}"
    "addEventListener('resize',medir);medir();"
    "})();</" "script>")
