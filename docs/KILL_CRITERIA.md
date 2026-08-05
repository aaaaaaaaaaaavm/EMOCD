# What would make VOLLEY pointless

`OPEN_PROBLEMS.md` lists 33 numbered defects of very different weight. Most are engineering work.
A few are threats to whether the machine has any reason to exist, and they are hard to see when
they sit in a numbered list next to a stale cross-reference.

This file separates them. For each: **the value at which VOLLEY has no reason to exist**, where
it sits today, the margin, and what would close it. Ordered by how close each is to its
threshold, not by discipline.

**Two are close and one may already be crossed at the 3U design point.** That is the reason to
write this down rather than discover it in a review.

---

## 1. Mass per satellite, against the satellite doing it itself

**The sharpest threat, and the one this repository has not previously stated.**

A customer wanting 16.5 m/s has an alternative: put a cold-gas module on the satellite. The
rocket equation is unkind to VOLLEY here.

| | |
|---|---|
| Propellant for 16.5 m/s on a 4 kg 3U, cold gas at Isp 60 s | **0.111 kg** |
| A COTS 3U cold-gas module, wet, including tank, valves and drive | **0.5 to 1.2 kg** |
| VOLLEY's share, 76.5 kg over 12 satellites | **6.38 kg** |
| **Ratio** | **VOLLEY is about 8x heavier for the same delta-v** |

The 76.5 kg rollup includes parametric enclosure, thermal and avionics lumps, but none is physically measured and the packaging masses remain provisional. At a plausible 20 kg of
missing mass the figure becomes 8.08 kg per satellite.

> **Kill threshold: above roughly 2 kg per satellite, a rational customer buys a propulsion
> module instead.** That threshold is an estimate, from canisterised dispensers at about 2 kg/U
> and cold-gas modules at 0.5 to 1.2 kg. It is not a sourced industry figure and should be
> refined before it carries any more weight than it already does.

**Status at 3U: crossed.** 6.375 kg against a 2 kg threshold.

### What closes it, and it is not an engineering fix

Smaller payloads. The deployer mass is fixed; the number of satellites it carries is not:

| Payload | Fits the existing magazine volume | Deployer mass per satellite |
|---|---|---|
| 3U CubeSat | 12 | 6.375 kg, **fails** |
| 1U | 40 | 1.92 kg, marginal |
| TubeSat | 41 | 1.88 kg, marginal |
| PocketQube 3P | 108 | 0.71 kg, passes |
| **PocketQube 1P** | 326 | **0.24 kg, passes by 2 to 5x** |

**These counts were wrong here until 2026-07-31 and the correction is downward.** They were
raw volumetric bounds carrying a note that realistic packing is 40 to 60 % of them, and then
quoted unadjusted anyway: PocketQube 1P appeared as ~546 per load and **0.14 kg**, passing by
6x. `analysis/payload_family.py` now calibrates the packing efficiency so the 3U case returns
the twelve the machine is actually laid out for, and applies the same 56.2 % to every class.
The threat still closes, by a smaller margin than was published. See
[`PAYLOAD_CLASSES.md`](PAYLOAD_CLASSES.md).

### The argument that survives even at 3U, stated after the number and not instead of it

A cold-gas module requires the satellite to **carry propulsion**: a pressure vessel, a
qualification campaign, range-safety review, integration schedule, and an attitude control
system able to point the thruster. VOLLEY requires none of that, because the satellite is never
modified.

For a customer who has already chosen propulsion, VOLLEY loses on mass and should. For the
propulsion-less satellite it targets, which is most 3U rideshare payloads, the comparison is not
available to them at all. **That is a real argument, and it is much weaker than a reader who
found the 8x themselves would allow.**

---

## 2. Envelope: it does not fit the ride it is designed for

| | |
|---|---|
| Closed envelope, longest dimension | **1839 mm** |
| ESPA Grande class limit | ~1270 mm |
| Over | **44 %** |

> **Kill threshold: if it will not fit a rideshare port, the entire hosted-deployer concept has
> no vehicle.** This is binary.

**Status: crossed for ESPA Grande.** Open as **P9**; the fix is PII-4 and needs an owner decision
on target host class rather than analysis. The brake sits beyond the 1500 mm release point and
the enclosure must span it, so the length is structural rather than packaging slack.

A free-flyer removes this constraint entirely, which is one of the arguments for PII-8.

---

## 3. The bank cannot source the shot

| | |
|---|---|
| Hard ceiling on bank ESR | **65 mΩ** |
| A single string of 32 × 190 F cells | **116 to 185 mΩ** |

> **Kill threshold: if no purchasable bank can deliver the pulse, there is no machine.**

**Status: crossed as designed.** Open as **P26**, with four parallel strings costed at PII-7:
closes it with roughly 2x margin, at four times the cells, mass and cost. **Fixable, but the fix
lands on threat 1**, since four times the bank mass raises the mass per satellite that is already
failing at 3U.

---

## 4. Tip-off at release

If the satellite leaves tumbling faster than it can detumble, the customer has lost the mission,
and no customer accepts that risk twice.

> **Kill threshold: tip-off above 2 °/s per axis**, the flown NRCSD figure.

**Resolved 2026-07-31, and the resolution made the threshold harder.** This entry used to say the
run sheet declared ≤5 °/s citing NRCSD-E while a sibling NRCSD ICD said 2 °/s, and that the
discrepancy had to be settled first. **There was no discrepancy — they are two different
deployers.** NRCSD is the internal one, flown through the ISS airlock hundreds of times, at
**< 2 °/s/axis**. NRCSD-E is the external Cygnus-mounted one at < 5 °/s/axis, a figure its own
publisher describes as pending further testing.

So the band was set against the looser comparator, from the provisional document, with no record
that the tighter flown number existed. **A7's band is now 2 °/s** and is 2.5x harder to pass than
it was. See **P30**.

**Status: unmodelled, and the threshold just moved the wrong way for us.** A7 is specified and not
run; E7 is open. This is the least validated part of the design, it gates PII-1, and the payload's
centre of mass sits 70 mm off the thrust line, which is the term that drives tip-off in the first
place.

---

## 5. Attitude rate at the moment of firing

The 0.027 m/s dispersion claim assumes the host is pointing where the model says. Twelve
satellites index across two transverse cassettes between shots, moving kilograms of mass around
the structure.

> **Kill threshold: residual attitude rate at trigger above what the servo can null.** Above it,
> the deterministic-placement claim collapses, and deterministic placement is the entire
> differentiator against a spring.

**Status: MODELLED 2026-07-31 as A13, CORRECTED 2026-08-03, and it still FAILS.** Open as
**E24**.

**The indexing is fine and the sled return is not.** Advancing a satellite one cassette pitch
moves 4 kg; returning the 9.445 kg sled down 1.5 m of track is the term that dominates, and it was
in no budget anywhere in this repository until A13 ran.

**What the first version of A13 got wrong.** It read the peak angular momentum of a mass *while
it was moving* as a residual host rate *after* it stopped, which violates angular-momentum
conservation in its own ideal rigid-body model. A rigid host counter-rotates during the move and
returns to zero rate when the mass stops. What it keeps is an **attitude offset**, not a rate.

| Host | Index peak | Return peak | Residual ideal rate | Worst-case offset |
|---|---:|---:|---:|---:|
| 200 kg | 0.0195 °/s | **0.4427 °/s** | 0 | 1.367° |
| 500 kg | 0.0060 °/s | **0.1362 °/s** | 0 | 0.421° |

**The declared bands still fail**, on transient peak rate rather than residual: rows 3 and 4 are
**FAIL**, row 5 passes *only inside the ideal rigid-body model* because structural ringing is not
modelled (**E25**), and row 7 is **VOID** — there is no attitude controller, thruster geometry or
propellant model from which to compute a propellant change.

**The cadence conclusion that used to sit here is withdrawn.** The 8.2 s rate-null time, the
18.1 s cadence floor, the 6.9 s return optimum and the counter-mass recommendation all followed
from the residual-rate error and do not survive it. Attitude restoration now depends on a
controller and a schedule that this project has not specified, so there is no floor to quote.

**What the threshold turns on is still a number nobody has written down.** The repository carries
**two** inter-shot intervals — 10–20 s in the paper, 1200 s in `astro.py`'s conjunction model —
and never reconciles them (**P31**). That contradiction is untouched by the correction, and it
still decides whether this failure is operationally significant or a rounding error.

---

## 6. Host recoil

65.6 N·s per shot, **0.787 kN·s** for a full manifest, about 0.37 kg of
hydrazine-class propellant for the host to null.

> **Kill threshold: if a host will not accept the momentum and the pointing disturbance, nobody
> flies it.**

**Status: quantified and modest.** The fuel bill is independent of host mass; host mass sets the
per-shot rate disturbance. This is the healthiest item on the list, and it is here because it is
a customer decision rather than an engineering one.

---

## 7. Whether 16.5 m/s is worth anything

The threat behind all the others. If the delta-v does not buy something a customer wants, the
mass, the envelope and the bank are all irrelevant.

| What one shot buys | | |
|---|---|---|
| Orbital lifetime | ×1.62 at mean activity | **not invariant across solar activity** (P16) |
| Constellation phasing, 30° | 1.4 to 6.9 days | against **25 days** by differential drag |
| Apogee placement | ±0.10 km | from the closed-loop dispersion |
| **Plane change** | **0.12°** | **effectively nil** |

> **Kill threshold: if differential drag or onboard propulsion delivers the same outcome, there
> is no product.**

**Status: survives, narrowly, on one axis.** The phasing case is strong: 18x faster than drag,
and drag cannot be scheduled. The lifetime case is modest. **The plane-change ceiling of 0.12°
means VOLLEY cannot change orbit in the way "deployment at a chosen orbit" might suggest**, and
any framing implying otherwise is wrong.

---

## What this list says, taken together

**The 3U configuration as designed fails three thresholds**: mass per satellite, envelope, and
bank sizing. Two have identified fixes that make the third worse, since a bigger bank and a
repackaged envelope both add mass.

**The payload ladder is the only change that improves all three at once.** Smaller satellites
divide the fixed deployer mass across more customers, and the mass argument reverses from an 8x
loss to a 6x win. That is why [`PAYLOAD_CLASSES.md`](PAYLOAD_CLASSES.md) is the highest-value
work available, ahead of any velocity recovery.

**Nothing here is fatal to the concept**, and two items are close enough to the line that they
should be treated as design drivers rather than open problems. That distinction is what this
file exists to make.

---

## Provenance

Every threshold above is either computed in `analysis/`, taken from a published standard, or
labelled as an estimate. **The 2 kg per satellite figure in threat 1 is an estimate**, and it is
the one doing the most work, so it is the one most worth refining. Cold-gas module masses are
from published COTS ranges rather than a specific quotation.
