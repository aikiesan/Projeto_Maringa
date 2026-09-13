# -*- coding: utf-8 -*-
"""Pagina local de revisao das ancoras. Gerada por `tools.p4_revisao --pagina`.

Separada do nucleo de proposito: aqui so mora apresentacao. O CSV continua sendo
a fonte de verdade — esta pagina e uma forma comoda de preenche-lo, nao um
segundo lugar onde a decisao vive.

Nao vai para o `hub_saida/`: mostra a afirmacao ao lado do trecho e da parafrase,
material de trabalho interno.
"""
from __future__ import annotations

import json

CSS = """
*{box-sizing:border-box}
body{margin:0;font:15px/1.55 system-ui,-apple-system,Segoe UI,sans-serif;
  background:#f6f7f6;color:#17211b}
header.top{position:sticky;top:0;z-index:9;background:#255438;color:#fff;
  padding:13px 22px;display:flex;gap:16px;align-items:center;flex-wrap:wrap}
header.top h1{font-size:15.5px;margin:0;font-weight:700}
header.top .c{font-size:13px;opacity:.92;font-variant-numeric:tabular-nums}
button{font:inherit;padding:7px 13px;border-radius:6px;border:0;cursor:pointer;
  background:#33DD9A;color:#10261a;font-weight:700}
button.g{background:rgba(255,255,255,.17);color:#fff}
button[aria-pressed=true]{outline:2px solid #33DD9A}
main{max-width:1060px;margin:0 auto;padding:20px}
.intro{color:#5d6b63;font-size:13.5px;max-width:72ch}
.af{background:#fff;border:1px solid #dfe4e0;border-radius:10px;
  padding:15px 17px;margin:0 0 16px}
.af>header{display:flex;gap:12px;align-items:baseline;flex-wrap:wrap;
  font-size:12.5px;color:#5d6b63;margin-bottom:7px}
.num{font-weight:700;color:#255438}
.pior{margin-left:auto;font-variant-numeric:tabular-nums}
.afirm{margin:0 0 13px;font-size:15.5px}
.cands{display:grid;gap:7px}
.cand{display:block;border:1px solid #e3e8e4;border-radius:8px;padding:9px 11px;
  cursor:pointer;background:#fbfcfb}
.cand.sel{border-color:#1baf7a;background:#f0fbf6;box-shadow:inset 3px 0 0 #1baf7a}
.cand input{margin-right:7px}
.meta{display:flex;gap:9px;align-items:center;flex-wrap:wrap;font-size:12px}
.sc{font-variant-numeric:tabular-nums;background:#255438;color:#fff;
  padding:1px 7px;border-radius:4px}
.mono{font-family:ui-monospace,Menlo,Consolas,monospace}
.dim{color:#255438;font-weight:700}
.nm{color:#5d6b63}
.tag{background:#ecefed;padding:1px 7px;border-radius:4px;color:#4a574f}
.conf-baixa{background:#fde8dc;color:#8a3c12}
.par{margin:6px 0 0;font-size:13.5px}
.term{margin:4px 0 0;font-size:11.5px;color:#7d8a82;font-family:ui-monospace,monospace}
.nenhuma{background:#f4f5f4}
.nota{width:100%;margin-top:9px;padding:6px 9px;border:1px solid #dfe4e0;
  border-radius:6px;font:inherit;font-size:13px;resize:vertical}
.oculto{display:none}
"""

JS = """
const D = JSON.parse(document.getElementById("dados").textContent);
const esc = s => String(s == null ? "" : s).replace(/[&<>"]/g,
  c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const idDe = r => r.interview + "|" + r.dim + "|" + r.ts;

// estado inicial vindo do CSV: decisao ja gravada
const escolha = {}, notas = {}, tocada = {};
D.ordem.forEach(n => {
  const rs = D.porN[n];
  const ac = rs.find(r => r.decisao === "aceita");
  if (ac) { escolha[n] = idDe(ac); tocada[n] = true; }
  else if (rs.some(r => r.decisao === "rejeitada")) { escolha[n] = ""; tocada[n] = true; }
  else escolha[n] = undefined;
  const cn = rs.find(r => r.nota);
  if (cn) notas[n] = cn.nota;
});

function cand(n, r) {
  const sel = escolha[n] === idDe(r) ? " sel" : "";
  return `<label class="cand${sel}" data-id="${esc(idDe(r))}">
    <input type="radio" name="d${esc(n)}" value="${esc(idDe(r))}"
      ${escolha[n] === idDe(r) ? "checked" : ""}>
    <span class="meta"><b class="sc">${esc(r.score)}</b>
      <span class="mono">${esc(r.interview)}</span>
      <span class="mono">${esc(r.ts)}</span>
      <span class="mono dim">${esc(r.dim)}</span>
      <span class="nm">${esc(r.dim_nome)}</span>
      <span class="tag">${esc(r.maturity)}</span>
      <span class="tag conf-${esc(r.confidence)}">confianca ${esc(r.confidence)}</span>
    </span>
    <p class="par">${esc(r.paraphrase)}</p>
    <p class="term">${esc((r.termos || "").split("|").join(" \\u00b7 "))}</p></label>`;
}

function bloco(n) {
  const rs = D.porN[n], a = rs[0];
  const forca = Math.max(...rs.map(r => parseFloat(r.score) || 0));
  const nenhumaSel = escolha[n] === "" ? " sel" : "";
  return `<article class="af" id="af-${esc(n)}">
    <header><span class="num">#${esc(n)}</span>
      <span class="sec">${esc(a.setor)} &middot; ${esc(a.subsecao)}</span>
      <span class="pior">melhor score ${forca.toFixed(2)}</span></header>
    <p class="afirm">${esc(a.afirmacao)}</p>
    <div class="cands">${rs.map(r => cand(n, r)).join("")}
      <label class="cand nenhuma${nenhumaSel}" data-id="">
        <input type="radio" name="d${esc(n)}" value=""
          ${escolha[n] === "" ? "checked" : ""}>
        <span class="meta"><b>nenhuma sustenta esta afirmacao</b></span>
        <p class="par">A afirmacao fica sem link na pagina do Produto 4, com marca
        visivel e contada. Ausencia de evidencia e resultado.</p></label></div>
    <textarea class="nota" rows="1" placeholder="nota (opcional)"
      >${esc(notas[n] || "")}</textarea></article>`;
}

document.getElementById("lista").innerHTML = D.ordem.map(bloco).join("");

function conta() {
  const rev = D.ordem.filter(n => tocada[n]).length;
  const ac = D.ordem.filter(n => escolha[n]).length;
  document.getElementById("cont").textContent =
    rev + " de " + D.ordem.length + " revisadas \\u00b7 " + ac + " com ancora aceita \\u00b7 "
    + (D.ordem.length - ac) + " sem ancora";
}
conta();

document.getElementById("lista").addEventListener("change", ev => {
  const inp = ev.target.closest("input[type=radio]");
  if (!inp) return;
  const art = inp.closest(".af"), n = art.id.slice(3);
  escolha[n] = inp.value; tocada[n] = true;
  art.querySelectorAll(".cand").forEach(c =>
    c.classList.toggle("sel", c.dataset.id === inp.value));
  conta();
});
document.getElementById("lista").addEventListener("input", ev => {
  if (!ev.target.classList.contains("nota")) return;
  notas[ev.target.closest(".af").id.slice(3)] = ev.target.value;
});

let sofalta = false;
const bt = document.getElementById("fsem");
bt.onclick = () => {
  sofalta = !sofalta;
  bt.setAttribute("aria-pressed", sofalta ? "true" : "false");
  document.querySelectorAll(".af").forEach(a =>
    a.classList.toggle("oculto", sofalta && tocada[a.id.slice(3)]));
};

document.getElementById("exp").onclick = () => {
  const q = s => '"' + String(s == null ? "" : s).replace(/"/g, '""') + '"';
  const out = [D.cols.join(",")];
  D.linhas.forEach(r => {
    const n = r.n, e = escolha[n];
    const copia = Object.assign({}, r);
    if (e === undefined) { /* nao tocada: preserva o que veio do CSV */ }
    else if (e === idDe(r)) copia.decisao = "aceita";
    else copia.decisao = "rejeitada";
    copia.nota = notas[n] || "";
    out.push(D.cols.map(c => q(copia[c])).join(","));
  });
  const blob = new Blob(["\\ufeff" + out.join("\\r\\n")],
                        {type: "text/csv;charset=utf-8"});
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "P4_ancoras_revisao.csv";
  a.click();
  URL.revokeObjectURL(a.href);
};
"""


def render(linhas: list[dict], cols: list[str], resumo: dict) -> str:
    """HTML da pagina de revisao. `linhas` sao as do CSV de revisao, sem orfas."""
    por_n: dict[str, list[dict]] = {}
    for r in linhas:
        por_n.setdefault(r["n"], []).append(r)
    for rs in por_n.values():
        rs.sort(key=lambda r: -float(r["score"] or 0))

    def forca(n):
        return max((float(r["score"] or 0) for r in por_n[n]), default=0.0)

    # da mais fraca para a mais forte: as de cima exigem leitura, nao conferencia
    ordem = sorted(por_n, key=lambda n: (forca(n), int(n)))

    dados = json.dumps({"porN": por_n, "ordem": ordem, "cols": cols,
                        "linhas": linhas}, ensure_ascii=False)
    return f"""<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Revisao das ancoras &mdash; Produto 4</title>
<style>{CSS}</style></head><body>
<header class="top">
  <h1>Revisao das ancoras &mdash; Secao 3 do Produto 4</h1>
  <span class="c" id="cont"></span>
  <button class="g" id="fsem" type="button" aria-pressed="false">so as nao revisadas</button>
  <button id="exp" type="button">baixar CSV</button>
</header>
<main>
<p class="intro">As <b>{resumo['afirmacoes']}</b> afirmacoes da Secao 3, tres candidatas
cada, <b>ordenadas da mais fraca para a mais forte</b> &mdash; as de cima sao as que
precisam de leitura, nao de conferencia. Marque a candidata que de fato sustenta a
afirmacao, ou &laquo;nenhuma&raquo;. O score ordena, nao decide. Ao terminar, baixe o
CSV e salve por cima de <code>produtos/P4_ancoras_revisao.csv</code>.</p>
<div id="lista"></div>
</main>
<script id="dados" type="application/json">{dados}</script>
<script>{JS}</script>
</body></html>"""
