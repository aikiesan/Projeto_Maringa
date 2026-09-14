# -*- coding: utf-8 -*-
"""Extrai os ativos da marca a partir das pranchas do manual de identidade.

    python -m tools.extrair_marca

As pranchas sao slides 5334x3000 com a marca sobre fundo chapado, e em tres
delas sobre uma marca d'agua do mapa da cidade. O que o Hub precisa e a marca
recortada, com fundo transparente, em tres tratamentos.

## Por que nao basta tornar o branco transparente

A marca colorida tem branco DENTRO dela: a arvore vazada no bosque e o vinco da
catedral. Trocar todo branco por transparencia abriria buracos no desenho. O que
se remove e so o fundo, isto e, a regiao branca conectada a borda da imagem.
Por isso a mascara e feita por componentes conexos, e nao por cor.

Nas pranchas de fundo escuro e cinza a marca e chapada (branco puro, ou grafite
puro), e ali o caminho certo e o inverso: selecionar a cor da marca, o que
descarta a marca d'agua do mapa junto com o fundo.

## Proveniencia

Fonte: «MARINGA EM ACAO PELO CLIMA - LOGO ID/», pranchas 03, 07, 08 e 11. As
pranchas ficam fora do git por tamanho; os PNGs gerados entram em
`assets/marca/`, que e versionado, porque sao ativos de publicacao.
"""
from __future__ import annotations

import glob
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

PRANCHAS = ROOT.glob("MARING* EM A* PELO CLIMA - LOGO ID/*.png")
DESTINO = ROOT / "assets" / "marca"

MARGEM = 24          # respiro em volta do recorte, em pixels da prancha
LARGURA_MAX = 1600   # a marca nunca e exibida maior que isso na web


def _pranchas() -> dict:
    out = {}
    for f in sorted(glob.glob(str(ROOT / "MARING* EM A* PELO CLIMA - LOGO ID" / "*.png"))):
        out[Path(f).stem.split("-")[-1]] = f
    if not out:
        raise SystemExit(
            "pranchas da identidade nao encontradas. Elas ficam em "
            "«MARINGA EM ACAO PELO CLIMA - LOGO ID/», fora do git.")
    return out


def _achatar(im, fundo):
    """Compoe sobre o fundo solido antes de mascarar.

    As pranchas sao PNG indexado COM transparencia, e `convert("RGBA")` deixa os
    pixels transparentes com RGB preto. Preto dista 147 do petroleo da prancha
    08, acima do corte, e por isso a mascara lia metade do slide como se fosse
    marca. Achatar primeiro elimina a classe inteira de erro, e nao so o sintoma.
    """
    from PIL import Image
    base = Image.new("RGBA", im.size, tuple(fundo) + (255,))
    base.alpha_composite(im.convert("RGBA"))
    return base


def _sem_fundo_conexo(im, fundo=(255, 255, 255), tol=26):
    """Alpha 0 onde o fundo encosta na borda. Preserva o branco interno."""
    import numpy as np
    from scipy import ndimage
    a = np.array(_achatar(im, fundo))
    rgb = a[:, :, :3].astype(int)
    canto = rgb[0, 0]
    fundo = (np.abs(rgb - canto).sum(axis=2) <= tol)
    rotulos, _ = ndimage.label(fundo)
    borda = set(rotulos[0, :]) | set(rotulos[-1, :]) | \
        set(rotulos[:, 0]) | set(rotulos[:, -1])
    borda.discard(0)
    externo = np.isin(rotulos, list(borda))
    a[:, :, 3] = np.where(externo, 0, 255)
    from PIL import Image
    return Image.fromarray(a, "RGBA")


# Medido nas pranchas, nao estimado. id08: fundo (0,64,83), marca d'agua do mapa
# (15,75,93), marca (248,248,248). id11: fundo (223,225,226), marca d'agua
# (207,209,210), marca (66,66,66). Em soma de canais, a marca d'agua dista 36 e
# 48 do fundo, e a marca dista 597 e 476. Cortar entre 120 e 260 separa os tres
# com folga larga dos dois lados.
CORTE_BAIXO, CORTE_ALTO = 120, 260


def _chapar(im, fundo, cor):
    """Marca chapada em `cor`, com alpha pela distancia ao fundo da prancha.

    A primeira versao media a distancia ate a COR DA MARCA, e por isso os
    pixels da marca, que sao (248,248,248) e nao branco puro, saiam com alpha
    parcial: a marca inteira ficava lavada. O que separa marca de fundo e a
    distancia ao FUNDO, e e nela que o corte tem de ser feito.
    """
    import numpy as np
    from PIL import Image
    a = np.array(_achatar(im, fundo))
    d = np.abs(a[:, :, :3].astype(int) - np.array(fundo)).sum(axis=2)
    alpha = np.clip((d - CORTE_BAIXO) * 255 // (CORTE_ALTO - CORTE_BAIXO),
                    0, 255).astype("uint8")
    saida = np.zeros_like(a)
    saida[:, :, 0], saida[:, :, 1], saida[:, :, 2] = cor
    saida[:, :, 3] = alpha
    return Image.fromarray(saida, "RGBA")


def _corte_do_simbolo(im) -> int:
    """A coluna do vao entre o simbolo e o texto, achada na propria imagem.

    Cortar por uma fracao da largura e chute, e o chute de 30% cortava a marca
    ao meio. O vao e a primeira faixa de colunas totalmente transparentes depois
    que o simbolo termina.
    """
    import numpy as np
    a = np.array(im)[:, :, 3]
    ocupada = a.max(axis=0) > 8
    inicio = int(np.argmax(ocupada))
    vazio = 0
    for x in range(inicio, len(ocupada)):
        vazio = vazio + 1 if not ocupada[x] else 0
        if vazio >= 12:                      # vao real, nao folga entre glifos
            return x - vazio
    raise SystemExit("vao entre simbolo e texto nao encontrado")


def _sem_sujeira(im, minimo=0.002, checar_borda=True):
    """Descarta manchas soltas antes de medir a caixa.

    Na prancha 08 sobrevive ao corte uma linha fina de guia, longe da marca.
    Ela nao aparece no desenho, mas estica a caixa do recorte e a imagem sai com
    proporcao errada. O criterio e area: componente com menos de `minimo` da
    area do maior nao e parte do desenho.
    """
    import numpy as np
    from scipy import ndimage
    from PIL import Image
    a = np.array(im.convert("RGBA"))
    rotulos, n = ndimage.label(a[:, :, 3] > 40)
    if n <= 1:
        return im
    areas = ndimage.sum(np.ones_like(rotulos), rotulos, range(1, n + 1))
    corte = areas.max() * minimo
    # A marca nunca encosta na borda do slide. Encostar denuncia artefato da
    # prancha: na 08 e uma linha de um pixel na coluna 5333, correndo os 3000 de
    # altura, com area grande o bastante para passar por qualquer corte de area.
    # O criterio de area sozinho nao pegava, e por isso sao dois criterios.
    na_borda = set()
    if checar_borda:
        na_borda = set(rotulos[0, :]) | set(rotulos[-1, :]) |             set(rotulos[:, 0]) | set(rotulos[:, -1])
        na_borda.discard(0)
    manter = {i + 1 for i, x in enumerate(areas)
              if x >= corte and (i + 1) not in na_borda}
    a[:, :, 3] = np.where(np.isin(rotulos, list(manter)), a[:, :, 3], 0)
    return Image.fromarray(a, "RGBA")


def _recortar(im, margem=MARGEM, limpar=True):
    """`limpar` so vale sobre a prancha inteira.

    Num recorte, os componentes legitimos encostam na borda do proprio recorte:
    o bosque do simbolo e cada traco do mapa. Limpar ali apagava o desenho, e
    foi o que aconteceu na primeira versao.
    """
    if limpar:
        im = _sem_sujeira(im)
    b = im.getbbox()
    if not b:
        raise SystemExit("recorte vazio: a mascara nao encontrou a marca")
    x0, y0, x1, y1 = b
    w, h = im.size
    return im.crop((max(0, x0 - margem), max(0, y0 - margem),
                    min(w, x1 + margem), min(h, y1 + margem)))


def _salvar(im, nome, largura=LARGURA_MAX):
    if im.width > largura:
        im = im.resize((largura, round(im.height * largura / im.width)),
                       __import__("PIL.Image", fromlist=["Image"]).LANCZOS)
    destino = DESTINO / nome
    im.save(destino, optimize=True)
    return destino, im.size


# O mapa e um traco fino sobre area grande, e em RGBA de 2000px pesa 3 MB: mais
# do que o Hub inteiro. Como ele entra na pagina como textura de baixa opacidade,
# a cor e uma so e o que importa e o alpha. Em paleta de um tom com oito niveis
# de transparencia, a mesma imagem pesa 48 KB e nao serrilha.
MAPA_LARGURA, MAPA_NIVEIS = 1800, 8


def _salvar_mapa(im, nome):
    import numpy as np
    from PIL import Image
    im = im.copy()
    im.thumbnail((MAPA_LARGURA, MAPA_LARGURA * 3), Image.LANCZOS)
    alpha = np.array(im)[:, :, 3].astype(int)
    idx = (alpha * (MAPA_NIVEIS - 1) // 255).astype("uint8")
    saida = Image.fromarray(idx, "L").convert("P")
    paleta, trns = [], []
    for i in range(MAPA_NIVEIS):
        paleta += [74, 74, 74]                       # grafite da marca
        trns.append(round(255 * i / (MAPA_NIVEIS - 1)))
    saida.putpalette(paleta + [0] * (768 - len(paleta)))
    destino = DESTINO / nome
    saida.save(destino, transparency=bytes(trns), optimize=True)
    return destino, saida.size


def gerar() -> list:
    from PIL import Image
    p = _pranchas()
    DESTINO.mkdir(parents=True, exist_ok=True)
    feitos = []

    # 1. marca colorida, sobre fundo branco chapado
    im = Image.open(p["07"]).convert("RGBA")
    feitos.append(_salvar(_recortar(_sem_fundo_conexo(im)), "projeto.png"))

    # 2. marca negativa, branca, sobre o petroleo com marca d'agua do mapa
    im = Image.open(p["08"]).convert("RGBA")
    branca = _recortar(_chapar(im, (0, 64, 83), (255, 255, 255)))
    feitos.append(_salvar(branca, "projeto-branco.png"))

    # 3. marca monocromatica grafite, sobre o cinza claro com a mesma marca d'agua
    im = Image.open(p["11"]).convert("RGBA")
    feitos.append(_salvar(_recortar(_chapar(im, (223, 225, 226), (74, 74, 74))),
                          "projeto-grafite.png"))

    # 4. o simbolo isolado, para favicon e para uso em espaco estreito.
    #    O simbolo e o terco esquerdo do conjunto; o corte e pela caixa da marca
    #    colorida, e a proporcao vem da prancha, nao de estimativa.
    colorida = _recortar(_sem_fundo_conexo(Image.open(p["07"]).convert("RGBA")))
    for fonte, nome in ((colorida, "simbolo.png"), (branca, "simbolo-branco.png")):
        x = _corte_do_simbolo(fonte)
        feitos.append(_salvar(_recortar(fonte.crop((0, 0, x, fonte.height)),
                                        margem=8, limpar=False),
                              nome, largura=512))

    # 5. o mapa da cidade, elemento grafico da identidade, em traco escuro sobre
    #    branco. Vai para o Hub como textura, aplicada com opacidade baixa.
    #    O mapa e feito de milhares de tracos soltos: nenhuma limpeza por area
    #    ou por borda se aplica a ele, e o recorte e pela regiao da prancha, nao
    #    pelo conteudo. Fora da regiao ficam o rotulo «ELEMENTO» a direita e o
    #    rodape de quatro cores embaixo, que nao sao o elemento.
    im = Image.open(p["03"]).convert("RGBA")
    w, h = im.size
    regiao = im.crop((0, 0, int(w * 0.60), int(h * 0.94)))
    #    Aqui NAO se usa `_sem_fundo_conexo`: ele torna opaco tudo o que nao
    #    encosta na borda, e num mapa de ruas os quarteirroes sao regioes
    #    fechadas. O resultado seria uma mancha chapada. Para traco, o alpha e a
    #    distancia ao branco do papel.
    mapa = _chapar(regiao, (255, 255, 255), (74, 74, 74))
    mapa = _recortar(mapa, limpar=False)
    feitos.append(_salvar_mapa(mapa, "mapa-cidade.png"))

    # 6. favicon: quadrado, com respiro, a partir do simbolo. A travessia inteira
    #    a 32px vira um borrao de tres linhas de texto ilegiveis; o simbolo
    #    sozinho ainda se reconhece.
    simbolo = _recortar(colorida.crop((0, 0, _corte_do_simbolo(colorida),
                                       colorida.height)), margem=0, limpar=False)
    feitos.append(_salvar(_quadrado(simbolo, 512, 0.14), "favicon.png",
                          largura=512))

    # 7. cartao social 1200x630, no enquadramento da capa oficial: petroleo,
    #    mapa a direita sangrando, travessia branca a esquerda. A meta og:image
    #    apontava para a marca em PNG transparente, que quase toda plataforma
    #    compoe sobre preto.
    feitos.append(_cartao_social(branca, mapa, "og.jpg"))
    return feitos


def _quadrado(im, lado, respiro=0.12):
    """Centraliza numa tela quadrada, com respiro proporcional."""
    from PIL import Image
    util = round(lado * (1 - 2 * respiro))
    t = im.copy()
    t.thumbnail((util, util), Image.LANCZOS)
    tela = Image.new("RGBA", (lado, lado), (0, 0, 0, 0))
    tela.alpha_composite(t, ((lado - t.width) // 2, (lado - t.height) // 2))
    return tela


def _cartao_social(marca_branca, mapa, nome, tam=(1200, 630)):
    from PIL import Image
    w, h = tam
    tela = Image.new("RGBA", tam, (15, 76, 92, 255))
    # o mapa em verde, sangrando pela direita, como na capa
    verde = Image.new("RGBA", tam, (78, 159, 61, 255))
    m = mapa.copy()
    escala = (h * 1.45) / m.height
    m = m.resize((round(m.width * escala), round(m.height * escala)), Image.LANCZOS)
    recorte = Image.new("RGBA", tam, (0, 0, 0, 0))
    recorte.alpha_composite(m, (round(w * 0.42), round(-h * 0.22)))
    tela.paste(verde, (0, 0), recorte.split()[3].point(lambda v: int(v * 0.85)))
    # a travessia branca, a esquerda
    t = marca_branca.copy()
    t.thumbnail((round(w * 0.44), round(h * 0.42)), Image.LANCZOS)
    tela.alpha_composite(t, (round(w * 0.06), round((h - t.height) / 2)))
    # JPEG e nao PNG: o cartao e imagem de fundo chapado com traco fino, e em
    # PNG pesa 461 KB contra 90 KB em JPEG de qualidade 88, sem diferenca visivel.
    destino = DESTINO / nome
    tela.convert("RGB").save(destino, quality=88, optimize=True, progressive=True)
    return destino, tela.size


def main() -> int:
    for destino, tam in gerar():
        print(f"  {destino.relative_to(ROOT)}  {tam[0]}x{tam[1]}  "
              f"{destino.stat().st_size // 1024} KB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
