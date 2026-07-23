from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np

W,H=1584,396
FB="/usr/share/fonts/truetype/liberation/"
bold=lambda s:ImageFont.truetype(FB+"LiberationSans-Bold.ttf",s)
reg =lambda s:ImageFont.truetype(FB+"LiberationSans-Regular.ttf",s)

# gradient bg
top=np.array([13,22,50]); bot=np.array([4,7,15])
grad=np.zeros((H,W,3),np.uint8)
for y in range(H): grad[y,:]=(top*(1-y/H)+bot*(y/H)).astype(np.uint8)
yy,xx=np.mgrid[0:H,0:W]
glow=np.exp(-(((xx-1150)/650)**2+((yy-40)/320)**2))
for c,v in enumerate([26,40,80]): grad[:,:,c]=np.clip(grad[:,:,c]+glow*v,0,255).astype(np.uint8)
img=Image.fromarray(grad,'RGB'); d=ImageDraw.Draw(img)
rng=np.random.default_rng(11)
for _ in range(80):
    x,y=rng.integers(0,W),rng.integers(0,H); r=rng.choice([1,1,1,2]); b=int(rng.integers(80,180))
    d.ellipse([x-r,y-r,x+r,y+r],fill=(b,b,min(255,b+25)))

def card(fig_path, box, pad=9):
    x0,y0,x1,y1=box; bw,bh=x1-x0,y1-y0
    im=Image.open(fig_path).convert("RGB")
    a=np.array(im); m=(a<250).any(2); ys,xs=np.where(m)
    im=im.crop((max(xs.min()-3,0),max(ys.min()-3,0),min(xs.max()+3,im.width),min(ys.max()+3,im.height)))
    iw,ih=im.size; s=min((bw-2*pad)/iw,(bh-2*pad)/ih); im=im.resize((int(iw*s),int(ih*s)),Image.LANCZOS)
    # soft shadow layer
    sh=Image.new("RGBA",(W,H),(0,0,0,0))
    ImageDraw.Draw(sh).rounded_rectangle([x0+3,y0+6,x1+3,y1+6],radius=16,fill=(0,0,0,110))
    sh=sh.filter(ImageFilter.GaussianBlur(10)); img.paste(sh,(0,0),sh)
    panel=Image.new("RGBA",(bw,bh),(0,0,0,0))
    ImageDraw.Draw(panel).rounded_rectangle([0,0,bw-1,bh-1],radius=13,fill=(255,255,255,246))
    img.paste(panel,(x0,y0),panel)
    img.paste(im,(x0+(bw-im.width)//2,y0+(bh-im.height)//2))

# hero layout diagram (large, right 45%) + two result plots stacked-ish on top
card("figs3/D02_layout.png",(858,146,1552,352))
card("figs3/F05_dragvs.png",(858,34,1190,140))
card("figs3/F01_shot.png",(1200,34,1552,140))

accent=(102,173,255)
d.text((60,50),"ADITYAVARDHAN MISHRA",font=bold(47),fill=(255,255,255))
d.text((63,110),"Mechanical Engineering   ·   Spacecraft Deployment Systems",font=reg(22),fill=(180,192,216))
d.rounded_rectangle([65,150,152,155],radius=2,fill=accent)
d.text((60,170),"EMOCD",font=bold(31),fill=accent)
d.text((192,178),"Electromagnetic CubeSat Deployer",font=reg(22),fill=(216,224,240))

# stat row — fixed even spacing, clear of bottom-left photo (start x=430)
stats=[("20.4 m/s","programmable ejection"),("12 × 3U","magazine-fed"),
       ("±0.03 m/s","deterministic placement"),("72 kg","ESPA-class")]
x=430
for i,(val,lab) in enumerate(stats):
    d.text((x,298),val,font=bold(27),fill=(255,255,255))
    d.text((x,336),lab,font=reg(16),fill=(150,164,190))
    x+=max(d.textlength(val,font=bold(27)),d.textlength(lab,font=reg(16)))+40

img.save("/mnt/user-data/outputs/EMOCD_LinkedIn_Banner.jpg","JPEG",quality=95)
# safe-zone preview: draw where LinkedIn photo circle sits
prev=img.copy(); pd=ImageDraw.Draw(prev,"RGBA")
pd.ellipse([56,232,216,392],outline=(255,120,120,255),width=3)
pd.text((60,214),"photo zone",font=reg(14),fill=(255,150,150))
prev.save("banner_preview.jpg","JPEG",quality=90)
print("done")
