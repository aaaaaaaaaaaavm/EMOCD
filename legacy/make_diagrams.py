import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle, Polygon
plt.rcParams.update({'font.family':'serif','figure.dpi':300,'savefig.bbox':'tight'})

# ---------- D1: system block diagram ----------
fig,ax=plt.subplots(figsize=(7.4,4.4)); ax.axis('off'); ax.set_xlim(0,10); ax.set_ylim(0,6.2)
def box(x,y,w,h,label,fs=8.5,fc='#f2f2f2'):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.06',fc=fc,ec='k',lw=1))
    ax.text(x+w/2,y+h/2,label,ha='center',va='center',fontsize=fs)
def arr(x1,y1,x2,y2,ls='-'):
    ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle='-|>',mutation_scale=11,lw=1,ls=ls,color='k'))
# power chain
box(0.2,4.9,1.9,0.8,'Host power /\nbattery (250 Wh)')
box(2.7,4.9,1.9,0.8,'Supercapacitor\nbank 6 F / 96 V')
box(5.2,4.9,1.9,0.8,'SiC bridge\n(PPU)')
box(7.7,4.9,2.1,0.8,'Ironless LSM stator\n(two-sided, 1.3 m)')
arr(2.1,5.3,2.7,5.3); arr(4.6,5.3,5.2,5.3); arr(7.1,5.3,7.7,5.3)
arr(7.7,5.05,7.15,5.05,ls=':'); ax.text(7.0,4.72,'regen',fontsize=7,ha='center')
# control
box(0.2,3.1,1.9,0.8,'Firing sequencer\n(orbit timing)')
box(2.7,3.1,1.9,0.8,'Velocity servo\n(closed loop)')
box(5.2,3.1,1.9,0.8,'Position sensors\n+ photogates')
box(7.7,3.1,2.1,0.8,'Interlocks: seat sw. /\nattitude-valid / arm')
arr(2.1,3.5,2.7,3.5); arr(5.2,3.5,4.6,3.5); arr(6.2,3.9,6.2,4.9); arr(3.65,3.9,3.65,4.9)
arr(8.75,3.9,8.75,4.9)
# mechanical
box(0.2,1.3,1.9,0.8,'Cassette L (6 sat)\nfollower + gate')
box(2.7,1.3,1.9,0.8,'Escapement +\nsled latch')
box(5.2,1.3,1.9,0.8,'Sled (Halbach,\n4 kg, reusable)')
box(7.7,1.3,2.1,0.8,'Eddy brake +\nring spring')
box(0.2,0.1,1.9,0.8,'Cassette R (6 sat)\nfollower + gate')
arr(2.1,1.7,2.7,1.7); arr(2.1,0.5,2.7,1.4); arr(4.6,1.7,5.2,1.7); arr(7.1,1.7,7.7,1.7)
arr(6.2,2.1,6.2,3.1)
# host interface
box(4.0,-1.1,3.2,0.8,'Host stage: ESPA mount, GNC attitude,\nRCS recoil null (EMOCD-A)',fs=8)
arr(5.6,-0.3,5.6,1.3,ls='--')
ax.set_ylim(-1.3,6.0)
plt.savefig('figs/D01_block.png'); plt.close()

# ---------- D2: layout cross-section (top view) ----------
fig,ax=plt.subplots(figsize=(7.4,3.6)); ax.axis('off'); ax.set_xlim(-0.2,10.2); ax.set_ylim(-0.4,5.4)
# track beam
ax.add_patch(Rectangle((1.0,2.3),8.4,0.5,fc='#d9d9d9',ec='k'))
ax.text(5.2,2.55,'LSM stator track (accel 1.3 m + coast-trim 0.2 m)',ha='center',va='center',fontsize=8)
# sled at breech
ax.add_patch(Rectangle((1.2,2.05),0.9,1.0,fc='#8c8c8c',ec='k'))
ax.text(1.65,3.25,'sled\n(home)',ha='center',fontsize=7)
# cassettes
for y0,lab in [(3.6,'Cassette L: 6 × 3U, follower →'),(0.5,'Cassette R: 6 × 3U, follower →')]:
    ax.add_patch(Rectangle((0.6,y0),4.4,1.1,fc='#f2f2f2',ec='k'))
    for i in range(6):
        ax.add_patch(Rectangle((0.75+i*0.7,y0+0.15),0.6,0.8,fc='white',ec='k',lw=0.8))
    ax.text(2.8,y0+1.25 if y0>2 else y0-0.28,lab,fontsize=7.5,ha='center')
# feed arrows
ax.add_patch(FancyArrowPatch((1.65,3.6),(1.65,3.1),arrowstyle='-|>',mutation_scale=10,color='k'))
ax.add_patch(FancyArrowPatch((1.65,1.6),(1.65,2.05),arrowstyle='-|>',mutation_scale=10,color='k'))
# brake
ax.add_patch(Rectangle((8.6,2.1),0.8,0.9,fc='#bfbfbf',ec='k',hatch='//'))
ax.text(9.0,3.15,'eddy brake\n+ ring spring',ha='center',fontsize=7)
# muzzle
ax.add_patch(FancyArrowPatch((9.4,2.55),(10.1,2.55),arrowstyle='-|>',mutation_scale=14,color='k'))
ax.text(9.8,2.85,'ejection\n22.4 m/s',fontsize=7,ha='center')
# supercap bay
ax.add_patch(Rectangle((5.6,3.6),2.2,1.1,fc='#e8e8e8',ec='k'))
ax.text(6.7,4.15,'Supercap bank\n+ PPU + avionics',ha='center',fontsize=7.5)
ax.add_patch(Rectangle((5.6,0.5),2.2,1.1,fc='#e8e8e8',ec='k'))
ax.text(6.7,1.05,'Battery, thermal,\nharness bay',ha='center',fontsize=7.5)
ax.text(5.0,-0.25,'ESPA Grande envelope ~1.07 × 1.17 m (plan view, not to scale)',fontsize=8,ha='center',style='italic')
plt.savefig('figs/D02_layout.png'); plt.close()
print("diagrams done")
