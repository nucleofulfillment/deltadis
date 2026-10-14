# Gera os icones do app MESA DELTA (logo DELTADIS sobre fundo ROXO) e troca os icones padrao do projeto Android.
import os, sys, glob
from PIL import Image, ImageDraw, ImageFilter, ImageChops

RES = sys.argv[1]            # .../android/app/src/main/res
LOGO = sys.argv[2]           # apk-mesa-logo.png (logo com fundo branco)
ROXO = (63, 28, 152, 255)    # #3F1C98

def logo_sem_fundo(caminho):
    im = Image.open(caminho).convert("RGBA")
    w, h = im.size
    # acha o que e fundo branco ligado as bordas e deixa transparente
    base = im.convert("RGB")
    m = Image.new("L", (w, h), 0)
    px = base.load()
    mp = m.load()
    pilha = [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)]
    vis = set()
    while pilha:
        x, y = pilha.pop()
        if (x, y) in vis or x < 0 or y < 0 or x >= w or y >= h:
            continue
        r, g, b = px[x, y]
        if min(r, g, b) < 238:
            continue
        vis.add((x, y)); mp[x, y] = 255
        pilha += [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    m = m.filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(1.2))   # come a borda branca
    alfa = ImageChops.invert(m)
    im.putalpha(alfa)
    return im.crop(im.getbbox())

logo = logo_sem_fundo(LOGO)

def icone(tam, frac, fundo=True):
    img = Image.new("RGBA", (tam, tam), ROXO if fundo else (0, 0, 0, 0))
    w = int(tam * frac)
    h = int(w * logo.height / logo.width)
    if h > tam * frac:
        h = int(tam * frac); w = int(h * logo.width / logo.height)
    l = logo.resize((w, h), Image.LANCZOS)
    img.alpha_composite(l, ((tam - w) // 2, (tam - h) // 2))
    return img

dens = {"mdpi": 1, "hdpi": 1.5, "xhdpi": 2, "xxhdpi": 3, "xxxhdpi": 4}
for d, k in dens.items():
    pasta = os.path.join(RES, "mipmap-" + d)
    if not os.path.isdir(pasta):
        continue
    icone(int(108 * k), 0.46, fundo=False).save(os.path.join(pasta, "ic_launcher_foreground.png"))   # adaptativo (fundo vem do xml)
    icone(int(48 * k), 0.62).save(os.path.join(pasta, "ic_launcher.png"))
    t = int(48 * k)
    r = icone(t, 0.56)
    m = Image.new("L", (t, t), 0)
    ImageDraw.Draw(m).ellipse((0, 0, t - 1, t - 1), fill=255)
    r.putalpha(m)
    r.save(os.path.join(pasta, "ic_launcher_round.png"))
    print("ok", d)

cor = os.path.join(RES, "values", "ic_launcher_background.xml")
open(cor, "w").write('<?xml version="1.0" encoding="utf-8"?>\n<resources>\n    <color name="ic_launcher_background">#3F1C98</color>\n</resources>\n')
print("fundo roxo ok")

for f in glob.glob(os.path.join(RES, "mipmap-anydpi*", "ic_launcher*.xml")) + glob.glob(os.path.join(RES, "drawable*", "ic_launcher_foreground.xml")):
    os.remove(f)
    print("removido", f)

# previa grande (so para conferir)
if len(sys.argv) > 3:
    icone(512, 0.62).save(sys.argv[3])
