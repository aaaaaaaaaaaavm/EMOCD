import numpy as np, math
mu=3.986004418e14; Re=6378.137e3; J2=1.08263e-3
def kepE(M,e):
    E=M.copy()
    for _ in range(12): E=E-(E-e*np.sin(E)-M)/(1-e*np.cos(E))
    return E
def pos(a,e,inc,raan,argp,M0,t):
    n=math.sqrt(mu/a**3); p=a*(1-e**2)
    # J2 secular rates
    dO=-1.5*J2*n*(Re/p)**2*math.cos(inc)
    dw= 0.75*J2*n*(Re/p)**2*(5*math.cos(inc)**2-1)
    dM= 0.75*J2*n*(Re/p)**2*math.sqrt(1-e**2)*(3*math.cos(inc)**2-1)
    M=(M0+(n+dM)*t)%(2*np.pi); Om=raan+dO*t; w=argp+dw*t
    E=kepE(M,e)
    nu=2*np.arctan2(np.sqrt(1+e)*np.sin(E/2), np.sqrt(1-e)*np.cos(E/2))
    r=a*(1-e*np.cos(E))
    xo=r*np.cos(nu); yo=r*np.sin(nu)
    cO,sO,ci,si,cw,sw=np.cos(Om),np.sin(Om),math.cos(inc),math.sin(inc),np.cos(w),np.sin(w)
    x=(cO*cw-sO*sw*ci)*xo+(-cO*sw-sO*cw*ci)*yo
    y=(sO*cw+cO*sw*ci)*xo+(-sO*sw+cO*cw*ci)*yo
    z=(sw*si)*xo+(cw*si)*yo
    return np.stack([x,y,z],-1)

alt=450e3; r0=Re+alt; v0=math.sqrt(mu/r0); inc=math.radians(51.6)
t=np.arange(0,30*86400,10.0)
# stage: circular
stage=pos(r0,1e-6,inc,0,0,0,t)
dv=25.0
def sat_elems(nu_fire):
    # fire prograde at true anomaly position nu_fire on the (circular) stage orbit:
    # new orbit: perigee at firing point -> argp = nu_fire, e from dv
    v2=v0+dv; a=1/(2/r0-v2**2/mu); e=1-r0/a
    return a,e,inc,0.0,nu_fire,0.0  # M0=0 at perigee = firing point... offset in time handled by firing sequence; simplify: all fired near t=0 at different points
scenA=[sat_elems(0.0) for i in range(12)]                       # all fired at same point
scenB=[sat_elems(i*2*np.pi/12) for i in range(12)]              # spread around orbit
for name,scen in [("A: all shots at one point",scenA),("B: spread over true anomaly",scenB)]:
    mins_stage=[]; 
    sats=[pos(*el,t) for el in scen]
    for s in sats:
        d=np.linalg.norm(s-stage,axis=1); mins_stage.append(d.min())
    # sat-sat min (sample pairs)
    ss=[]
    for i in range(12):
        for j in range(i+1,12):
            d=np.linalg.norm(sats[i]-sats[j],axis=1); ss.append(d.min())
    print(f"{name}: min sat-stage dist over 30 d = {min(mins_stage)/1e3:.1f} km; min sat-sat = {min(ss)/1e3:.1f} km")
print("(Note: 10 s sampling -> sub-km encounters bounded, not resolved; screening-level result. All shots prograde: sats sit above stage except at perigee.)")
