import numpy as np, math, json

mu = 3.986004418e14; Re = 6378.137e3
# C1: Static exponential atmosphere (Vallado Table 8-4 style, mean solar activity) — MODEL LIMITATION FLAGGED
# (base_alt_km, rho0 kg/m^3, H km)
tbl = [(0,1.225,7.249),(25,3.899e-2,6.349),(30,1.774e-2,6.682),(40,3.972e-3,7.554),(50,1.057e-3,8.382),
(60,3.206e-4,7.714),(70,8.770e-5,6.549),(80,1.905e-5,5.799),(90,3.396e-6,5.382),(100,5.297e-7,5.877),
(110,9.661e-8,7.263),(120,2.438e-8,9.473),(130,8.484e-9,12.636),(140,3.845e-9,16.149),(150,2.070e-9,22.523),
(180,5.464e-10,29.740),(200,2.789e-10,37.105),(250,7.248e-11,45.546),(300,2.418e-11,53.628),
(350,9.518e-12,53.298),(400,3.725e-12,58.515),(450,1.585e-12,62.828),(500,6.967e-13,63.822),
(600,1.454e-13,71.835),(700,3.614e-14,88.667),(800,1.170e-14,124.64),(900,5.245e-15,181.05),(1000,3.019e-15,268.00)]
bases = np.array([t[0] for t in tbl]); rhos = np.array([t[1] for t in tbl]); Hs = np.array([t[2] for t in tbl])
def rho(h_km):
    i = np.searchsorted(bases, h_km, side='right')-1
    i = np.clip(i,0,len(tbl)-1)
    return rhos[i]*np.exp(-(h_km-bases[i])/Hs[i])

def lifetime(a0, e0, BC, max_years=30):
    """Per-revolution orbit-averaged decay via Gauss tangential equations. BC*=m/(Cd A) kg/m2."""
    a, e = a0, e0
    t = 0.0
    E = np.linspace(0, 2*np.pi, 181)
    while True:
        n = math.sqrt(mu/a**3); T = 2*np.pi/n
        r = a*(1-e*np.cos(E))
        h_km = (r-Re)/1e3
        if (a*(1-e)-Re)/1e3 < 120: return t/86400/365.25, 'decayed'
        v = np.sqrt(mu*(2/r-1/a))
        cosnu = (np.cos(E)-e)/(1-e*np.cos(E))
        f_t = -0.5*rho(h_km)*v**2/BC          # tangential drag decel (m/s^2)
        dt_dE = (1-e*np.cos(E))/n
        da = np.trapezoid(2*a**2*v/mu*f_t*dt_dE, E)
        de = np.trapezoid(2*(e+cosnu)/v*f_t*dt_dE, E)
        # adaptive multi-rev step: decay slow at high alt
        k = max(1, int(min( abs(0.05e3/ (abs(da)+1e-9)), 5000)))  # step so a changes <=50 m... cap 5000 revs
        a += da*k; e = max(0.0, e+de*k); t += T*k
        if t > max_years*365.25*86400: return max_years, 'survived_cap'

BCs = [40, 61, 90]   # kg/m^2 : high-drag 3U, nominal (4kg/(2.2*0.03)), low-drag
cases = []
for alt in [350, 400, 450, 500]:
    r0 = Re+alt*1e3; v0 = math.sqrt(mu/r0)
    for dv in [0, 15, 25]:
        v2 = v0+dv; a = 1/(2/r0 - v2**2/mu); e = 1-r0/a if dv>0 else 0.0
        apo = (2*a-r0-Re)/1e3 if dv>0 else alt
        for BC in BCs:
            L, st = lifetime(a, e, BC)
            cases.append(dict(alt=alt, dv=dv, apo=round(apo), BC=BC, life_yr=round(L,2), status=st))
print(f"{'fire alt':>8} {'dv':>4} {'apogee':>7} {'BC':>4} {'lifetime yr':>12}")
base = {}
for c in cases:
    key=(c['alt'],c['BC'])
    if c['dv']==0: base[key]=c['life_yr']
    ratio = c['life_yr']/base[key] if base.get(key) else float('nan')
    print(f"{c['alt']:>8} {c['dv']:>4} {c['apo']:>7} {c['BC']:>4} {c['life_yr']:>12} {'(x%.2f)'%ratio if c['dv']>0 else ''} {c['status'] if c['status']!='decayed' else ''}")

print("\n=== C2: drift seeding vs differential drag ===")
for alt in [450, 500]:
    r0=Re+alt*1e3; v0=math.sqrt(mu/r0); T=2*np.pi*math.sqrt(r0**3/mu)
    for dv in [2,5,10]:
        da = 2*r0**2*dv/ (mu/v0) / r0  # = 2 a dv / v
        da = 2*r0*dv/v0
        dT = 3*np.pi*da/ (v0)  # dT = 3*pi*da/(n*a) ... use dT/T = 1.5 da/a
        dT = 1.5*da/r0*T
        drift_per_day = dT/T * 2*np.pi*r0 * (86400/T) /1e3  # km/day along-track
        deg_day = dT/T*360*(86400/T)
        t30 = 30/deg_day
        print(f"alt {alt}, ddv={dv} m/s: da={da/1e3:.1f} km, drift={drift_per_day:.0f} km/day = {deg_day:.2f} deg/day -> 30 deg in {t30:.1f} days")
