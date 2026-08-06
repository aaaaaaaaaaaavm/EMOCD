# A17: does the force-ripple chirp excite the track's structural modes?

**Closes:** `OPEN_PROBLEMS.md` **E23**.

> ## RUN 2026-08-05. Verdict **FAIL — three of five bands, and E23's own argument is falsified**
>
> Bands committed at **`13b4b3b`**, before `analysis/chirp_response.py` existed. None widened.
>
> **E23 predicted this would be benign. It is not.** The sweep is *not* too fast for resonant
> buildup at the 109 Hz fixed-fixed mode, and the failure does not go away at any plausible Q.

## Result, 2026-08-05

Ripple amplitude **13.75 N** on 1389.3 N, sled acceleration 103.33 m/s². Peak dynamic
amplification, normalised so it is independent of modal mass:

| Crossing | Sweep rate | Q=20 | Q=50 | Q=100 | Q=200 | Q=350 | Q=500 |
|---|---:|---:|---:|---:|---:|---:|---:|
| 6th harmonic → 48 Hz pinned | 12 916 Hz/s | 1.09 | 1.12 | 1.13 | **1.13** | 1.13 | 1.13 |
| 6th harmonic → 109 Hz fixed | 12 916 Hz/s | 2.96 | 3.21 | 3.30 | **3.34** | 3.36 | 3.37 |
| **Fundamental → 109 Hz fixed** | 2 153 Hz/s | 6.51 | 7.51 | 7.95 | **8.18** | 8.29 | 8.33 |

| # | Question | Band | Result | Verdict |
|---|---|---|---:|---|
| 1 | Amplification at 109 Hz, Q ≤ 200 | < 2× | **3.34×** | **FAIL** |
| 2 | Amplification at 48 Hz, Q ≤ 200 | < 2× | 1.13× | **PASS** |
| 3 | Q at which amplification reaches 2× | report | **≤ 20 for both fixed-mode crossings** | reported |
| 4 | Peak displacement vs the ±0.05 mm gap budget | < 25 % | **49 %** | **FAIL** |
| 5 | Amplification at the fundamental crossing | < 2× | **8.18×** | **FAIL** |

### Why E23's argument fails, and it is not about Q

E23 reasoned that transit through any plausible half-power bandwidth takes about a millisecond,
too fast for buildup, and that the answer therefore hinged on a Q the repository does not have.
**Q is not the variable that matters here.** Between Q = 20 and Q = 500 the amplification at the
fundamental crossing moves only from 6.51 to 8.33 — it is already saturated at the lowest damping
anyone would assign to bolted aluminium.

What governs it is the **normalised sweep rate**, `rate/f²`. For the 6th harmonic through 48 Hz
that is 5.6 and the response barely builds. For the fundamental through 109 Hz it is **0.18**: the
excitation dwells near resonance for many cycles and the mode has time to respond regardless of
damping. **Band 3's answer is therefore that there is no Q low enough to make this benign**, which
is the opposite of what the item expected.

**The fundamental is the dangerous crossing, not the 6th harmonic**, and E23's table only listed
it in passing. It happens at 5.23 m/s, 50.6 ms into the stroke, 132.5 mm along — well clear of the
breech, contradicting E23's remark that the crossings occur while the sled is still next to the
launch-lock hardware. That was true of the 6th-harmonic crossings and not of the one that matters.

### What is robust here and what is not

**The amplification figures are robust.** They are dimensionless and independent of modal mass, so
they do not depend on the effective-mass assumption.

**Band 4's displacement is not.** It uses a uniform-beam effective mass of half the distributed
20 kg, and more importantly **the ripple force travels with the sled** — a moving load on a beam,
which this SDOF model does not represent. 49 % of the gap budget is an indication that the
coupling is worth taking seriously, not a number to design against.

### Consequence

**E23 is closed as an analysis and becomes a design driver.** `sizing.py`'s static "above 70 Hz to
clear the launch primary band" is necessary and not sufficient: the track also has to survive an
8× amplified ripple excitation at its own fixed-fixed mode, twelve times per campaign. That needs
a damping specification, which the project does not have, and it makes **T-2's sine sweep a
pass/fail qualification item rather than a signature comparison.**

Logged as a new numbered defect.

---

## Why

`sizing.py::track_first_mode()` checks the track against a **static** target — above 70 Hz to
clear the launch primary band. That is the right check for launch and the wrong one for the shot.

The electrical excitation is not at a fixed frequency. It sweeps from zero as `f = n·v/λ` with
λ = 48 mm, so **every shot chirps through the whole band below the running frequency**, twelve
times per campaign. E23 tabulates the crossings: the 6th harmonic passes the 48 Hz pinned mode
3.7 ms in and the 109 Hz fixed mode 8.3 ms in, both within the first few millimetres of travel
while the sled is still next to the breech and the launch-lock hardware.

**E23's own text says the likely answer is benign and that nobody has shown it.** The sweep rate
is roughly `a/λ` ≈ 2.2 kHz/s, so transit through any plausible half-power bandwidth takes about a
millisecond — too fast for resonant buildup. **But that argument depends on Q, and no Q, damping
ratio or loss factor appears anywhere in this repository.** `docs/CROSS_INDUSTRY.md` found no
citation addressing swept excitation of a linear stage, because industrial stages run at constant
velocity and do not chirp.

## Method

`analysis/chirp_response.py`. A single-degree-of-freedom oscillator at each mode, driven by the
ripple force under a **linear frequency chirp** at the rate the shot actually produces, integrated
through the crossing. The response is compared against the static deflection the same force
amplitude would produce.

**Q is swept, not chosen.** Bolted aluminium structure plausibly runs Q = 20 to 500; the sweep
covers it and the result is reported as a function of Q, the same posture A6 took with the
covariance it could not obtain.

Excitation amplitude is the **±0.99 % force ripple** on 1389.255 N from `motor_results.json`, and
the sweep rate follows from the current 10.533 g, not the superseded 105 m/s² in E23's table.

## Acceptance bands

| # | Question | Band | What a miss means |
|---|---|---|---|
| 1 | Peak dynamic amplification at the 109 Hz fixed-fixed mode, at Q ≤ 200 | **< 2× static** | resonant buildup is real and the track needs a dynamic design case, not just a launch one |
| 2 | Same at the 48 Hz pinned-pinned mode, Q ≤ 200 | **< 2× static** | as above, and worse — 48 Hz is the softer bracket |
| 3 | Q at which amplification first reaches 2× | **report** | this is the number the structure has to be shown to beat, and it is the deliverable even if bands 1 and 2 pass |
| 4 | Peak displacement at the worst case against the ±0.05 mm gap budget | **< 25 % of budget** | ripple-driven motion eating the airgap tolerance would couple structure to thrust |
| 5 | Amplification at the fundamental crossing of 109 Hz (5.23 m/s, 130 mm in) | **< 2× static** | the fundamental carries far more force than the 6th harmonic |

**Band 3 is the point of the analysis.** Bands 1, 2 and 5 are expected to pass. If they do, the
value delivered is not "it is fine" — it is **the Q above which it stops being fine**, which turns
an unquantified worry into a requirement the structure can be tested against in T-2's signature
sweep.

## If a band fails

E23 becomes a design driver rather than a check: the track needs a damping specification, and
`sizing.py`'s static 70 Hz target is insufficient on its own. That would also make T-2's sine
sweep a pass/fail qualification item rather than a signature comparison.
