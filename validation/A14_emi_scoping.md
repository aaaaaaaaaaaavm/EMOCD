# A14: what the deployer's electromagnetic environment does to the payload and to comms

**Advances:** `OPEN_PROBLEMS.md` **E12**, open since the first defect sweep and the oldest
unquantified item in the project. **Does not close it** — E12 closes on T-6, a measurement.

> ## RUN 2026-08-05. Verdict **six of eight PASS, one FAIL, one VOID as declared**
>
> Bands were committed at **`c274473`**, before `validation/emi/emi_scoping.py` existed. `git log`
> is the evidence. No band was widened.
>
> **Band 4 FAILS, and it fails by 611×.** The static Halbach field at the payload's nearest face
> is **61.1 mT** — 1357× Earth's field and 611× a magnetometer's full scale. The switching
> transient, which is what everyone including me assumed was the problem, is **not** the dominant
> term. Results below.

## Result, 2026-08-05

| # | Question | Band | Result | Verdict |
|---|---|---|---:|---|
| 1 | EMF from commutation, 10 cm² loop at the nearest face | < 50 mV | **11.83 mV** | **PASS** |
| 2 | EMF from 20 kHz PWM ripple, same loop and station | < 50 mV | **36.01 mV** | **PASS, narrowly** |
| 3 | Worst of the above against the digital threshold | < 400 mV | 36.01 mV | **PASS** |
| 4 | Static field at the nearest face vs magnetometer full scale | ≤ 100 µT | **61.08 mT** | **FAIL, ×611** |
| 5 | Static field at CoM and far face, multiples of Earth | report; VOID | 10.3× / 7.6× | **VOID as declared** |
| 6 | Spectral margin below the SiC knee at every comms band | > 40 dB | **56 dB** worst | **PASS** |
| 7 | Radiation efficiency at the 20–40 kHz fundamental | < 1e-6 | **6.0e-8** | **PASS** |
| 8 | Coilgun-to-VOLLEY induced-EMF ratio at equal geometry | > 100× | **666×** | **PASS** |

### The field at each station

| Station | Behind the array back face | AC armature field | Static field | EMF, commutation | EMF, 20 kHz ripple |
|---|---:|---:|---:|---:|---:|
| Payload nearest face | 6 mm | 5.515 mT | **61.081 mT** | 11.83 mV | 36.01 mV |
| Payload centre of mass | 56 mm | 0.0079 mT | 0.463 mT | 0.017 mV | 0.052 mV |
| Payload far face | 106 mm | 0.0000 mT | 0.341 mT | 0.000 mV | 0.000 mV |

### What this actually found

**The dominant term is the permanent magnets, not the drive.** That is the opposite of what the
question is usually asked about, and it is the finding worth carrying: the payload's nearest face
sits 6 mm behind a Halbach array and sees 61 mT, while the entire switching transient produces
36 mV in an unshielded loop at the same place. A customer worried about the *inverter* is worried
about the wrong thing.

**Band 2 passes narrowly and that matters.** 36 mV against a 50 mV threshold is 1.4× of margin, on
an upper-bound calculation with no shielding and no payload structure. At 40 kHz the ripple halves
and so does the EMF, to about 18 mV. **This corroborates P33 independently**: the 20 kHz end of
the declared switching range is defensible on loss but marginal on coupling, and the design should
sit at the top of the range.

**Comms is not a live concern.** The SiC knee is 6.4–15.9 MHz, putting UHF 56–72 dB below it, GPS
L1 80–96 dB and S-band 86–102 dB, and the 1.839 m structure has a radiation efficiency of
**1.5e-8 to 6.0e-8** at its own drive frequency — it cannot radiate at the fundamental. The
credible coupling path to a launch vehicle's communications is **conducted, through a shared power
bus**, not radiated, which is a specification problem rather than a physics one.

### The two far stations are in a regime this model gets wrong, and P3 says so

The decay sweep behind the array is exponential to about 40 mm and then flattens into an
edge-effect tail: 61.1 mT at 6 mm, 7.8 at 16 mm, 2.2 at 26 mm, then 0.62, 0.46, 0.34 mT at 42, 56
and 106 mm. **P3 already records that this model's 20 mm and 50 mm stray values do not reproduce
the paper's**, attributing it to sensitivity to modelled array length, with edge effects
dominating the far field. That is exactly the regime the CoM and far-face rows sit in.

**So band 4's failure is solid and bands 5's numbers are not.** The nearest-face value is in the
exponential near field, where the 10 mm station reproduces exactly and P3 says the model is
sound. The CoM and far-face figures inherit P3's uncertainty, which is a second and independent
reason band 5 is VOID rather than a soft pass.

### Band 8: the 2021 judgement was right, and it was still not justified

Per Feng et al.'s stage parameters, a coilgun stage discharges **392 kA** at a 217 Hz equivalent
rate, giving **355.6 mV** in the same loop at the same 0.3 m standoff against VOLLEY's 0.534 mV —
a ratio of **666×**. The band asked for > 100×, so the electromagnetic half of the 2025
architecture decision holds.

**It holds by a margin nobody had computed.** `docs/HISTORY.md` records that the judgement was an
instinct about pulsed megaampere discharges next to unshielded electronics. The instinct was
correct. It was still an instinct, and 666× is the first number this project has ever put behind
it. Both halves of that sentence belong in the record.

Both sides of the ratio use the same crude infinite-wire model so the comparison is symmetric.
VOLLEY's three-phase fields largely cancel at distance, so that model **overstates** VOLLEY and
the true ratio is larger than 666×. The absolute VOLLEY figures in the table above use the
harmonic-decay model, not the wire model.

### Consequences, taken from the rule fixed before the run

Outcome 1 was the declared case: bands 1–3 pass and band 4 fails, so the dominant term is static
and E12 splits. The AC half is scoped and hands off to T-6 for confirmation. **The static half
becomes a new numbered defect**, because a 3U payload cannot fly a magnetometer in this magazine
without a keep-out or a shield, and that is a payload compatibility constraint belonging in the
interface specification rather than an appendix.

**This analysis does not close E12.** E12 closes on T-6, which is a measurement, and nothing here
is measured.

---

## Why this analysis exists

Two separate facts put it here on the same day.

**The 2025 decision to drop the coilgun rested partly on this and never computed it.** My
2021–2025 notebooks give two reasons for abandoning the coilgun: the acceleration is enormous and
"the EMI environment is awful", and either defeats the point of carrying an *unmodified* CubeSat
([`../docs/HISTORY.md`](../docs/HISTORY.md#why-the-coilgun-was-actually-dropped)). The
acceleration half is now a number in ADR-003. The electromagnetic half has no working behind it
anywhere. An architecture was rejected on grounds that were never calculated, and the successor
has never had its own calculated either.

**The same gap exists in my other electromagnetic launch paper**, whose abstract lists
"electromagnetic coupling" among challenges "identified and analyzed" while its body never
returns to the subject ([`../docs/SKILLS.md`](../docs/SKILLS.md)). Two studies, no EMI
calculation in either.

**And the question has now been asked from outside the project**, by a systems engineer wanting
to know what the emissions do to the payload and to the launch vehicle's communications. That is
exactly the pair E12 covers and has never answered.

**P33 is what makes it computable today.** Until 2026-08-05 this repository had no phase current
and no winding inductance — `motor_model.shot()` integrates in sheet current and its `I_peak` is
the DC-link draw. `analysis/drive_electrical.py` now supplies both, so the `dI/dt` that drives
inductive coupling is a derived quantity rather than a guess.

## What this is, and what it is not

**It is a scoping calculation from quantities already in `analysis/results/`.** No new apparatus,
no new constants, no measurement. Its purpose is to establish **which term dominates** — the
switching transient or the static Halbach field — so that T-6 measures the right thing, and to
put a number against a nine-year-old judgement.

**It is not an EMC qualification.** MIL-STD-461 RE102/CE102 limits are absolute field strengths
at a specified distance with a specified antenna; reproducing them needs a radiating model this
project does not have. Bands 6 and 7 below are therefore **relative** margins, which is what a
scoping pass can honestly assert. T-6 in [`../docs/QUALIFICATION_PLAN.md`](../docs/QUALIFICATION_PLAN.md)
remains the measurement and nothing here substitutes for it.

**It is model-to-model at best, and mostly model-to-comparator.** E4 stands: nothing measured.

## The geometry, read from CAD rather than assumed

`cad/parameters.json` `sled` and `payload_3u` fix where the payload actually sits. The Halbach
array's back face is at **z = 14 mm** from the thrust line (`halbach_array_z_outer`). The payload
is 100 mm tall with its centre of mass 70 mm above the thrust line
(`payload_com_offset_above_thrust_line`), so it spans z = 20 to 120 mm.

| Station | Distance behind the array back face |
|---|---|
| Payload nearest face | **6 mm** |
| Payload centre of mass | **56 mm** |
| Payload far face | **106 mm** |

**The nearest face is 6 mm from the back of a Halbach array**, inside the 10 mm station at which
`verify_field.py` already reports 22.7 mT. That is the number this analysis exists to take
seriously.

## Inputs, every one traceable

| Quantity | Value | Source |
|---|---|---|
| Peak phase current | 373.2 A | `drive_electrical.phase_current_peak_A` |
| Phase inductance | 19.70 µH | `drive_electrical.phase_inductance_H` |
| Commutation fundamental | 341.4 Hz | `drive_electrical.commutation_Hz` |
| `dI/dt`, commutation / PWM | 8.007e5 / 4.874e6 A/s | `drive_electrical.didt_*` |
| Sheet current amplitude | 126 kA/m | `motor_model.K_RATED` × 0.9 |
| Magnetic wavelength | 48 mm | `motor_model.LAM` |
| Static stray field, 10/20/50 mm | 22.7 / 4.3 / 0.4 mT | `field_verification.stray_field` |
| Switching frequency | 20–40 kHz | `paper.tex`, drive section |
| Structure longest dimension | 1.839 m | `docs/KILL_CRITERIA.md` §2 |

## Comparators, and their provenance

**P30's lesson applies here.** That defect was setting a band at the easier of two available
comparators without recording that a tighter one existed. So each comparator below carries what
it is and how firm it is.

| Comparator | Value | Status |
|---|---|---|
| Earth's magnetic field, LEO | **45 µT** | factual, 25–65 µT range |
| Attitude-magnetometer full scale | **±100 µT** | **class figure**, not a datasheet. COTS CubeSat magnetometers measure Earth's field and typically saturate between ±60 and ±100 µT. To be replaced by a specific part before this is cited |
| Digital logic noise margin, 3.3 V CMOS | **400 mV** | class figure, V_IH/V_OH typical |
| Analog / sensor front end | **50 mV** | class figure, deliberately the stricter of the two |
| Comms bands | UHF 400 MHz, GPS L1 1575.42 MHz, S-band 2200 MHz | standard allocations |
| Coilgun comparator | Feng et al. per-stage discharge | ADR-003, `docs/PRIOR_ART.md` |

**One comparator is deliberately absent.** A threshold for permanently magnetising a payload's
soft-magnetic parts would need a materials list this project does not have. Rather than invent
one, band 5 reports the field and is **declared VOID-able** on that ground.

---

## Acceptance bands

Declared before the script exists. Each is capable of failing.

| # | Question | Band | What a miss means |
|---|---|---|---|
| 1 | Induced EMF from commutation in a 10 cm² unshielded loop at the payload's **nearest face** | **< 50 mV** | above the analog threshold, an unmodified CubeSat's sensor lines see the shot |
| 2 | Induced EMF from **PWM ripple at 20 kHz**, same loop and station | **< 50 mV** | the 16.3 % ripple couples; argues for the 40 kHz end of the range |
| 3 | Either of the above against the **digital** threshold | **< 400 mV** | a miss here is a design problem, not a caveat |
| 4 | Static field at the payload **nearest face**, against magnetometer full scale | **≤ 100 µT** | a magnetometer-carrying payload cannot fly in this magazine unshielded |
| 5 | Static field at payload **CoM** and **far face**, in multiples of Earth's field | **report**; VOID as a magnetisation test, no materials list exists | — |
| 6 | Spectral margin at UHF, GPS L1 and S-band below the SiC switching knee | **> 40 dB at every band** | switching harmonics reach a comms band and T-6 must be prioritised |
| 7 | Radiation efficiency of the 1.839 m structure at the 20–40 kHz fundamental | **< 1e-6** | the machine is an efficient antenna at its own drive frequency, which would be a surprise |
| 8 | Coilgun-to-VOLLEY ratio of induced EMF at equal geometry | **> 100×** | **this is the band that tests the 2021 judgement.** Below ~10× and the decision's electromagnetic half was wrong |

### Bands 4 and 8 are the two that matter

**Band 4 is expected to be the hard one** and is written to fail rather than to be survived: 22.7 mT
at 10 mm against a 100 µT comparator is a factor of 227 before the 6 mm station is even
evaluated. If it fails, the honest consequence is not a footnote — it is that **the magnetic
keep-out is a payload compatibility constraint**, and it belongs in the interface specification
and on the front page, not in an appendix.

**Band 8 is the one with a verdict attached to a past decision.** If the ratio is large, the 2021
judgement was right, and the sheet should say it was right *without having been calculated*,
which is not the same as having been justified. If the ratio is small, ADR-003's electromagnetic
reasoning was wrong and that must be recorded as plainly as P17 and P22 were.

## What happens at each outcome, fixed now

1. **Bands 1–3 pass, band 4 fails.** The dominant term is the static field, not the switching
   transient. E12 splits: the AC half is scoped and closes to T-6 for confirmation; the static
   half becomes a **new numbered P-item** about payload compatibility, and T-6's priority rises.
2. **Bands 1–3 fail.** The switching design is implicated. `paper.tex`'s claim that EMI "is
   contained by keeping the high-`di/dt` loop area small, filtering the bank input, and enclosing
   the converter in a shielded housing" becomes a defect, because it would be asserting mitigation
   against an unquantified threat that turned out to be real.
3. **Band 6 or 7 fails.** The launch-vehicle comms question is live rather than closed, and T-6
   moves ahead of the benchtop programme.
4. **Band 8 fails.** ADR-003 gains a second amendment and `HISTORY.md` is corrected: the coilgun
   was dropped for a reason that does not hold.

**No band here may be widened after the run.** A missed band produces a numbered defect, not a
revised target — the rule in [`README.md`](README.md) that makes this directory tests rather than
exercises.
