from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np, math

W,H=1584,396
FB="/usr/share/fonts/truetype/liberation/"
mono=lambda s:ImageFont.truetype(FB+"LiberationMono-Regular.ttf",s)
monob=lambda s:ImageFont.truetype(FB+"LiberationMono-Bold.ttf",s)

# ---------- dark blueprint base ----------
base=np.zeros((H,W,3),np.uint8)
base[:]= (10,16,34)                              # deep blueprint navy
# subtle vertical richness
yy,xx=np.mgrid[0:H,0:W]
glow=np.exp(-(((xx-780)/900)**2+((yy-150)/360)**2))
for c,v in enumerate([8,16,30]): base[:,:,c]=np.clip(base[:,:,c]+glow*v,0,255)
img=Image.fromarray(base,'RGB'); d=ImageDraw.Draw(img,'RGBA')

# ---------- grid paper ----------
minor=(60,110,180,55); major=(80,150,230,90)
for x in range(0,W,20): d.line([(x,0),(x,H)],fill=minor,width=1)
for y in range(0,H,20): d.line([(0,y),(W,y)],fill=minor,width=1)
for x in range(0,W,100): d.line([(x,0),(x,H)],fill=major,width=1)
for y in range(0,H,100): d.line([(0,y),(W,y)],fill=major,width=1)

# palette (energetic)
CY=(64,224,255); MAG=(255,88,180); YEL=(255,214,64); GRN=(80,240,160); ORG=(255,150,70); WHT=(232,240,255)

def dim(p1,p2,txt,col=CY,off=0,fs=14):
    (x1,y1),(x2,y2)=p1,p2
    d.line([p1,p2],fill=col+(230,),width=2)
    for (x,y) in (p1,p2):
        d.line([(x,y-5),(x,y+5)],fill=col+(230,),width=2)
    mx,my=(x1+x2)//2,(y1+y2)//2
    tw=d.textlength(txt,font=mono(fs))
    d.rectangle([mx-tw/2-4,my-off-10,mx+tw/2+4,my-off+10],fill=(10,16,34,235))
    d.text((mx-tw/2,my-off-8),txt,font=mono(fs),fill=col)

# ======================================================================
# MAIN ASSEMBLY DRAWING  — side elevation of the deployer, blueprint style
# coordinate frame: track baseline y=250, x from 120..1180
# ======================================================================
bx0,bx1,by=150,1150,238
# --- track / stator rails (double-sided) ---
d.rectangle([bx0,by-6,bx1-120,by+6],outline=CY+(255,),width=2)
d.rectangle([bx0,by-30,bx1-120,by-18],outline=CY+(180,),width=2)   # upper stator
d.rectangle([bx0,by+18,bx1-120,by+30],outline=CY+(180,),width=2)   # lower stator
# hatch the stator windings
for x in range(bx0+8,bx1-128,16):
    d.line([(x,by-30),(x+8,by-18)],fill=CY+(120,),width=1)
    d.line([(x,by+18),(x+8,by+30)],fill=CY+(120,),width=1)

# --- sled (Halbach mover) at ~30% stroke ---
sx=bx0+240
d.rectangle([sx,by-22,sx+90,by+22],outline=MAG+(255,),width=3)
# halbach arrows inside sled
for i,ang in enumerate([90,0,270,180,90,0]):
    cx=sx+10+i*13; cy=by
    dx,dy=int(9*math.cos(math.radians(ang))),int(-9*math.sin(math.radians(ang)))
    d.line([(cx,cy-dy//2),(cx+0,cy+dy//2)],fill=MAG+(220,),width=2)
    d.line([(cx-dx,cy),(cx+dx,cy)] if ang in (0,180) else [(cx,cy-9),(cx,cy+9)],fill=MAG+(200,),width=2)
d.text((sx+4,by-40),"SLED  (Halbach PM mover, 4.86 kg)",font=mono(12),fill=MAG)

# --- ejection arrow / muzzle ---
mzx=bx1-120
d.line([(mzx,by),(mzx+80,by)],fill=YEL+(255,),width=3)
d.polygon([(mzx+80,by-8),(mzx+100,by),(mzx+80,by+8)],fill=YEL+(255,))
d.text((mzx+8,by-26),"20.4 m/s",font=monob(16),fill=YEL)
d.text((mzx+8,by+10),"16.3 g",font=mono(13),fill=YEL)

# --- eddy brake block near muzzle ---
d.rectangle([mzx-70,by-24,mzx-10,by+24],outline=GRN+(255,),width=2)
for x in range(mzx-66,mzx-12,10): d.line([(x,by-24),(x+10,by+24)],fill=GRN+(120,),width=1)
d.text((mzx-96,by+30),"eddy brake +200g cap",font=mono(11),fill=GRN)

# --- cassettes (two, above & below track) as magazine of 6 ---
for side in (-1,1):
    cy=by+side*78
    d.rectangle([bx0+120,cy-24,bx0+120+360,cy+24],outline=ORG+(230,),width=2)
    for k in range(6):
        cxx=bx0+130+k*58
        d.rectangle([cxx,cy-18,cxx+48,cy+18],outline=ORG+(180,),width=1)
    # follower arrow toward track
    d.polygon([(bx0+300,cy-side*24),(bx0+292,cy-side*40),(bx0+308,cy-side*40)],fill=ORG+(220,))
lab_y=by-78-30
d.text((bx0+120,lab_y),"CASSETTE  6 x 3U   (magazine-fed)",font=mono(12),fill=ORG)
d.text((bx0+120,by+78+28),"CASSETTE  6 x 3U",font=mono(12),fill=ORG)

# --- dimension lines ---
dim((bx0,by+128),(bx1-120,by+128),"1.5 m track  (1.3 accel + 0.2 coast-trim)",col=CY,off=0)
dim((bx0,by-118),(sx,by-118),"feed",col=MAG,off=0,fs=12)

# ======================================================================
# TITLE BLOCK (engineering drawing corner) — bottom right
# ======================================================================
tb_x,tb_y=1180,past=0
tbx,tby,tbw,tbh=1188,236,384,150
d.rectangle([tbx,tby,tbx+tbw,tby+tbh],outline=CY+(255,),width=2)
for yy2 in (tby+30,tby+64,tby+98):
    d.line([(tbx,yy2),(tbx+tbw,yy2)],fill=CY+(120,),width=1)
d.line([(tbx+250,tby),(tbx+250,tby+98)],fill=CY+(120,),width=1)
d.text((tbx+10,tby+7),"EMOCD  —  ELECTROMAGNETIC",font=monob(16),fill=WHT)
d.text((tbx+10,tby+34),"CubeSat orbital deployer",font=mono(13),fill=(150,180,220))
d.text((tbx+10,tby+40),"",font=mono(13),fill=WHT)
d.text((tbx+10,tby+70),"linear synchronous motor",font=mono(13),fill=(150,180,220))
d.text((tbx+258,tby+34),"REV  4",font=mono(13),fill=GRN)
d.text((tbx+258,tby+70),"SHT 1/1",font=mono(13),fill=(150,180,220))
d.text((tbx+10,tby+104),"12x 3U  |  ±0.03 m/s  |  72 kg  |  ESPA-G",font=mono(12),fill=YEL)
d.text((tbx+10,tby+126),"drawn-to-analysis  ·  not to scale",font=mono(11),fill=(120,150,190))

# ======================================================================
# top strip: small blueprint callouts (spec chips) 
# ======================================================================
chips=[("v_exit","20.4 m/s",YEL),("thrust Kt","11.2 N/kA·m",CY),("3σ","0.027 m/s",MAG),
       ("lifetime","×1.80",GRN),("net/shot","2.08 kJ",ORG),("eff","40%",CY)]
x=150
for name,val,col in chips:
    w=max(d.textlength(name,font=mono(12)),d.textlength(val,font=monob(15)))+22
    d.rounded_rectangle([x,26,x+w,74],radius=8,outline=col+(230,),width=2,fill=(255,255,255,10))
    d.text((x+11,32),name,font=mono(12),fill=(150,180,220))
    d.text((x+11,50),val,font=monob(15),fill=col)
    x+=w+16

# faint corner registration marks
for (cx,cy) in [(20,20),(W-20,20),(20,H-20),(W-20,H-20)]:
    d.line([(cx-10,cy),(cx+10,cy)],fill=CY+(160,),width=1)
    d.line([(cx,cy-10),(cx,cy+10)],fill=CY+(160,),width=1)

img.convert("RGB").save("/mnt/user-data/outputs/EMOCD_LinkedIn_Banner.jpg","JPEG",quality=95)
print("done",img.size)
