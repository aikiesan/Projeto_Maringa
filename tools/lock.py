"""
Cifra a página publicada com uma senha.

O painel vai ao ar como **texto cifrado**. O que o servidor entrega é o cabeçalho,
o CSS e uma tela de senha; todo o conteúdo — corpus, evidências, contatos, base do
Produto 3 e o próprio código que renderiza — está dentro de um bloco AES-256-GCM.
A chave é derivada no navegador por PBKDF2-HMAC-SHA256 sobre a senha, com sal
aleatório. Sem a senha, não há dado no arquivo: nem no código-fonte, nem no cache.

Isso é diferente de esconder a tabela com JavaScript, que não protege nada.

A senha vem de `PAINEL_SENHA` no ambiente ou do arquivo `.senha` na raiz (fora do
git). Mínimo de 12 caracteres.

    $env:PAINEL_SENHA = "sua senha longa aqui"
    python -m tools.build_site

Limite honesto: a força disso é a força da senha. Quem baixar o arquivo pode
tentar senhas offline; as 250 mil iterações tornam isso caro, não impossível.
Use algo longo — quatro ou cinco palavras aleatórias valem mais que doze
caracteres embaralhados — e combine-a por um canal diferente do que leva o link.
"""

from __future__ import annotations

import base64
import os
from pathlib import Path

ITERACOES = 250_000
MIN_SENHA = 12


def senha_configurada(root: Path) -> str | None:
    senha = os.environ.get("PAINEL_SENHA", "").strip()
    if not senha:
        arq = root / ".senha"
        if arq.exists():
            senha = arq.read_text(encoding="utf-8").strip()
    if not senha:
        return None
    if len(senha) < MIN_SENHA:
        raise SystemExit(f"lock: a senha precisa de ao menos {MIN_SENHA} caracteres "
                         f"(tem {len(senha)})")
    return senha


def cifrar(texto: str, senha: str) -> dict:
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

    salt, iv = os.urandom(16), os.urandom(12)
    chave = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt,
                       iterations=ITERACOES).derive(senha.encode("utf-8"))
    ct = AESGCM(chave).encrypt(iv, texto.encode("utf-8"), None)
    b64 = lambda x: base64.b64encode(x).decode()  # noqa: E731
    return {"salt": b64(salt), "iv": b64(iv), "ct": b64(ct), "iter": ITERACOES}


TELA = """
<div id="lock">
  <form id="lockform" autocomplete="off">
    <p class="kicker">IPPLAM × CEPAL · Painel interno</p>
    <h1>Conteúdo protegido</h1>
    <p class="sub">Esta página contém registros de entrevista coletados sob termo de
    consentimento e dados de contato da equipe do projeto. O conteúdo está cifrado:
    sem a senha, ele não existe neste arquivo.</p>
    <label for="pw">Senha</label>
    <input id="pw" type="password" autocomplete="current-password" autofocus
           placeholder="senha do painel" spellcheck="false">
    <button type="submit" id="go">Abrir painel</button>
    <p id="msg" role="status" aria-live="polite"></p>
  </form>
</div>
<div id="app" hidden></div>

<style>
#lock{min-height:100vh;display:grid;place-items:center;padding:24px;background:var(--paper)}
#lockform{max-width:46ch;width:100%;background:var(--surface);border:1px solid var(--line);
  border-left:3px solid var(--accent);padding:30px 32px;box-shadow:var(--shadow)}
#lockform h1{font-size:1.5rem;margin:0 0 12px}
#lockform .sub{font-size:14px;color:var(--muted);margin:0 0 22px;line-height:1.55}
#lockform label{display:block;font-family:var(--mono);font-size:10.5px;letter-spacing:.12em;
  text-transform:uppercase;color:var(--muted);margin-bottom:6px}
#pw{width:100%;font:15px var(--mono);padding:11px 13px;border:1px solid var(--line-strong);
  border-radius:3px;background:var(--paper);color:var(--ink)}
#pw:focus{outline:2px solid var(--accent);outline-offset:1px}
#go{margin-top:14px;width:100%;font:600 14px var(--sans);padding:11px;cursor:pointer;
  border:1px solid var(--accent);border-radius:3px;background:var(--accent);color:#fff}
#go:hover{filter:brightness(1.08)}
#go[disabled]{opacity:.6;cursor:progress}
#msg{margin:12px 0 0;font-size:13px;min-height:1.2em;color:var(--crit-ink,#a52c2c)}
#msg.ok{color:var(--muted)}
</style>

<script>
(function () {
  "use strict";
  const BLOB = JSON.parse(document.getElementById("locked").textContent);
  const b = s => Uint8Array.from(atob(s), c => c.charCodeAt(0));
  const form = document.getElementById("lockform");
  const msg = document.getElementById("msg");
  const go = document.getElementById("go");

  async function abrir(senha) {
    const km = await crypto.subtle.importKey("raw", new TextEncoder().encode(senha),
      "PBKDF2", false, ["deriveKey"]);
    const key = await crypto.subtle.deriveKey(
      { name: "PBKDF2", salt: b(BLOB.salt), iterations: BLOB.iter, hash: "SHA-256" },
      km, { name: "AES-GCM", length: 256 }, false, ["decrypt"]);
    const plano = await crypto.subtle.decrypt(
      { name: "AES-GCM", iv: b(BLOB.iv) }, key, b(BLOB.ct));
    return new TextDecoder().decode(plano);
  }

  function montar(html) {
    const app = document.getElementById("app");
    app.innerHTML = html;
    // innerHTML não executa <script>: recolhe todos e avalia numa única closure,
    // para que as funções declaradas em um sejam visíveis no seguinte.
    const codigo = [...app.querySelectorAll("script:not([type])")].map(s => s.textContent);
    document.getElementById("lock").remove();
    app.hidden = false;
    new Function(codigo.join("\\n;\\n"))();
  }

  form.addEventListener("submit", async e => {
    e.preventDefault();
    const senha = document.getElementById("pw").value;
    if (!senha) return;
    go.disabled = true;
    msg.className = "ok";
    msg.textContent = "Derivando a chave…";
    try {
      const html = await abrir(senha);
      msg.textContent = "Abrindo…";
      montar(html);
    } catch (err) {
      go.disabled = false;
      msg.className = "";
      msg.textContent = "Senha incorreta.";
      document.getElementById("pw").select();
    }
  });
})();
</script>
"""


def trancar(html: str, senha: str) -> str:
    """Devolve a página com tudo depois do CSS substituído por um bloco cifrado."""
    # O documento tem mais de um bloco <style>: o reset do cabeçalho e o tema.
    # O corte é no ÚLTIMO </style> antes do conteúdo, para que a tela de senha
    # herde as variáveis de cor, tipografia e sombra do tema.
    marco = html.find("<header")
    if marco < 0:
        marco = len(html)
    corte = html.rfind("</style>", 0, marco)
    if corte < 0:
        raise SystemExit("lock: não encontrei o fim do bloco de estilo")
    corte += len("</style>")
    cabeca, corpo = html[:corte], html[corte:]

    fim = corpo.rfind("</body>")
    rodape = corpo[fim:] if fim >= 0 else ""
    corpo = corpo[:fim] if fim >= 0 else corpo

    import json
    blob = cifrar(corpo, senha)
    return (cabeca
            + '\n<script type="application/json" id="locked">'
            + json.dumps(blob) + "</script>\n"
            + TELA + rodape)
