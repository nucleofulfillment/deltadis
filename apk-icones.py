# Gera os icones do app (logo DELTADIS) e troca os icones padrao do projeto Android.
import os, sys
from PIL import Image, ImageDraw

RES = sys.argv[1]            # .../android/app/src/main/res
LOGO = sys.argv[2]           # apk-logo.png
logo = Image.open(LOGO).convert("RGBA")
BG = (255, 255, 255, 255)

def com_logo(tam, frac):
    """Quadrado tam x tam, fundo branco, logo centralizada ocupando 'frac' da largura."""
    img = Image.new("RGBA", (tam, tam), BG)
    w = int(tam * frac)
    h = int(w * logo.height / logo.width)
    l = logo.resize((w, h), Image.LANCZOS)
    img.alpha_composite(l, ((tam - w) // 2, (tam - h) // 2))
    return img

dens = {"mdpi": 1, "hdpi": 1.5, "xhdpi": 2, "xxhdpi": 3, "xxxhdpi": 4}
for d, k in dens.items():
    pasta = os.path.join(RES, "mipmap-" + d)
    if not os.path.isdir(pasta):
        continue
    # icone adaptativo (108dp): logo dentro da area segura
    fg = com_logo(int(108 * k), 0.50)
    fg.save(os.path.join(pasta, "ic_launcher_foreground.png"))
    # icone antigo quadrado (48dp)
    q = com_logo(int(48 * k), 0.70)
    q.save(os.path.join(pasta, "ic_launcher.png"))
    # icone redondo (48dp)
    t = int(48 * k)
    r = com_logo(t, 0.60)
    m = Image.new("L", (t, t), 0)
    ImageDraw.Draw(m).ellipse((0, 0, t - 1, t - 1), fill=255)
    r.putalpha(m)
    r.save(os.path.join(pasta, "ic_launcher_round.png"))
    print("ok", d)

# fundo do icone adaptativo = branco
cor = os.path.join(RES, "values", "ic_launcher_background.xml")
open(cor, "w").write('<?xml version="1.0" encoding="utf-8"?>\n<resources>\n    <color name="ic_launcher_background">#FFFFFF</color>\n</resources>\n')
print("fundo branco ok")
