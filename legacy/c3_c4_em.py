import numpy as np, math

print("=== C3: Halbach field & motor constant ===")
Br=1.30; d=0.008; lam=0.048; k=2*math.pi/lam; M=4
B0 = Br*(1-math.exp(-k*d))*(math.sin(math.pi/M)/(math.pi/M))
gap=0.012  # winding space between two arrays (m): 10 mm winding + 2x1 mm clearance
y_mid = gap/2
B_mid_one = B0*math.exp(-k*(y_mid))
B_eff = 2*B_mid_one*0.9  # two opposed arrays, 0.9 spatial-average factor over winding depth
print(f"B0(surface)={B0:.3f} T, per-array at winding mid ({y_mid*1e3:.0f} mm): {B_mid_one:.3f} T, effective two-sided <B>~{B_eff:.3f} T")

# active area: sled 0.34 m long x 0.09 m wide, both faces
A_face=0.34*0.09; A=2*A_face
K_sheet = 45e3  # A/m surface current (adiabatic pulse rating)
F_max = B_eff*K_sheet*A
print(f"active area {A:.3f} m^2, K={K_sheet/1e3:.0f} kA/m -> F_max = {F_max:.0f} N")

print("\n=== C3: shot ODE with supercap sag (4 kg sat + 4 kg sled, 1.5 m track) ===")
m_sat, m_sled = 4.0, 4.0; m=m_sat+m_sled
track=1.50; accel_zone=1.30; trim_zone=track-accel_zone
g_cap=25*9.81
F_cmd = min(F_max*0.9, m*g_cap*m_sat/m)  # limit by sat g: a<=25g -> F<=m_tot*a
F_cmd = min(F_max*0.9, m*(25*9.81))      # a = F/m ; sat feels a too -> F <= m*25g
kF = B_eff*0.34*2*0.9   # N per (A-turn of sheet-equivalent)... use F=kF*Ieq with Ieq=K*width_eff
# simpler: command force directly; compute electrical from F: P_elec = F*v/eta_inst + I^2R
eta_motor=0.82
C_bank=6.0; V0=96.0; ESR=0.012  # 32s x ~200F cells -> 6.25F, ESR ~12 mOhm total
dt=1e-4; x=v=0.0; t=0; Vc=V0; E_drawn=0
log=[]
while x<accel_zone:
    F = F_cmd
    a = F/m; v+=a*dt; x+=v*dt; t+=dt
    P = F*v/eta_motor + 200  # +200W electronics
    I = P/max(Vc,40)
    Vc -= I*dt/C_bank
    E_drawn += P*dt
    log.append((t,x,v,Vc,I,F))
v_release_target=v
# trim zone: servo small corrections, F~0
t_trim = trim_zone/v; t+=t_trim; x=track
arr=np.array(log)
print(f"accel end: v={v:.1f} m/s at x={accel_zone} m, t={t*1e3:.0f} ms, a={F_cmd/m/9.81:.1f} g (sat limit 25 g)")
print(f"peak current={arr[:,4].max():.0f} A, bank sag {V0:.0f}->{arr[:,3].min():.1f} V ({(1-arr[:,3].min()/V0)*100:.1f}%)")
print(f"energy drawn={E_drawn/1e3:.2f} kJ, payload KE={0.5*m_sat*v**2/1e3:.2f} kJ, sled KE={0.5*m_sled*v**2/1e3:.2f} kJ")
print(f"end-to-end eff (payload KE/drawn) = {0.5*m_sat*v**2/E_drawn*100:.0f}% (before regen credit)")
E_regen = 0.5*m_sled*v**2*0.55
print(f"regen credit ~55% of sled KE = {E_regen/1e3:.2f} kJ -> net {(E_drawn-E_regen)/1e3:.2f} kJ/shot, eff {0.5*m_sat*v**2/(E_drawn-E_regen)*100:.0f}%")

print("\n=== C3: Monte Carlo velocity dispersion ===")
rng=np.random.default_rng(1)
N=4000
# open-loop: B +-3%, mass +-2%, ESR +-20%, force ripple 2%
vs=[]
for _ in range(N):
    Bf=1+rng.normal(0,0.01); mf=m*(1+rng.normal(0,0.0067)); Ff=F_cmd*Bf*(1+rng.normal(0,0.0067))
    a=Ff/mf; vv=math.sqrt(2*a*accel_zone); vs.append(vv)
vs=np.array(vs); 
print(f"open-loop: mean {vs.mean():.2f} m/s, 3-sigma {3*vs.std():.2f} m/s ({3*vs.std()/vs.mean()*100:.2f}%)")
# closed-loop: velocity measured by encoder (0.1% ) + trim in coast zone (+-0.05 m/s residual)
v_cl = vs.mean() + rng.normal(0,0.05/3,N) + vs.mean()*rng.normal(0,0.001/3,N)
print(f"closed-loop (servo+trim): 3-sigma {3*v_cl.std():.3f} m/s ({3*v_cl.std()/vs.mean()*100:.3f}%)")

print("\n=== C3: coil adiabatic heating per shot ===")
J=6e6  # A/m^2 in copper during pulse
t_pulse=arr[-1,0]
dT = (J**2)*1.7e-8*t_pulse/(8960*385)
print(f"J={J/1e6:.0f} A/mm^2 for {t_pulse*1e3:.0f} ms: coil dT = {dT:.2f} K per shot (adiabatic)")

print("\n=== C4: eddy-current brake sizing ===")
sig=5.8e7; t_fin=0.004; B=0.85; 
# F = sigma * t * B^2 * A_pole * v  (plate drag, first order)
v0=v; m_s=m_sled
for A_pole in [0.008, 0.012, 0.016]:
    c = sig*t_fin*B**2*A_pole   # F = c*v
    # exponential decel: v(t)=v0 exp(-c t/m); distance to 2 m/s:
    d_stop = m_s/c*math.log(v0/2.0)*v0/ (v0/ (v0-2))  # not exact; integrate
    # integrate numerically
    vv=v0; xx=0
    while vv>1.5:
        F=c*vv; a=F/m_s; vv-=a*1e-4; xx+=vv*1e-4
    Fpk=c*v0
    print(f"A_pole={A_pole*1e4:.0f} cm^2: F_peak={Fpk:.0f} N ({Fpk/(m_s*9.81):.0f} g on sled), distance to 1.5 m/s = {xx*100:.0f} cm")
E_fin=0.5*m_sled*v0**2
m_fin=t_fin*0.08*0.30*8960
print(f"fin (4mm x 8cm x 30cm Cu): {m_fin:.2f} kg, absorbs {E_fin:.0f} J -> dT={E_fin/(m_fin*385):.1f} K/shot")
print(f"ring-spring catches residual 1.5 m/s: E={0.5*m_sled*1.5**2:.1f} J (trivial)")
