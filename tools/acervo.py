# -*- coding: utf-8 -*-
"""Acesso ao acervo de transcricoes anonimizadas.

Quem precisa das 17 transcricoes nao e so o Hub: a ferramenta que gera o anexo
de entrega (`tools/transcricoes_entrega.py`) e a medicao de autoidentificacao
(`tools/hub/retencao.py`) leem o mesmo material. A regra de onde ele vem, e a
garantia de que nao fica copia solta no disco, e regra de acervo e nao de
apresentacao, entao mora aqui.

O acervo nunca entra no git. Este modulo nao escreve nada.
"""
from __future__ import annotations

import contextlib
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ANON = ROOT / "saida_anonimizacao"
ANON_ZIP = ROOT / "anexos" / "Anexo_05_Transcricoes_Anonimizadas.zip"

SUFIXO = "_Transcricao_anonimizada.docx"


@contextlib.contextmanager
def fonte_transcricoes():
    """Diretorio com os .docx anonimizados.

    Prefere `saida_anonimizacao/` quando existe (a saida corrente de
    `anonimizar_transcricoes.py`); senao extrai o Anexo 05 para um diretorio
    temporario que e apagado no fim — o acervo nao deve deixar copia solta.

    Devolve None quando nao ha nem um nem outro, e cabe a quem chama decidir se
    isso e aviso ou falha dura.
    """
    if ANON.is_dir() and any(ANON.glob("*.docx")):
        yield ANON
        return
    if ANON_ZIP.exists():
        with tempfile.TemporaryDirectory(prefix="hub_transc_") as td:
            with zipfile.ZipFile(ANON_ZIP) as z:
                z.extractall(td)
            yield Path(td)
        return
    yield None


def codigo(caminho) -> str:
    """Codigo da sessao a partir do nome do arquivo: ENT-013_Transcricao… → ENT-013."""
    return Path(caminho).name.replace(SUFIXO, "").replace(".docx", "")
