from PIL import Image, ImageDraw, ImageFont
import numpy as np, random

W,H=1584,396
MONO="/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf"
MONOB="/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf"
mono=lambda s:ImageFont.truetype(MONO,s)
monob=lambda s:ImageFont.truetype(MONOB,s)

# ---- desktop backdrop (dark, faint) ----
img=Image.new("RGB",(W,H),(18,20,27))
d=ImageDraw.Draw(img)

def trim(p):
    im=Image.open(p).convert("RGB"); a=np.array(im); m=(a<250).any(2); ys,xs=np.where(m)
    return im.crop((max(xs.min()-3,0),max(ys.min()-3,0),min(xs.max()+3,im.width),min(ys.max()+3,im.height)))

def plot_window(fig, box, title):
    x0,y0,x1,y1=box; bw,bh=x1-x0,y1-y0
    win=Image.new("RGB",(bw,bh),(255,255,255))
    wd=ImageDraw.Draw(win)
    # titlebar
    bar=26; wd.rectangle([0,0,bw,bar],fill=(226,228,232))
    for i,c in enumerate([(255,95,86),(255,189,46),(39,201,63)]):
        wd.ellipse([10+i*18,8,20+i*18,18],fill=c)
    wd.text((72,6),title,font=mono(12),fill=(90,94,100))
    wd.line([0,bar,bw,bar],fill=(200,202,206))
    im=trim(fig); iw,ih=im.size; s=min((bw-14)/iw,(bh-bar-10)/ih)
    im=im.resize((int(iw*s),int(ih*s)),Image.LANCZOS)
    win.paste(im,((bw-im.width)//2,bar+(bh-bar-im.height)//2+2))
    # window border + subtle shadow
    d.rectangle([x0-1,y0-1,x1+1,y1+1],outline=(0,0,0))
    img.paste(win,(x0,y0))

def term_window(box, lines, title="bash — emocd"):
    x0,y0,x1,y1=box; bw,bh=x1-x0,y1-y0
    win=Image.new("RGB",(bw,bh),(18,20,26))
    wd=ImageDraw.Draw(win)
    bar=26; wd.rectangle([0,0,bw,bar],fill=(46,48,56))
    for i,c in enumerate([(255,95,86),(255,189,46),(39,201,63)]):
        wd.ellipse([10+i*18,8,20+i*18,18],fill=c)
    wd.text((70,6),title,font=mono(12),fill=(170,174,182))
    y=bar+8
    for kind,txt in lines:
        col={"p":(120,224,143),"c":(150,150,158),"o":(220,222,228),"n":(240,200,120),"cy":(120,205,255)}[kind]
        f=monob(13) if kind=="p" else mono(13)
        wd.text((12,y),txt,font=f,fill=col); y+=18
    d.rectangle([x0-1,y0-1,x1+1,y1+1],outline=(0,0,0))
    img.paste(win,(x0,y0))

# ---- terminal (left) with real-looking run output ----
term=[
 ("p","(emocd) $ python c3_c4_em.py"),
 ("cy","== winding-resolved motor model =="),
 ("o","Kt = 11.22 N per kA/m,  ripple +/-1.26%"),
 ("o","K_rated=140 kA/m (J=23 A/mm^2): F_cmd=1414 N"),
 ("o","3U: v_exit=20.37 m/s,  a_sat=16.3 g"),
 ("o","shot: 128 ms  Ipk=323 A  sag=4.9%"),
 ("o","drawn=2.63 kJ  eff=40%  coil dT=0.24 K"),
 ("o","closed-loop MC: 3sigma = 0.027 m/s"),
 ("p","(emocd) $ python c1_c2_astro.py"),
 ("cy","== lifetime + drift seeding =="),
 ("o","+20.4 m/s -> lifetime x1.80  (BC-invariant)"),
 ("o","xval Cowell vs avg: 99.4%"),
 ("o","30 deg spacing: 1.4-6.9 d  (drag: 25 d)"),
 ("p","(emocd) $ python solid_mass.py"),
 ("o","DRY 72.3 kg  LOADED 120.3 kg  CG 0.46 m"),
 ("p","(emocd) $ _"),
]
term_window((16,20,556,376),term)

# ---- plot windows (right cluster, slightly overlapping like a messy desktop) ----
plot_window("figs3/D02_layout.png",(600,150,1240,372),"D02_layout.png — Figure 2")
plot_window("figs3/F01_shot.png",(600,20,900,150+2),"F01_shot.png")
plot_window("figs3/F05_dragvs.png",(912,20,1176,150+2),"F05_dragvs.png")
plot_window("figs3/F03_mc.png",(1252,150,1568,340),"F03_mc.png")
plot_window("figs3/F04_life.png",(1188,20,1568,150+2),"F04_life.png")

img.save("/mnt/user-data/outputs/EMOCD_LinkedIn_Banner.jpg","JPEG",quality=94)
print("done", img.size)
