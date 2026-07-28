# Design options: recovering exit velocity

**Status: exploration, not a result.** Every row below was computed on 2026-07-28 by driving
`analysis/motor_model.py` with modified inputs — the repo's own field model and shot
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
| Magnets 8 → 6 mm | 8.53 | 9.30 | 140 | 1.30 m | **15.68 m/s** | 19.5 % |
| Magnets 8 → 5 mm | 8.07 | 8.16 | 140 | 1.30 m | **15.01 m/s** | 19.0 % |
| Raise sheet current | 9.45 | 11.22 | **213** | 1.30 m | 20.37 m/s | 18.4 % |
| Lengthen the stroke | 9.45 | 11.22 | 140 | **1.97 m** | 20.37 m/s | — |
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
Doubling the winding widens the magnetic gap 12 → 22 mm, which costs a third of the thrust
constant — 11.22 → 7.46 N per kA/m. But sheet current doubles at *unchanged current
density*, and that more than compensates. With ordinary pocketing it clears the target at
J = 21 A/mm², the same copper loading as today.

Critically: **the stator does not ride the sled.** Its extra copper costs dry mass (P10 is
already open on that) but not exit velocity.

## What two-layer costs, and why it is not free

- **Copper loss doubles**, 672 J → roughly 1344 J per shot, and the campaign thermal case in
  `sizing.py` doubles with it.
- **Peak current goes to about 580 A** against 392 today. That collides with the A8 finding:
  the shot model has no ESR at all, and terminal sag is already 10.25 % rather than the
  published 4.88 %. At 580 A through 12–20 mΩ the droop is worse again, and the servo
  headroom behind the 0.027 m/s dispersion claim needs recomputing before two-layer can be
  called a fix.
- **Stator winding mass roughly doubles** — feeds directly into P10.
- Gen1 built two layers and Gen2/Gen3 built one; `parameters.json` still flags the decision
  open. This analysis is the first time the electromagnetic consequence has been costed.

## A reconciliation worth checking

Pocketing 40 % of the titanium gives 7.50 kg — **exactly the figure P5 quotes for the CAD
sled** — and 17.88 m/s, exactly the figure P8 quotes. That suggests the 7.50 kg was never
the as-drawn mass but an estimate with lightening already assumed, in which case P15's
9.445 kg and P5's 7.50 kg are the same design before and after pocketing rather than two
conflicting measurements.

**This is an inference, not a finding.** Check it against the CAD Master Plan that produced
the 7.50 kg before treating it as settled.

## Recommended order

1. **Run A4.** Every row above is priced against a mass that is currently unverified by
   structural analysis. CalculiX is installed; the decision rule is already declared.
2. **Then close G3-D4** with the thermal and electrical consequences computed, not only the
   magnetic ones.
3. **Put an ESR into `motor_model.py` regardless.** At 392 A it is a rounding error; at
   580 A it is not.
4. **Then** propagate to the scripts and the paper, once, per the standing rule.

## The option nobody wants to say out loud

Re-scope the claim to 17–18 m/s. That is still eight times what a spring deployer delivers,
and it is what the machine as drawn will actually do. It is not free either: P8 puts the
lifetime multiplier at ×1.68 at 17.88 m/s rather than ×1.80, so the astrodynamics headline
moves with it — and ×1.80 is the number GMAT has just independently confirmed.
