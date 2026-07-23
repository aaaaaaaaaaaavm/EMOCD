const fs = require('fs');
const { Document, Packer, Paragraph, TextRun, AlignmentType, Table, TableRow, TableCell,
  WidthType, Footer, PageNumber, NumberFormat, SectionType, LineRuleType, BorderStyle } = require('docx');

const FONT='Times New Roman';
const T=(t,o={})=>new TextRun(Object.assign({text:t,font:FONT,size:20},o));
const P=(ch,o={})=>new Paragraph(Object.assign({children:Array.isArray(ch)?ch:[ch],
  alignment:AlignmentType.JUSTIFIED,spacing:{line:240,lineRule:LineRuleType.AUTO,after:80}},o));
const body=(t)=>P(T(t));
const H=(t)=>P(T(t.toUpperCase(),{bold:true}),{alignment:AlignmentType.CENTER,spacing:{before:160,after:100,line:240,lineRule:LineRuleType.AUTO}});
const HS=(t)=>P(T(t,{italics:true,bold:false}),{alignment:AlignmentType.LEFT,spacing:{before:120,after:60,line:240,lineRule:LineRuleType.AUTO}});

function tbl(caption, rows, widths, fs=16){
  const cap=P(T(caption,{size:16,smallCaps:true}),{alignment:AlignmentType.CENTER,spacing:{before:100,after:40,line:240,lineRule:LineRuleType.AUTO}});
  const t=new Table({columnWidths:widths,width:{size:widths.reduce((a,b)=>a+b,0),type:WidthType.DXA},
    rows:rows.map((r,ri)=>new TableRow({children:r.map((c,ci)=>new TableCell({
      width:{size:widths[ci],type:WidthType.DXA},
      children:[new Paragraph({alignment:ci===0?AlignmentType.LEFT:AlignmentType.CENTER,
        spacing:{line:216,lineRule:LineRuleType.AUTO},
        children:[T(c,{size:fs,bold:ri===0})]})]})) }))});
  const post=P(T('',{size:8}),{spacing:{after:60,line:240,lineRule:LineRuleType.AUTO}});
  return [cap,t,post];
}

const children=[];

// ---------- Title block (single column feel inside col section start) ----------
const titleSection=[
  P(T('EMOCD: A Linear-Motor Electromagnetic Deployment System for Deterministic CubeSat Orbit Seeding from Small Launch Vehicles',{size:36,bold:false}),{alignment:AlignmentType.CENTER,spacing:{before:0,after:160,line:276,lineRule:LineRuleType.AUTO}}),
  P(T('Adityavardhan Mishra',{size:22}),{alignment:AlignmentType.CENTER,spacing:{after:20,line:240,lineRule:LineRuleType.AUTO}}),
  P(T('Department of Mechanical Engineering, Symbiosis Institute of Technology,',{size:20,italics:true}),{alignment:AlignmentType.CENTER,spacing:{after:0,line:240,lineRule:LineRuleType.AUTO}}),
  P(T('Symbiosis International (Deemed University), Pune, India',{size:20,italics:true}),{alignment:AlignmentType.CENTER,spacing:{after:20,line:240,lineRule:LineRuleType.AUTO}}),
  P(T('PRN 23070125054 (Fourth-year B.Tech.)',{size:20}),{alignment:AlignmentType.CENTER,spacing:{after:200,line:240,lineRule:LineRuleType.AUTO}}),
];

// ---------- Abstract ----------
const abstract=[
  P([T('Abstract',{bold:true,italics:true}),T('\u2014Secondary payloads on rideshare missions inherit the orbit of the primary customer, and the spring deployers that release them impart 1\u20132 m/s, too little to change that orbit in any useful way. This paper presents the design and analysis of EMOCD, a magazine-fed electromagnetic deployer that ejects unmodified CubeSats at a programmable velocity an order of magnitude above spring systems while remaining within standard qualification loads. An architecture trade led to an ironless double-sided Halbach-array linear synchronous motor driving a reusable 4 kg permanent-magnet sled along a 1.5 m track, with twelve 3U satellites fed from two transverse cassettes, a contactless eddy-current arrest brake, and supercapacitor pulse power. A verified electromagnetic model brackets the exit velocity at 19.8\u201322.4 m/s for a 3U payload at 15.3\u201319.7 g, with 52% net electrical efficiency and a closed-loop velocity dispersion of 0.054 m/s (3\u03c3), equivalent to \u00b10.19 km of apogee placement. Orbit-decay analysis shows one maximum-velocity ejection multiplies a propulsion-less satellite\u2019s orbital lifetime by 1.8\u20131.9, and differential ejection velocities of 2\u201310 m/s establish 30\u00b0 constellation spacing in 1.4\u20136.9 days, against weeks to months for differential-drag phasing. The system closes at roughly 105 kg dry within an ESPA Grande allocation. Host-integration budgets are developed for restartable kick stages, with Skyroot Aerospace\u2019s Vikram-1 Orbit Adjustment Module and ISRO\u2019s POEM identified as candidate hosts, and the concept is positioned against spring deployers and propulsive transfer vehicles in the Indian launch ecosystem.',{size:18})],{spacing:{after:80,line:240,lineRule:LineRuleType.AUTO}}),
  P([T('Index Terms',{bold:true,italics:true}),T('\u2014CubeSat deployment, electromagnetic launch, Halbach array, linear synchronous motor, rideshare, small launch vehicles, constellation phasing.',{size:18})],{spacing:{after:120,line:240,lineRule:LineRuleType.AUTO}}),
];

// ---------- I. Introduction ----------
const s1=[H('I. Introduction'),
body('The rideshare model has cut the cost of reaching orbit for small satellites, and it has done so by removing their choice of destination. A CubeSat manifested as a secondary payload is released wherever the primary customer\u2019s mission ends, through a spring deployer whose 1\u20132 m/s separation velocity exists for clearance, not for orbit shaping. Satellites that carry propulsion can correct for this. The large class that cannot, which includes most university missions and cost-constrained commercial payloads, remains wherever it was dropped, at whatever altitude and phasing the manifest happened to produce.'),
body('Two families of hardware currently bracket this problem. Below it sit the flight-proven spring systems, typified by the J-SSOD at 1.1\u20131.7 m/s [2] and commercial deployers of the EXOpod class at about 2 m/s [22]. Above it sit propulsive orbital transfer vehicles, which move an entire bus through hundreds or thousands of m/s but at a cost, mass, and integration burden far beyond what a 4 kg satellite needing a 20 m/s nudge can justify. Between the two lies an unserved regime. No published deployment system operates in the tens of m/s, although the astrodynamic utility of that band, for lifetime extension and for constellation seeding, is substantial and quantifiable.'),
body('This paper develops a system for exactly that band. EMOCD (Electromagnetic Orbital CubeSat Deployer) is a magazine-fed linear-motor launcher that accelerates unmodified CubeSats on a reusable carrier sled and releases them at a servo-controlled velocity. The contributions are: (1) an architecture trade showing why a linear synchronous motor, not a coilgun, is the correct electromagnetic topology at CubeSat structural limits; (2) a complete system design covering the magazine, arrest, restraint, power, and abort functions; (3) ten quantitative analyses spanning launch performance, astrodynamics, deployment safety, and host interaction, with an independently verified magnetic field model; and (4) an integration and positioning study for the Indian launch ecosystem, including capacity and recoil budgets for Skyroot Aerospace\u2019s Vikram family and a comparison against the deployment and transfer services of Exolaunch and Bellatrix Aerospace.'),
body('All figures of merit in this paper derive from numerical models executed for this study; where a model rests on an assumption, the assumption is stated, and where an external figure is a company claim rather than an independently verified one, it is marked as such.')];

// ---------- II. Related Work ----------
const s2=[H('II. Related Work'),
body('Deployment heritage. The P-POD established the rail-and-spring standard, and the ISS-based J-SSOD and NanoRacks systems industrialized it [2], [3]. The failure record is instructive: the NanoRacks ball-lock anomaly, in which jack-screw preload above 0.11 N\u00b7m drove the release mechanism toward seizure, traced to a load path in which ascent preload passed through the release device itself [1]. EMOCD\u2019s restraint architecture is designed against precisely this fault class. The closest electromagnetic relative is a proposed multi-CubeSat deployer using permanent-magnet conveying and ejection stages, demonstrated analytically and in prototype at 0.4\u20131.4 m/s [4]; EMOCD extends the same Lorentz-force principle to twenty times that velocity.'),
body('Electromagnetic launch. Coilgun research at Sandia National Laboratories examined nanosatellite launch at km/s scales [5], [6], establishing both the promise of contactless acceleration and its costs: single-stage reluctance coilguns convert 1\u20132% of stored energy to kinetic energy, and useful efficiency requires long multi-stage guns. Ironless permanent-magnet linear machines occupy the opposite corner of the design space. The Halbach array concentrates flux on one working face [12], and the Inductrack program demonstrated that such arrays paired with passive or driven conductors produce large forces with no iron and no sliding contact [11].'),
body('Supporting technologies. Space-qualified supercapacitors have progressed from evaluation to an established supply chain through ESA-led programmes [9], [10], providing pulse power in the kJ class at hundreds of amperes. Eddy-current dampers have decades of flight heritage in deployment mechanisms, valued for being contactless, wear-free, and vacuum-compatible [15]; EMOCD uses the same physics as its arrest brake. On the astrodynamics side, Planet Labs demonstrated propulsion-free constellation phasing by differential drag, with campaigns operating over weeks to months [7], [8]. That timescale is the benchmark against which EMOCD\u2019s impulsive seeding is measured. Finally, ISRO\u2019s POEM programme converted the spent PSLV fourth stage into a stabilized hosted-payload platform, flying four missions and closing POEM-3 with a controlled, debris-free reentry [13], [14], establishing the regulatory template for operating equipment on a spent stage.'),
body('The gap this paper addresses is the deployment regime between roughly 3 and 50 m/s: above every flown spring, far below every gun, and claimed by no published system.')];

// ---------- III. System Architecture ----------
const s3=[H('III. System Architecture'),
HS('A. Requirements'),
body('The driving requirements are: eject an unmodified 3U CubeSat, imposing no armature, no plating, and no electrical interface on the customer satellite; keep payload acceleration within standard qualification loads (25\u201330 g quasi-static); fit an ESPA Grande envelope and mass allocation; provide per-satellite programmable velocity with dispersion small against its astrodynamic effect; carry a twelve-satellite manifest with autonomous sequencing; provide inhibits and a defined abort capability; and hand recoil to the host vehicle in a form its attitude control can absorb.'),
HS('B. Topology Trade: Coilgun Versus Linear Synchronous Motor'),
body('The payload sets the trade before the electromagnetics do. Whatever the launcher, exit velocity is bounded by v = \u221a(2aL): at 25\u201330 g over a 1.3\u20132 m stroke the ceiling is 26\u201335 m/s. The coilgun\u2019s defining advantage, a velocity ceiling in the km/s range, is therefore unreachable by the payload it would carry, while its defining costs remain: 1\u20132% single-stage efficiency [5], microsecond pulse timing against the suck-back effect, and a ferromagnetic or conductive armature bolted to the customer\u2019s satellite. A linear synchronous motor concedes nothing in the reachable envelope (maglev traction exceeds 150 m/s) and inverts every cost: drive efficiency above 70%, continuous servo control in place of fire-and-commit timing, and, decisively, a reusable sled that carries the magnets so the satellite carries nothing. Table I summarizes the trade. The LSM was selected without close contest.'),
...tbl('TABLE I. Topology trade at CubeSat structural limits',[
['Criterion','Reluctance coilgun','Ironless LSM + sled'],
['Velocity ceiling (payload-limited)','26\u201335 m/s','26\u201335 m/s'],
['Efficiency (electrical\u2192payload KE)','1\u20132% single-stage [5]','52% verified (Sec. V-A)'],
['Satellite modification','Armature required','None'],
['Velocity control','Pulse timing, open-loop','Closed-loop servo'],
['Abort','None once fired','To ~45% of stroke'],
['Field on stored satellites','Pulsed, unshielded','Halbach self-shielded'],
],[2000,1250,1250]),
HS('C. Layout and Firing Cycle'),
body('The launcher is organized around a single 1.5 m track: a 1.3 m acceleration zone followed by a 0.2 m coast-and-trim zone. The stator is an ironless double-sided three-phase copper winding; the mover is a 4 kg sled carrying opposed Halbach arrays (48 mm wavelength, 8 mm N45SH blocks, four blocks per wavelength) across a 12 mm winding gap. Two transverse cassettes of six 3U satellites each flank the breech. The cycle is: the cassette follower advances one pitch and slides a satellite laterally onto the sled cradle (a sub-newton operation in microgravity); a detent latch engages; a two-finger escapement retains the next satellite; the motor accelerates the stack; force is removed in the coast-trim zone where the servo makes its final correction; the sled enters the brake and decelerates while the satellite, no longer pushed, separates and departs along the sled\u2019s guide extensions. Retention during acceleration costs nothing, since inertia presses the satellite into the aft backstop, and release costs nothing, since braking the sled is the release. The sled then returns at low speed and the cycle repeats. Shot cadence is set by supercapacitor recharge, roughly 10\u201320 s at a 150\u2013300 W allocation.'),
HS('D. Restraint, Inhibits, and Abort'),
body('Launch restraint separates the preload path from the release path, the inverse of the NanoRacks fault [1]. A one-shot retention gate at each cassette exit carries ascent preload directly into structure; the escapement is caged during ascent and sees launch loads never; the sled is held by a motorized over-center cam lock. Firing requires a three-inhibit chain: redundant seat switches confirming the satellite is fully aboard the sled, an attitude-valid flag from the host, and a sequencer arm. Abort is available to approximately 45% of the stroke, at which point braking distance for the combined sled and satellite exceeds the remaining track; the muzzle buffer is sized to capture an aborted combined mass at reduced speed.'),
HS('E. Arrest'),
body('The sled arrives at the brake with about 1.0 kJ. Motor regeneration alone cannot arrest it, because braking force is bounded by the same force constant as acceleration and would require more track than exists. A copper-fin eddy-current brake provides the bulk arrest: force proportional to velocity, no contact, no consumables, and flight heritage in the damper class [15]. Authority is abundant, so the design constraint inverts and the pole entry is tapered to cap sled deceleration near 200 g, protecting the sintered magnet bonds. The 0.86 kg fin absorbs each shot with a 3.0 K temperature rise and radiates it between shots; a ring-spring stop catches the residual below 1.5 m/s.'),
HS('F. Power and Materials'),
body('Pulse energy comes from a 6 F, 96 V supercapacitor bank switched by a SiC bridge; cells of this class have an established space-qualification path [9], [10]. Campaign energy is small: twelve shots draw about 30 kJ, so a 1.7 kg battery covers a full campaign with the host or a small array recharging between shots. Materials follow three rules: nothing conductive rides the changing field (titanium sled chassis, PEEK formers), nothing near the track is ferromagnetic except by design (beryllium-copper springs, A-286 fasteners), and nothing outgasses near customer optics (ASTM E595-compliant polymers, dry-film lubrication, sealed roller cartridges). Satellite-contact rails are hard-anodized aluminium per the CubeSat standard.')];

// ---------- IV. Analytical Models ----------
const s4=[H('IV. Analytical Models and Verification'),
HS('A. Electromagnetic Shot Model'),
body('The Halbach airgap field is modeled as a decaying wave, B(y) = B\u2080e^(\u2212ky) with k = 2\u03c0/\u03bb, and the double-sided arrangement sums the two faces. Thrust is computed from a surface-current model, F = \u27e8B\u27e9KA, with K the winding sheet-current density (45 kA/m adiabatic pulse rating) over the 0.061 m\u00b2 active area. The shot is integrated as an ODE coupling sled-plus-satellite dynamics to the supercapacitor circuit, including bank sag through the discharge and a lumped 82% drive efficiency. A 4000-run Monte Carlo over field, mass, resistance, and force-ripple tolerances gives the velocity dispersion, evaluated open-loop and with the closed-loop encoder servo and coast-trim correction.'),
HS('B. Independent Field Verification'),
body('Because the wave model carries the force budget, it was checked against an independent magnetostatic computation using a validated permanent-magnet field library (analytic cuboid superposition, magpylib). The exercise was deliberately adversarial. The array rotation-sense convention was determined empirically by probing a single array on both faces rather than asserted, a step that caught two successive sign errors whose outputs matched single-array fingerprints too precisely to be coincidence. The converged results: single-array mid-gap field 0.351 T against the wave model\u2019s 0.351 T; double-sided mid-gap peak 0.694 T against the predicted 0.702 T. Across the \u00b15 mm winding region the spatial mean of the thrust-producing transverse component is 0.483 T, while the fundamental peak is 0.694 T. The design value of 0.62 T used by the shot model therefore sits inside the verified bracket rather than at a confirmed point, and all performance figures in Section V are quoted across that bracket. The stray field behind the array back face, which sets the magnetic keep-out for stored satellites, computes to 22.7 mT at 10 mm, 4.7 mT at 20 mm, and 1.0 mT at 50 mm.'),
HS('C. Astrodynamics'),
body('Orbital lifetime is computed by per-revolution orbit-averaged decay: the Gauss tangential equations are integrated by quadrature over eccentric anomaly with a static exponential atmosphere at mean solar activity [19], and multi-revolution steps sized to bound the semi-major-axis change. Constellation seeding uses the along-track drift rate produced by an ejection-velocity split, \u0394a = 2a\u0394v/v and the resulting period difference. Deployment safety is screened by propagating the stage and all twelve deployed ellipses with Keplerian motion plus secular J2 for 30 days at 5\u201310 s sampling, recording minimum pairwise distances. Tip-off is budgeted as angular impulse over the released satellite\u2019s transverse inertia (0.042 kg\u00b7m\u00b2 for a 3U).')];

// ---------- V. Results ----------
const s5=[H('V. Performance Results'),
HS('A. Launch Performance'),
body('For the 3U reference (4 kg satellite, 4 kg sled, 1.3 m acceleration), the shot model gives, across the verified field bracket: exit velocity 19.8\u201322.4 m/s at 15.3\u201319.7 g on the satellite, a 116\u2013131 ms pulse, peak current 316\u2013463 A, and bank sag of 3.6\u20134.6%. Energy drawn is 1.9\u20132.5 kJ per shot; crediting 55% regenerative recovery of the sled\u2019s kinetic energy, the net cost is 1.5\u20131.9 kJ at 52% end-to-end efficiency, a figure that holds at both ends of the bracket. Holding the nominal 22.4 m/s at the pessimistic field requires 28% more sheet current, raising copper current density from 6.0 to 7.7 A/mm\u00b2; adiabatic coil heating remains below 0.05 K per shot, so the thermal margin is three orders of magnitude and the recovery path is essentially free. Closed-loop velocity dispersion is 0.054 m/s (3\u03c3), a factor of nine below open-loop, dominated by the servo and photogate chain rather than by plant tolerances.'),
HS('B. Astrodynamic Utility'),
body('Lifetime. A prograde ejection raises apogee while leaving perigee at the deployment altitude, so the correct claim is a longer-lived ellipse, not a new circular orbit. At 450 km with a ballistic coefficient of 61 kg/m\u00b2, the decay model gives lifetime multipliers of 1.56 at 15 m/s, 1.77 at 19.8 m/s, and 1.90 at 22.4 m/s, the machine\u2019s verified range; the multiplier is nearly invariant across 350\u2013500 km and across ballistic coefficients of 40\u201390 kg/m\u00b2, which makes it robust against the largest model uncertainty, since absolute lifetimes swing severalfold with solar activity while the ratio does not. One maximum-velocity shot therefore buys a propulsion-less satellite most of a doubling of its orbital life.'),
body('Constellation seeding. Differential ejection velocities put adjacent satellites on measurably different periods. Splits of 2, 5, and 10 m/s produce along-track separation of 4.3, 10.9, and 21.7 degrees per day at 450 km, reaching a 30\u00b0 spacing target in 6.9, 2.8, and 1.4 days respectively. The flown propulsion-free alternative, differential drag, phases constellations over weeks to months [7]. EMOCD compresses the seeding phase of such campaigns by one to two orders of magnitude; a hybrid concept, impulsive seeding followed by drag trim, follows naturally.'),
HS('C. Deployment Safety'),
body('Every prograde shot leaves an ellipse whose perigee sits at the firing altitude, so the deployed fleet re-crosses the stage\u2019s orbit by construction. Screening over 30 days for twelve 22.4 m/s-class shots staggered 20 minutes apart shows a minimum satellite-to-stage distance of 62 km and satellite-to-satellite minimum of 5.8 km; the along-track phase realigns after 113 orbits, about 7.3 days. Disposing of the stage before the first realignment, which restartable kick stages do as a matter of course, raises the pre-disposal minimum to 348 km. These are screening-level figures at 5\u201310 s sampling; per-shot conjunction products remain a mission-operations deliverable.'),
HS('D. Error, Tip-Off, and Host Budgets'),
body('The measured 3\u03c3 velocity dispersion of 0.054 m/s maps to \u00b10.19 km of apogee placement at 450 km, sub-kilometre deterministic orbit insertion for a satellite with no propulsion. The tip-off budget, dominated by residual trim force acting on centre-of-mass offset and by rail-clearance couples, sums to 3.9 deg/s worst case against the 5 deg/s requirement class of ISS-heritage deployers [16], and the coast-trim release is what makes the budget close: at full force the first term alone would approach 34 deg/s. Recoil per shot is the satellite\u2019s momentum only, 79\u201390 N\u00b7s, because the sled\u2019s share returns through the brake. Table II gives the payload family and Table III the per-shot recoil on candidate host masses.'),
...tbl('TABLE II. Payload family across the verified field bracket (1.3 m acceleration, 4 kg sled)',[
['Class','Exit velocity','Acceleration'],
['1U (1.3 kg)','24.3\u201327.5 m/s','23.2\u201329.7 g'],
['3U (4 kg)','19.8\u201322.4 m/s','15.3\u201319.7 g'],
['6U (8 kg)','16.2\u201318.3 m/s','10.2\u201313.1 g'],
['12U (12 kg)','14.0\u201315.8 m/s','7.7\u20139.8 g'],
],[1300,1650,1550]),
...tbl('TABLE III. Recoil budget per 3U shot (89.6 N\u00b7s nominal) versus host mass',[
['Host class','\u0394V per shot','12-shot total'],
['300 kg kick stage','299 mm/s','3.6 m/s'],
['600 kg kick stage','149 mm/s','1.8 m/s'],
['900 kg (PS4 class)','100 mm/s','1.2 m/s'],
['420 t (ISS class)','0.2 mm/s','2.6 mm/s'],
],[1700,1400,1400]),
HS('E. Mass and Power'),
body('The dry mass estimate, pending CAD, is 105 kg: structure and bracket 27, ironless stator 36, sled 4, brake and stop 3, cassettes 9, supercapacitor bank and power electronics 12, thermal 6, avionics and harness 8. Loaded with twelve 3U satellites the system is about 153 kg against an ESPA Grande allocation of 320\u2013465 kg. Campaign heat is roughly 23 kJ over a few hours, thermally trivial; the sizing case is the local transient in the brake fin and coil, both shown small above.')];

// ---------- VI. Ecosystem ----------
const s6=[H('VI. Host Integration and the Indian Launch Ecosystem'),
HS('A. Two Operating Modes'),
body('EMOCD-A, the attached mode analyzed above, mounts on a host stage and borrows its attitude knowledge and control, carrying no gyros or thrusters of its own; recoil torque is nulled by the host at a cost of grams of propellant per shot. EMOCD-F, a free-flyer in the transfer-vehicle mold, adds its own GNC and is the growth path for missions needing multi-day firing geometry; it is noted here and not further analyzed.'),
HS('B. Skyroot Vikram as Host'),
body('Skyroot Aerospace\u2019s Vikram-1, whose maiden flight window opened in July 2026, is a four-stage vehicle with three solid Kalam stages and a restartable liquid fourth stage, the Orbit Adjustment Module, carrying one Raman-2 engine, four Raman Mini thrusters, and eight cold-gas thrusters, stage-tested through more than a thousand pulses in October 2025 [20], [21]. The OAM\u2019s stated role, delivering precise final velocity and restarting to place satellites in different orbits, is functionally the same role ISRO\u2019s PS4 plays for POEM, and it makes the OAM the natural Indian host for EMOCD-A: the module supplies attitude and recoil authority, and EMOCD converts each coast into a twelve-satellite deterministic dispersion without a separate burn per customer.'),
body('The capacity arithmetic is stated plainly. Against Vikram-1\u2019s published 350 kg to low Earth orbit [21], a loaded EMOCD is 44% of the vehicle, so a Vikram-1 flight is a dedicated demonstration rather than a rideshare element. The announced Vikram-1U at 550 kg brings the fraction to 28%, and Vikram-2 at roughly 900 kg [21] to 17%, where EMOCD becomes an ordinary manifest item. One integration quantity cannot be closed from public information: the OAM\u2019s mass and control authority are not disclosed [20], so Table III brackets the recoil parametrically across 300\u2013900 kg host classes. Obtaining the OAM mass, thruster impulse budget, and coast duration is the single data exchange that converts this section from parametric to specific, and it is posed here as a direct question to the vehicle provider. A secondary observation follows from the recoil physics: correction propellant depends only on total ejected momentum, about 1.1 kN\u00b7s for a full manifest, roughly half a kilogram of hydrazine-class propellant regardless of host mass; host mass determines the per-shot rate disturbance, not the fuel bill.'),
HS('C. Positioning Against Existing Offerings'),
body('Three services now define the deployment landscape on and around Indian vehicles. Exolaunch, under its October 2025 partnership with Skyroot, brings flight-proven separation hardware to Vikram: CarboNIX rings for microsatellites and EXOpod deployers at about 2 m/s, with hundreds of deployments of heritage [22]. Bellatrix Aerospace offers Pushpak, an orbital transfer vehicle contracted with NSIL in October 2024, with company-stated capacity of 750 kg and up to 7 km/s of \u0394V through combined electric and green propulsion [23]; its propulsion modules Rudra and Arka have flown on POEM-3 and POEM-4, while Pushpak itself, like Exolaunch\u2019s Reliant tug, has not yet flown as of this writing. EMOCD does not compete with either end of this landscape on its own terms. It cannot move a bus or change a plane, and a spring cannot place twelve satellites on twelve chosen ellipses. Table IV states the comparison. The honest positioning is a middle tier that currently has no demonstrated occupant: per-satellite deterministic velocity, ten times spring authority, at deployer-class rather than tug-class mass and complexity, serving exactly the propulsion-less payload population that neither springs nor tugs address. On a Vikram manifest the three tiers stack rather than collide: Exolaunch hardware for standard separations, EMOCD for velocity-managed dispersal, a transfer vehicle when a customer genuinely needs a different orbit.'),
...tbl('TABLE IV. Deployment and transfer options for small satellites on Indian launch vehicles',[
['Attribute','Spring deployer (EXOpod class)','EMOCD (this work)','OTV (Pushpak class)'],
['Velocity authority','~2 m/s fixed','2\u201322 m/s programmable','100s\u20131000s m/s (co. stated)'],
['Per-satellite targeting','No','Yes, \u00b10.054 m/s','Yes, full orbit change'],
['Satellite modification','None','None','Rides as payload'],
['System mass for 12\u00d73U','~10\u201320 kg','~153 kg loaded','~100s kg + propellant'],
['Plane / LTAN change','No','No (\u22640.4\u00b0 ceiling)','Yes'],
['Flight status','Flown, extensive','Design study','Announced, unflown'],
],[1500,1000,1000,1000],13),
HS('D. Demonstration Path'),
body('The regulatory and operational template for flying equipment on a spent stage already exists in India: POEM has hosted payloads on four missions and retired POEM-3 through a controlled reentry [13], [14]. A captive-carry EMOCD, running full sled cycles with a payload that is never released, requires no deployment approvals while gathering the reaction-load and servo data that certify the firing event. Either POEM or an OAM extended-coast experiment serves; the choice belongs to whichever provider engages first.')];

// ---------- VII. Limitations ----------
const s7=[H('VII. Limitations'),
body('Six limits bound the claims. The atmosphere model is static at mean solar activity, so absolute lifetimes carry severalfold uncertainty while the quoted ratios are robust. The motor force constant is verified only to a bracket, 0.483\u20130.694 T effective field, and a winding-resolved finite-element model is the open task that pins it. The eddy-brake law is first-order plate drag, acceptable because authority exceeds need by more than an order of magnitude. Conjunction figures are screening-level at finite sampling and do not replace per-shot collision-avoidance products. Host budgets for the Vikram OAM are parametric because the stage\u2019s mass is not public. Mass figures are pre-CAD estimates and are labelled as such. None of these limits threatens feasibility; each defines the next unit of work.')];

// ---------- VIII. Roadmap & Conclusion ----------
const s8=[H('VIII. Development Roadmap'),
body('The programme is deliberately ground-testable, which few orbital deployment concepts can claim. Phase 0, largely complete, is the validated analytical model with the independent field verification reported here; its close-out is the winding-resolved FEA. Phase 1 is a 0.5 m benchtop track at reduced energy. Phase 2 is the full 1.5 m track firing a 4 kg mass simulator into the eddy brake with the complete feed cycle, at which point the velocity, dispersion, and tip-off claims become measured quantities; the entire phase is within a university laboratory budget. Phase 3 covers vacuum tribology of the rollers, escapement, and dry films. Phase 4 is the captive-carry flight demonstration of Section VI-D.'),
H('IX. Conclusion'),
body('A magazine-fed linear-motor deployer closes, on verified numbers, a deployment regime that current hardware leaves empty. The design ejects unmodified 3U CubeSats at 19.8\u201322.4 m/s within standard qualification loads, at 52% electrical efficiency and 0.054 m/s dispersion, from a 105 kg system that fits a standard secondary-payload allocation. That authority converts directly into utility no spring can provide and no tug can economically match for this payload class: most of a doubling of orbital lifetime per shot, and constellation spacing established in days instead of months. The concept asks one question of a launch provider, the mass and authority of its kick stage, and offers in return a way to sell every rideshare customer their own orbit.')];

// ---------- References ----------
const refs=[
'[1] C. Lewis, "Failure of the ball-lock mechanism on the NanoRacks CubeSat deployer," in Proc. 44th Aerospace Mechanisms Symp. (ESMATS archive), 2018.',
'[2] JAXA, "JEM payload accommodation handbook, vol. 8: Small satellite deployment interface control document," via UNOOSA KiboCUBE.',
'[3] NASA Small Spacecraft Systems Virtual Institute, "State-of-the-art of small spacecraft technology: Integration, launch, deployment, and orbital transport," NASA.',
'[4] "Design and analysis of a new deployer for the in orbit release of multiple stacked CubeSats," Remote Sensing, vol. 14, no. 17, art. 4205, 2022.',
'[5] B. N. Turman et al., "Coilgun launcher for nanosatellites," Sandia National Laboratories, OSTI conf. report.',
'[6] R. J. Kaye et al., "Electromagnetic coilgun launcher for space applications," Sandia National Laboratories, OSTI 125180.',
'[7] C. Foster et al., "Constellation phasing with differential drag on Planet Labs satellites," J. Spacecraft and Rockets, vol. 55, no. 2, pp. 473\u2013483, 2018.',
'[8] C. Foster, H. Hallam, and J. Mason, "Orbit determination and differential-drag control of Planet Labs CubeSat constellations," arXiv:1509.03270, 2015.',
'[9] F. Faure et al., "Qualification of COTS supercapacitors for space applications," in Proc. ESA Space Passive Component Days, 2018.',
'[10] "Towards supercapacitors in space applications," in Proc. European Space Power Conf., 2017.',
'[11] R. F. Post and D. D. Ryutov, "The Inductrack: A simpler approach to magnetic levitation," IEEE Trans. Appl. Supercond., vol. 10, no. 1, pp. 901\u2013904, 2000.',
'[12] K. Halbach, "Design of permanent multipole magnets with oriented rare earth cobalt material," Nucl. Instrum. Methods, vol. 169, pp. 1\u201310, 1980.',
'[13] ISRO, "PSLV-C58/XPoSat mission: POEM-3 accomplishes zero orbital debris mission," Mar. 2024.',
'[14] ISRO, "POEM-4 completes 1000 orbits in space," 2025.',
'[15] "Eddy current damper modelling for space mechanisms," Actuators (MDPI); CDA InterCorp flight-heritage documentation.',
'[16] NanoRacks, "NanoRacks CubeSat deployer (NRCSD) interface definition document," 2018.',
'[17] V. Yudintsev, "Separation dynamics of CubeSats" (deployment tip-off analysis).',
'[18] D. A. Vallado, Fundamentals of Astrodynamics and Applications, 4th ed. Hawthorne, CA: Microcosm Press, 2013 (exponential atmosphere model).',
'[19] D. A. Vallado, ibid., Gauss variational equations and orbit-averaged decay.',
'[20] Skyroot Aerospace, "Orbit Adjustment Module full stage-level test" (public statement), Oct. 14, 2025; Orbital Today coverage, Oct. 15, 2025.',
'[21] J. Foust, "Skyroot prepares for first orbital launch attempt," SpaceNews, Jul. 7, 2026.',
'[22] Exolaunch, "CarboNIX" and "EXOpod Nova" product documentation; Exolaunch\u2013Skyroot strategic partnership announcement, Oct. 14, 2025.',
'[23] Bellatrix Aerospace, "Bellatrix Aerospace and NSIL sign MoU to integrate Bellatrix\u2019s OTV in NSIL\u2019s launch missions," Oct. 9, 2024.',
'[24] ISRO, "POEM-4 payloads, SpaDeX mission," 2024.',
];
const s9=[H('References'),
...refs.map(r=>P(T(r,{size:16}),{alignment:AlignmentType.LEFT,spacing:{line:216,lineRule:LineRuleType.AUTO,after:40}}))];

// note line
const note=[P(T('Analysis code, models, and the independent field-verification scripts are available from the author. CAD geometry and finite-element field maps are in progress and intentionally excluded from this revision.',{size:16,italics:true}),{spacing:{before:120,line:216,lineRule:LineRuleType.AUTO}})];

const colChildren=[...abstract,...s1,...s2,...s3,...s4,...s5,...s6,...s7,...s8,...s9,...note];

const M=1080; // ~0.75 in margins
const doc=new Document({
  styles:{default:{document:{run:{font:FONT,size:20},paragraph:{spacing:{line:240,lineRule:LineRuleType.AUTO}}}}},
  sections:[
    {properties:{page:{margin:{top:M,bottom:M,left:M,right:M},pageNumbers:{start:1,formatType:NumberFormat.DECIMAL}}},
     footers:{default:new Footer({children:[new Paragraph({alignment:AlignmentType.CENTER,children:[new TextRun({font:FONT,size:18,children:[PageNumber.CURRENT]})]})]})},
     children:titleSection},
    {properties:{type:SectionType.CONTINUOUS,column:{count:2,space:360},page:{margin:{top:M,bottom:M,left:M,right:M}}},
     children:colChildren},
  ],
});
Packer.toBuffer(doc).then(b=>{fs.writeFileSync('EMOCD_IEEE_Paper.docx',b);console.log('written',b.length);});
