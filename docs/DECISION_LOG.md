# Decision log

Why each major change happened, not just what it changed to. Reconstructed from the
project record. This exists because "we switched to a linear motor" is useless
without the reason, and because two of these reversals came from finding my own
earlier answer wrong.

---

## 2021-04: Concept, with the architecture deliberately left open
Origin: watching a Rocket Lab Photon launch deploying CubeSats (22 March 2021). The
observation was that rideshare secondaries inherit the primary's orbit and the spring
that ejects them adds 1-2 m/s, which is enough for clearance and nothing else.

The original framing explicitly left the mechanism open: *"this would use an
electromagnetic rail such as what is used in maglev or we could use the coil gun tech
whichever seems to be more feasible and more efficient on mass and space."* First
concept was built around a coilgun and presented at ARDE / INSARM 2021.

## 2023: Host reframed: free-flyer to spent upper stage
Trigger: learning about ISRO's POEM, which keeps a spent PSLV fourth stage alive as a
stabilised platform.

Reasoning: a free-flying deployer has to carry its own attitude control, power and
recoil management. A spent stage already has all three, and its mass is large enough
to absorb ejection recoil that would tumble a small free-flyer. The stage becomes a
launch pad rather than debris.

Consequence: the attached variant (later VOLLEY-A) carries no CMGs and no thrusters.

## mid-2025: Coilgun to linear synchronous motor (the pivotal change)
This is the decision that reshaped everything downstream.

The reasoning runs through the payload, not the launcher. Exit velocity is bounded by
`v = sqrt(2 a L)`, and the payload's own qualification limit caps `a` at 25-30 g. Over
any stroke that fits a secondary-payload envelope, that ceiling is 26-35 m/s **whatever
the launcher is**. So the coilgun's single genuine advantage, a velocity ceiling in the
km/s range, is unreachable by the satellite it would be launching, while every one of
its costs remains:

- ~~1-2 % single-stage efficiency (Sandia-lineage literature)~~ **Struck 2026-07-30.**
  True of the single-stage reluctance machines cited, but not of coilguns generally:
  Feng et al. report 14.9-19.9 % for a multi-stage on-orbit CubeSat launcher, which is
  this design's own range. The argument was never load-bearing and is withdrawn rather
  than re-sourced. See ADR-003's amendment and `docs/PRIOR_ART.md`.
- microsecond pulse timing against the suck-back effect
- a ferromagnetic or conductive armature bolted to the *customer's* satellite
- no abort once fired

A linear synchronous motor concedes nothing inside the reachable envelope (maglev
traction exceeds 150 m/s) and inverts every cost: high drive efficiency, continuous
servo control instead of fire-and-commit timing, and (decisively) a **reusable sled**
that carries the magnets so the customer satellite carries nothing.

Verified outcome: 32 % electrical-to-payload efficiency against the coilgun's 1-2 %.

## 2025: Iron-core to ironless stator
An iron-core double-sided stator computed to roughly 65 kg of laminations plus 32 kg of
copper, which alone would have consumed the mass budget, and its permanent-magnet
attraction preloads the sled bearings with kilonewtons. Going ironless drops the stator
to a few kilograms of copper, removes cogging (better velocity servo, better tip-off),
and eliminates the bearing preload problem. Cost is higher current for the same force,
acceptable at a duty cycle of one ~130 ms pulse per shot.

Second-order benefit that mattered later: because the geometry is ironless, the field
problem is linear and analytic superposition is *exact*, which is what made the
independent magpylib cross-check meaningful.

## 2025: Regenerative arrest to eddy-current brake (correcting my own error)
I originally claimed regenerative braking would arrest the sled and credited 55 % energy
recovery. That was wrong: braking force is bounded by the same thrust constant as
acceleration, so motor-only braking needs 1.2-2.6 m of track, more than exists.

Replaced with a copper-fin eddy-current brake: force proportional to velocity,
contactless, no wear, flight heritage in the damper class. Authority turned out to be
abundant, so the design constraint inverted, the pole entry is now *tapered* to cap
sled deceleration near 200 g and protect the sintered magnet bonds, rather than sized
up for force.

Knock-on correction: the sled's kinetic energy is dissipated in the brake by design and
is **not** recovered. Crediting it as regeneration was double-counting; efficiency was
restated 40 % to 32 %.

> **Amended 2026-07-31 by A11. The paragraph above stays as written because it is what was
> decided and the arrest half of it is still right. The knock-on was drawn wider than the
> argument supported.**
>
> "Motor braking cannot *arrest* the sled" and "none of the sled's energy can be recovered"
> are different claims, and only the first was ever argued. Nobody asked the second question
> for five years, and the reason is legible: after a 55 % regeneration credit turned out to be
> a double-count, crediting zero was the safe response. Safe is not the same as correct.
>
> [`../validation/A11_regen_braking.md`](../validation/A11_regen_braking.md) asked it. Braking
> at the same sheet-current rating over 240 mm of added stator downstream of release returns
> **296.6 J, 23.0 % of the sled's 1291 J**, and lifts efficiency from 19.0 to **21.2 %**.
> Copper during the braking pulse is 15 J, because it is 15.6 ms over 240 mm of winding rather
> than 157 ms over 1300 mm.
>
> **The eddy brake stays.** It still absorbs 952 J of every shot. This supplements the decision
> above; it does not reverse it. Adopted into the Phase I baseline under
> [`programme/ADOPTION.md`](programme/ADOPTION.md) Amendment 3, and it opened P28: the regen
> stator and the fin do not both fit the arrest section as currently sized.

## 2025: Abort claim corrected
I originally described abort as available "anytime before release". Deceleration is
limited by the same motor force, so with the loaded carriage the true commit point is
~45 % of stroke at ~13.5 m/s. The safety argument was moved upstream to a three-inhibit
chain that must be green before the shot *starts*, making mid-stroke abort a
contingency rather than a load-bearing safety feature.

## 2025: Magazine: dual transverse cassettes
Chosen over a revolver drum (wastes corners of every cylinder-to-rectangle interface,
~60 % packing), a 2-DOF conveying platform (needs a stator cell under every storage
position, and random access is pointless when deployment order is fixed at integration),
and a tandem in-tube stack (disqualified outright, the sled must return through that
volume).

Bonus property: alternating left, right feed keeps lateral CoM asymmetry to one satellite
at most, cutting the thrust-line offset that drives recoil torque.

## 2025: Retention gate architecture
Directly motivated by the NanoRacks ball-lock anomaly, where ascent preload ran
*through* the release mechanism and jack-screw torque above 0.11 N·m drove it toward
seizure. VOLLEY routes stack preload through a one-shot retention gate straight into
structure; the escapement is caged during ascent and sees launch loads never. This makes
that failure mode geometrically impossible rather than merely unlikely.

## 2025: Coast-and-trim release zone
The last 0.2 m of track applies only small servo corrections, so release happens at
near-zero force. This is what makes the tip-off budget close: at full force the leading
term alone would approach 34 °/s against a 5 °/s requirement.

## 2026-07: Framing: host-specific to host-agnostic
The paper was briefly written around one launch provider. Reframed so the deployer is
specified against a generic four-item host interface (secondary-payload mount,
150-300 W, attitude reference with recoil authority, disposal path), with specific
vehicles appearing only as worked candidate examples. The engineering did not change;
the claim's scope did.

## 2026-07: Publish publicly
Concept and results released via LinkedIn and this repository. Detailed operating point
was deliberately withheld from the public post but **is** disclosed by publishing these
scripts. See `OPEN_PROBLEMS.md` E14, this is irreversible and was not preceded by a
provisional filing.

### 2026-08-03 correction to the regeneration addendum

The decision to recover energy before the eddy brake remains accepted. At the corrected
operating point the same model returns **291.4 J**, 23.0% of the sled's 1268.3 J, leaving
**934.7 J** to the brake and giving **20.99%** net electrical-to-payload efficiency.
