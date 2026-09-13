# -*- coding: utf-8 -*-
"""Casca comum do Hub: CSS, cabeçalho, rodapé e componentes de gráfico.

Identidade visual do projeto — família verde do material de apresentação
(verde-floresta #255438, verde-menta #33DD9A) e a marca de onda da Brisa.

As cores dos GRÁFICOS são outra coisa: saem da paleta categórica validada, com
o verde na primeira posição para casar com a marca. A ordem
#1baf7a · #eb6834 · #2a78d6 · #eda100 passou em todos os gates do validador nos
modos claro e escuro (pior par adjacente ΔE 9.2 protan/deutan, 27.6 visão
normal). Não troque uma cor de série por uma cor de marca sem revalidar.
"""

import cabecalho as CAB

NAV = [
    ("index.html", "Início"),
    ("projeto.html", "O projeto"),
    ("produto4.html", "Produto 04"),
    ("painel.html", "Painel de evidências"),
    ("instituicoes.html", "Instituições"),
    ("transcricoes.html", "Transcrições"),
]

CSS = """
:root{
  color-scheme: light;
  --plane:#eef0f2; --surface:#ffffff; --realce:#e4eef0;
  --ink:#1c1c1c; --ink2:#4a4a4a; --mut:#6d7075;
  --grid:#dfe3e6; --axis:#c2c8cd; --ring:rgba(11,11,11,.10);

  /* marca do projeto «Maringá em Ação pelo Clima».
     Azul petróleo e verde médio vêm do manual de identidade; os tons -2 são
     escurecimentos para estado ativo. NÃO confundir com as cores de série dos
     gráficos, logo abaixo: cor de marca e cor de dado são coisas diferentes,
     e as de série foram validadas separadamente. */
  --floresta:#0f4c5c; --floresta-2:#0a3542; --menta:#4e9f3d;
  /* clareado do verde da marca, para texto sobre o petróleo: o verde
     médio puro da paleta rende 2.88 de contraste ali, abaixo de
     qualquer piso. Mesmo matiz, só mais claro. */
  --menta-clara:#7bc66c;
  --link:#0f4c5c; --sobre-marca:#ffffff;
  --num:#0f4c5c;            /* números de destaque, sobre plano claro */
  --logo:none;              /* filtro do wordmark preto */

  /* séries — paleta validada, verde na primeira posição */
  --s1:#1baf7a; --s2:#eb6834; --s3:#2a78d6; --s4:#eda100;
  --good:#0ca30c; --warn:#fab219; --crit:#d03b3b;
  --max:1140px;
}
@media (prefers-color-scheme:dark){
  :root:not([data-theme="light"]){
    color-scheme: dark;
    --plane:#0d1114; --surface:#161b1f; --realce:#12303a;
    --ink:#fff; --ink2:#c3ccd2; --mut:#8d979e;
    --grid:#2a3238; --axis:#3b454c; --ring:rgba(255,255,255,.10);
    --floresta:#0f3d4a; --floresta-2:#0a2b35; --menta:#4e9f3d;
    --menta-clara:#7bc66c; --link:#7bc66c; --num:#7bc66c; --logo:invert(1);
    --s1:#199e70; --s2:#d95926; --s3:#3987e5; --s4:#c98500;
  }
}
:root[data-theme="dark"]{
  color-scheme: dark;
  --plane:#0d1114; --surface:#161b1f; --realce:#12303a;
  --ink:#fff; --ink2:#c3ccd2; --mut:#8d979e;
  --grid:#2a3238; --axis:#3b454c; --ring:rgba(255,255,255,.10);
  --floresta:#0f3d4a; --floresta-2:#0a2b35; --menta:#4e9f3d;
  --menta-clara:#7bc66c; --link:#7bc66c; --num:#7bc66c; --logo:invert(1);
  --s1:#199e70; --s2:#d95926; --s3:#3987e5; --s4:#c98500;
}

*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%; scroll-behavior:smooth}
body{
  margin:0; background:var(--plane); color:var(--ink);
  font:15px/1.62 system-ui,-apple-system,"Segoe UI",sans-serif;
}
.wrap{max-width:var(--max); margin:0 auto; padding-inline:20px}
a{color:var(--link); text-underline-offset:2px}
a:hover{color:var(--ink)}
img{max-width:100%}

/* ---- cabeçalho ---- */
header.top .wrap{display:flex; align-items:center; gap:16px; flex-wrap:wrap;
  padding-block:11px}
.marca{display:flex; align-items:center; gap:10px; text-decoration:none;
  color:var(--ink); white-space:nowrap}
.marca img{height:19px; width:auto; display:block; filter:var(--logo)}
.marca b{font-weight:650; font-size:14.5px; letter-spacing:-.012em}
.marca i{font-style:normal; color:var(--mut); font-weight:400}
/* ---- hero ---- */
.hero-faixa{
  background:linear-gradient(158deg,var(--floresta) 0%,var(--floresta-2) 100%);
  color:var(--sobre-marca); position:relative; overflow:hidden;
  border-bottom:3px solid var(--menta);
}
.hero-faixa::after{
  content:""; position:absolute; right:-60px; bottom:-40px; width:540px; height:286px;
  background:url(marca/onda.png) right bottom/contain no-repeat;
  opacity:.16; pointer-events:none;
}
.hero-faixa .wrap{padding-block:56px 48px; position:relative; z-index:1}
.hero-faixa .selo{
  display:inline-block; font-size:11.5px; letter-spacing:.11em; text-transform:uppercase;
  color:var(--menta-clara); font-weight:680; margin-bottom:16px;
}
.hero-faixa h1{color:var(--sobre-marca); margin-bottom:18px; max-width:20ch}
.hero-faixa .lede{color:rgba(255,255,255,.84); max-width:62ch; margin-bottom:0}
.hero-faixa .lede strong{color:var(--sobre-marca); font-weight:600}

.faixa-kpi{background:var(--surface); border-bottom:1px solid var(--grid)}
.faixa-kpi .wrap{display:grid; gap:0;
  grid-template-columns:repeat(auto-fit,minmax(168px,1fr))}
.faixa-kpi div{padding:22px 22px 20px; border-left:1px solid var(--grid)}
.faixa-kpi div:first-child{border-left:0; padding-left:0}
.faixa-kpi b{display:block; font-size:clamp(28px,4.3vw,38px); line-height:1;
  letter-spacing:-.032em; font-weight:660; margin-bottom:6px; color:var(--num)}
.faixa-kpi span{display:block; font-size:12.5px; color:var(--ink2); line-height:1.4}

/* ---- tipografia ---- */
h1{font-size:clamp(28px,4.6vw,44px); line-height:1.1; letter-spacing:-.026em;
   margin:0 0 14px; font-weight:670}
h2{font-size:clamp(20px,2.8vw,26px); line-height:1.22; letter-spacing:-.017em;
   margin:52px 0 14px; font-weight:650; padding-top:14px;
   border-top:1px solid var(--grid)}
h2:first-child{border-top:0; padding-top:0; margin-top:0}
h3{font-size:16.5px; letter-spacing:-.008em; margin:30px 0 8px; font-weight:640}
p{margin:0 0 14px; max-width:74ch}
.lede{font-size:clamp(16px,2.1vw,18.5px); line-height:1.55; color:var(--ink2);
  max-width:70ch; margin-bottom:24px}
.mut{color:var(--mut)}
small,.sm{font-size:13px}
main{padding-block:36px 68px}
main.wrap > h1:first-child{margin-top:8px}

/* ---- cartões ---- */
.grade{display:grid; gap:14px; margin:22px 0}
.g2{grid-template-columns:repeat(auto-fit,minmax(290px,1fr))}
.g3{grid-template-columns:repeat(auto-fit,minmax(232px,1fr))}
.g4{grid-template-columns:repeat(auto-fit,minmax(180px,1fr))}
.card{
  background:var(--surface); border:1px solid var(--ring); border-radius:13px;
  padding:19px 19px 17px;
}
.card h3{margin-top:0}
.card p:last-child{margin-bottom:0}
a.card{text-decoration:none; color:inherit; display:block;
  transition:border-color .13s, transform .13s, box-shadow .13s}
a.card:hover{border-color:var(--menta); transform:translateY(-2px);
  box-shadow:0 6px 22px rgba(37,84,56,.10)}
a.card .seta{color:var(--link); font-weight:640; margin-top:10px}
a.card h3{display:flex; align-items:baseline; gap:9px}
a.card h3::before{content:""; width:7px; height:7px; border-radius:2px;
  background:var(--menta); flex:none; transform:translateY(-2px)}

.kpi b{display:block; font-size:clamp(27px,4.6vw,36px); line-height:1.05;
  letter-spacing:-.03em; font-weight:660; margin-bottom:5px}
.kpi span{display:block; font-size:13px; color:var(--ink2); line-height:1.35}

/* ---- destaque numérico ---- */
.destaque{background:var(--realce); border-radius:14px; padding:26px 26px 22px;
  margin:26px 0; border:1px solid var(--ring)}
.destaque .n{font-size:clamp(44px,8vw,68px); line-height:.96; font-weight:670;
  letter-spacing:-.04em; color:var(--num); margin:0 0 8px}
.destaque p{margin:0; max-width:62ch}

/* ---- tabelas ---- */
.tw{overflow-x:auto; margin:18px 0; border:1px solid var(--ring); border-radius:13px;
  background:var(--surface)}
table{border-collapse:collapse; width:100%; font-size:13.5px}
th,td{text-align:left; padding:10px 14px; border-bottom:1px solid var(--grid);
  vertical-align:top}
th{font-weight:630; color:var(--ink2); font-size:12.5px; letter-spacing:.012em;
  position:sticky; top:0; background:var(--surface); z-index:1}
tbody tr:last-child td{border-bottom:0}
tbody tr:hover td{background:var(--realce)}
td.num,th.num{text-align:right; font-variant-numeric:tabular-nums; white-space:nowrap}
code{font:12.5px/1.5 ui-monospace,SFMono-Regular,Menlo,monospace;
  background:var(--realce); padding:1px 5px; border-radius:5px}

.pill{display:inline-block; font-size:11.5px; font-weight:620; padding:2px 9px;
  border-radius:999px; background:var(--realce); color:var(--ink2);
  border:1px solid var(--ring); white-space:nowrap}

/* ---- gráficos ---- */
figure{margin:22px 0 28px}
figcaption{font-size:13px; color:var(--ink2); margin-top:11px; max-width:72ch}
.legenda{display:flex; gap:18px; flex-wrap:wrap; margin:0 0 13px; font-size:12.5px;
  color:var(--ink2); list-style:none; padding:0}
.legenda li{display:flex; align-items:center; gap:7px}
.chip{width:11px; height:11px; border-radius:3px; flex:none}

.barras{display:grid; gap:7px; margin:4px 0 0}
.barra{display:grid; grid-template-columns:minmax(92px,auto) 1fr auto; gap:12px;
  align-items:center; font-size:13px}
.barra .rot{color:var(--ink2)}
.barra .trilho{background:var(--grid); border-radius:4px; height:16px; overflow:hidden}
.barra .fill{display:block; height:100%; border-radius:4px; background:var(--s1);
  min-width:3px}
.barra .val{font-variant-numeric:tabular-nums; color:var(--ink2); min-width:34px;
  text-align:right; font-weight:600}



.empilhada{display:grid; gap:9px}
/* ---- figuras descritivas ------------------------------------------- */
.fig{margin:22px 0 0; padding:0}
.fig-t{font-size:15px; margin:0 0 10px; font-weight:700}
.fig .leg{font-size:13px; color:var(--ink2); margin:9px 0 0; max-width:68ch}
.barra .frac{color:var(--mut); font-weight:400; margin-left:5px; font-size:12px}
.numeros{margin:9px 0 0; font-size:13px}
.numeros>summary{cursor:pointer; color:var(--ink2); width:max-content;
  padding:3px 2px; border-radius:4px}
.numeros>summary.numeros table{border-collapse:collapse; margin:8px 0 0; font-size:13px}
.numeros th,.numeros td{border-bottom:1px solid var(--grid); padding:5px 12px 5px 0;
  text-align:left}
.numeros td.n,.numeros th:last-child{text-align:right; font-variant-numeric:tabular-nums}
.rolo{overflow-x:auto}
.multiplos{display:grid; grid-template-columns:repeat(auto-fit,minmax(258px,1fr));
  gap:18px 26px; margin:4px 0 0}
.mult-cel h4{font-size:13.5px; margin:0 0 7px; font-weight:700}
.mult-cel h4 .mut{color:var(--mut); font-weight:400}
/* folga de 2px entre segmentos: separa as marcas sem inventar uma cor de borda */
.empilhada .pilha i+i{box-shadow:-2px 0 0 var(--plane)}

.linha-ano{display:grid; grid-template-columns:52px 1fr 44px; gap:12px;
  align-items:center}
.linha-ano .ano{font-size:13px; color:var(--ink2); font-variant-numeric:tabular-nums}
.pilha{display:flex; height:24px; border-radius:4px; overflow:hidden; gap:2px}
.pilha i{font-style:normal; font-size:11px; font-weight:640; color:#fff;
  display:flex; align-items:center; justify-content:center; min-width:0;
  overflow:hidden}
.linha-ano .tot{font-size:12.5px; color:var(--mut); text-align:right;
  font-variant-numeric:tabular-nums}

/* ---- avisos ---- */
.nota{border-left:3px solid var(--menta); background:var(--surface);
  padding:15px 17px; border-radius:0 11px 11px 0; margin:22px 0; font-size:14px;
  box-shadow:inset 0 0 0 1px var(--ring)}
.nota p:last-child{margin-bottom:0}
.nota strong{font-weight:640}

/* ---- rodapé ---- */
footer.pe{border-top:1px solid var(--grid); margin-top:60px; padding-block:30px 44px;
  font-size:13px; color:var(--ink2); background:var(--surface)}
footer.pe p{max-width:76ch}
.logos{display:flex; align-items:center; gap:26px; flex-wrap:wrap;
  margin:0 0 20px; padding-bottom:20px; border-bottom:1px solid var(--grid)}
.logos img{height:30px; width:auto; display:block}
.logos img.brisa{height:24px; filter:var(--logo)}
.logos .txt{font-size:12px; color:var(--mut); line-height:1.35; max-width:16ch}

/* ---- busca ---- */
.busca{display:flex; gap:10px; flex-wrap:wrap; margin:18px 0 4px; align-items:center}
.busca input,.busca select{
  font:14px system-ui,-apple-system,sans-serif; padding:9px 12px;
  border:1px solid var(--axis); border-radius:9px; background:var(--surface);
  color:var(--ink); min-width:0;
}
.busca input{flex:1 1 230px}
.busca input:focus,.busca select:focus{outline:2px solid var(--menta);
  outline-offset:1px; border-color:transparent}
.conta{font-size:12.5px; color:var(--mut); margin:11px 0 0}

/* ---- transcrições ---- */
.turno{display:grid; grid-template-columns:138px 1fr; gap:14px; padding:8px 0;
  border-bottom:1px solid var(--grid); align-items:start}
.turno:last-child{border-bottom:0}
.turno .quem{font-size:12.5px; font-weight:620; color:var(--ink2); padding-top:2px}
.turno .quem.e{color:var(--s2)}
.turno .txt{max-width:72ch}
.marca-t{font-variant-numeric:tabular-nums; font-size:12px; color:var(--mut);
  margin:26px 0 4px; letter-spacing:.02em; padding-top:6px;
  border-top:1px dashed var(--grid)}
.corte{color:var(--mut); font-style:italic}

@media (max-width:700px){
  nav  .faixa-kpi div{border-left:0; border-top:1px solid var(--grid); padding-inline:0}
  .faixa-kpi div:first-child{border-top:0}
  .hero-faixa::after{width:300px; height:160px; opacity:.12}
  .barra{grid-template-columns:minmax(74px,auto) 1fr auto}
  .linha-ano{grid-template-columns:42px 1fr 38px}
  .turno{grid-template-columns:1fr; gap:1px; padding:10px 0}
  .turno .quem{padding-top:0}
}
/* ==== Produto 04 ==================================================== */

.p4-kpi{display:grid; grid-template-columns:repeat(auto-fit,minmax(150px,1fr));
  gap:1px; background:var(--grid); border:1px solid var(--grid);
  border-radius:10px; overflow:hidden; margin:0 0 22px}
.p4-kpi>div{background:var(--surface); padding:14px 16px; display:flex;
  flex-direction:column; gap:2px}
.p4-kpi b{font-size:26px; line-height:1.05; font-variant-numeric:tabular-nums}
.p4-kpi span{font-size:12.5px; color:var(--ink2)}

.p4-baixar{margin:0 0 26px; padding:12px 14px; border:1px solid var(--grid);
  border-left:3px solid var(--s2); border-radius:8px; background:var(--surface)}

/* --- duas colunas: sumario fixo + documento --- */
.p4{display:grid; grid-template-columns:250px minmax(0,1fr); gap:34px;
  align-items:start}
.p4-sum{position:sticky; top:72px; max-height:calc(100vh - 96px);
  overflow-y:auto; font-size:13px}
.p4-sum>details{border:1px solid var(--grid); border-radius:8px;
  background:var(--surface); padding:10px 12px}
.p4-sum>details>summary{cursor:pointer; font-weight:700; padding:2px 0}
.p4-sum>details>summary.sumario ul{list-style:none; margin:8px 0 0; padding:0}
.sumario ul ul{margin:2px 0 6px 0}
.sumario a{display:block; padding:3px 6px; border-radius:5px; color:var(--ink2);
  text-decoration:none; line-height:1.35}
.sumario a:hover{background:var(--grid); color:var(--ink)}
.sumario a.aqui{background:var(--s1); color:#fff}
.sumario .n1>a{font-weight:700; color:var(--ink); margin-top:5px}
.sumario .cn{display:inline-block; min-width:16px; color:var(--s1);
  font-variant-numeric:tabular-nums; font-weight:700}
.sumario .n1>a.aqui .cn{color:#fff}
.sumario li.n2 a{padding-left:20px; font-size:12.5px}
.sumario li.n3 a{padding-left:32px; font-size:12.5px; color:var(--mut)}

/* --- o documento --- */
.p4-doc{max-width:74ch}
.p4-doc section.cap{scroll-margin-top:78px; margin:0 0 42px}
.p4-doc h2{display:flex; gap:10px; align-items:baseline;
  border-bottom:2px solid var(--s1); padding-bottom:8px; margin:0 0 16px}
.p4-doc h2 .cn{color:var(--s1); font-variant-numeric:tabular-nums}
.p4-doc h3{margin:26px 0 9px; font-size:17px; scroll-margin-top:78px}
.p4-doc h4{margin:20px 0 7px; font-size:15px; color:var(--ink2);
  scroll-margin-top:78px}
.p4-doc p{margin:0 0 12px}
.p4-doc blockquote{margin:14px 0; padding:10px 16px; border-left:3px solid var(--grid);
  color:var(--ink2); font-size:14.5px; background:var(--surface)}
.p4-doc .quadro-leg{font-size:12.5px; color:var(--mut); margin:14px 0 6px;
  font-weight:700}
.p4-doc table.quadro{border-collapse:collapse; font-size:13px; min-width:100%}
.p4-doc table.quadro th,.p4-doc table.quadro td{border:1px solid var(--grid);
  padding:6px 9px; text-align:left; vertical-align:top}
.p4-doc table.quadro tr:first-child{background:var(--grid); font-weight:700}

.quadro-suprimido{margin:12px 0 18px; padding:12px 15px; border-radius:8px;
  border:1px dashed var(--grid); background:var(--surface)}
.quadro-suprimido p{margin:0; font-size:13.5px; color:var(--ink2)}

/* --- afirmacoes da Secao 3 --- */
.contador{margin:0 0 18px; padding:10px 14px; border-radius:8px;
  background:var(--surface); border:1px solid var(--grid); font-size:13.5px}
.contador button{font:inherit; font-size:13px; margin-left:8px; cursor:pointer;
  border:1px solid var(--grid); background:transparent; color:var(--ink);
  border-radius:6px; padding:3px 9px}
.contador button[aria-pressed=true]{background:var(--s1); color:#fff;
  border-color:var(--s1)}

ul.afs{list-style:none; margin:0 0 16px; padding:0; display:grid; gap:10px}
ul.afs>li{padding:0 0 0 34px; position:relative}
li.af{padding:10px 12px 10px 40px; border-radius:8px; background:var(--surface);
  border:1px solid var(--grid); scroll-margin-top:78px}
li.af .af-n{position:absolute; left:11px; top:11px; font-size:11.5px;
  color:var(--mut); font-variant-numeric:tabular-nums; font-weight:700}
li.af.com{border-left:3px solid var(--s1)}
li.af.sem{border-left:3px solid var(--grid)}
li.af:target{outline:2px solid var(--s1); outline-offset:2px}

.ancs{display:flex; flex-wrap:wrap; gap:6px; margin-top:9px}
a.anc{display:inline-flex; gap:7px; align-items:center; text-decoration:none;
  font-size:11.5px; padding:3px 9px; border-radius:999px;
  background:var(--s1); color:#fff}
a.anc:hover{filter:brightness(1.08)}
a.anc .anc-ts,a.anc .anc-dim{opacity:.82}
.sem-anc{display:inline-block; margin-top:9px; font-size:11.5px; padding:3px 9px;
  border-radius:999px; border:1px dashed var(--mut); color:var(--mut)}
.sem-anc.exemplo{margin:0}
.origem{display:inline-block; font-size:11px; padding:2px 8px; border-radius:999px;
  background:var(--realce); color:var(--ink2); border:1px solid var(--grid)}
li.af.origem-humano .origem{background:var(--s1); color:#fff; border-color:var(--s1)}
.p4-doc .nota .origem{margin:0 2px}

/* --- matriz de avaliacao --- */
table.matriz{border-collapse:collapse; font-size:13px; min-width:100%}
table.matriz th{text-align:left; border-bottom:2px solid var(--grid);
  padding:8px 11px 8px 0; font-size:12px; color:var(--ink2);
  text-transform:uppercase; letter-spacing:.03em; white-space:nowrap}
table.matriz td{border-bottom:1px solid var(--grid); padding:8px 11px 8px 0;
  vertical-align:top}
table.matriz td.n,table.matriz th.n{text-align:right;
  font-variant-numeric:tabular-nums; white-space:nowrap}
table.matriz td.perfil{font-size:12px; color:var(--ink2)}
.mini{display:inline-block; vertical-align:middle; width:42px; height:7px;
  background:var(--grid); border-radius:3px; margin-right:7px; overflow:hidden}
.mini i{display:block; height:100%; background:var(--s2); border-radius:3px}

@media (max-width:900px){
  .p4{grid-template-columns:1fr; gap:16px}
  .p4-sum{position:static; max-height:none}
  .p4-doc{max-width:none}
}
@media (max-width:520px){
  .p4-kpi b{font-size:22px}
  li.af{padding-left:34px}
}

/* --- impressao: o produto precisa sair em PDF legivel --- */
@media print{
  header.top,.p4-sum,.contador button,.numeros>summary,
  .menu,button.tema,.pular,footer.pe .logos{display:none!important}
  .numeros[open] table{display:table}
  body{background:#fff; color:#000}
  .p4{display:block}
  .p4-doc{max-width:none}
  .p4-doc section.cap{break-inside:auto}
  .p4-doc h2{break-before:page; break-after:avoid}
  .p4-doc section.cap:first-child h2{break-before:auto}
  .p4-doc h3,.p4-doc h4{break-after:avoid}
  li.af,blockquote,table,figure{break-inside:avoid}
  a.anc{background:none; color:#000; border:1px solid #000}
  a.anc::after{content:" (" attr(href) ")"; font-size:9px}
  .p4-kpi{border:1px solid #000}
}
""" + CAB.CSS


def pagina(arquivo, titulo, descricao, corpo, extra_js="", hero=""):
    """Monta uma pagina do Hub. `hero`, quando dado, e a faixa de abertura.

    O cabecalho vem de `cabecalho.py`, que e a MESMA implementacao usada pelo
    painel de evidencias. Duplicar aqui foi o erro anterior: a barra do painel
    ficou parecida mas nao igual, com cores fixas e sem botao de tema.
    """
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{titulo} · Maringá em Ação pelo Clima</title>
<meta name="description" content="{descricao}">
<meta property="og:title" content="{titulo} · Maringá em Ação pelo Clima">
<meta property="og:description" content="{descricao}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Maringá em Ação pelo Clima">
<meta property="og:image" content="marca/projeto.png">
<meta name="twitter:card" content="summary">
<link rel="icon" href="marca/projeto.png" type="image/png">
<link rel="stylesheet" href="hub.css">
{CAB.JS_PRE}
</head>
<body>
{CAB.marcacao(arquivo, NAV)}
{hero}
<main class="wrap" id="conteudo">
{corpo}
</main>
<footer class="pe"><div class="wrap">
  <div class="logos">
    <img class="brisa" src="marca/brisa.png" alt="Brisa Soluções Ambientais">
    <img src="marca/cepal.png" alt="CEPAL · Nações Unidas">
    <span class="txt">Instituto de Pesquisa e Planejamento Urbano de Maringá</span>
  </div>
  <p><strong>Projeto Maringá em Ação pelo Clima.</strong> Avaliação das condições
  habilitantes ao financiamento climático urbano, pela metodologia CCFLA/CEPAL
  <em>Assessing Subnational Enabling Framework Conditions for Urban Climate Finance</em>.
  Consultoria técnica de apoio ao projeto de assessoria entre o Instituto de Pesquisa
  e Planejamento Urbano de Maringá (IPPLAM) e a Comissão Econômica para a América
  Latina e o Caribe (CEPAL/ONU), executada pela Brisa Soluções Ambientais.</p>
  <p class="mut">As entrevistas são publicadas em camada anonimizada. Nomes de
  participantes, contatos e a instituição do próprio entrevistado não entram em
  nenhuma página deste Hub. A composição dos conselhos municipais é ato público e
  aparece nominalmente.</p>
</div></footer>

{CAB.JS_POS}
{extra_js}
</body>
</html>"""


def hero(selo, titulo, lede):
    return f"""<section class="hero-faixa"><div class="wrap">
  <span class="selo">{selo}</span>
  <h1>{titulo}</h1>
  <p class="lede">{lede}</p>
</div></section>"""


def faixa_kpi(itens):
    return ('<section class="faixa-kpi"><div class="wrap">'
            + "".join(f"<div><b>{v}</b><span>{r}</span></div>" for v, r in itens)
            + "</div></section>")


# ------------------------------------------------------------------ gráficos
def barras(itens, cor="var(--s1)", maximo=None, sufixo=""):
    m = maximo or max((v for _, v in itens), default=1) or 1
    linhas = []
    for rot, val in itens:
        pct = 100 * val / m
        linhas.append(
            f'<div class="barra"><span class="rot">{rot}</span>'
            f'<span class="trilho"><i class="fill" style="width:{pct:.1f}%;'
            f'background:{cor}"></i></span>'
            f'<span class="val">{val}{sufixo}</span></div>')
    return '<div class="barras">' + "".join(linhas) + "</div>"


def legenda(pares):
    li = "".join(f'<li><span class="chip" style="background:{c}"></span>{r}</li>'
                 for r, c in pares)
    return f'<ul class="legenda">{li}</ul>'


def empilhada(linhas, series):
    out = []
    for rot, vals in linhas:
        tot = sum(vals) or 1
        segs = []
        for (nome, cor), v in zip(series, vals):
            if not v:
                continue
            pct = 100 * v / tot
            txt = str(v) if pct >= 11 else ""
            segs.append(f'<i style="flex:0 0 {pct:.2f}%;background:{cor}" '
                        f'title="{nome}: {v}">{txt}</i>')
        out.append(f'<div class="linha-ano"><span class="ano">{rot}</span>'
                   f'<span class="pilha">{"".join(segs)}</span>'
                   f'<span class="tot">{sum(vals)}</span></div>')
    return '<div class="empilhada">' + "".join(out) + "</div>"
