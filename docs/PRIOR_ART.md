# Prior art

> **All five works below have been read.** Metadata verified against the publisher record; all
> numbers quoted are the authors' own unless marked *derived here*, in which case the arithmetic is
> shown. This file was first written from abstracts alone on 2026-07-29 and **three of its
> conclusions were wrong**; the corrections are listed at the bottom rather than silently applied.

**What to do about all of it is in [`RESEARCH_POSITION.md`](RESEARCH_POSITION.md)**, organised
by adopt / cite / avoid / replicate / concede. This file is the evidence; that one is the
position.

This file exists because a literature check on 2026-07-29 found **published work on this exact
concept that the paper did not cite**. Two claims in `paper/paper.tex` did not survive it, and one
argument in `ADR-003` turned out to be false. All are corrected rather than defended. Logged as
**P22**.

Two independent groups are working in this space:

| Group | Works | Approach |
|---|---|---|
| **NUDT**, Changsha, Feng, Yang, Wu | 1 paper, 2025 | Induction coilgun, high velocity, reachable domain |
| **Harbin Institute of Technology**, Mechatronics, Yue, Zhao, F. Yang, X. Yang *et al.* | 3 papers, 2022-2025 | Magazine storage and electromagnetic transport, **with hardware** |

---

## 1. The nearest neighbour: and it is not as near as the abstract suggested

### Feng, Yang & Wu (2025): *Design and Reachable Domain Analysis of On-orbit Electromagnetic Launcher for CubeSats*

*Int. J. Aerospace Engineering* **2025**, art. 3000765, 17 pp · DOI
[10.1155/ijae/3000765](https://doi.org/10.1155/ijae/3000765) · NUDT, Changsha · received 3 Jun 2025,
accepted 22 Sep 2025

**Their design, from Table 2 and the conclusion:** a three-stage induction coilgun, stages of
1300 mm each, **3.9 m total**: driving a 20 kg payload (armature *plus* CubeSat). Stator coils
copper, **armature coils aluminium**. Charging 10 to 16 kV gives exit velocity 230 to 321.56 m/s
roughly linearly, at efficiency falling **19.9 % to 14.9 %**, from stored energy **2.70 to 6.91 MJ**.
Peak electromagnetic force ~300 kN at 10 kV, **above 600 kN at 16 kV**. Then a 3-D reachable-domain
envelope via an enhanced alpha-shape algorithm: non-convex and simply connected for a fixed
manoeuvre point, ring-shaped for free manoeuvre points.

**Method: simulation throughout.** Coupled circuit, electromagnetic, mechanical model validated
against nonlinear FEM, plus two-body orbital simulation. **No hardware.** The phrase "experimental
results" appears twice and both times refers to simulation runs; "Experimental points" is a figure
series label. *This corrects the abstract-level reading, which had left open whether they had built
anything.* On maturity, this project and Feng's are peers: both are TRL 2-3 design studies.

**What it breaks in this paper.** §I asserted *"no published deployment system operates in the tens
of m/s."* False, Feng operates at hundreds, published eight months before this repository went
public. The claim now restricts to **flown hardware**, which is what the comparison table always
actually showed. Their own Table 1 surveys the same spring deployers at 1-2 m/s and identifies the
same gap, so the gap is real; it was the word *published* that was wrong.

**What survives, and is much stronger than the abstract suggested.** *Derived here* from their
published figures:

| | Feng et al. | This design | Ratio |
|---|---|---|---|
| Mean acceleration | 321.56 m/s over 3.9 m to **1352 g** | 91 m/s² to **9.3 g** | **145x** |
| Peak | >600 kN on 20 kg to **~3060 g** | 10.7 g | ~286x |
| Energy per shot | **6.91 MJ** | 2.88 kJ | **2400x** |
| Payload interface | Aluminium **armature coils** on the payload | Magnets on a reusable sled | |

A standard CubeSat qualifies to roughly 14 g quasi-static. Feng's design imposes ~100x that. This is
not a flaw in their work, a 20 kg purpose-built body tolerating 10³ g is a coherent design for
debris removal and rapid response, which is what they target. But it is not a *rideshare secondary
CubeSat*, and the 6.91 MJ per shot is why their paper has to size a solar array for recharge while
this one draws under a watt-hour.

**Where they are genuinely ahead.** The **reachable-domain formulation** is a better astrodynamic
product than a lifetime multiplier: it answers "which orbits does one shot make available" directly,
in three dimensions, rather than reporting a scalar ratio. This project should adopt it. Candidate
Phase II item, and the strongest single thing to take from this literature.

**On "precise velocity control".** Their mechanism is **charging-voltage selection** (10 to 16 kV,
approximately linear in exit velocity), with armature position/velocity feedback used for *stage
trigger timing*. That is real velocity selection. **They quote no dispersion figure**, so this
design's 0.027 m/s 3σ has nothing to compare against, the differentiator survives, but as a claim
about absent evidence rather than about impossibility.

---

## 2. The Harbin programme: magazine-fed electromagnetic deployment, with hardware

One group, three papers, 2022 to 2025. Architecturally the closest thing to this project's cassette
magazine, and the only work here with measurements.

### Zhao, Yue, Mu, Yang & Yang (2022): *Design and Analysis of a New Deployer for the In-Orbit Release of Multiple Stacked CubeSats*
*Remote Sensing* **14**(17) 4205 · DOI [10.3390/rs14174205](https://doi.org/10.3390/rs14174205)

A large-capacity deployer that replaces compression springs with **electromagnetic actuators** for
transport and release of stacked CubeSats. The origin of the line.

### Xu, Yue, Zhao, Yang, Wu, Pan, Tang & Zhang (2024): *Improved A\* Algorithm for Path Planning Based on CubeSats In-Orbit Electromagnetic Transfer System*
*Aerospace* **11**(5) 394 · DOI [10.3390/aerospace11050394](https://doi.org/10.3390/aerospace11050394)

CubeSats are pushed layer by layer from a 3-D stack onto a 2-D conveying platform, then moved to a
release window by a planar two-axis drive. An improved A\* planner coordinates many simultaneous
transfers, with a cost term for **attitude disturbance caused by the transfers themselves**, a
shifting centre of mass degrades platform pointing and therefore release accuracy.

> **This is a gap in the present work, and it was found by reading their problem statement rather
> than by examining this design.** This project budgets recoil from the *shot* (65.6 N·s) and has
> nothing on disturbance from **magazine indexing between shots**. Opened as **E24**.

### Zhao, Zhang, Zhao, Li, Zhang, Yang, Yue *et al.* (2025): *Simulation Analysis and Experimental Verification of the Transport Characteristics of a High-Volume CubeSat Storage Device*
*Aerospace* **12**(6) 466 · DOI [10.3390/aerospace12060466](https://doi.org/10.3390/aerospace12060466)
· HIT with Harbin Space Star Data System Technology

**A prototype was built and measured.** The quantity reported is pushing speed, **32.8 mm/s** during
the transport stroke, with collisions observed in both simulation and experiment and model
limitations stated for extreme conditions.

> **Precise about the maturity gap, because the abstract-level reading overstated it.** What they
> measured is a **slow transport mechanism**, not an ejection. It is not a validated electromagnetic
> launcher. But they built hardware and this project has built none, E4 has been open throughout,
> and their willingness to report observed collisions is the standard
> [`BENCHTOP_TESTS.md`](BENCHTOP_TESTS.md) is written to.

---

## 3. The experimental benchmark, and why it cannot settle what it was expected to

### Einat & Orbach (2023): *A multi-stage 130 m/s reluctance linear electromagnetic launcher*
*Scientific Reports* **13** · DOI
[10.1038/s41598-022-27022-z](https://doi.org/10.1038/s41598-022-27022-z) · Ariel University

Measured, not simulated: a multi-stage reluctance launcher reaching **130 m/s**, the highest reported
for a reluctance coilgun, with a modular method for cascading further stages and a stated route to
lunar launch. The paper's own survey of the field is the most useful thing in it, Manzoor 36 m/s at
6 J, Deng 340 g at 30 J, Song 21.68 kg to 143 m/s, typical projectiles 2-11 g.

**The projectile here is 2.5 g**: about 21 J of kinetic energy. Five orders of magnitude below a 4 kg
CubeSat.

> **This was ranked #2 on the must-read list to settle ADR-003's claim that coilgun efficiency is
> "1-2 % in the literature". It cannot, and the claim was wrong anyway.** At 2.5 g nothing here
> transfers to CubeSat scale, and Feng reports 14.9-19.9 % at 20 kg. ADR-003's efficiency argument
> has been **withdrawn entirely**: it was unsourced, it was false, and it was never the reason the
> coilgun was rejected. The armature and the g-limit were.

---

## What reading them changed

| Written from the abstract | After reading |
|---|---|
| "Feng et al. design and analysis, no experiment *reported in the abstract*" | Confirmed: **simulation only.** This project and Feng's are maturity peers, not behind |
| "321.56 m/s at 10.7 g requires a 493 m track", a hypothetical | Replaced by fact: their **actual** 3.9 m barrel gives **1352 g** mean, ~3060 g peak. The real number is far more decisive than the hypothetical |
| ADR-003's "1-2 % efficiency", unsourced, removed *pending Einat* | **False.** Feng reports 14.9-19.9 %. Einat cannot settle it (2.5 g). Argument withdrawn, not deferred |
| *Aerospace* 12(6) 466 "has experimental verification", framed as a maturity gap | True but narrower: a **32.8 mm/s transport mechanism**, not an ejection. Gap is real, smaller than implied |
| Two bibliography entries with unverified authors | Both author lists now verified from the PDFs; `paper.tex` bibliography complete |

## What this changed in the repository

| Item | Change |
|---|---|
| `paper/paper.tex` §I | "no published deployment system operates in the tens of m/s" to restricted to flown hardware; Feng and the Harbin line cited; the g-limit argument made quantitative against their 3.9 m barrel |
| `paper/paper.tex` abstract | Contribution re-scoped to *programmable, qualification-compatible ejection of unmodified satellites* |
| `docs/adr/003` | Efficiency argument **withdrawn as false**; "cannot command velocity closed-loop" to a claim about absent dispersion evidence. Decision unchanged, now with numbers |
| `OPEN_PROBLEMS.md` | **P22** opened; **E24** opened (magazine-indexing disturbance, from Xu et al.) |
| `docs/RELATED_WORK.md` | "Direct competitors" section added; it had none |
| `docs/BENCHTOP_TESTS.md` | B-1 and B-2 bands **derived** from an error budget rather than chosen, by `validation/bench/bench_predict.py`; two procedural traps documented |
| Phase II candidate | **Adopt reachable-domain analysis** in place of, or alongside, the lifetime multiplier |
