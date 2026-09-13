# Procedência de `data/legislacao.json`

22 normas municipais que formam o arcabouço climático de Maringá.

**Fonte primária:** `DRIVE_FILES/pasta integra legislação/LIstagem atualizada da
legislação.docx`, a listagem consolidada entregue pelo município.

**Como este arquivo foi criado (13/09/2026):** reconstruído a partir de
`hub_saida/dados/legislacao.csv`, que era a saída já extraída da listagem. O
arquivo que o gerador lia antes — `/home/claude/hub_legislacao.json` — vivia
apenas na sandbox de uma sessão anterior e **nunca foi versionado**; era a única
fonte de `legislacao.html` e teria se perdido na primeira regeneração.

Campos: `norma`, `ano`, `ementa`.

Se a listagem municipal for atualizada, este arquivo é regerado a partir dela —
não editado à mão (regra 5.4).
