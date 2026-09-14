# -*- coding: utf-8 -*-
"""Relacao de pontos focais, cifrada, para poder ser versionada.

    $env:PAINEL_SENHA = "..."
    python -m tools.contatos_cifrados

## O problema que isto resolve, e o que NAO resolve

`data/contacts.json` tem 24 pontos focais com nome, organizacao, cargo, e-mail e
telefone. Ele saiu do versionamento em 12/09 e esta no `.gitignore` desde entao.

Pedir «commita o arquivo e poe uma senha para abrir» tem duas leituras, e so uma
funciona. Commitar o JSON em claro e acrescentar uma tela de senha nao protege
nada: o dado esta no arquivo, e qualquer um que clone o repositorio ou abra o
codigo-fonte da pagina o le sem tocar na tela. Uma tela de senha sobre dado em
claro e enfeite.

O que funciona e o que esta feito aqui: o dado e **cifrado** antes de ser
gravado, com o mesmo mecanismo que `tools/lock.py` ja usa no painel, AES-256-GCM
com chave derivada por PBKDF2-HMAC-SHA256 e 250 mil iteracoes. O arquivo
versionado e texto cifrado; sem a senha ele nao contem os contatos, nem no
codigo-fonte nem no cache do navegador. O JSON em claro continua fora do git.

## Os limites, declarados

1. **A forca disto e a forca da senha.** Quem tiver o arquivo pode tentar senhas
   offline. As 250 mil iteracoes encarecem a tentativa, nao a impedem. Uma senha
   formada pelo nome do projeto mais o ano e adivinhavel por quem conhece o
   projeto, que e exatamente o publico de quem teria o arquivo.
2. **Cifrar agora nao apaga o passado.** O JSON em claro esta no historico de
   `aikiesan/Projeto_Maringa` e continua alcancavel por SHA. Isto protege o
   arquivo daqui para a frente e nao desfaz a exposicao anterior.
3. **Sao dados pessoais de terceiros.** Os 24 nao consentiram em publicacao;
   consentiram em participar. Este arquivo e instrumento de trabalho da equipe,
   nao material de divulgacao.

A senha vem de `PAINEL_SENHA` no ambiente ou de `.senha` na raiz, os dois fora
do git. Ela nunca e gravada neste arquivo nem no arquivo gerado.
"""
from __future__ import annotations

import html as H
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

ORIGEM = ROOT / "data" / "contacts.json"
DESTINO = ROOT / "data" / "contatos.html"

COLUNAS = (("code", "Código"), ("name", "Nome"), ("organization", "Organização"),
           ("acronym", "Sigla"), ("role", "Cargo"), ("email", "E-mail"),
           ("phone", "Telefone"), ("group_type", "Grupo"),
           ("contact_status", "Situação"))

# Tokens minimos da marca. A pagina e autonoma de proposito: ela nao carrega o
# `hub.css`, porque nao pertence ao Hub e nao deve ser servida junto com ele.
ESTILO = """
:root{--petroleo:#0F4C5C; --verde:#4E9F3D; --grafite:#4A4A4A; --linha:#E9ECEF;
  --paper:#ffffff; --surface:#ffffff; --line:#E9ECEF; --ink:#222; --mut:#666}
*{box-sizing:border-box}
body{margin:0; font:15px/1.5 "Segoe UI",system-ui,-apple-system,sans-serif;
  color:var(--ink); background:var(--paper)}
header{background:var(--petroleo); color:#fff; padding:22px 26px}
header .kicker{margin:0 0 4px; font-size:11.5px; letter-spacing:.11em;
  text-transform:uppercase; color:#7bc66c; font-weight:680}
header h1{margin:0; font-size:22px; font-weight:700}
main{padding:26px; max-width:1180px; margin:0 auto}
p.nota{color:var(--mut); font-size:13.5px; max-width:78ch}
table{border-collapse:collapse; width:100%; font-size:13.5px; margin-top:16px}
th,td{border:1px solid var(--linha); padding:7px 9px; text-align:left;
  vertical-align:top}
th{background:var(--petroleo); color:#fff; font-weight:650; font-size:12.5px}
tr:nth-child(even) td{background:#fafbfc}
.tw{overflow-x:auto}
"""


def _tabela(contatos) -> str:
    cab = "".join(f"<th>{H.escape(r)}</th>" for _, r in COLUNAS)
    linhas = []
    for c in sorted(contatos, key=lambda x: str(x.get("code") or "")):
        tds = "".join(f"<td>{H.escape(str(c.get(k) or ''))}</td>" for k, _ in COLUNAS)
        linhas.append(f"<tr>{tds}</tr>")
    return (f'<div class="tw"><table><thead><tr>{cab}</tr></thead>'
            f'<tbody>{"".join(linhas)}</tbody></table></div>')


def _pagina(dados) -> str:
    contatos = dados["contacts"]
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow, noarchive">
<title>Pontos focais · uso interno</title>
<style>{ESTILO}</style>
</head>
<body>
<header>
  <p class="kicker">IPPLAM × CEPAL · Maringá em Ação pelo Clima</p>
  <h1>Pontos focais do projeto</h1>
</header>
<main>
  <p class="nota"><strong>Uso interno.</strong> {len(contatos)} pontos focais, com
  nome, organização, cargo e contato. Os titulares consentiram em participar da
  consultoria, não em ter seus contatos divulgados. Não republique este conteúdo,
  não o cole em mensagem e não o anexe a material de divulgação.</p>
  {_tabela(contatos)}
</main>
</body>
</html>"""


def gerar(origem: Path = ORIGEM, destino: Path = DESTINO) -> dict:
    from tools import lock

    senha = lock.senha_configurada(ROOT)
    if not senha:
        raise SystemExit(
            "senha não configurada. Defina PAINEL_SENHA no ambiente ou crie o "
            "arquivo .senha na raiz, que está fora do git. Gravar a relação sem "
            "cifra seria pior do que não gravar.")
    if not origem.exists():
        raise SystemExit(f"{origem} não encontrado. Ele fica fora do git.")

    dados = json.loads(origem.read_text(encoding="utf-8"))
    pagina = _pagina(dados)
    trancada = lock.trancar(pagina, senha)

    # Trava: o texto cifrado não pode conter nenhum dado em claro. Sem esta
    # conferência, um erro no corte de `trancar` publicaria a tabela inteira e
    # o sintoma seria invisível, porque a tela de senha apareceria do mesmo jeito.
    amostra = []
    for c in dados["contacts"]:
        for campo in ("name", "email", "phone"):
            v = str(c.get(campo) or "").strip()
            if v and v in trancada:
                amostra.append(f"{campo}={v[:28]}")
    if amostra:
        raise SystemExit(
            "o arquivo cifrado ainda contém dado em claro: "
            + "; ".join(amostra[:6])
            + ". Nada foi gravado.")

    destino.write_text(trancada, encoding="utf-8")
    return {"contatos": len(dados["contacts"]), "destino": destino,
            "bytes": destino.stat().st_size, "iteracoes": lock.ITERACOES,
            "senha_chars": len(senha)}


def main() -> int:
    r = gerar()
    print(f"{r['destino'].relative_to(ROOT)}")
    print(f"  {r['contatos']} pontos focais, cifrados em AES-256-GCM")
    print(f"  chave por PBKDF2-HMAC-SHA256, {r['iteracoes']:,} iterações"
          .replace(",", "."))
    print(f"  {r['bytes'] // 1024} KB · nenhum dado em claro no arquivo")
    print(f"  senha de {r['senha_chars']} caracteres, não gravada em lugar nenhum")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
