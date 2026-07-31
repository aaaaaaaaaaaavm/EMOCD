# Phase II: deferred work, and how it gets back

Everything here would make the design **better**. Nothing here makes it **correct**. That
distinction is the whole of the change-control rule in [`../BASELINE.md`](BASELINE.md), and
it is why these items are deferred while P17, which is tedious and improves nothing anyone
will notice, is not.

Phase II lives in **[VOLLEY-lab](https://github.com/aaaaaaaaaaaavm/VOLLEY-lab)**, a separate
repository with no baseline and no stability promise. It is separate because a soft boundary
inside the flagship is one `git checkout` from becoming an edit to the frozen baseline.

---

## The gate

**Phase II items are reviewed only at baseline boundaries.** The next boundary opens after
thesis submission. Between boundaries, items may be *added* and *worked on* freely, that is
what the lab is for, but nothing is promoted into the Phase I baseline.

**Every item carries an entry criterion written when it was deferred**, not when it is
reviewed. This is the same discipline as declaring acceptance bands before a run, and for
exactly the same reason: a criterion written afterwards is written by someone who already knows
what they want the answer to be.

At a boundary each item gets one of three outcomes, recorded here:

| | |
|---|---|
| **Promoted** | Criterion met. Becomes baseline work, gets an ADR, propagates scripts to figures to paper |
| **Held** | Criterion not yet met. Stays with the reason recorded |
| **Dropped** | Criterion shown unreachable, or the item is superseded. Stays in this file struck through, dropped items are evidence too |

An item may not be promoted by finding it interesting. It is promoted by meeting the criterion
it was given.

---

## Deferred items

### PII-1: Momentum-transfer release

**The strongest idea in the project, and it defers.**

Sled and payload need not separate at the same speed. A momentum-conserving spring push at the
end of the stroke recovers the entire velocity shortfall for **41.8 J against a 2881 J shot
(1.5 %)**, and brake duty *falls* because the sled leaves slower. Against stroke-lengthening,
which needs **673 mm** more envelope on a machine already 44 % over ESPA, this needs **43 mm** of
guided rail.

**Re-run 2026-07-31 with regeneration in the model, and the two compound.** Regeneration takes a
fixed ~296 J over the 240 mm of regen stator whatever speed the sled enters at, so the kick and
the recovery act on different terms rather than competing. Together they take
electrical-to-payload efficiency from **21.2 % to 31.6 %** and brake duty from **1291 J with
neither to 711 J with both**. That is past the 31.5 % the superseded 4.86 kg design claimed, on a
sled twice the mass.

Held at the 25 g qualification limit the kick is 15.6 ms over 42.7 mm at 981 N, an ordinary
spring, not a shock event. Full working in
[`DESIGN_OPTIONS_exit_velocity.md`](DESIGN_OPTIONS_exit_velocity.md).

> **Entry criterion.** A7 (separation and tip-off) must run and show that a guided release
> through 43 mm of relative travel holds tip-off inside the band **against its correctly
> sourced value**, the run sheet declares ≤5 °/s citing NRCSD-E while the sibling NRCSD ICD
> says 2 °/s, and that must be resolved first. Plus a mechanism concept that resets twelve
> times and has a safing path for a cocked 42 J spring through the existing three-inhibit
> chain.

**Why it is not Phase I:** it adds a mechanism to the release path, the one place ADR-008
deliberately removed complexity, and it would reopen the tip-off claim, which is already the
least validated part of the design.

### PII-2: Rib-stiffened chassis

A4 shows the drawn plate passes with a **17x stress margin**, so mass can come out. Uniform
thinning is nearly worthless, deflection goes as 1/t³, the budget is spent near 5.5 mm for
0.30 kg, worth about 0.2 m/s. Real reduction needs section depth, and **nobody has designed
one**, which is why the 60 % pocketing row in `DESIGN_OPTIONS_exit_velocity.md` is unsupported.

> **Entry criterion.** A rib-stiffened design that meets A4's three declared bands, 0.025 mm
> airgap closure per plate, 587 MPa allowable, first mode > 200 Hz, at a mass whose exit
> velocity beats 16.537 m/s by more than the ±20 % uncertainty on K<sub>t</sub>. Anything
> inside that uncertainty is not yet a demonstrated gain.

### PII-3: Two-layer stator (G3-D4)

Gen1 built two layers (324 conductors), Gen2 and Gen3 one (162). The decision is flagged open
in `cad/parameters.json` and **sits upstream of K<sub>t</sub>**. Doubling the winding widens
the magnetic gap 12 to 22 mm and drops K<sub>t</sub> from 11.22 to 7.46 N per kA/m, but sheet
current doubles at unchanged current density: **20.61 m/s at a 7.50 kg sled, J still
21 A/mm²**. The stator does not ride the sled, so its copper costs dry mass, not velocity.

> **Entry criterion.** A1 must run first, this trades one K<sub>t</sub> against another, and
> both are currently checked only analytic-against-analytic. **Then PII-7 must be settled, and
> that is now a gate rather than a caution.** `analysis/velocity_levers.py` computes the bank ESR
> ceiling for every lever by bisecting the real integrator: two-layer draws **597 A** and drops
> the ceiling from 66 to **39 mohm**, which needs four parallel strings with no margin, and with
> 40 % pocketing it is 637 A and 36 mohm. The electromagnetic case for two-layer is the best in
> the table and its power-system case is the worst. **PII-3 may not be reviewed before PII-7
> closes.**

### PII-4: Envelope repackaging (P9)

The closed envelope is **1839 mm against ESPA Grande's ~1270 mm (44 % over**) because the
brake sits beyond the 1500 mm release point and the enclosure must span it. Options: shorten
the track, repackage the brake, or accept a host that does not impose the envelope.

> **Entry criterion.** Owner decision on target host class, which is not an engineering
> question. If ESPA Grande is retained, a packaging concept that fits ~1270 mm without
> reducing stroke below what the velocity claim needs.

**Note:** P9 stays open as a Phase I *defect*, the paper must state the overrun honestly,
which it now does. Only the *fix* is Phase II.

### PII-5: Variable-shape atmosphere in `astro.py`

P16's root cause: solar activity enters as a uniform density scale and ballistic coefficient
enters the same multiplicative slot, so neither sweep can move the ratio it claims to test.
The model's arithmetic is not wrong; its parameterisation cannot express the effect being
claimed.

> **Entry criterion.** A5 re-run at the current operating point, plus GMAT at BC 40 and 90 to
> establish what the true BC dependence actually is. Replacing the atmosphere before knowing
> that would be fixing a model against an unmeasured target.

**Phase I keeps the honest version:** quote the multiplier at a stated activity level and claim
no invariance. That is already done.

### PII-6: Reachable-domain analysis

The strongest single thing the prior-art review turned up. Feng et al. compute a 3-D envelope of
the orbits one shot makes available, reconstructed with an alpha-shape algorithm. This project
reports a scalar lifetime multiplier, which answers a smaller question: how much longer does the
satellite stay up, rather than where can it be put.

Their method is better, and [`PRIOR_ART.md`](PRIOR_ART.md) says so rather than working around it.
A deployer whose selling point is a programmable per-satellite velocity should be able to state
what that velocity buys as a region, not a number.

> **Entry criterion.** A5 re-run at the current operating point first. A reachable domain built on
> a superseded delta-v would be an elaborate way to publish a stale result, and P19 already records
> one of those.

**Not Phase I.** The scalar multiplier is correct, sourced and cross-checked against GMAT. It is
narrower than the alternative, which makes the envelope an improvement rather than a correction,
and `docs/BASELINE.md`'s rule puts improvements here.

### PII-7: A bank that can actually source the shot (P26)

**Phase I if the programme wants a defensible rated point; Phase II only because the current
one is honestly labelled as not closing.** A10 established a hard ceiling of **65 mohm** on bank
ESR, and a single string of 32 x 190 F cells gives 116 to 185 mohm.

Parallel strings divide resistance and multiply capacitance. The bank is priced in
`analysis/cost.py` at INR 240,000 for 32 cells, so each added string costs the same again:

| Strings | Cells | Bank C | Bank ESR | Against the 65 mohm ceiling | Bank cost |
|---|---|---|---|---|---|
| 1, as designed | 32 | 5.9 F | 116-185 mohm | **fails, 1.8-2.8x over** | INR 240 k |
| 2 | 64 | 11.9 F | 58-93 mohm | marginal, fails at the pessimistic end | INR 480 k |
| 3 | 96 | 17.8 F | 39-62 mohm | closes, no margin | INR 720 k |
| **4** | **128** | **23.8 F** | **29-46 mohm** | **closes with roughly 2x margin** | **INR 960 k** |
| 6 | 192 | 35.6 F | 19-31 mohm | comfortable | INR 1.44 M |

Four strings is the first row that closes at the pessimistic ESR with margin left for
temperature and ageing, both of which move ESR the wrong way. It costs **four times the cells
and four times the bank mass**, against a mass rollup that already excludes the enclosure,
radiator and avionics (P10), and a cost model in which the bank is already the second largest
line at 17.8 %.

**The alternatives, neither costed here:**

- **Accept a lower rated point.** Lower commanded force lowers peak power, which raises the
  ESR ceiling. This trades exit velocity for a buildable bank and needs the trade curve
  computed before it can be argued.
- **Change technology.** Lithium-ion capacitors trade ESR for energy density; a battery plus a
  small capacitor front end moves the pulse burden elsewhere. **The reading gap that blocked this
  is now closed**: `LITERATURE.md`'s pulsed-power cluster went from 2 entries to 29 on
  2026-07-31, covering ESR definition and measurement, ageing and derating, pulse-forming
  networks, and lithium-ion capacitors including one flown system (NESSIE, 2013). None of it has
  been *read* yet, and the entry criterion below is unchanged by that.

> **Entry criterion.** ~~The pulsed-power literature gap filled first~~ **(done 2026-07-31,
> 29 entries)**, then that cluster actually read, and then a cell selected from a manufacturer
> datasheet rather than a distributor listing, with **DC** ESR at the operating temperature and
> its derating with age. Two things the new reading list already flags make this sharper: the
> published end-of-life criterion for these parts is a **two-fold ESR increase**, and operation
> to −40 °C can double ESR without shortening life. A10's ceiling has no room for either.
> **A bank chosen on an interpolated ESR would repeat the error that produced P26.**

**Why this is not simply Phase I.** It is a sizing decision with a 4x cost and mass
consequence, and the honest Phase I position is the one now published: the rated point assumes
a bank that cannot be bought, and that is stated rather than quietly re-sized.

### PII-8 to PII-11: recorded in the lab, not here

Four items live in [VOLLEY-lab](https://github.com/aaaaaaaaaaaavm/VOLLEY-lab) rather than this
file, because they are programme directions and scaling studies rather than deferred fixes to
this design. **The flagship stays authoritative for PII numbering**, so they are listed here to
stop the numbers forking, which they briefly did.

| | |
|---|---|
| **PII-8** | **VOLLEY as a free-flyer.** A long deployed track plus release at perigee reaches TLI and Mars-class C3 without exceeding CubeSat qualification. Three unsolved problems in front of it: airgap straightness at 0.7 to 2 ppm over a deployed structure, a 294 kJ shot against a bank that already fails at 2.88, and whether 25 g survives review as a *sustained* load rather than a transient |
| **PII-9** | **The lunar case.** Where this technology has always belonged, and the O'Neill mass driver it descends from. 1.33 MJ/kg to lunar orbit, so 15 kW launches a tonne a day. The payload is ore, so the g-limit that governs this entire design disappears |
| **PII-10** | **Magazine indexing disturbance** (E24). Designing an indexing sequence that minimises attitude disturbance. The *bookkeeping* half is an error correction and belongs upstream in Phase I; only the optimisation belongs in the lab |
| **PII-11** | **[A deployable track, and the side-rail layout](https://github.com/aaaaaaaaaaaavm/VOLLEY-lab/blob/main/PII-11_deployable_track.md).** A telescoping track long enough to accelerate *and* regeneratively arrest the sled reaches **48 % electrical-to-payload efficiency against 21.2 %**, deletes the eddy brake, closes P28, and stows at 1150 mm — **inside** the ESPA Grande envelope this design misses by 44 %. The only option in the programme that improves velocity and envelope together. The side-rail half loses on thrust in every variant priced and is there because it drives the tip-off moment to zero |

> **Entry criterion for PII-8, PII-9 and PII-11: none, deliberately.** None is a candidate for
> this baseline. The correct outcome for the thesis is that all stay closed until the Phase I
> deliverables ship, and the flagship currently has three crossed kill criteria, one failed
> validation and no measured number.
>
> **PII-11 is the one that will be hardest to leave shut**, because unlike the others it improves
> the machine that is actually being built rather than describing a different one. That is exactly
> why it needs the gate: `docs/BASELINE.md` puts architecture changes in Phase II **by type**, and
> a deployable structure is an architecture change however good its numbers are.

---

## Review log

| Boundary | Date | Outcomes |
|---|---|---|
| *(none yet)* | | First boundary opens after thesis submission |

## Adding an item

Name it, state what it buys with a number, say **why it is improvement rather than
correction**, and write its entry criterion before you stop thinking about it. An item without
a criterion is not deferred, it is abandoned with extra steps.
