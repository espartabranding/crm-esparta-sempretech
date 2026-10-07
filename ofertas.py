"""Gera a página de oferta de cada conta estudada, para enviar por WhatsApp.

Uma página por conta em docs/ofertas/, com o combo de entrada dela, e um índice com a mensagem pronta.
As páginas não usam JavaScript nem arquivo externo: a animação é só CSS, e as fotos e a fonte vão embutidas,
porque a pré-visualização do WhatsApp e do iPhone não executa script. A única imagem fora da página é a da
pré-visualização do link (og:image), uma por combo, em docs/ofertas/og/.

O desenho é de estúdio de produto: fundo claro e frio, um azul só, linhas finas de desenho técnico, título em
Impact e a foto do produto inteira e muito grande. Cada item é apresentado pelo que resolve antes do nome.
"""

import base64
import html
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
from pathlib import Path
from urllib.parse import quote

RAIZ = Path(__file__).parent
SAIDA = RAIZ / "docs" / "ofertas"
FOTOS = RAIZ / "ofertas_img"
PROPOSTAS = RAIZ / "propostas.json"
PDFS = SAIDA / "pdf"
# O PDF é um caderno em A4 deitado: capa, um produto por página, galeria, demais itens, resumo e fecho.
PDF_LARGURA, PDF_ALTURA = 1440, 1018
PDF_CSS = """
@page{size:1440px 1018px;margin:0}
:root{--borda:40px}
html,body{width:1440px}
body{padding:0}
.barra,.dedo{display:none}
.faixa{width:100%;max-width:1300px;box-sizing:border-box;padding:0 60px}
.topo,.painel,.perto,.ainda,.conta,.fecho{height:1018px;box-sizing:border-box;overflow:hidden;display:flex;flex-direction:column;justify-content:center;padding-top:0;padding-bottom:0;break-inside:avoid;break-after:page}
.heroi{grid-template-columns:.92fr 1.08fr;column-gap:10px;grid-template-areas:"abre palco" "resto palco";align-items:start;margin-top:26px}
.abre{align-self:end}
h1{font-size:90px}
.palco{height:700px;margin:0 -40px 0 0}
.palco .principal{width:660px}
.luz{width:620px}.anel{width:680px}.anel.a2{width:540px}
.nota-t::after{width:56px}
.resto{padding-bottom:0}
.resto .botao{width:auto}
.preco b{font-size:76px}
.ganhos{grid-template-columns:1fr 1fr;margin-top:22px}
.ganhos li,.ganhos li:nth-child(even){padding:12px 14px 12px 34px;border-right:1px solid var(--linha)}
.ganhos li:nth-child(even){border-right:0}
.ganhos li::before,.ganhos li:nth-child(even)::before{left:12px;top:18px}
.painel .faixa{grid-template-columns:1fr 1.15fr;gap:30px}
.painel:nth-of-type(even) .faixa{grid-template-columns:1.15fr 1fr}
.painel:nth-of-type(even) .cena{order:-1}
.painel h2{font-size:80px}
.painel .apoio{font-size:20px}
.cena{min-height:680px;margin:0}
.cena .luz{width:600px}.cena .anel{width:660px}.cena img{width:660px}
.perto,.ainda{height:auto;display:block;overflow:visible}
.perto{padding:54px 0 44px;break-after:auto}
.ainda{padding:44px 0 50px}
.perto h2,.ainda h2{font-size:62px;margin-top:12px}
.galeria{overflow:visible;display:grid;grid-template-columns:repeat(4,1fr);margin:0;padding:26px 0 0}
.galeria li{flex:none}
.galeria img{aspect-ratio:auto;height:250px}
.itens{grid-template-columns:repeat(var(--colunas,3),minmax(0,1fr));margin-top:24px}
.item{break-inside:avoid}
.item img{aspect-ratio:auto;height:190px}
.item h3{font-size:28px}
.conta .faixa{display:grid;grid-template-columns:1fr 1fr;gap:80px;align-items:center}
.conta h2{font-size:84px}
.total b{font-size:100px}
.lotes b{font-size:30px}
.fecho{height:928px;break-after:auto}
.fecho h2{font-size:150px}
.fecho p{font-size:20px}
footer{height:84px;box-sizing:border-box}
"""
NAVEGADORES = (
    Path(os.environ.get("PROGRAMFILES", "")) / "Google/Chrome/Application/chrome.exe",
    Path(os.environ.get("PROGRAMFILES(X86)", "")) / "Google/Chrome/Application/chrome.exe",
    Path(os.environ.get("PROGRAMFILES(X86)", "")) / "Microsoft/Edge/Application/msedge.exe",
)
# Coleta do site da SempreTech (texto, preço e fotos de cada produto), feita em 06/10/2026.
SITE = Path(os.environ.get("OFERTAS_SITE", Path.home() / "Desktop" / "SempreTech" / "site"))
ENDERECO = "https://espartabranding.github.io/crm-esparta-sempretech/ofertas/"
# Para onde o botão da oferta leva: o WhatsApp divulgado no site da SempreTech.
WHATSAPP = "557130349662"
TELEFONE = "(71) 3034-9662"
CONSULTA = "06/10/2026"
GALERIA = 4  # fotos do produto principal
DESTAQUES = 3  # itens que ganham painel inteiro; os demais vão para a grade

# Produto do site (id) -> nome, ficha em poucas palavras, o que ele resolve e a frase de apoio.
PRODUTOS = {
    "6733": ("Computador Gamer i7 9700 X-Linne", ["Core i7 de 9ª geração", "16 GB DDR4", "SSD M.2 de 512 GB", "GTX 750 Ti de 4 GB"],
             "Potência para projeto, edição e arte", "Processador i7, 16 GB de memória e placa de vídeo dedicada de 4 GB no mesmo gabinete."),
    "5895": ("Computador i3 10100 X-Linne", ["Core i3 de 10ª geração", "8 GB de memória", "SSD de 240 GB", "Roda o Windows 11"],
             "Roda o Windows 11 e segue recebendo atualizações", "Processador de 10ª geração com SSD: a máquina liga depressa e continua no sistema atual."),
    "5359": ("Monitor LG de 22\" com ajuste de altura", ["22 polegadas", "Ajuste de altura", "Revisado"],
             "Tela grande, na altura certa", "22 polegadas com ajuste de altura, para trabalhar o dia inteiro no projeto."),
    "6595": ("Nobreak Coletek de 1500 VA", ["1500 VA", "Bivolt", "8 tomadas"],
             "A energia cai, o trabalho fica", "Nobreak de 1500 VA com 8 tomadas: tempo para salvar o arquivo e desligar direito."),
    "5185": ("Kit teclado e mouse sem fio Logitech MK270", ["Sem fio", "Teclado e mouse"],
             "Mesa sem fio", "Teclado e mouse Logitech sem fio, no mesmo kit."),
    "6499": ("Monitor VX Pro de 15,6\"", ["15,6 polegadas", "HDMI e VGA", "60 Hz"],
             "Tela nova em cada posição", "Monitor de 15,6 polegadas com HDMI e VGA."),
    "3951": ("Headset Logitech H111", ["Com microfone", "Analógico"],
             "Áudio em cada posição", "Headset com microfone para aula, treinamento e atendimento, sem um ouvir o outro."),
    "6593": ("Teclado USB TCN Slim 950", ["USB", "Slim"], "Teclado incluso", "Teclado USB slim, pronto para ligar."),
    "6591": ("Mouse USB TCN", ["USB", "1200 DPI"], "Mouse incluso", "Mouse óptico USB de 1200 DPI."),
    "1655": ("Estabilizador TS Shara Powerest", ["300 VA", "4 tomadas"],
             "Cada máquina protegida da oscilação", "Estabilizador de 300 VA com 4 tomadas, um por posição."),
    "981": ("Monitor AOC de 18,5\"", ["18,5 polegadas", "VGA e HDMI"],
            "Tela para o dia inteiro", "Monitor AOC de 18,5 polegadas, com VGA e HDMI."),
    "6165": ("Headset Intelbras CHS 40 USB", ["USB", "Mono", "Para operação"],
             "Headset feito para operação", "Intelbras CHS 40 USB: liga direto no computador e aguenta o turno."),
    "5351": ("Nobreak Ragtech Save de 600 VA", ["600 VA", "115, 127 e 220 V"],
             "A energia oscila, o sistema segue no ar", "Nobreak de 600 VA: tempo para concluir o que estava aberto e desligar direito."),
    "4093": ("Bobina térmica 80 x 30 mm", ["80 x 30 mm", "Caixa com 30"],
             "Bobina no mesmo pedido", "Caixa com 30 bobinas térmicas de 80 x 30 mm, para o cupom não faltar."),
    "5597": ("SSD XByte de 120 GB", ["120 GB", "SATA 2,5\""],
             "O upgrade que mais sai da bancada", "Cinco SSDs de 120 GB para trocar HD lento por disco rápido."),
    "3543": ("Memória HyperX Fury DDR4 de 8 GB", ["8 GB", "DDR4 3600 MHz"],
             "Memória para a máquina voltar a render", "Cinco pentes DDR4 de 8 GB HyperX Fury."),
    "6667": ("Fonte ATX de 500 W", ["500 W", "PFC ativo"],
             "Fonte na prateleira, reparo no mesmo dia", "Três fontes ATX de 500 W com PFC ativo."),
    "1269": ("HD Western Digital de 500 GB", ["500 GB", "Western Digital"],
             "Espaço para o cliente que precisa", "Dois HDs Western Digital de 500 GB."),
    "3783": ("Teclado USB Logitech K120", ["USB", "Logitech"], "Teclado Logitech", "Teclado USB Logitech K120."),
    "309": ("Mouse USB Logitech M90", ["USB", "Logitech"], "Mouse Logitech", "Mouse USB Logitech M90."),
    "4063": ("Câmera Bullet metal AHD", ["1080p", "Infravermelho 25 m", "IP66"],
             "Caixa, estoque e acessos sob câmera", "Câmeras de alta definição com visão noturna."),
}

# Combo -> itens (id do produto, quantidade), na ordem de destaque. O primeiro é o produto principal.
COMBOS = {
    "C1": {
        "nome": "Estação Criativa", "de": "da", "unidade": "estação", "plural": "estações",
        "titulo": "Projeto pesado, máquina à altura.",
        "chamada": "O arquivo pesado abre. O trabalho não para.",
        "texto": "A estação completa para projeto, edição e arte: computador i7 com placa de vídeo dedicada, monitor de 22 polegadas e nobreak.",
        "pontos": ["Placa de vídeo dedicada", "Monitor de 22\" com ajuste de altura", "Nobreak de 1500 VA", "Teclado e mouse sem fio"],
        "itens": [("6733", 1), ("5359", 1), ("6595", 1), ("5185", 1)],
    },
    "C2": {
        "nome": "Laboratório Pronto", "de": "do", "unidade": "posição", "plural": "posições",
        "titulo": "Toda a turma em máquina nova.",
        "chamada": "A turma entra e todas as máquinas respondem igual.",
        "texto": "Cada posição do laboratório chega completa e na mesma configuração: computador, monitor, headset, teclado, mouse e estabilizador.",
        "pontos": ["Roda o Windows 11", "Headset em cada posição", "Estabilizador por máquina", "Mesma configuração em todas"],
        "itens": [("5895", 1), ("3951", 1), ("1655", 1), ("6499", 1), ("6593", 1), ("6591", 1)],
    },
    "C3": {
        "nome": "Posição de Atendimento", "de": "da", "unidade": "posição", "plural": "posições",
        "titulo": "Posição pronta. Operador atendendo.",
        "chamada": "A posição chega pronta para o operador.",
        "texto": "Computador, monitor, headset de operação e estabilizador, na mesma configuração para toda a equipe.",
        "pontos": ["Headset de operação", "Roda o Windows 11", "Estabilizador por posição", "Reposição de headset a R$ 59,90"],
        "itens": [("5895", 1), ("6165", 1), ("981", 1), ("1655", 1), ("6593", 1), ("6591", 1)],
    },
    "C4": {
        "nome": "Caixa Pronto", "de": "do", "unidade": "caixa", "plural": "caixas",
        "titulo": "Caixa novo, venda protegida.",
        "chamada": "O caixa acompanha o sistema fiscal e não cai com a energia.",
        "texto": "Computador de décima geração, monitor e nobreak em cada ponto de venda, com a bobina térmica no mesmo fornecimento.",
        "pontos": ["Roda o Windows 11", "Nobreak em cada caixa", "Bobina térmica inclusa", "Monitor, teclado e mouse"],
        "itens": [("5895", 1), ("5351", 1), ("4093", 1), ("6499", 1), ("6593", 1), ("6591", 1)],
    },
    "C5": {
        "nome": "Parceiro Técnico", "de": "do", "unidade": "cesta", "plural": "cestas",
        "titulo": "A peça que falta, em Salvador.",
        "chamada": "Os componentes de maior giro, com fornecedor em Salvador.",
        "texto": "Uma cesta de reposição para a bancada: SSD, memória, fonte e HD, os itens que mais atrasam reparo quando faltam.",
        "pontos": ["5 SSDs de 120 GB", "5 memórias DDR4 de 8 GB", "3 fontes de 500 W", "2 HDs de 500 GB"],
        "itens": [("5597", 5), ("3543", 5), ("6667", 3), ("1269", 2)],
    },
    "C6": {
        "nome": "Escritório em Dia", "de": "do", "unidade": "estação", "plural": "estações",
        "titulo": "O escritório inteiro no Windows 11.",
        "chamada": "Estações que voltam a receber atualizações de segurança.",
        "texto": "O Windows 10 deixou de receber atualizações em outubro de 2025. Esta estação roda o Windows 11 e vem com monitor e nobreak.",
        "pontos": ["Roda o Windows 11", "Nobreak em cada estação", "Monitor de 18,5\"", "Teclado e mouse Logitech"],
        "itens": [("5895", 1), ("5351", 1), ("981", 1), ("3783", 1), ("309", 1)],
    },
    "C7": {
        "nome": "Segurança", "de": "da", "unidade": "kit", "plural": "kits",
        "titulo": "Caixa, estoque e acessos sob câmera.",
        "chamada": "Caixa, estoque e acessos sob câmera.",
        "texto": "Kit com quatro câmeras de alta definição, com visão noturna.",
        "pontos": ["4 câmeras", "1080p", "Visão noturna"],
        "itens": [("4063", 4)],
    },
}

esc = html.escape


def reais(valor: float) -> str:
    return "R$ " + f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def slug(texto: str) -> str:
    sem_acento = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", sem_acento.lower()).strip("-")


# Produto -> a que parte do trabalho ele responde (o rótulo que abre o painel dele).
AREA = {
    "6733": "Processamento", "5895": "Processamento", "5359": "Tela", "6499": "Tela", "981": "Tela", "6595": "Energia", "5351": "Energia",
    "1655": "Energia", "5185": "Periféricos", "6593": "Periféricos", "6591": "Periféricos", "3783": "Periféricos", "309": "Periféricos",
    "3951": "Áudio", "6165": "Áudio", "4093": "Suprimento", "5597": "Armazenamento", "1269": "Armazenamento", "3543": "Memória",
    "6667": "Alimentação", "4063": "Segurança",
}


def foto(produto: dict, n: int = 0) -> str | None:
    """Foto do produto como está no site, reduzida e embutida. A cópia fica em ofertas_img/, para gerar sem a coleta."""
    arquivo = FOTOS / f"{produto['id']}-{n}.webp"
    if not arquivo.exists():
        if not SITE.exists():
            return None
        from PIL import Image

        nomes = produto["imagens"] if isinstance(produto["imagens"], list) else json.loads(produto["imagens"].replace("'", '"'))
        if n >= len(nomes):
            return None
        imagem = Image.open(SITE / "produtos" / produto["pasta"] / nomes[n]).convert("RGBA")
        fundo = Image.new("RGBA", imagem.size, "white")
        fundo.alpha_composite(imagem)
        fundo = fundo.convert("RGB")
        fundo.thumbnail((720, 720))
        saida = BytesIO()
        fundo.save(saida, "WEBP", quality=76)
        FOTOS.mkdir(exist_ok=True)
        arquivo.write_bytes(saida.getvalue())
    return "data:image/webp;base64," + base64.b64encode(arquivo.read_bytes()).decode()


def capa(sigla: str, combo: dict) -> None:
    """Imagem da pré-visualização do link no WhatsApp: 1200 x 630, com o produto principal e o preço."""
    arquivo = SAIDA / "og" / f"{sigla.lower()}.jpg"
    if arquivo.exists():
        return
    from PIL import Image, ImageDraw, ImageFilter, ImageFont

    def fonte(tamanho: int):
        for nome in ("impact.ttf", "segoeuib.ttf", "arialbd.ttf"):
            try:
                return ImageFont.truetype(nome, tamanho)
            except OSError:
                continue
        return ImageFont.load_default(tamanho)

    tela = Image.new("RGB", (1200, 630), "#F2F6FF")
    pincel = ImageDraw.Draw(tela)
    for x in range(0, 1200, 40):  # grade técnica
        pincel.line([(x, 0), (x, 630)], fill="#DCE5FF")
    for y in range(0, 630, 40):
        pincel.line([(0, y), (1200, y)], fill="#DCE5FF")
    brilho = Image.new("RGB", (1200, 630), "#F2F6FF")
    ImageDraw.Draw(brilho).ellipse((620, 20, 1220, 620), fill="#9FC4FF")
    tela = Image.blend(tela, Image.composite(brilho.filter(ImageFilter.GaussianBlur(90)), tela, Image.new("L", (1200, 630), 150)), 0.9)
    pincel = ImageDraw.Draw(tela)
    produto = Image.open(BytesIO(base64.b64decode(combo["linhas"][0]["fotos"][0].split(",", 1)[1]))).convert("RGB")
    produto.thumbnail((440, 440))
    cartao = Image.new("RGB", (480, 480), "white")
    cartao.paste(produto, ((480 - produto.width) // 2, (480 - produto.height) // 2))
    mascara = Image.new("L", (480, 480), 0)
    ImageDraw.Draw(mascara).rounded_rectangle((0, 0, 480, 480), 36, fill=255)
    pincel.rounded_rectangle((664, 69, 1156, 561), 40, outline="#1437FF", width=5)
    tela.paste(cartao, (670, 75), mascara)
    pincel.rounded_rectangle((60, 54, 112, 106), 12, fill="#1437FF")
    pincel.text((86, 80), "ST", font=fonte(26), fill="white", anchor="mm")
    pincel.text((128, 80), "SempreTech", font=fonte(34), fill="#060B1F", anchor="lm")
    y = 190
    for palavra in combo["nome"].upper().replace(" DE ", " DE ").replace(" EM ", " EM ").split(" "):
        pincel.text((60, y), palavra.replace(" ", " "), font=fonte(96), fill="#060B1F")
        y += 102
    pincel.text((60, y + 24), reais(combo["total"]), font=fonte(78), fill="#1437FF")
    pincel.text((62, y + 112), f"por {combo['unidade']}, a preço de site", font=fonte(28), fill="#4A5678")
    arquivo.parent.mkdir(parents=True, exist_ok=True)
    tela.save(arquivo, "JPEG", quality=88)


def montar_combos() -> dict:
    catalogo = FOTOS / "produtos.json"
    if (SITE / "ofertas.json").exists():
        produtos = {p["id"]: p for p in json.loads((SITE / "ofertas.json").read_text(encoding="utf-8"))}
    else:
        produtos = json.loads(catalogo.read_text(encoding="utf-8"))
    usados = {}
    for sigla, combo in COMBOS.items():
        combo["linhas"] = []
        for posicao, (pid, qtd) in enumerate(combo["itens"]):
            p = produtos[pid]
            usados[pid] = {k: p[k] for k in ("id", "nome", "preco", "pasta", "imagens", "url")}
            nome, ficha, beneficio, apoio = PRODUTOS[pid]
            fotos = [f for f in (foto(p, n) for n in range(GALERIA if posicao == 0 else 1)) if f]
            combo["linhas"].append({"nome": nome, "ficha": ficha, "beneficio": beneficio, "apoio": apoio, "area": AREA[pid], "qtd": qtd,
                                    "preco": float(p["preco"]), "fotos": fotos})
        combo["total"] = round(sum(linha["qtd"] * linha["preco"] for linha in combo["linhas"]), 2)
        capa(sigla, combo)
    FOTOS.mkdir(exist_ok=True)
    catalogo.write_text(json.dumps(usados, ensure_ascii=False, indent=1), encoding="utf-8")
    return COMBOS


def _fonte() -> str:
    """Impact não vem no Android nem no iPhone: a Anton, quase igual, vai embutida para esses aparelhos."""
    arquivo = FOTOS / "anton-latin.woff2"
    if not arquivo.exists():
        return ""
    dados = base64.b64encode(arquivo.read_bytes()).decode()
    return f'@font-face{{font-family:"Anton";src:url(data:font/woff2;base64,{dados}) format("woff2");font-display:swap}}'


# Estúdio de produto: fundo claro e frio, um azul só, linhas finas de desenho técnico. O produto é o maior
# elemento de cada tela; o título vai em Impact, e o resto fica leve para ele aparecer. A foto entra inteira e o
# branco dela se funde ao fundo claro (mix-blend-mode:multiply).
CSS = """
:root{--tinta:#0A1020;--tinta-2:#5B6478;--fundo:#F3F5F9;--branco:#fff;--linha:#D9DFEA;--azul:#1F4DFF;--azul-2:#6C93FF;--noite:#070B1C;--zap:#25D366;
  --cartaz:Impact,"Anton","Haettenschweiler","Arial Narrow",sans-serif;--fonte:"Segoe UI",system-ui,-apple-system,Roboto,"Helvetica Neue",Arial,sans-serif;
  --mono:ui-monospace,"Cascadia Mono","Roboto Mono",Menlo,Consolas,monospace;--borda:clamp(20px,5vw,40px)}
*,*::before,*::after{box-sizing:border-box}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%;overflow-x:hidden;background:var(--branco)}
body{margin:0;background:var(--branco);color:var(--tinta);font:400 17px/1.6 var(--fonte);padding-bottom:76px;overflow-x:hidden}
img{max-width:100%;display:block}
h1,h2,h3,p,ul,dl,dd{margin:0}
ul{list-style:none;padding:0}
a{color:inherit}
:focus-visible{outline:2px solid var(--azul);outline-offset:4px}
.faixa{position:relative;max-width:1200px;margin:0 auto;padding:0 var(--borda)}
.cartaz{font-family:var(--cartaz);font-weight:400;text-transform:uppercase;line-height:1;letter-spacing:.012em}
.rotulo{display:flex;align-items:center;gap:12px;font:600 11.5px/1 var(--mono);letter-spacing:.22em;text-transform:uppercase;color:var(--azul)}
.rotulo::before{content:"";width:28px;height:1px;background:currentColor}
.produto{mix-blend-mode:multiply}

/* Abertura */
.topo{position:relative;isolation:isolate;overflow:hidden;background:linear-gradient(180deg,#fff 0%,#EEF2FA 62%,#E3E9F6 100%);padding:20px 0 0}
/* grade fina de desenho técnico, que some para cima */
.topo::before{content:"";position:absolute;inset:0;z-index:-1;background-image:linear-gradient(rgba(31,77,255,.07) 1px,transparent 1px),linear-gradient(90deg,rgba(31,77,255,.07) 1px,transparent 1px);background-size:56px 56px;-webkit-mask-image:linear-gradient(to top,#000,transparent 75%);mask-image:linear-gradient(to top,#000,transparent 75%)}
.cabeca{display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap}
.marca{display:flex;align-items:center;gap:10px;font-weight:700;font-size:17px;letter-spacing:-.01em}
.marca i{display:grid;place-items:center;width:30px;height:30px;border-radius:8px;background:var(--tinta);color:#fff;font:700 13px var(--fonte);font-style:normal}
.para{font:500 12px/1.3 var(--mono);letter-spacing:.04em;color:var(--tinta-2)}
.para b{color:var(--tinta);font-weight:600}
.heroi{display:grid;grid-template-areas:"abre" "palco" "resto";margin-top:clamp(28px,6vw,56px)}
.abre{grid-area:abre}
.resto{grid-area:resto;padding-bottom:clamp(40px,7vw,72px)}
h1{font-size:clamp(52px,15.6vw,148px);margin-top:16px;line-height:.98}
h1 em{font-style:normal;color:var(--azul)}
.texto{max-width:44ch;font-size:clamp(17px,2.2vw,20px);font-weight:300;color:var(--tinta-2);margin-top:18px}
.palco{grid-area:palco;position:relative;display:grid;place-items:center;height:min(108vw,760px);margin:8px calc(var(--borda)*-1) 0}
/* pedestal de luz e anéis finos */
.luz{position:absolute;width:min(92vw,640px);aspect-ratio:1;border-radius:50%;background:radial-gradient(closest-side,#fff 55%,rgba(255,255,255,0) 100%)}
.anel{position:absolute;width:min(98vw,700px);aspect-ratio:1;border-radius:50%;border:1px solid rgba(31,77,255,.22);animation:gira 60s linear infinite}
.anel::after{content:"";position:absolute;top:-4px;left:50%;width:7px;height:7px;border-radius:50%;background:var(--azul)}
.anel.a2{width:min(78vw,560px);border-style:dashed;border-color:rgba(31,77,255,.28);animation-duration:90s;animation-direction:reverse}
.anel.a2::after{display:none}
.palco .principal{position:relative;width:min(104vw,720px);aspect-ratio:1;object-fit:contain;animation:entra 1.2s cubic-bezier(.16,.8,.2,1) both,flutua 7s ease-in-out 1.2s infinite}
/* anotações de desenho técnico em volta do produto */
.nota-t{position:absolute;display:flex;align-items:center;gap:8px;font:600 11px/1.2 var(--mono);letter-spacing:.1em;text-transform:uppercase;color:var(--tinta);white-space:nowrap;opacity:0;animation:surge .8s ease forwards}
.nota-t::before{content:"";width:6px;height:6px;border-radius:50%;background:var(--azul);box-shadow:0 0 0 4px rgba(31,77,255,.16)}
.nota-t::after{content:"";height:1px;width:clamp(18px,6vw,56px);background:var(--azul);transform-origin:left;animation:traca .8s cubic-bezier(.2,.7,.2,1) both;animation-delay:inherit}
.nota-t.n1{left:var(--borda);top:6%;animation-delay:1s}
.nota-t.n2{right:var(--borda);top:14%;flex-direction:row-reverse;animation-delay:1.2s}
.nota-t.n2::after{transform-origin:right}
.nota-t.n3{left:var(--borda);bottom:13%;animation-delay:1.4s}
.nota-t.n4{right:var(--borda);bottom:5%;flex-direction:row-reverse;animation-delay:1.6s}
.nota-t.n4::after{transform-origin:right}
.preco{display:flex;flex-wrap:wrap;align-items:baseline;gap:4px 14px;margin-top:26px;padding-top:22px;border-top:1px solid var(--linha)}
.preco b{font:400 clamp(44px,12vw,76px)/1 var(--cartaz);letter-spacing:.01em}
.preco span{font-size:14px;color:var(--tinta-2)}
.botao{display:inline-flex;align-items:center;justify-content:center;gap:12px;background:var(--tinta);color:#fff;font-weight:600;font-size:16px;letter-spacing:.01em;text-decoration:none;padding:17px 28px;border-radius:999px;transition:background .25s,transform .25s}
.botao:hover{background:var(--azul);transform:translateY(-2px)}
.botao svg{width:22px;height:22px;flex:none;color:var(--zap)}
.resto .botao{margin-top:24px;width:100%}
.ganhos{display:grid;grid-template-columns:1fr 1fr;margin-top:30px;border-top:1px solid var(--linha)}
.ganhos li{position:relative;padding:14px 8px 14px 26px;border-bottom:1px solid var(--linha);font-size:14.5px;font-weight:600;line-height:1.3}
.ganhos li:nth-child(odd){border-right:1px solid var(--linha)}
.ganhos li:nth-child(even){padding-left:38px}
.ganhos li::before{content:"";position:absolute;left:4px;top:19px;width:12px;height:7px;border-left:2px solid var(--azul);border-bottom:2px solid var(--azul);rotate:-45deg}
.ganhos li:nth-child(even)::before{left:16px}
.sobe{opacity:0;animation:sobe .9s cubic-bezier(.16,.8,.2,1) forwards;animation-delay:calc(var(--i,0)*120ms + 120ms)}

/* Painéis: um benefício, um produto, muito grande */
.painel{position:relative;isolation:isolate;overflow:hidden;padding:clamp(64px,11vw,140px) 0;background:var(--branco)}
.painel:nth-of-type(even){background:linear-gradient(180deg,var(--fundo),#fff)}
.painel .faixa{display:grid;gap:8px;align-items:center}
.painel h2{font-size:clamp(46px,13vw,104px);margin-top:18px}
.painel .apoio{margin-top:18px;font-size:clamp(17px,2.2vw,20px);font-weight:300;color:var(--tinta-2);max-width:36ch}
.painel .nome{margin-top:30px;font:600 11.5px var(--mono);letter-spacing:.14em;text-transform:uppercase;color:var(--tinta-2)}
.ficha{margin-top:12px;border-top:1px solid var(--linha);max-width:460px}
.ficha li{position:relative;padding:12px 0 12px 26px;border-bottom:1px solid var(--linha);font-size:15.5px;font-weight:600}
.ficha li::before{content:"";position:absolute;left:2px;top:50%;width:8px;height:8px;margin-top:-4px;border-radius:50%;background:var(--azul);box-shadow:0 0 0 4px rgba(31,77,255,.14)}
.painel .valor{margin-top:22px;font:400 34px/1 var(--cartaz)}
.painel .valor small{font:500 12px var(--mono);letter-spacing:.04em;margin-left:10px;color:var(--tinta-2)}
.cena{position:relative;display:grid;place-items:center;min-height:min(104vw,680px);margin:0 calc(var(--borda)*-1)}
.cena .luz{width:min(88vw,600px)}
.cena .anel{width:min(96vw,660px);animation-duration:80s}
.cena img{position:relative;width:min(104vw,680px);aspect-ratio:1;object-fit:contain}
.qtd{font:600 11.5px var(--mono);letter-spacing:.14em;color:var(--tinta-2)}

/* Galeria do produto principal */
.perto{padding:clamp(56px,9vw,110px) 0;background:var(--fundo)}
.perto h2,.ainda h2{font-size:clamp(40px,10.5vw,84px);margin-top:18px}
.galeria{display:flex;gap:16px;overflow-x:auto;scroll-snap-type:x mandatory;padding:30px var(--borda) 12px;margin:0 calc(var(--borda)*-1);scrollbar-width:none;-webkit-overflow-scrolling:touch}
.galeria::-webkit-scrollbar{display:none}
.galeria li{flex:0 0 min(84vw,420px);scroll-snap-align:center;background:#fff;border-radius:20px;overflow:hidden;border:1px solid var(--linha)}
.galeria img{width:100%;aspect-ratio:1;object-fit:contain;transition:transform .8s cubic-bezier(.16,.8,.2,1)}
.galeria li:hover img{transform:scale(1.06)}
.dedo{font:500 12px var(--mono);letter-spacing:.06em;color:var(--tinta-2);margin-top:8px}

/* Os demais itens */
.ainda{padding:clamp(56px,9vw,110px) 0}
.itens{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1px;margin-top:30px;background:var(--linha);border:1px solid var(--linha);border-radius:20px;overflow:hidden}
.item{display:flex;flex-direction:column;background:#fff;padding:10px 16px 20px;isolation:isolate}
.item img{width:100%;aspect-ratio:1;object-fit:contain;transition:transform .8s cubic-bezier(.16,.8,.2,1)}
.item:hover img{transform:scale(1.07)}
.item h3{font:400 clamp(21px,5.6vw,30px)/1.02 var(--cartaz);text-transform:uppercase;letter-spacing:.012em;margin-top:6px}
.item p{font-size:13.5px;color:var(--tinta-2);margin-top:8px;line-height:1.4}
.item b{margin-top:auto;padding-top:14px;font:400 22px var(--cartaz)}

/* Resumo, na faixa escura */
.conta{position:relative;isolation:isolate;overflow:hidden;background:var(--noite);color:#fff;padding:clamp(64px,11vw,130px) 0}
.conta::before{content:"";position:absolute;inset:0;z-index:-1;background-image:linear-gradient(rgba(108,147,255,.09) 1px,transparent 1px),linear-gradient(90deg,rgba(108,147,255,.09) 1px,transparent 1px);background-size:56px 56px;-webkit-mask-image:radial-gradient(80% 70% at 70% 30%,#000,transparent);mask-image:radial-gradient(80% 70% at 70% 30%,#000,transparent)}
.conta::after{content:"";position:absolute;z-index:-1;width:620px;height:620px;border-radius:50%;background:var(--azul);filter:blur(140px);opacity:.38;top:-240px;right:-220px}
.conta .rotulo{color:var(--azul-2)}
.conta h2{font-size:clamp(42px,11.5vw,96px);margin-top:18px}
.conta h2 em{font-style:normal;color:var(--azul-2)}
.lista{margin-top:30px;border-top:1px solid rgba(255,255,255,.16)}
.lista li{display:flex;align-items:baseline;gap:14px;padding:14px 0;border-bottom:1px solid rgba(255,255,255,.16);font-size:15px}
.lista li span:first-child{flex:1;color:#D5DBEA}
.lista li span:last-child{font:500 14px var(--mono);white-space:nowrap}
.total{display:flex;justify-content:space-between;align-items:flex-end;gap:12px;margin-top:26px}
.total span{font:500 11.5px var(--mono);letter-spacing:.2em;text-transform:uppercase;color:#A9B3CC}
.total b{font:400 clamp(52px,14.5vw,112px)/.92 var(--cartaz);white-space:nowrap}
.lotes{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));margin-top:40px;border:1px solid rgba(255,255,255,.16);border-radius:18px;overflow:hidden}
.lotes li{padding:18px 12px;border-right:1px solid rgba(255,255,255,.16)}
.lotes li:last-child{border-right:0}
.lotes small{display:block;font:500 11px var(--mono);letter-spacing:.12em;text-transform:uppercase;color:#A9B3CC}
.lotes b{display:block;font:400 clamp(17px,4.6vw,32px)/1.1 var(--cartaz);margin-top:8px;white-space:nowrap}
.nota{font-size:13px;color:#A9B3CC;margin-top:16px;max-width:60ch}
.extra{margin-top:36px;display:grid;grid-template-columns:120px 1fr;gap:18px;align-items:center;border:1px solid rgba(255,255,255,.16);border-radius:18px;padding:12px 18px 12px 12px;background:rgba(255,255,255,.04)}
.extra img{width:120px;height:120px;object-fit:contain;background:#fff;border-radius:12px}
.extra .rotulo{font-size:10.5px}
.extra b{display:block;font:400 28px/1 var(--cartaz);text-transform:uppercase;letter-spacing:.012em;margin-top:10px}
.extra p{font-size:14px;color:#D5DBEA;margin-top:6px;line-height:1.45}

.fecho{position:relative;text-align:center;padding:clamp(72px,12vw,150px) 0;background:linear-gradient(180deg,#fff,var(--fundo))}
.fecho h2{font-size:clamp(60px,17vw,168px)}
.fecho h2 em{font-style:normal;color:var(--azul)}
.fecho p{margin:20px auto 30px;max-width:40ch;font-size:clamp(17px,2.2vw,20px);font-weight:300;color:var(--tinta-2)}
.fecho .fone{display:block;margin-top:22px;font:500 13px var(--mono);letter-spacing:.06em;color:var(--tinta-2)}
footer{padding:22px 0 12px;font-size:12.5px;color:var(--tinta-2);border-top:1px solid var(--linha)}

/* Barra fixa no celular */
.barra{position:fixed;left:0;right:0;bottom:0;z-index:40;display:flex;align-items:center;justify-content:space-between;gap:12px;background:rgba(255,255,255,.9);-webkit-backdrop-filter:blur(14px);backdrop-filter:blur(14px);border-top:1px solid var(--linha);padding:10px 16px calc(10px + env(safe-area-inset-bottom,0px));animation:sobe .7s 1.8s both}
.barra small{display:block;font:500 11px/1.2 var(--mono);letter-spacing:.04em;color:var(--tinta-2)}
.barra b{font:400 25px/1.1 var(--cartaz);white-space:nowrap}
.barra .botao{font-size:15px;padding:13px 20px;white-space:nowrap}

@keyframes sobe{from{opacity:0;transform:translateY(26px)}to{opacity:1;transform:none}}
@keyframes entra{from{opacity:0;transform:scale(.86) translateY(30px)}to{opacity:1;transform:none}}
@keyframes flutua{0%,100%{translate:0 0}50%{translate:0 -10px}}
@keyframes gira{to{transform:rotate(1turn)}}
@keyframes surge{to{opacity:1}}
@keyframes traca{from{transform:scaleX(0)}to{transform:scaleX(1)}}
@keyframes aparece{from{opacity:0;transform:translateY(40px)}to{opacity:1;transform:none}}
@keyframes revela{from{clip-path:inset(0 0 100% 0);transform:translateY(24px)}to{clip-path:inset(0);transform:none}}
@keyframes cresce{from{opacity:0;transform:scale(.8)}to{opacity:1;transform:none}}
/* Onde o navegador liga a animação à rolagem, cada bloco entra ao aparecer na tela; onde não liga, fica visível. */
@supports (animation-timeline:view()){
  .rola{animation:aparece linear both;animation-timeline:view();animation-range:entry 0% entry 60%}
  .painel h2{animation:revela linear both;animation-timeline:view();animation-range:entry 10% cover 32%}
  .cena img{animation:cresce linear both;animation-timeline:view();animation-range:entry 0% cover 40%}
}
@media (min-width:700px){
  .itens{grid-template-columns:repeat(3,minmax(0,1fr))}
  .ganhos{grid-template-columns:repeat(4,1fr)}
  .ganhos li,.ganhos li:nth-child(even){padding:16px 14px 16px 34px;border-right:1px solid var(--linha)}
  .ganhos li:last-child{border-right:0}
  .ganhos li::before,.ganhos li:nth-child(even)::before{left:12px;top:22px}
}
@media (min-width:980px){
  body{padding-bottom:0}
  .barra{display:none}
  .heroi{grid-template-columns:.92fr 1.08fr;column-gap:10px;grid-template-areas:"abre palco" "resto palco";align-items:start}
  .abre{align-self:end}
  h1{font-size:clamp(76px,8.2vw,148px)}
  .palco{height:760px;margin:0 calc(var(--borda)*-1) 0 0}
  .palco .principal{width:720px}
  .resto .botao{width:auto}
  .ganhos{grid-template-columns:1fr 1fr}
  .ganhos li:nth-child(even){border-right:0}
  .painel .faixa{grid-template-columns:1fr 1.15fr;gap:30px}
  .painel:nth-of-type(even) .faixa{grid-template-columns:1.15fr 1fr}
  .painel:nth-of-type(even) .cena{order:-1}
  .cena{margin:0}
  .painel h2{font-size:clamp(60px,6.6vw,108px)}
  .galeria{overflow:visible;display:grid;grid-template-columns:repeat(4,1fr);margin:0;padding:30px 0 0}
  .galeria li{flex:none}
  .dedo{display:none}
  .conta .faixa{display:grid;grid-template-columns:1fr 1fr;gap:80px;align-items:start}
  .itens{grid-template-columns:repeat(var(--colunas,3),minmax(0,1fr))}
}
@media (max-width:350px){
  .nota-t.n3,.nota-t.n4{display:none}
  .barra small{display:none}
}
@media (prefers-reduced-motion:reduce){
  *,*::before,*::after{animation:none!important;transition:none!important}
  .sobe,.nota-t{opacity:1}
}
/* Impressão e PDF: sem animação, tudo visível e com as cores de fundo */
@media print{
  *,*::before,*::after{animation:none!important;transition:none!important;-webkit-print-color-adjust:exact;print-color-adjust:exact}
  .sobe,.nota-t,.rola{opacity:1!important;transform:none!important}
  .painel h2{clip-path:none!important}
  body{padding-bottom:0}
  .barra,.dedo{display:none}
  .painel,.item,.galeria li,.lista li{break-inside:avoid}
}
"""

ICONE = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.600 15.100L2 22l5-1.300A10 10 0 1 0 12 2Zm0 1.800a8.200 8.200 0 0 1 7 12.500 8.200 8.200 0 0 1-11 2.900l-.400-.200-2.900.800.800-2.800-.300-.500A8.200 8.200 0 0 1 12 3.800Zm-3.300 4c-.200 0-.500 0-.700.300-.300.300-1 1-1 2.300s1 2.700 1.200 2.900c.100.200 2 3.200 5 4.300 2.400.900 2.900.700 3.400.700.500-.100 1.700-.700 1.900-1.300.200-.700.200-1.200.200-1.300-.100-.200-.300-.200-.600-.400l-1.900-.900c-.300-.100-.500-.200-.700.100l-.900 1.100c-.200.200-.300.200-.600.100-.300-.200-1.200-.500-2.300-1.400-.800-.800-1.400-1.700-1.600-2-.200-.300 0-.400.100-.600l.400-.500.300-.500c.100-.200 0-.400 0-.500l-.900-2c-.200-.500-.400-.500-.600-.500h-.600Z"/></svg>'


def _titulo(texto: str) -> str:
    """A última frase do título sai em azul."""
    partes = re.split(r"(?<=[.,])\s+", texto, maxsplit=1)
    return esc(partes[0]) + (f" <em>{esc(partes[1])}</em>" if len(partes) > 1 else "")


def pagina(conta: dict, combos: dict) -> str:
    sigla, secundario = conta["combo"].split()[0], (conta.get("combo_secundario") or "").split()[:1]
    c = combos[sigla]
    extra = combos.get(secundario[0]) if secundario else None
    empresa = conta["empresa"]
    linhas = c["linhas"]
    principal, destaques, resto = linhas[0], linhas[:DESTAQUES], linhas[DESTAQUES:]
    mensagem = f"Olá. Gostaria de receber a proposta {c['de']} {c['nome']} para {empresa}."
    whats = esc(f"https://wa.me/{WHATSAPP}?text={quote(mensagem)}")
    botao = f'<a class="botao" href="{whats}" target="_blank" rel="noopener">{ICONE}Pedir a proposta pelo WhatsApp</a>'
    notas = "".join(f'<span class="nota-t n{i + 1}">{esc(x)}</span>' for i, x in enumerate(principal["ficha"][:4]))

    def vezes(linha: dict) -> str:
        return f"{linha['qtd']} × " if linha["qtd"] > 1 else ""

    paineis = "".join(
        f"""<section class="painel"><div class="faixa">
  <div>
    <p class="rotulo rola">{esc(linha['area'])}</p>
    <h2 class="cartaz">{esc(linha['beneficio'])}</h2>
    <p class="apoio rola">{esc(linha['apoio'])}</p>
    <p class="nome rola">{esc(vezes(linha) + linha['nome'])}</p>
    <ul class="ficha rola">{''.join(f'<li>{esc(x)}</li>' for x in linha['ficha'])}</ul>
    <p class="valor rola">{reais(linha['qtd'] * linha['preco'])}<small>no site, em {CONSULTA}</small></p>
  </div>
  <div class="cena"><span class="luz"></span><span class="anel"></span><img class="produto" src="{linha['fotos'][0]}" alt="{esc(linha['nome'])}" loading="lazy"></div>
</div></section>"""
        for linha in destaques
    )
    grade = "" if not resto else f"""<section class="ainda"><div class="faixa">
  <p class="rotulo rola">Mais no conjunto</p>
  <h2 class="cartaz rola">E ainda vem</h2>
  <ul class="itens rola" style="--colunas:{min(len(resto), 3)}">{''.join(f'''<li class="item"><img class="produto" src="{linha["fotos"][0]}" alt="{esc(linha["nome"])}" loading="lazy">
    <h3>{esc(linha["beneficio"])}</h3><p>{esc(vezes(linha) + linha["nome"])}</p><b>{reais(linha["qtd"] * linha["preco"])}</b></li>''' for linha in resto)}</ul>
</div></section>"""
    galeria = "" if len(principal["fotos"]) < 2 else f"""<section class="perto"><div class="faixa">
  <p class="rotulo rola">{esc(principal['nome'])}</p>
  <h2 class="cartaz rola">Veja de perto</h2>
  <ul class="galeria">{''.join(f'<li class="rola"><img src="{f}" alt="{esc(principal["nome"])}, foto {i + 1}" loading="lazy"></li>' for i, f in enumerate(principal['fotos']))}</ul>
  <p class="dedo">Deslize para ver mais fotos →</p>
</div></section>"""
    lotes = "" if sigla == "C5" else (
        '<ul class="lotes rola">'
        + "".join(f"<li><small>{n} {c['unidade'] if n == 1 else c['plural']}</small><b>{reais(n * c['total'])}</b></li>" for n in (1, 5, 10))
        + '</ul><p class="nota rola">Soma dos itens a preço de site. Para lotes, a condição comercial é definida na proposta.</p>'
    )
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#ffffff">
<title>{esc(c['nome'])} para {esc(empresa)} · SempreTech</title>
<meta name="description" content="{esc(c['chamada'])} {reais(c['total'])} por {c['unidade']}, a preço de site.">
<meta property="og:title" content="{esc(c['nome'])} para {esc(empresa)}">
<meta property="og:description" content="{esc(c['chamada'])} {reais(c['total'])} por {c['unidade']}.">
<meta property="og:type" content="website">
<meta property="og:image" content="{ENDERECO}og/{sigla.lower()}.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<style>{_fonte()}{CSS}</style>
</head>
<body>
<header class="topo"><div class="faixa">
  <div class="cabeca sobe"><div class="marca"><i>ST</i>SempreTech</div><p class="para">Proposta para <b>{esc(empresa)}</b></p></div>
  <div class="heroi">
    <div class="abre">
      <p class="rotulo sobe" style="--i:1">{esc(c['nome'])}</p>
      <h1 class="cartaz sobe" style="--i:2">{_titulo(c['titulo'])}</h1>
    </div>
    <div class="palco">
      <span class="luz"></span><span class="anel"></span><span class="anel a2"></span>
      <img class="principal produto" src="{principal['fotos'][0]}" alt="{esc(principal['nome'])}">
      {notas}
    </div>
    <div class="resto">
      <p class="texto sobe" style="--i:3">{esc(c['texto'])}</p>
      <p class="preco sobe" style="--i:4"><b>{reais(c['total'])}</b><span>por {c['unidade']}, a preço de site</span></p>
      <div class="sobe" style="--i:5">{botao}</div>
      <ul class="ganhos sobe" style="--i:6">{''.join(f'<li>{esc(p)}</li>' for p in c['pontos'])}</ul>
    </div>
  </div>
</div></header>

<main>
{paineis}
{galeria}
{grade}
<section class="conta"><div class="faixa">
  <div>
    <p class="rotulo rola">Resumo do conjunto</p>
    <h2 class="cartaz rola">Tudo isto em <em>cada {c['unidade']}</em></h2>
    <ul class="lista rola">{''.join(f'<li><span>{esc(vezes(linha) + linha["nome"])}</span><span>{reais(linha["qtd"] * linha["preco"])}</span></li>' for linha in linhas)}</ul>
    <p class="total rola"><span>Total por {c['unidade']}</span><b>{reais(c['total'])}</b></p>
  </div>
  <div>
    {lotes if lotes else '<p class="nota rola" style="font-size:16px;color:#D5DBEA;margin-top:0">As quantidades da cesta são uma referência. A cotação sai com os componentes e os volumes que a assistência mais utiliza.</p>'}
    {f'<div class="extra rola"><img src="{extra["linhas"][0]["fotos"][0]}" alt="" loading="lazy"><div><p class="rotulo">Complemento sugerido</p><b>{esc(extra["nome"])}</b><p>{esc(extra["chamada"])} {reais(extra["total"])} por {extra["unidade"]}.</p></div></div>' if extra else ''}
  </div>
</div></section>
</main>

<section class="fecho"><div class="faixa">
  <h2 class="cartaz rola">Peça a <em>proposta</em></h2>
  <p class="rola">Informe a quantidade de {c['plural']} e a SempreTech envia a proposta para {esc(empresa)}, com a configuração e o valor.</p>
  <div class="rola">{botao}</div>
  <a class="fone" href="tel:+{WHATSAPP}">ou ligue: {TELEFONE}</a>
</div></section>

<footer><div class="faixa">Preços de varejo do site sempretechba.com.br, consultados em {CONSULTA}, sujeitos a alteração e à disponibilidade em estoque. Imagens dos produtos conforme o site; o gabinete pode variar com o estoque.</div></footer>

<div class="barra"><div><small>{esc(c['nome'])}, por {c['unidade']}</small><b>{reais(c['total'])}</b></div><a class="botao" href="{whats}" target="_blank" rel="noopener">{ICONE}Pedir proposta</a></div>
</body>
</html>
"""


def indice(linhas: list[dict]) -> str:
    corpo = "".join(
        f"""<tr><td><b>{esc(linha['empresa'])}</b><small>{esc(linha['ordem'])} · {esc(linha['cidade'])}</small></td>
<td>{esc(linha['combo'])}<small>{reais(linha['total'])} por {linha['unidade']}</small></td>
<td><a href="{linha['arquivo']}">Ver a oferta</a><small>{f'<a href="{esc(linha["whats"])}" target="_blank" rel="noopener">Abrir o WhatsApp da conta</a>' if linha['whats'] else 'Sem telefone'}</small>
<details><summary>Mensagem</summary><p>{esc(linha['mensagem'])}</p></details></td></tr>"""
        for linha in linhas
    )
    return f"""<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow"><title>Ofertas por WhatsApp · SempreTech</title>
<style>body{{margin:0;background:#F4F6FC;color:#0E1730;font:400 15px/1.5 "Segoe UI",system-ui,sans-serif}}main{{max-width:1000px;margin:0 auto;padding:28px 16px 60px}}
h1{{font-size:30px;letter-spacing:-.02em;margin:0 0 6px}}p{{margin:0 0 18px;color:#5A6685;max-width:70ch}}
.rol{{overflow-x:auto;background:#fff;border:1px solid #DDE2F0;border-radius:14px}}table{{width:100%;border-collapse:collapse;min-width:640px}}
th,td{{text-align:left;padding:12px 14px;border-bottom:1px solid #DDE2F0;vertical-align:top}}th{{font-size:11.5px;letter-spacing:.06em;text-transform:uppercase;color:#5A6685}}
small{{display:block;color:#5A6685;font-size:13px}}a{{color:#2B50FF}}details p{{margin:8px 0 0;color:#0E1730;max-width:52ch}}summary{{cursor:pointer;color:#2B50FF;font-size:13px}}</style></head>
<body><main><h1>Ofertas por WhatsApp</h1>
<p>Uma página de oferta para cada uma das {len(linhas)} contas com proposta: as estudadas e as que estão na etapa de proposta. O link "Abrir o WhatsApp da conta" já leva a mensagem pronta; troque [Seu nome] antes de enviar. Envie só para número que a empresa divulga para contato comercial ou com permissão dada por telefone.</p>
<div class="rol"><table><thead><tr><th>Conta</th><th>Oferta</th><th>Enviar</th></tr></thead><tbody>{corpo}</tbody></table></div></main></body></html>
"""


def gerar() -> None:
    SAIDA.mkdir(parents=True, exist_ok=True)
    combos = montar_combos()
    plano = json.loads((RAIZ / "contas.json").read_text(encoding="utf-8"))
    ordem = {"s1": "Semana 1", "s2": "Semana 2", "validar": "Validar dados antes"}
    # Contas que o registro manual deixou na etapa de proposta (a última etapa anotada de cada uma).
    etapa = {}
    tentativas = RAIZ / "tentativas.json"
    for t in sorted(json.loads(tentativas.read_text(encoding="utf-8")) if tentativas.exists() else [], key=lambda t: t["quando"]):
        if t.get("etapa"):
            etapa[t["conta"]] = t["etapa"]
    em_proposta = {conta for conta, e in etapa.items() if e in ("apresentar", "enviar")}
    linhas, propostas = [], {}
    for conta in plano["contas"]:
        # Ganham proposta as contas estudadas e as que estão na etapa de apresentar a proposta personalizada.
        if not conta.get("combo") or not (conta.get("onda") in ordem or conta["id"] in em_proposta):
            continue
        arquivo = f"{slug(conta['empresa'])}.html"
        (SAIDA / arquivo).write_text(pagina(conta, combos), encoding="utf-8")
        c = combos[conta["combo"].split()[0]]
        mensagem = (
            f"Bom dia. Aqui é [Seu nome], da SempreTech, distribuidora de informática de Salvador. "
            f"Preparamos uma proposta {c['de']} {c['nome']} para {conta['empresa']}: {ENDERECO}{arquivo} "
            f"Posso apresentar os detalhes por aqui ou em uma ligação?"
        )
        numero = re.sub(r"\D", "", conta.get("telefone") or "")
        linha = {"empresa": conta["empresa"], "cidade": conta["cidade"], "ordem": ordem.get(conta["onda"], "Em fase de proposta"), "combo": c["nome"], "total": c["total"], "unidade": c["unidade"],
                 "arquivo": arquivo, "pdf": f"pdf/{arquivo[:-5]}.pdf", "mensagem": mensagem, "whats": f"https://wa.me/{numero}?text={quote(mensagem)}" if numero else ""}
        linhas.append(linha)
        propostas[conta["id"]] = {k: linha[k] for k in ("combo", "total", "unidade", "arquivo", "pdf", "mensagem", "whats")}
    # Sai a página (e o PDF) de conta que deixou de ter proposta.
    validas = {linha["arquivo"][:-5] for linha in linhas} | {"index"}
    for sobra in [*SAIDA.glob("*.html"), *PDFS.glob("*.pdf")]:
        if sobra.stem not in validas:
            sobra.unlink()
    (SAIDA / "index.html").write_text(indice(linhas), encoding="utf-8")
    # O painel lê este arquivo para mostrar a proposta dentro da ficha de cada conta.
    PROPOSTAS.write_text(json.dumps(propostas, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(linhas)} ofertas em {SAIDA}")


def _pdf(navegador: Path, origem: Path, destino: Path) -> None:
    """Imprime a oferta como caderno em A4 deitado e põe a marca, a empresa e o número em cada página."""
    import pymupdf
    from PIL import Image

    fonte = origem.read_text(encoding="utf-8")
    empresa = html.unescape(re.search(r'class="para">Proposta para <b>(.*?)</b>', fonte).group(1))
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as pasta:
        temp = Path(pasta)
        # O navegador deixa pastas de trabalho na pasta temporária; aqui elas somem junto com esta.
        ambiente = {**os.environ, "TEMP": pasta, "TMP": pasta}
        (temp / "oferta.html").write_text(fonte.replace("</head>", f"<style>{PDF_CSS}</style></head>", 1), encoding="utf-8")
        # O navegador às vezes devolve o arquivo vazio quando vários rodam ao mesmo tempo: tenta de novo.
        for _ in range(4):
            subprocess.run(
                [str(navegador), "--headless=new", "--disable-gpu", "--no-pdf-header-footer", f"--user-data-dir={temp / 'perfil'}",
                 f"--print-to-pdf={temp / 'oferta.pdf'}", (temp / "oferta.html").as_uri()],
                check=False, capture_output=True, timeout=180, env=ambiente,
            )
            if (temp / "oferta.pdf").is_file() and (temp / "oferta.pdf").stat().st_size:
                break
        doc = pymupdf.open(temp / "oferta.pdf")
        # As fotos entram sem compressão no PDF do navegador; em JPEG o arquivo cai para um terço.
        feitas = set()
        for folha in doc:
            for imagem in folha.get_images(full=True):
                ref, mascara = imagem[0], imagem[1]
                if ref in feitas or mascara:
                    continue
                feitas.add(ref)
                foto = Image.open(BytesIO(pymupdf.Pixmap(doc, ref).tobytes("png"))).convert("RGB")
                foto.thumbnail((600, 600), Image.LANCZOS)
                saida = BytesIO()
                foto.save(saida, "JPEG", quality=74, optimize=True)
                folha.replace_image(ref, stream=saida.getvalue())
        for n, folha in enumerate(doc, 1):
            if n in (1, len(doc)):
                continue  # a capa já traz a marca e a empresa, e a última página tem o rodapé com as condições
            largura, altura = folha.rect.width, folha.rect.height
            # Rodapé claro nas páginas escuras e escuro nas claras.
            amostra = folha.get_pixmap(dpi=20, clip=pymupdf.Rect(40, altura - 40, 200, altura - 14)).samples
            cor = (0.66, 0.70, 0.80) if sum(amostra) / len(amostra) < 110 else (0.36, 0.39, 0.47)
            folha.insert_text((45, altura - 24), f"SempreTech  ·  Proposta para {empresa}", fontsize=8.5, fontname="helv", color=cor)
            numero = f"{n} / {len(doc)}"
            folha.insert_text((largura - 45 - pymupdf.get_text_length(numero, "helv", 8.5), altura - 24), numero, fontsize=8.5, fontname="helv", color=cor)
        doc.set_metadata({"title": f"Proposta SempreTech para {empresa}", "author": "SempreTech"})
        doc.save(destino, garbage=4, deflate=True, deflate_fonts=True, use_objstms=1)
        doc.close()


def gerar_pdfs(refazer: bool = False) -> None:
    """PDF de cada oferta em docs/ofertas/pdf/. Só gera os que faltam, a não ser que se peça para refazer."""
    navegador = next((n for n in NAVEGADORES if n.is_file()), None)
    if not navegador:
        raise SystemExit("Chrome ou Edge não encontrado para gerar os PDFs.")
    if refazer:
        shutil.rmtree(PDFS, ignore_errors=True)
    PDFS.mkdir(parents=True, exist_ok=True)
    paginas = [p for p in sorted(SAIDA.glob("*.html")) if p.name != "index.html"]
    faltam = [p for p in paginas if not (PDFS / f"{p.stem}.pdf").exists()]
    with ThreadPoolExecutor(4) as fila:
        list(fila.map(lambda p: _pdf(navegador, p, PDFS / f"{p.stem}.pdf"), faltam))
    print(f"{len(faltam)} PDFs gerados em {PDFS} ({len(paginas) - len(faltam)} já existiam)")


if __name__ == "__main__":
    gerar()
    # uv run python ofertas.py --pdf gera os PDFs que faltam; --pdf-refazer gera todos de novo.
    if "--pdf" in sys.argv or "--pdf-refazer" in sys.argv:
        gerar_pdfs(refazer="--pdf-refazer" in sys.argv)
