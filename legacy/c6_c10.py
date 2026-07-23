import math
print("=== C6: PS4/POEM attitude budget per shot (parametric — PS4 mass approx, flag in paper) ===")
J_shot = 4*22.4   # N s (sat momentum only; sled recovered)
for M_stage in [900, 1100, 1300]:
    print(f"PS4-class {M_stage} kg: dV/shot = {J_shot/M_stage*1000:.0f} mm/s; 12 shots = {12*J_shot/M_stage:.2f} m/s")
# torque: mount offset r=0.6 m (PS4 dia ~2.8 m, side mount), canted through CoM -> residual arm 0.05-0.15 m
for arm in [0.05, 0.15]:
    H = J_shot*arm
    # He cold gas thrusters: assume 10 N class at 1.2 m arm, Isp ~ 160 s
    tb = H/(10*1.2); mp = 10*tb/(160*9.81)
    print(f"residual arm {arm} m: H={H:.1f} N m s -> null burn {tb:.2f} s, He used {mp*1e3:.1f} g/shot; campaign {12*mp*1e3:.0f} g")

print("\n=== C7: tip-off error budget (3U: I_t = 0.042 kg m^2, req <5 deg/s, target <2) ===")
I=0.042
items=[("residual trim force 10 N x 5 mm CoM offset x 20 ms", 10*0.005*0.020),
       ("rail clearance couple during coast (2 N x 10 mm x 50 ms)", 2*0.010*0.050),
       ("release spring-back of guides (est. impulse)", 0.0008),
       ("sled rate at release (servo residual 0.05 deg/s transferred)", I*math.radians(0.05))]
tot=0
for name,dL in items:
    w=math.degrees(dL/I); tot+=dL
    print(f"  {name}: dL={dL*1e3:.2f} mN m s -> {w:.2f} deg/s")
print(f"  RSS-ish total ~ {math.degrees(tot/I):.2f} deg/s worst-case sum  -> meets <5 deg/s req; near <2 deg/s target")

print("\n=== C8: system rollups ===")
E_shot_net=1.92e3
print(f"battery: 12 shots x 2.5 kJ drawn = 30 kJ = 8.3 Wh + avionics 4 h x 60 W = 240 Wh -> ~250 Wh -> ~1.7 kg Li-ion (150 Wh/kg)")
# thermal: campaign losses
loss = 12*(2.47e3-1.0e3-0.55e3) + 12*1.0e3   # coil/PPU losses + brake fin heat
print(f"campaign heat: ~{loss/1e3:.0f} kJ over ~4 h -> avg {loss/(4*3600):.0f} W -> radiator ~{loss/(4*3600)/ (0.85*5.67e-8*(290**4-150**4)):.2f} m^2 (eps 0.85, 290 K vs deep space+albedo approx)")
mass={"structure+bracket":27,"stator Cu+formers (ironless)":36,"sled (4 kg incl Halbach+Ti)":4,
"eddy brake + ring spring":3,"cassettes x2 + followers + gates":9,"supercap bank+PPU+SiC":12,
"thermal":6,"avionics+IMU+harness+battery":8}
tot=sum(mass.values())
for k,v in mass.items(): print(f"  {k}: {v} kg")
print(f"  DRY ~{tot} kg; +12x4 kg = {tot+48} kg loaded (ESPA Grande 320-465 kg cap)")

print("\n=== C9: velocity error -> orbit error (at 450 km, 22.4 m/s shot) ===")
mu=3.986004418e14; Re=6378.137e3; r0=Re+450e3; v0=math.sqrt(mu/r0)
for pct in [0.1,0.25,0.5,1.0]:
    dv_err=22.4*pct/100
    d_apo=4*r0*dv_err/v0/1e3
    print(f"velocity error {pct}% ({dv_err:.3f} m/s): apogee error ~{d_apo:.2f} km")
print(f"measured 3-sigma 0.054 m/s -> apogee known/placed to ~{4*r0*0.054/v0/1e3:.2f} km")

print("\n=== C10: payload family (F_max=1717 N, sled 4 kg, accel zone 1.3 m) ===")
F=1717*0.9
print(f"{'sat kg':>7} {'a (g_sat)':>10} {'v_exit':>7} {'notes'}")
for m_sat,gcap in [(1.3,30),(4,25),(8,25),(12,25)]:
    m=m_sat+4
    a=min(F/m, gcap*9.81)
    v=math.sqrt(2*a*1.3)
    lim = "force-limited" if F/m < gcap*9.81 else "g-limited"
    print(f"{m_sat:>7} {a/9.81:>10.1f} {v:>7.1f}  {lim}")
