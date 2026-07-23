import numpy as np, math, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams.update({'font.family':'serif','font.size':10,'axes.grid':True,'grid.alpha':0.3,
'figure.dpi':300,'savefig.bbox':'tight','axes.spines.top':False,'axes.spines.right':False})
mu=3.986004418e14; Re=6378.137e3
FIG='figs/'

# ---------- F1/F2: shot ODE profile ----------
m_sat,m_sled=4.0,4.0; m=m_sat+m_sled
accel_zone=1.30; track=1.5
F_cmd=1717*0.9
C_bank=6.0; V0=96.0
eta=0.82; dt=1e-4
x=v=t=0; Vc=V0; rows=[]
while x<accel_zone:
    a=F_cmd/m; v+=a*dt; x+=v*dt; t+=dt
    P=F_cmd*v/eta+200; I=P/max(Vc,40); Vc-=I*dt/C_bank
    rows.append((t,x,v,Vc,I,F_cmd))
arr=np.array(rows)
# coast-trim
t2=np.linspace(arr[-1,0], arr[-1,0]+(track-accel_zone)/v, 40)
fig,ax=plt.subplots(1,2,figsize=(7.2,2.8))
ax[0].plot(arr[:,1],arr[:,2],'k-')
ax[0].plot([accel_zone,track],[v,v],'k--',lw=1)
ax[0].axvspan(accel_zone,track,alpha=0.12,color='gray')
ax[0].set_xlabel('Position along track (m)'); ax[0].set_ylabel('Velocity (m/s)')
ax[0].annotate('coast-trim\nzone',(1.38,8),ha='center',fontsize=8)
ax[0].set_title('(a) Velocity profile')
ax[1].plot(arr[:,0]*1e3,arr[:,3],'k-',label='Bank voltage (V)')
ax2=ax[1].twinx(); ax2.plot(arr[:,0]*1e3,arr[:,4],'k:',label='Current (A)'); ax2.spines['right'].set_visible(True)
ax[1].set_xlabel('Time (ms)'); ax[1].set_ylabel('Bank voltage (V)'); ax2.set_ylabel('Current (A)')
ax[1].set_title('(b) Electrical profile')
lines=[plt.Line2D([],[],color='k',ls='-'),plt.Line2D([],[],color='k',ls=':')]
ax[1].legend(lines,['Bank voltage','Current'],loc='center right',fontsize=8)
plt.tight_layout(); plt.savefig(FIG+'F01_shot_profile.png'); plt.close()
v_exit=v

# ---------- F3: Monte Carlo ----------
rng=np.random.default_rng(1); N=4000
vs=[]
for _ in range(N):
    Bf=1+rng.normal(0,0.01); mf=m*(1+rng.normal(0,0.0067)); Ff=F_cmd*Bf*(1+rng.normal(0,0.0067))
    vs.append(math.sqrt(2*Ff/mf*accel_zone))
vs=np.array(vs)
v_cl=vs.mean()+rng.normal(0,0.05/3,N)+vs.mean()*rng.normal(0,0.001/3,N)
fig,ax=plt.subplots(figsize=(4.6,2.9))
ax.hist(vs,60,alpha=0.55,color='gray',label=f'Open-loop (3$\\sigma$={3*vs.std():.2f} m/s)')
ax.hist(v_cl,60,alpha=0.75,color='k',label=f'Closed-loop (3$\\sigma$={3*v_cl.std():.3f} m/s)')
ax.set_xlabel('Exit velocity (m/s)'); ax.set_ylabel('Count'); ax.legend(fontsize=8)
plt.savefig(FIG+'F03_montecarlo.png'); plt.close()

# ---------- F4: lifetime (re-run C1 compact) ----------
tbl=[(150,2.070e-9,22.523),(180,5.464e-10,29.740),(200,2.789e-10,37.105),(250,7.248e-11,45.546),(300,2.418e-11,53.628),
(350,9.518e-12,53.298),(400,3.725e-12,58.515),(450,1.585e-12,62.828),(500,6.967e-13,63.822),(600,1.454e-13,71.835),(700,3.614e-14,88.667)]
bases=np.array([x[0] for x in tbl]); rhos=np.array([x[1] for x in tbl]); Hs=np.array([x[2] for x in tbl])
def rho(h):
    i=np.clip(np.searchsorted(bases,h,side='right')-1,0,len(tbl)-1)
    return rhos[i]*np.exp(-(h-bases[i])/Hs[i])
def lifetime(a0,e0,BC):
    a,e,t=a0,e0,0.0
    E=np.linspace(0,2*np.pi,181)
    while True:
        n=math.sqrt(mu/a**3); T=2*np.pi/n
        r=a*(1-e*np.cos(E)); h=(r-Re)/1e3
        if (a*(1-e)-Re)/1e3<120: return t/86400/365.25
        vv=np.sqrt(mu*(2/r-1/a)); cosnu=(np.cos(E)-e)/(1-e*np.cos(E))
        ft=-0.5*rho(h)*vv**2/BC; dtdE=(1-e*np.cos(E))/n
        da=np.trapezoid(2*a**2*vv/mu*ft*dtdE,E); de=np.trapezoid(2*(e+cosnu)/vv*ft*dtdE,E)
        k=max(1,int(min(abs(50/(abs(da)+1e-9)),5000)))
        a+=da*k; e=max(0,e+de*k); t+=T*k
        if t>30*365.25*86400: return 30.0
BC=61.0
alts=np.array([350,375,400,425,450,475,500])
L0=[];L15=[];L25=[]
for alt in alts:
    r0=Re+alt*1e3; v0=math.sqrt(mu/r0)
    L0.append(lifetime(r0,1e-6,BC))
    for dv,L in [(15,L15),(25,L25)]:
        a=1/(2/r0-(v0+dv)**2/mu); L.append(lifetime(a,1-r0/a,BC))
fig,ax=plt.subplots(figsize=(4.8,3.0))
ax.semilogy(alts,L0,'ko-',label='Circular (no boost)')
ax.semilogy(alts,L15,'ks--',mfc='white',label='+15 m/s prograde')
ax.semilogy(alts,L25,'k^:',mfc='gray',label='+25 m/s prograde')
ax.set_xlabel('Deployment altitude (km)'); ax.set_ylabel('Orbital lifetime (years)')
ax.legend(fontsize=8)
plt.savefig(FIG+'F04_lifetime.png'); plt.close()

# ---------- F5: drift seeding ----------
fig,ax=plt.subplots(figsize=(4.8,3.0))
alt=450; r0=Re+alt*1e3; v0=math.sqrt(mu/r0); T=2*np.pi*math.sqrt(r0**3/mu)
tdays=np.linspace(0,10,200)
for dv,ls in [(2,'-'),(5,'--'),(10,':')]:
    da=2*r0*dv/v0; dT=1.5*da/r0*T
    deg_day=dT/T*360*(86400/T)
    ax.plot(tdays,deg_day*tdays,'k',ls=ls,label=f'$\\Delta$v split = {dv} m/s')
ax.axhline(30,color='gray',lw=1); ax.text(0.2,31,'30$^\\circ$ target spacing',fontsize=8)
ax.set_xlabel('Time since deployment (days)'); ax.set_ylabel('Along-track separation (deg)')
ax.legend(fontsize=8); ax.set_ylim(0,120)
plt.savefig(FIG+'F05_drift.png'); plt.close()

# ---------- F6: conjunction (re-run compact C5b) ----------
J2=1.08263e-3
def kepE(M,e):
    E=M.copy()
    for _ in range(15): E=E-(E-e*np.sin(E)-M)/(1-e*np.cos(E))
    return E
def pos(a,e,inc,raan,argp,M0,t):
    n=math.sqrt(mu/a**3); p=a*(1-e**2)
    dO=-1.5*J2*n*(Re/p)**2*math.cos(inc); dw=0.75*J2*n*(Re/p)**2*(5*math.cos(inc)**2-1)
    dM=0.75*J2*n*(Re/p)**2*math.sqrt(1-e**2)*(3*math.cos(inc)**2-1)
    M=(M0+(n+dM)*t); Om=raan+dO*t; w=argp+dw*t
    E=kepE(M%(2*np.pi),e)
    nu=2*np.arctan2(np.sqrt(1+e)*np.sin(E/2),np.sqrt(1-e)*np.cos(E/2))
    r=a*(1-e*np.cos(E)); xo=r*np.cos(nu); yo=r*np.sin(nu)
    cO,sO=np.cos(Om),np.sin(Om); ci,si=math.cos(inc),math.sin(inc); cw,sw=np.cos(w),np.sin(w)
    return np.stack([(cO*cw-sO*sw*ci)*xo+(-cO*sw-sO*cw*ci)*yo,
                     (sO*cw+cO*sw*ci)*xo+(-sO*sw+cO*cw*ci)*yo,(sw*si)*xo+(cw*si)*yo],-1)
alt=450e3; r0=Re+alt; v0=math.sqrt(mu/r0); inc=math.radians(51.6)
dv=25.0; v2=v0+dv; a1=1/(2/r0-v2**2/mu); e1=1-r0/a1
t=np.arange(0,30*86400,10.0); n0=math.sqrt(mu/r0**3)
stage=pos(r0,1e-6,inc,0,0,0,t)
fig,ax=plt.subplots(figsize=(5.4,3.0))
mins=[]
for k in range(12):
    tk=k*1200.0; argp=n0*tk%(2*np.pi); n1=math.sqrt(mu/a1**3)
    s=pos(a1,e1,inc,0,argp,-n1*tk,t)
    mask=t>tk+3600
    d=np.linalg.norm(s[mask]-stage[mask],axis=1)/1e3
    mins.append(d.min())
    if k==0: ax.plot(t[mask]/86400,d,color='gray',lw=0.4,alpha=0.8,label='Sat 1 – stage range')
ax.axhline(min(mins),color='k',ls='--',lw=1,label=f'Fleet minimum = {min(mins):.0f} km')
ax.set_xlabel('Time (days)'); ax.set_ylabel('Separation distance (km)')
ax.legend(fontsize=8); ax.set_ylim(0,None)
plt.savefig(FIG+'F06_conjunction.png'); plt.close()

# ---------- F7: payload family ----------
F=1717*0.9
fam=[(1.3,'1U'),(4,'3U'),(8,'6U'),(12,'12U')]
vsx=[]; gs=[]
for ms,_ in fam:
    a=min(F/(ms+4),25*9.81); vsx.append(math.sqrt(2*a*1.3)); gs.append(ms*0+ a/9.81)
fig,ax=plt.subplots(figsize=(4.6,2.9))
xpos=np.arange(4)
b=ax.bar(xpos,vsx,0.5,color='gray',edgecolor='k')
ax.set_xticks(xpos); ax.set_xticklabels([f[1] for f in fam])
ax.set_ylabel('Exit velocity (m/s)'); ax.set_xlabel('Payload class')
for i,(vv,gg) in enumerate(zip(vsx,gs)):
    ax.text(i,vv+0.5,f'{vv:.1f} m/s\n({gg:.0f} g)',ha='center',fontsize=8)
ax.set_ylim(0,32)
plt.savefig(FIG+'F07_family.png'); plt.close()

# ---------- F8: eddy brake ----------
sig=5.8e7; tf=0.004; B=0.85; m_s=4.0; A=0.004
c=sig*tf*B**2*A
vv=v_exit; xx=0; hist=[]
while vv>1.0:
    Fb=min(c*vv, m_s*200*9.81)   # taper-limited to 200 g
    aa=Fb/m_s; vv-=aa*1e-4; xx+=vv*1e-4; hist.append((xx,vv,Fb))
h=np.array(hist)
fig,ax=plt.subplots(figsize=(4.8,2.9))
ax.plot(h[:,0]*100,h[:,1],'k-')
ax.set_xlabel('Distance into brake (cm)'); ax.set_ylabel('Sled velocity (m/s)')
ax2=ax.twinx(); ax2.plot(h[:,0]*100,h[:,2]/(m_s*9.81),'k:'); ax2.set_ylabel('Deceleration (g)'); ax2.spines['right'].set_visible(True)
ax.legend([plt.Line2D([],[],color='k'),plt.Line2D([],[],color='k',ls=':')],['Velocity','Deceleration'],fontsize=8)
plt.savefig(FIG+'F08_brake.png'); plt.close()

# ---------- F9: tip-off budget ----------
I=0.042
items=[('Trim force ×\nCoM offset',10*0.005*0.020),('Rail clearance\ncouple',2*0.010*0.050),
('Guide release\nspring-back',0.0008),('Sled rate\nresidual',I*math.radians(0.05))]
fig,ax=plt.subplots(figsize=(4.8,2.9))
vals=[math.degrees(d/I) for _,d in items]
ax.bar(range(4),vals,0.5,color='gray',edgecolor='k')
ax.axhline(5,color='k',ls='--',lw=1); ax.text(2.6,5.1,'NRCSD-class requirement (5 deg/s)',fontsize=7)
ax.axhline(2,color='k',ls=':',lw=1); ax.text(3.0,2.1,'target (2 deg/s)',fontsize=7)
ax.set_xticks(range(4)); ax.set_xticklabels([i[0] for i in items],fontsize=7)
ax.set_ylabel('Tip-off contribution (deg/s)')
plt.savefig(FIG+'F09_tipoff.png'); plt.close()

# ---------- F10: mass rollup ----------
mass={'Structure &\nbracket':27,'Stator (Cu +\nformers)':36,'Sled':4,'Brake +\nspring':3,
'Cassettes ×2':9,'Supercap\n+ PPU':12,'Thermal':6,'Avionics +\nharness':8}
fig,ax=plt.subplots(figsize=(5.2,2.9))
ax.barh(range(len(mass)),list(mass.values()),color='gray',edgecolor='k')
ax.set_yticks(range(len(mass))); ax.set_yticklabels(list(mass.keys()),fontsize=8)
ax.set_xlabel('Mass (kg)'); ax.invert_yaxis()
ax.text(30,6.5,f'Dry total ≈ {sum(mass.values())} kg\nLoaded (12×4 kg) ≈ {sum(mass.values())+48} kg',fontsize=8)
plt.savefig(FIG+'F10_mass.png'); plt.close()

print("exit velocity:",round(v_exit,1))
import os
for f in sorted(os.listdir('figs')): print(f)
