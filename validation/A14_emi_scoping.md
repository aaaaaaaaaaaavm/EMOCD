# A14: what the deployer's electromagnetic environment does to the payload and to comms

**Advances:** `OPEN_PROBLEMS.md` **E12**, open since the first defect sweep and the oldest
unquantified item in the project. **Does not close it** — E12 closes on T-6, a measurement.

> ## BANDS DECLARED 2026-08-05. NOT YET RUN.
>
> Everything below the "Acceptance bands" heading was written and committed **before**
> `validation/emi/emi_scoping.py` existed. `git log` is the evidence. No result appears in this
> file yet, and no band in it may be widened once one does.

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
