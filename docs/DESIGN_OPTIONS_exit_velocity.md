# Design options: recovering exit velocity

**Status: exploration, not a result.** Every row below was computed on 2026-07-28 by driving
`analysis/motor_model.py` with modified inputs, the repo's own field model and shot
integrator, no new physics. Nothing here has been adopted, no script or paper value has
changed, and none of it is a substitute for A4.

## The problem

P15: the Gen3 sled measured from CAD solid volumes is **9.445 kg**, against the 4.86 kg
`motor_model.py` assumes. At that mass the same machine delivers **16.54 m/s**, not the
headline 20.37.

## What each lever actually buys

Target 20.37 m/s. Sled mass 9.445 kg unless stated. `Kt` recomputed from the repo's field
model wherever the magnetic geometry changes.

| Lever | Sled | Kt (N/kA/m) | K (kA/m) | Stroke | Exit velocity | Efficiency |
|---|---|---|---|---|---|---|
| Today's assumption | 4.86 | 11.22 | 140 | 1.30 m | 20.37 m/s | 31.5 % |
| **As drawn** | **9.45** | 11.22 | 140 | 1.30 m | **16.54 m/s** | 19.6 % |
| Pocket 40 % of the titanium | 7.50 | 11.22 | 140 | 1.30 m | 17.88 m/s | 23.4 % |
| Pocket 60 % (aggressive) | 6.53 | 11.22 | 140 | 1.30 m | 18.68 m/s | 25.9 % |
| Magnets 8 to 6 mm | 8.53 | 9.30 | 140 | 1.30 m | **15.68 m/s** | 19.5 % |
| Magnets 8 to 5 mm | 8.07 | 8.16 | 140 | 1.30 m | **15.01 m/s** | 19.0 % |
| Raise sheet current | 9.45 | 11.22 | **213** | 1.30 m | 20.37 m/s | 18.4 % |
| Lengthen the stroke | 9.45 | 11.22 | 140 | **1.97 m** | 20.37 m/s | |
| **Two-layer stator** | 9.45 | **7.46** | **280** | 1.30 m | 19.06 m/s | 18.0 % |
| **Two-layer + 40 % pocketing** | 7.50 | 7.46 | 280 | 1.30 m | **20.61 m/s** | 21.6 % |

### Reading the table

**Mass reduction alone cannot close the gap.** Even 60 % pocketing of every titanium part
reaches 18.68 m/s. The titanium is 4.86 kg of the 9.45; the magnets are another 3.67 and
cannot be removed without removing thrust with them.

**Thinning the magnets moves backwards.** The Halbach field decays as e^(−ky) with
k = 2π/λ = 131 m⁻¹, so 25 % less magnet costs more thrust than the mass saves: 6 mm magnets
give 15.68 m/s, *worse* than doing nothing. Worth recording so nobody tries it.

**Raising sheet current works but spends the thermal budget.** 213 kA/m against the 140 kA/m
rating means J = 31.9 A/mm² against 21 today, a 52 % overload, and efficiency falls to
18.4 %. `sizing.py` `magnet_temperature()` currently shows the 140 kA/m rating with 8 kA/m
of headroom at ΔT = 40 K; that analysis would have to be redone at 213.

**Lengthening the stroke works and breaks the packaging.** 1.97 m of acceleration zone adds
673 mm to an envelope already 44 % over the ESPA Grande class limit (P9). This is the
cheapest option electrically and the most expensive one architecturally.

**The two-layer stator is the interesting one, and it is already an open decision (G3-D4).**
Doubling the winding widens the magnetic gap 12 to 22 mm, which costs a third of the thrust
constant, 11.22 to 7.46 N per kA/m. But sheet current doubles at *unchanged current
density*, and that more than compensates. With ordinary pocketing it clears the target at
J = 21 A/mm², the same copper loading as today.

Critically: **the stator does not ride the sled.** Its extra copper costs dry mass (P10 is
already open on that) but not exit velocity.

## What two-layer costs, and why it is not free

- **Copper loss doubles**, 672 J to roughly 1344 J per shot, and the campaign thermal case in
  `sizing.py` doubles with it.
- **Peak current goes to about 580 A** against 392 today. That collides with the A8 finding:
  the shot model has no ESR at all, and terminal sag is already 10.25 % rather than the
  published 4.88 %. At 580 A through 12-20 mΩ the droop is worse again, and the servo
  headroom behind the 0.027 m/s dispersion claim needs recomputing before two-layer can be
  called a fix.
- **Stator winding mass roughly doubles**: feeds directly into P10.
- Gen1 built two layers and Gen2/Gen3 built one; `parameters.json` still flags the decision
  open. This analysis is the first time the electromagnetic consequence has been costed.

## A reconciliation worth checking

Pocketing 40 % of the titanium gives 7.50 kg, **exactly the figure P5 quotes for the CAD
sled**, and 17.88 m/s, exactly the figure P8 quotes. That suggests the 7.50 kg was never
the as-drawn mass but an estimate with lightening already assumed, in which case P15's
9.445 kg and P5's 7.50 kg are the same design before and after pocketing rather than two
conflicting measurements.

**This is an inference, not a finding.** Check it against the CAD Master Plan that produced
the 7.50 kg before treating it as settled.

## A lever that is not in the table above: let the sled and payload separate at different speeds

Every option costed so far accelerates sled and payload as one rigid mass to the same exit
velocity, then releases them. They do not have to leave together. If a spring or cam does a
momentum-conserving push between sled and payload over the last part of the stroke, the
lighter payload leaves faster and the heavier sled recoils slower, and the sled's kinetic
energy is thrown away in the eddy brake by design (E8), so slowing it costs the mission
nothing and reduces brake duty.

At the as-drawn 9.445 kg sled and 4.0 kg payload, both at 16.537 m/s, total momentum is
222.34 kg·m/s and total kinetic energy 1838.4 J. Holding momentum and solving for the
energy the spring must add:

| Target payload v | Sled recoils to | Extra energy | Share of the 2630 J shot | Sled KE into brake |
|---|---|---|---|---|
| 17.50 m/s | 16.13 m/s | 2.6 J | 0.10 % | 1229 J |
| 18.00 m/s | 15.92 m/s | 6.1 J | 0.23 % | 1197 J |
| 19.00 m/s | 15.49 m/s | 17.3 J | 0.66 % | 1133 J |
| 20.00 m/s | 15.07 m/s | 34.1 J | 1.30 % | 1073 J |
| **20.37 m/s** | **14.91 m/s** | **41.8 J** | **1.59 %** | **1050 J** |

Recovering the entire headline shortfall costs **41.8 J against a 2630 J shot**, and brake
duty *falls* from 1291 J to 1050 J.

### The constraint that decides it is the payload's g-limit, not the energy

The energy is trivial; the question is whether the push can be delivered without exceeding
the 25 g qualification limit that "unmodified CubeSat" depends on. Delivering 3.833 m/s to
4.0 kg is a 15.33 N·s impulse, over a 2 ms release that is 195 g and the option is dead. It
is only the interaction *time* that decides this, and time is a design variable. Held at
exactly 25 g:

| Target payload v | Impulse | Kick duration | Relative spring stroke | Force |
|---|---|---|---|---|
| 18.00 m/s | 5.85 N·s | 6.0 ms | 6.2 mm | 981 N |
| 20.00 m/s | 13.85 N·s | 14.1 ms | 34.8 mm | 981 N |
| **20.37 m/s** | **15.33 N·s** | **15.6 ms** | **42.7 mm** | **981 N** |

981 N over 43 mm is an ordinary spring, not a shock event. Across a 100 x 100 mm pusher face
that is 98 kPa. The payload sees 10.7 g during the main stroke and 25 g during the kick,
**sequentially rather than simultaneously**, so the peak is 25 g, at the limit, with no
margin, which is itself a reason to target 19-20 m/s rather than the full 20.37.

### Why this is worth costing properly

Compare against the stroke-lengthening row in the table above. That buys the same velocity
for **673 mm** of extra envelope on a machine already 44 % over ESPA Grande (P9). This buys
it for **43 mm** of extra guided rail. It does not touch Kt, current density, magnet mass, or
dry mass, so it is orthogonal to every other row, it can be combined with any of them.

### What it costs, stated honestly

- **Tip-off is the real objection.** A spring at separation is precisely the mechanism this
  project's pitch claims to improve on, and 981 N is one to two orders of magnitude above a
  standard CubeSat separation spring. The answer, if there is one, is that the payload stays
  in the guide rails through all 43 mm of relative travel, so the guides carry any lateral
  load and the release is still guided, but that is an assertion, not a result. **It makes
  A7 (separation and tip-off, unrun) load-bearing rather than optional.**
- **A cocked 42 J spring is stored energy** on a machine whose safety case is built on a
  three-inhibit no-fire chain (B14) and a retention gate that separates preload from the
  release path (B13). It needs a safing path for an abort after cocking.
- **It must reset twelve times** without adjustment, inside the cassette cadence.
- **The 25 g budget is spent.** Any later growth in payload mass or main-stroke acceleration
  has nowhere to go.

### Status

**Exploration, not a result.** The momentum and energy arithmetic above is exact and
reproducible from the repo's own masses; the mechanism does not exist in CAD, no spring has
been sized, and the tip-off question is exactly the one thing that could kill it. Nothing in
`analysis/` or `cad/` has been changed.

## Recommended order

1. ~~**Run A4.**~~ **Done 2026-07-28.** The as-drawn plate passes all three declared bands,
   so there is no structural argument for a lighter chassis, a lighter one must be
   *designed* (rib-stiffened), which is what the 60 % pocketing row now rests on and why
   that row is marked unsupported.
2. **Cost the momentum-transfer release**, because it is the cheapest row in energy terms by
   two orders of magnitude and the cheapest in envelope terms by a factor of fifteen. The
   work it needs is mechanism design and A7, not more electromagnetics.
3. **Then close G3-D4** with the thermal and electrical consequences computed, not only the
   magnetic ones.
4. **Put an ESR into `motor_model.py` regardless.** At 392 A it is a rounding error; at
   580 A it is not.
5. **Then** propagate to the scripts and the paper, once, per the standing rule.

## The option nobody wants to say out loud

Re-scope the claim to 17-18 m/s. That is still eight times what a spring deployer delivers,
and it is what the machine as drawn will actually do. It is not free either: P8 puts the
lifetime multiplier at x1.68 at 17.88 m/s rather than x1.80, so the astrodynamics headline
moves with it.

How much it moves is worth stating, because the velocity number and the mission number are
not equally sensitive. Driving `astro.py` directly at 450 km:

| Exit velocity | Boosted lifetime | Multiplier |
|---|---|---|
| 16.54 m/s (as-drawn) | 2.120 yr | **x1.624** |
| 17.88 m/s (P8) | 2.198 yr | x1.684 |
| 20.37 m/s (headline) | 2.348 yr | **x1.799** |

A **23 % shortfall in velocity costs 9.7 % of the lifetime multiplier.** The re-scoped
machine still nearly doubles a propulsion-less satellite's life. That does not make the
shortfall acceptable, but it does mean the honest number is a design point rather than a
collapse, and it should be argued in mission terms, not only in m/s.

On the x1.80 itself: GMAT independently reproduces it at mean and high solar activity, but
**falsified the claim that the ratio is invariant across activity** (P16), so the multiplier
should be quoted at a stated activity level rather than as a constant.
