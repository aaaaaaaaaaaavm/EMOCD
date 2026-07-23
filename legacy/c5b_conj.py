import numpy as np, math
mu=3.986004418e14; Re=6378.137e3; J2=1.08263e-3
def kepE(M,e):
    E=M.copy()
    for _ in range(15): E=E-(E-e*np.sin(E)-M)/(1-e*np.cos(E))
    return E
def pos(a,e,inc,raan,argp,M0,t):
    n=math.sqrt(mu/a**3); p=a*(1-e**2)
    dO=-1.5*J2*n*(Re/p)**2*math.cos(inc)
    dw= 0.75*J2*n*(Re/p)**2*(5*math.cos(inc)**2-1)
    dM= 0.75*J2*n*(Re/p)**2*math.sqrt(1-e**2)*(3*math.cos(inc)**2-1)
    M=(M0+(n+dM)*t); Om=raan+dO*t; w=argp+dw*t
    E=kepE(M%(2*np.pi),e)
    nu=2*np.arctan2(np.sqrt(1+e)*np.sin(E/2), np.sqrt(1-e)*np.cos(E/2))
    r=a*(1-e*np.cos(E))
    xo=r*np.cos(nu); yo=r*np.sin(nu)
    out=np.empty(xo.shape+(3,))
    cO,sO=np.cos(Om),np.sin(Om); ci,si=math.cos(inc),math.sin(inc); cw,sw=np.cos(w),np.sin(w)
    out[...,0]=(cO*cw-sO*sw*ci)*xo+(-cO*sw-sO*cw*ci)*yo
    out[...,1]=(sO*cw+cO*sw*ci)*xo+(-sO*sw+cO*cw*ci)*yo
    out[...,2]=(sw*si)*xo+(cw*si)*yo
    return out

alt=450e3; r0=Re+alt; v0=math.sqrt(mu/r0); inc=math.radians(51.6)
T0=2*np.pi*math.sqrt(r0**3/mu)
dv=25.0; v2=v0+dv; a1=1/(2/r0-v2**2/mu); e1=1-r0/a1
T1=2*np.pi*math.sqrt(a1**3/mu); dT=T1-T0
print(f"stage T={T0:.0f} s, sat T={T1:.0f} s, dT={dT:.1f} s/orbit -> phase realignment ~ {T0/dT:.0f} orbits = {T0/dT*T0/86400:.1f} days")

t=np.arange(0,30*86400,5.0)
# stage circular; theta_stage(t) = n0 t (measured from firing node)
# Fire sat k at t_k = k*20 min, when stage is at angle n0*t_k. Sat perigee = that angle; sat M0 such that at t_k sat is at perigee.
n0=2*np.pi/T0
stage=pos(r0,1e-6,inc,0.0,0.0,0.0,t)
mins_stage=[]; sats=[]; tks=[]
for k in range(12):
    tk=k*1200.0
    argp = n0*tk % (2*np.pi)     # perigee at stage's position at firing
    n1=math.sqrt(mu/a1**3)
    M0 = -n1*tk                   # so M(tk)=0 (at perigee) at firing time
    s=pos(a1,e1,inc,0.0,argp,M0,t)
    sats.append(s); tks.append(tk)
    mask = t > tk+3600            # exclude first hour after own release
    d=np.linalg.norm(s[mask]-stage[mask],axis=1)
    mins_stage.append(d.min())
print(f"scenario: 12 shots, 20 min apart, all prograde 25 m/s, spread by firing time")
print(f"min sat-stage distance (excl. 1st hr): {min(mins_stage)/1e3:.1f} km  | median {np.median(mins_stage)/1e3:.1f} km")
ss=[]
for i in range(12):
    for j in range(i+1,12):
        mask=t>max(tks[i],tks[j])+3600
        d=np.linalg.norm(sats[i][mask]-sats[j][mask],axis=1); ss.append(d.min())
print(f"min sat-sat distance: {min(ss)/1e3:.1f} km")
# with stage disposal at day 2:
mins2=[]
for k,s in enumerate(sats):
    mask=(t>tks[k]+3600)&(t<2*86400)
    d=np.linalg.norm(s[mask]-stage[mask],axis=1); mins2.append(d.min())
print(f"if stage disposed at day 2: min sat-stage before disposal = {min(mins2)/1e3:.1f} km")
