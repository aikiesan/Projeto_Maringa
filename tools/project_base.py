"""
Seções da base do projeto (Produto 3) no painel: produtos, mapeamento de
organizações, COMDEMA, matriz de evidência documental e pontos focais.

Lê `data/*.json` — a base que já estava versionada — e devolve o HTML e o JS a
serem injetados no painel por `tools.build_site`.

ATENÇÃO: a seção de pontos focais expõe nome, e-mail e telefone. A página só
deve ser servida atrás de autenticação (Cloudflare Access) ou aberta localmente.
"""

from __future__ import annotations

import json
from pathlib import Path

FILES = ["overview", "organizations", "comdema", "contacts"]


def load(base: Path) -> dict:
    out = {}
    for name in FILES:
        p = base / f"{name}.json"
        if p.exists():
            out[name] = json.loads(p.read_text(encoding="utf-8"))
    return out


HTML = """
<section>
  <p class="eyebrow">Base do projeto · Produto 3</p>
  <div class="col">
    <h2>Onde a consultoria está</h2>
    <p>As seções acima tratam do que as entrevistas dizem. Estas tratam do
    aparato que as sustenta: os produtos contratados, o mapeamento institucional
    que definiu quem seria ouvido, a composição do conselho ambiental e a matriz
    documental que triangula a evidência de entrevista.</p>
  </div>
  <div class="two" id="produtos"></div>
</section>

<section>
  <p class="eyebrow">Mapeamento institucional</p>
  <div class="col">
    <h2>Trinta e quatro organizações, quatro dimensões</h2>
    <p>Cada organização foi vinculada a uma dimensão CCFLA principal — é o
    mapeamento que define de quem se espera evidência sobre o quê. Comparar esta
    tabela com a matriz de cobertura acima é o modo direto de ver quais fontes
    previstas ainda não foram ouvidas.</p>
  </div>
  <div class="controls" id="orgfilter"><span class="lbl">Grupo</span></div>
  <div class="scroll">
    <table id="orgs">
      <thead><tr>
        <th>Código</th><th>Organização</th><th>Sigla</th><th>Esfera</th>
        <th>Grupo</th><th>Dimensão principal</th><th>Contato</th>
      </tr></thead>
      <tbody></tbody>
      <caption id="orgscap"></caption>
    </table>
  </div>
</section>

<section>
  <p class="eyebrow">COMDEMA</p>
  <div class="col">
    <h2>Seis anos de composição do conselho</h2>
    <p>Sistematização dos atos de nomeação de 2021 a 2026. A coluna que interessa
    ao diagnóstico é a última: quem atravessou os seis anos. Continuidade de
    conselheiro é uma das poucas medidas objetivas de memória institucional
    disponíveis — e a dimensão <span class="c">4.2.3</span> depende dela.</p>
  </div>
  <div class="scroll">
    <table id="comdemayears">
      <thead><tr><th>Ano</th><th class="n">Total</th><th class="n">Público</th>
      <th class="n">Privado</th><th class="n">Academia</th>
      <th class="n">Sociedade civil</th></tr></thead>
      <tbody></tbody>
    </table>
  </div>
  <div class="controls" id="comfilter"><span class="lbl">Representação</span></div>
  <div class="scroll">
    <table id="comdema">
      <thead><tr><th>Conselheiro</th><th>Representação</th><th>Vínculo</th>
      <th>Anos</th><th>Seis anos</th></tr></thead>
      <tbody></tbody>
      <caption id="comdemacap"></caption>
    </table>
  </div>
</section>

<section>
  <p class="eyebrow">Evidência documental</p>
  <div class="col">
    <h2>A Matriz 2, e o que ela ainda deve</h2>
    <p>Documentos que confirmam, qualificam ou contradizem a evidência de
    entrevista. É por aqui que as dimensões sem fonte oral podem ser sustentadas —
    <span class="c">2.2.2</span> e <span class="c">2.2.3</span> saem de PPA, LDO,
    LOA e relatórios de execução, não de conversa.</p>
  </div>
  <div class="scroll">
    <table id="docs">
      <thead><tr><th>Código</th><th>Documento</th><th>Categoria</th>
      <th>Tipo</th><th>Órgão</th><th>Situação</th></tr></thead>
      <tbody></tbody>
    </table>
  </div>
</section>

<section>
  <p class="eyebrow">Pontos focais · uso interno</p>
  <div class="col">
    <h2>Quem responde por cada organização</h2>
  </div>
  <div class="note alert">
    <h3>Esta seção não pode ser aberta</h3>
    <p>Abaixo há nome, cargo, e-mail e telefone de pontos focais. Vários deles são
    as mesmas pessoas que aparecem no corpus como <span class="c">ENT-0xx</span> —
    cruzar as duas tabelas reidentifica entrevistado. Esta página deve ser servida
    apenas atrás de autenticação ou aberta localmente; não a publique sem
    controle de acesso, e não a encaminhe por e-mail.</p>
  </div>
  <div class="controls" id="ctfilter"><span class="lbl">Situação</span></div>
  <div class="scroll">
    <table id="contacts">
      <thead><tr><th>Código</th><th>Ponto focal</th><th>Organização</th>
      <th>Função</th><th>E-mail</th><th>Telefone</th><th>Situação</th></tr></thead>
      <tbody></tbody>
      <caption id="contactscap"></caption>
    </table>
  </div>
</section>
"""


JS = r"""
/* ================= base do projeto (Produto 3) ================= */
const PB = JSON.parse(document.getElementById("pb").textContent);
const GRP = ["Público", "Privado", "Academia", "Sociedade Civil"];
const GRPVAR = {"Público":"--s1","Privado":"--s2","Academia":"--s3","Sociedade Civil":"--s4"};
const grpVar = g => GRPVAR[g] || (g && g.indexOf("Público") === 0 ? "--s1" : "--muted");

/* ---- produtos ---- */
(function () {
  const st = { "CONCLUÍDO": "ok", "EM FINALIZAÇÃO": "ok", "PRÓXIMO PASSO": "no", "PLANEJADO": "no" };
  const pill = { "CONCLUÍDO": "acc", "EM FINALIZAÇÃO": "warn", "PRÓXIMO PASSO": "crit", "PLANEJADO": "neu" };
  document.getElementById("produtos").innerHTML =
    (PB.overview?.project_products || []).map(p => `
      <div class="card ${st[p.status] || "ok"}">
        <div class="t">${esc(p.phase)} · <span class="pill ${pill[p.status] || "neu"}">${esc(p.status)}</span></div>
        <p style="margin:0 0 6px;font-weight:700;font-size:.95rem">${esc(p.name)}</p>
        <p style="margin:0;font-size:13px;color:var(--muted)">${esc(p.desc)}</p>
      </div>`).join("");
})();

/* ---- organizações ---- */
(function () {
  const orgs = PB.organizations?.organizations || [];
  let sel = new Set(GRP);
  const box = document.getElementById("orgfilter");
  const btns = GRP.map(g => {
    const b = document.createElement("button");
    b.className = "chip"; b.type = "button"; b.setAttribute("aria-pressed", "true");
    b.innerHTML = `<i class="dot" style="background:var(${grpVar(g)})"></i>${g}`;
    b.onclick = () => {
      if (sel.has(g)) sel.delete(g); else sel.add(g);
      if (!sel.size) sel = new Set(GRP);
      btns.forEach((x, k) => x.setAttribute("aria-pressed", sel.has(GRP[k]) ? "true" : "false"));
      render();
    };
    box.appendChild(b); return b;
  });
  function render() {
    const rows = orgs.filter(o => [...sel].some(g => (o.group_type || "").indexOf(g) >= 0));
    document.querySelector("#orgs tbody").innerHTML = rows.map(o => `
      <tr>
        <td class="mono">${esc(o.code)}</td>
        <td>${esc(o.name)}</td>
        <td class="mono">${esc(o.acronym || "—")}</td>
        <td>${esc(o.sphere || "—")}</td>
        <td><span class="sw" style="background:var(${grpVar(o.group_type)})"></span>${esc(o.group_type)}</td>
        <td>${esc((o.ccfla_main || "").split("–")[0].trim() || "—")}<br>
            <span style="font-size:11.5px;color:var(--muted)">${esc((o.ccfla_main || "").split("–").slice(1).join("–").trim())}</span></td>
        <td>${(o.contact_status || "").toUpperCase().indexOf("CONFIRMADO") >= 0
              ? '<span class="pill acc">Confirmado</span>'
              : `<span class="pill neu">${esc(o.contact_status || "—")}</span>`}</td>
      </tr>`).join("");
    document.getElementById("orgscap").textContent =
      `${rows.length} de ${orgs.length} organizações. Dimensão principal conforme o mapeamento do Produto 3.`;
  }
  render();
})();

/* ---- COMDEMA ---- */
(function () {
  const ys = PB.comdema?.yearly_stats || [];
  const max = Math.max(1, ...ys.map(y => y.total));
  document.querySelector("#comdemayears tbody").innerHTML = ys.map(y => `
    <tr>
      <td class="mono">${y.year}</td>
      <td class="n"><b>${y.total}</b>
        <span style="display:inline-block;vertical-align:middle;margin-left:8px;width:70px;height:9px;background:var(--surface-3);border-radius:2px">
          <i style="display:block;height:100%;width:${Math.round(100 * y.total / max)}%;background:var(--accent);border-radius:2px"></i></span></td>
      <td class="n">${y.public_count}</td><td class="n">${y.private_count}</td>
      <td class="n">${y.academia_count}</td><td class="n">${y.soc_civil_count}</td>
    </tr>`).join("");

  const ms = PB.comdema?.members || [];
  const core = ms.filter(m => m.is_six_years);
  let only6 = false, sel = new Set(GRP);
  const box = document.getElementById("comfilter");
  const btns = GRP.map(g => {
    const b = document.createElement("button");
    b.className = "chip"; b.type = "button"; b.setAttribute("aria-pressed", "true");
    b.innerHTML = `<i class="dot" style="background:var(${grpVar(g)})"></i>${g}`;
    b.onclick = () => {
      if (sel.has(g)) sel.delete(g); else sel.add(g);
      if (!sel.size) sel = new Set(GRP);
      sync(); render();
    };
    box.appendChild(b); return b;
  });
  const b6 = document.createElement("button");
  b6.className = "chip"; b6.type = "button"; b6.style.marginLeft = "8px";
  b6.textContent = `Só os seis anos (${core.length})`;
  b6.setAttribute("aria-pressed", "false");
  b6.onclick = () => { only6 = !only6; sync(); render(); };
  box.appendChild(b6);
  function sync() {
    btns.forEach((x, k) => x.setAttribute("aria-pressed", sel.has(GRP[k]) ? "true" : "false"));
    b6.setAttribute("aria-pressed", only6 ? "true" : "false");
  }
  function render() {
    const rows = ms.filter(m => (!only6 || m.is_six_years)
      && [...sel].some(g => (m.group_represented || "").indexOf(g) >= 0));
    document.querySelector("#comdema tbody").innerHTML = rows.map(m => `
      <tr>
        <td>${esc(m.name)}</td>
        <td><span class="sw" style="background:var(${grpVar(m.group_represented)})"></span>${esc(m.group_represented)}</td>
        <td>${esc(m.affiliation || "—")}</td>
        <td class="mono" style="font-size:11px">${esc(m.years_present || "")}</td>
        <td>${m.is_six_years ? '<span class="pill acc">6 anos</span>' : ""}</td>
      </tr>`).join("");
    document.getElementById("comdemacap").textContent =
      `${rows.length} de ${ms.length} registros de conselheiro. ${core.length} atravessaram os seis anos — `
      + `a fração do conselho que carrega memória institucional entre gestões.`;
  }
  render();
})();

/* ---- matriz documental ---- */
(function () {
  const ds = PB.overview?.doc_evidence_matrix || [];
  document.querySelector("#docs tbody").innerHTML = ds.map(d => {
    const done = (d.status || "").toLowerCase().indexOf("analisado") >= 0
              || (d.status || "").toLowerCase().indexOf("sistematizado") >= 0;
    const partial = (d.status || "").toLowerCase().indexOf("análise") >= 0;
    return `<tr>
      <td class="mono">${esc(d.code)}</td><td>${esc(d.name)}</td>
      <td>${esc(d.category)}</td><td>${esc(d.type)}</td><td>${esc(d.org)}</td>
      <td><span class="pill ${done ? "acc" : partial ? "warn" : "neu"}">${esc(d.status)}</span></td>
    </tr>`;
  }).join("");
})();

/* ---- pontos focais ---- */
(function () {
  const cs = PB.contacts?.contacts || [];
  let onlyConf = false;
  const box = document.getElementById("ctfilter");
  const b = document.createElement("button");
  b.className = "chip"; b.type = "button"; b.setAttribute("aria-pressed", "false");
  b.textContent = "Só confirmados";
  b.onclick = () => { onlyConf = !onlyConf; b.setAttribute("aria-pressed", onlyConf ? "true" : "false"); render(); };
  box.appendChild(b);
  function render() {
    const rows = cs.filter(c => !onlyConf || (c.contact_status || "").toUpperCase().indexOf("CONFIRMADO") >= 0);
    document.querySelector("#contacts tbody").innerHTML = rows.map(c => `
      <tr>
        <td class="mono">${esc(c.code)}</td>
        <td>${esc(c.name)}</td>
        <td>${esc(c.organization)}${c.acronym ? ` <span class="mono" style="color:var(--muted)">${esc(c.acronym)}</span>` : ""}</td>
        <td>${esc(c.role || "—")}</td>
        <td class="mono" style="font-size:11.5px">${esc(c.email || "—")}</td>
        <td class="mono" style="font-size:11.5px">${esc(c.phone || "—")}</td>
        <td>${(c.contact_status || "").toUpperCase().indexOf("CONFIRMADO") >= 0
              ? '<span class="pill acc">Confirmado</span>'
              : `<span class="pill neu">${esc(c.contact_status || "—")}</span>`}</td>
      </tr>`).join("");
    document.getElementById("contactscap").textContent =
      `${rows.length} de ${cs.length} pontos focais. Dado de contato institucional — uso restrito à equipe da consultoria.`;
  }
  render();
})();
"""
