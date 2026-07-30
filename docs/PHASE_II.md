# Phase II: deferred work, and how it gets back

Everything here would make the design **better**. Nothing here makes it **correct**. That
distinction is the whole of the change-control rule in [`../BASELINE.md`](BASELINE.md), and
it is why these items are deferred while P17, which is tedious and improves nothing anyone
will notice, is not.

Phase II lives in **[EMOCD-lab](https://github.com/aaaaaaaaaaaavm/EMOCD-lab)**, a separate
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
end of the stroke recovers the entire velocity shortfall for **41.8 J against a 2630 J shot
(1.6 %)**, and brake duty *falls*, 1291 to 1050 J, because the sled leaves slower. Against
stroke-lengthening, which needs **673 mm** more envelope on a machine already 44 % over ESPA,
this needs **43 mm** of guided rail.

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
> both are currently checked only analytic-against-analytic. Then peak current at ~580 A must
> be shown compatible with the A8 ESR finding, which flagged the pulse chain at 392 A.

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

---

## Review log

| Boundary | Date | Outcomes |
|---|---|---|
| *(none yet)* | | First boundary opens after thesis submission |

## Adding an item

Name it, state what it buys with a number, say **why it is improvement rather than
correction**, and write its entry criterion before you stop thinking about it. An item without
a criterion is not deferred, it is abandoned with extra steps.
