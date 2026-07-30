# Cross-industry review

Dossier §8 asks for continuous study of industrial automation, robotics, CNC, semiconductor
manufacturing, linear motors, particle accelerators, maglev, precision positioning, vacuum
engineering and EV power electronics. The TRB prompt asks to *"borrow proven solutions from any
engineering discipline"* and to *"prefer evidence over novelty."*

This document applies that to the open E-items. **Several of them are treated in this
repository as open research when they are routine elsewhere.** The purpose here is to retire
what can be retired **by citation rather than by analysis**: and, equally, to say clearly
where the industrial analogue does *not* apply.

> ## The regime caveat, which governs everything below
>
> Ironless linear motors are a commodity product and vacuum-rated versions run semiconductor
> wafer stages. But the duty cycles are not comparable:
>
> | | Wafer stage | VOLLEY |
> |---|---|---|
> | Velocity | sub-m/s to a few m/s | **16.5 m/s** |
> | Duty | continuous, millions of cycles | **157 ms, twelve times per campaign** |
> | Thermal | steady-state limited | **adiabatic, pulse-limited** |
>
> A citation that a problem is solved at 0.5 m/s continuous is **not** evidence it is solved
> at 16.5 m/s pulsed. Where that gap matters it is stated and the item stays open.

---

## E19: Eddy-current heating inside the magnet blocks

**Verdict: real, well-characterised elsewhere, and the standard mitigation costs thrust.
Item stays open, but it is no longer unexplored.**

This is a named, extensively studied loss mechanism in permanent-magnet machines. Harmonic
content in the field, from the winding's own spatial harmonics and from PWM switching,
induces eddy currents in the conductive NdFeB bulk. The consequence is exactly the one E19
anticipated: local heating that risks **irreversible** demagnetisation, not the recoverable
remanence drift `sizing.py` models.

**The industry-standard mitigation is magnet segmentation**, dividing each block into
electrically insulated segments. Complete segmentation is effective and **reduces thrust and
mechanical robustness**, which is why partial segmentation is studied as the compromise
([Zhang et al. *IET Power Electronics* 2021](https://ietresearch.onlinelibrary.wiley.com/doi/full/10.1049/pel2.12009);
[partial-segmentation study for PMLSMs, UTS OPUS](https://opus.lib.uts.edu.au/bitstream/10453/140691/3/Reduction%20of%20Magnet%20Eddy%20Current%20Loss%20in%20PMSM%20by%20Using%20Partial%20Magnet%20Segment%20Method.pdf)).

**What this changes for VOLLEY.** Segmentation is a design option that did not previously exist
in this project's vocabulary, and it interacts directly with two things already on the books:
it would reduce K<sub>t</sub>, which is already the weakest-supported number here; and it
weakens blocks that must survive a kN-class assembly operation (`MANUFACTURING.md` §2).

**Why it does not close.** The literature is overwhelmingly steady-state rotating machines.
VOLLEY's duty is a 157 ms pulse twelve times per campaign, thermally far gentler in the mean,
but the peak is what drives the knee point. **Nobody has computed it here**, and the citation
does not compute it for us.

## E21: Vacuum tribology of the rollers

**Verdict: substantially retired by citation. This is solved engineering with a handbook.**

E21 recorded that the repository contains nothing on lubrication, cold welding or galling for
four rollers carrying ~1.48 kN per pair, reused twelve times in vacuum. That gap is real, but
the underlying engineering is not open research.

The **ESA Space Tribology Handbook** (Roberts, ESTL/AEA Technology,
[ESA Bulletin 94](https://www.esa.int/esapub/bulletin/bullet94/ROB.pdf)) exists precisely for
this, covering lubricant and component selection, rolling-element and linear bearings, and
testing. Established facts it supplies: terrestrial lubricants evaporate in hard vacuum;
unlubricated metallic surfaces wear rapidly and can **cold weld**; the accepted solutions are
low-vapour-pressure oils and greases, or solid lubrication with **MoS₂** as the broadly
accepted choice. [ESTL](https://www.esrtechnology.com/index.php/sectors/26-centres/estl) runs
thermal-vacuum accelerated life testing for exactly this class of component.

**What this changes.** E21 moves from "unanalysed risk" to "specification task with a standard
reference." The action is to select a lubrication approach against the handbook and state it in
`cad/parameters.json`, not to conduct research. **Twelve cycles is a trivial life requirement**
by space-mechanism standards, the handbook's concern is thousands to millions.

**What still needs doing:** MoS₂ performs differently under high contact stress and its
transfer-film behaviour is load-dependent, so the 1.48 kN per pair figure must be checked
against bearing ratings rather than assumed acceptable. That is a selection calculation, not
an experiment.

## E11: Outgassing, and external support for ADR-004

**Verdict: the ironless choice is independently supported. Item stays open pending T-4.**

ADR-004 chose an ironless stator for cogging and mass reasons. It turns out to be the standard
choice for vacuum service for an additional reason this project had not recorded: **coreless
construction lowers outgassing**, and vacuum-compatible ironless linear motors are catalogue
products from multiple vendors
([Tecnotion](https://www.tecnotion.com/applications/semiconductors/),
[Dover Motion](https://dovermotion.com/applications/high-vacuum-positioning-systems/),
[Gorman Dynamics](https://www.gormandynamics.com/vacuum-motor-umv)).

That VOLLEY's architecture converges with fielded vacuum practice is worth stating in the paper.
It does not close E11, which is about **this** design's material set against ASTM E595, that
is T-4 in `QUALIFICATION_PLAN.md`.

## E23: Force ripple through the track's structural modes

**Verdict: partially addressed. The cogging half is retired; the sweep half is not.**

Ironless motors are consistently specified as **zero-cogging**: with no iron, there is no
detenting against the magnet pitch (Tecnotion, HansMotor, and every vendor in this class). So
the largest ripple source in an iron-core machine is absent by construction, which is a second
independent justification for ADR-004.

**But E23 is not about cogging.** It is about the *electrical* ripple, the ±1.26 % 6th
harmonic in `motor_model.py`, sweeping from zero through the track's 48 Hz and 109 Hz modes
during every shot, crossing both inside the first 4-50 ms. Industrial stages run at constant or
slowly varying velocity and do not chirp. **No citation found addresses this**, and the item
stays open as written.

## E22: Parasitic eddy drag on track structure

**Verdict: recognised in practice, not quantified here.**

The industrial answer is architectural rather than analytical: vendor ironless motors keep
conductive structure out of the magnet track's field, and the same applies here. This is a
design rule to adopt, not a number to compute, but adopting it requires the track-to-array
standoff, which `cad/parameters.json` does not pin down as a single value.

**Action:** specify a minimum standoff for conductive structure as a design rule, then check
the CAD against it. Cheaper than the analysis E22 currently implies.

## E20: Brake force-time profile

**Verdict: not addressed by this review.** Eddy-current braking has extensive literature and
this pass did not search it. Recorded as not done rather than padded with a plausible-sounding
citation. B-4 in `BENCHTOP_TESTS.md` remains the cheap route to a first measured point.

---

## Summary

| Item | Before | After |
|---|---|---|
| E19 magnet eddy heating | unexplored | **characterised**; segmentation is the standard mitigation and it costs thrust |
| E21 vacuum tribology | unanalysed | **substantially retired**: ESA handbook, MoS₂, 12 cycles is trivial |
| E11 outgassing | open | open, but **ADR-004 gains external support** |
| E23 ripple through modes | open | **cogging half retired**, sweep half genuinely novel |
| E22 parasitic eddy drag | open | **reframed** as a design rule, not an analysis |
| E20 brake profile | open | open, **not reviewed** |

**The honest conclusion, which cuts both ways.** Two items were being treated as research when
they are standard practice with references, that is exactly the waste §8 exists to prevent.
But the review also confirmed that **E23's sweep behaviour appears genuinely unusual**, because
industrial linear motors do not accelerate a mass through their entire velocity range in
157 ms. Where this project is ordinary, it should borrow. Where it is not, it should stop
assuming someone else has already solved the problem.

*Every claim above is cited to a retrieved source. Vendor pages are marketing material and are
cited only for what a product category routinely does, never for a performance number. Nothing
here is treated as verified under E16 beyond what the linked sources state.*
