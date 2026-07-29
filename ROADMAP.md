# Roadmap

> **The dates below are assumed, not fixed.** They are written against a standard Indian
> final-year calendar — thesis submission around **April–May 2027**, viva **May–June 2027**,
> placement season running from now. If your actual dates differ, correct this file first;
> everything downstream is sequenced from it.
>
> Last updated **2026-07-29**.

This project publishes its own defects — nineteen numbered problems and twenty-three open
engineering items. That is deliberate, and it only reads as rigour if there is also a plan
for closing them. This is that plan.

---

## Where this stands today

| | |
|---|---|
| Maturity | TRL 2–3. Analysis and CAD complete; nothing built or measured |
| Rated performance | **16.5 m/s at 10.7 g**, from a sled mass measured in CAD, not estimated |
| Validations run | 3 of 8 — **but all three predate the current operating point** (P19) |
| Biggest single gap | K<sub>t</sub> = 11.22 N per kA/m is checked only analytic-against-analytic. Every headline number is downstream of it |
| Paper | Source current as of 2026-07-29; committed PDF needs a rebuild |

---

## Next — by end of August 2026

**1. A1, the airgap field.** *Closes E1, E2; underwrites every other number.*
The thrust constant has never been checked by a second physical method. FEMM 4.2 runs under
Wine (documented at `femm.info/wiki/linuxsupport`; `py2femm` automates the Lua path), and
Elmer or GetDP+Gmsh are native-Linux alternatives that are meshed differential FEM rather
than integral superposition. The DXF and run sheet already exist in `analysis/femm/`, so
this is an install problem, not a modelling one. **Do this first.** If K<sub>t</sub> is
wrong, everything below is re-work.

**2. Re-run A8.** *Closes half of P19.*
Minutes of work — `validation/spice/emocd_shot.cir` needs its `.param` line moved to the
current operating point. Re-read the declared bands **before** running, not after.

**3. Answer the rib-stiffened chassis question.** *Closes P5, P8, E2 properly.*
A4 says the drawn plate passes with a 17× stress margin, so mass can come out — but nobody
has designed the lighter chassis, which makes the 60 % pocketing row in
`docs/DESIGN_OPTIONS_exit_velocity.md` unsupported. Until this is settled, re-running A5
just banks another stale result.

## Then — September to November 2026

**4. A7, separation and tip-off.** *Closes E7; gates the momentum-transfer option.*
Retry `pychrono` from conda-forge (it is not on PyPI, which is the likely cause of the
"not installable" note). **Check the acceptance band against its source first** — the run
sheet declares ≤5 °/s citing NRCSD-E, and the sibling NRCSD ICD says 2 °/s.

**5. Cost the momentum-transfer release properly.** *Attacks P8 from a new direction.*
`docs/DESIGN_OPTIONS_exit_velocity.md` shows it recovers the full velocity shortfall for
41.8 J against a 2630 J shot, and for 43 mm of guided rail against the 673 mm that
lengthening the stroke would need. It needs a mechanism design and A7 behind it. This is
the most promising unexplored direction in the project.

**6. Close P17.** Write the run sheet with a band declared **in advance**, then propagate
`sizing.py` once — the corrected attraction moves plate stress, retention-gate sizing and
the A4 load together.

## Then — December 2026 to February 2027

**7. Re-run A5** once the mass is settled, at the current operating point. Days of wall
time for the low-activity leg; schedule it, do not babysit it.

**8. A6, conjunction P<sub>c</sub>.** ~50 lines of scipy against the OEM ephemerides
`validation/gmat/` already emits. E18's covariance problem stands regardless, so state the
assumption rather than pretending to a covariance that does not exist.

**9. Run A9 — decay against flown CubeSats.** `validation/A9_tle_decay.md`, bands already
declared, script already written (`validation/tle/fit_decay.py`). Needs only a machine with
ordinary internet and a free Space-Track account — it is blocked here by network policy, not
by difficulty. **This is the only analysis specified anywhere that compares the model against
something that happened** rather than against another model.

**10. Replace the modelled comparator with flown data.** Foster et al.'s differential-drag
results for Planet Labs are open-access (arXiv 1806.01218, 1509.03270). The cheapest
credibility improvement available: one modelled number becomes one measured number.

## Before submission — March to April 2027

**11. ~~Rebuild the paper~~** — done 2026-07-29; TeX Live installed and the PDF now matches source.
**12. Final consistency sweep** — every number in every document against
`analysis/results/*.json`, the way the 173-value reproduction check was run.
**13. Thesis document** assembled from the paper, the CAD record and the validation
history.

---

## What is deliberately not on this list

**Hardware.** E4 records that nothing has been built. That has not changed, but as of
2026-07-29 the protocol exists: `docs/BENCHTOP_TESTS.md` specifies four sub-scale experiments
with bands declared in advance, and `docs/QUALIFICATION_PLAN.md` specifies the full campaign.
**B-1 — a Halbach pair on a gaussmeter — costs roughly the price of two magnets and is the
single highest-value thing anyone could do to this project.** It is listed here rather than in
the dated sequence above because it depends on a budget and a bench, not on a date.

**Anything that would move a number without an analysis behind it.** The standing rule holds:
record the discrepancy, run the analysis, propagate once.
