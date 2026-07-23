import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle, FancyBboxPatch, Circle, Polygon
import matplotlib.font_manager as fm

fig, ax = plt.subplots(figsize=(12, 6.75), dpi=100)
ax.set_xlim(0, 16); ax.set_ylim(0, 9); ax.axis('off')
ax.set_facecolor('#0d1b2a'); fig.patch.set_facecolor('#0d1b2a')

INK='#e8eef5'; ACC='#4ea8de'; WARM='#f6bd60'; MUT='#8fa3b8'

# subtle starfield
import numpy as np
rng=np.random.default_rng(7)
for _ in range(90):
    x,y=rng.uniform(0,16),rng.uniform(0,9); s=rng.uniform(0.5,2.2)
    ax.plot(x,y,'.',color='white',alpha=rng.uniform(0.15,0.5),ms=s)

# ---- Earth arc, lower left ----
th=np.linspace(0,2*np.pi,200)
ax.add_patch(plt.Circle((1.5,-2.2),5.0,color='#274060',zorder=1))
ax.add_patch(plt.Circle((1.5,-2.2),5.0,fill=False,ec=ACC,lw=1.5,alpha=0.5,zorder=2))

# ---- spent rocket stage (the "launch pad in space") ----
stage_x=2.4
ax.add_patch(FancyBboxPatch((stage_x,3.1),2.0,2.8,boxstyle='round,pad=0.05',
            fc='#3a506b',ec=INK,lw=1.6,zorder=5))
# nozzle
ax.add_patch(Polygon([[stage_x+0.6,3.1],[stage_x+1.4,3.1],[stage_x+1.15,2.4],[stage_x+0.85,2.4]],
            closed=True,fc='#2b3a4f',ec=INK,lw=1.3,zorder=5))
ax.text(stage_x+1.0,6.15,'spent rocket stage',color=MUT,fontsize=11,ha='center',style='italic')
ax.text(stage_x+1.0,4.9,'(the platform)',color=MUT,fontsize=9.5,ha='center')

# ---- the deployer body mounted on the stage ----
dep_x=4.6
ax.add_patch(FancyBboxPatch((dep_x,3.6),5.2,1.9,boxstyle='round,pad=0.05',
            fc='#1b263b',ec=ACC,lw=2.0,zorder=6))

# magazine of stacked cubesats (left inside deployer)
for i in range(4):
    ax.add_patch(Rectangle((dep_x+0.35,3.8+i*0.36),0.55,0.30,fc=WARM,ec=INK,lw=1.0,zorder=8))
ax.text(dep_x+0.62,5.65,'magazine',color=WARM,fontsize=9.5,ha='center')

# track with sled
track_y=4.15
ax.plot([dep_x+1.3,dep_x+4.7],[track_y,track_y],color=MUT,lw=3,solid_capstyle='round',zorder=7)
ax.plot([dep_x+1.3,dep_x+4.7],[track_y+0.5,track_y+0.5],color=MUT,lw=3,solid_capstyle='round',zorder=7)
# sled carrying one cubesat, mid-track
sled_x=dep_x+2.7
ax.add_patch(Rectangle((sled_x,track_y+0.05),0.9,0.45,fc=ACC,ec=INK,lw=1.2,zorder=9))
ax.add_patch(Rectangle((sled_x+0.17,track_y+0.52),0.55,0.42,fc=WARM,ec=INK,lw=1.0,zorder=10))
ax.text(dep_x+3.0,3.35,'reusable magnetic sled on a linear motor',color=ACC,fontsize=9.5,ha='center',style='italic')

# ---- the ejected cubesat + velocity arrow ----
ax.add_patch(Rectangle((11.3,4.5),0.7,0.55,fc=WARM,ec=INK,lw=1.2,zorder=9))
ax.add_patch(FancyArrowPatch((10.1,4.75),(13.7,4.75),arrowstyle='-|>',
            mutation_scale=26,lw=3,color=WARM,zorder=8))
ax.text(12.5,5.5,'released at a\nchosen speed',color=WARM,fontsize=11,ha='center',fontweight='bold')

# three faint 'future orbits' fanning out
for dy,al in [(1.4,0.9),(0.0,0.6),(-1.4,0.4)]:
    ax.add_patch(FancyArrowPatch((12.6,4.75),(15.4,4.75+dy),arrowstyle='-|>',
                mutation_scale=14,lw=1.3,color=INK,alpha=al*0.5,ls=(0,(4,3)),zorder=6))
ax.text(15.0,2.7,'different orbits,\none satellite at a time',color=MUT,fontsize=9.5,ha='center',style='italic')

# ---- recoil arrow (opposite), small ----
ax.add_patch(FancyArrowPatch((4.5,2.75),(3.2,2.75),arrowstyle='-|>',
            mutation_scale=14,lw=1.5,color='#e07a5f',alpha=0.8,zorder=6))
ax.text(4.9,2.5,'recoil absorbed by the stage',color='#e07a5f',fontsize=8.5,ha='left',alpha=0.9)

# ---- title / caption band ----
ax.text(0.4,8.5,'EMOCD',color=INK,fontsize=30,fontweight='bold',ha='left')
ax.text(0.42,7.75,'an electromagnetic deployer that gives each CubeSat its own orbit',
        color=MUT,fontsize=13,ha='left',style='italic')

ax.text(15.6,0.35,'concept illustration — not to scale',color=MUT,fontsize=8,ha='right',alpha=0.7)

plt.tight_layout(pad=0.3)
plt.savefig('/mnt/user-data/outputs/EMOCD_concept.jpg',dpi=100,facecolor='#0d1b2a',bbox_inches='tight')
print("saved")
