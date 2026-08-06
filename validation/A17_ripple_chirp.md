# A17: does the force-ripple chirp excite the track's structural modes?

**Closes:** `OPEN_PROBLEMS.md` **E23**.

> ## BANDS DECLARED 2026-08-05. NOT YET RUN.
>
> Committed before `analysis/chirp_response.py` existed.

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
