# Project history

> ## This git history was reconstructed on 2026-07-29
>
> The project began on **22 March 2021**. It was not under version control until
> **23 July 2026**, when the working files were exported into this repository. The commits
> before that export date were created during the reconstruction and **their author dates are
> design-period markers, not original commit times**, there were no original commits to
> preserve.
>
> Git records this itself: every reconstructed commit carries an **author date** at its design
> period and a **committer date of 2026-07-29**. `git log --format='%ad | %cd'` shows both.
>
> **Four of the six milestones below are approximate.** Where the record fixes a date, it is
> marked *documented*. Where it only gives a range, `cad/CHANGELOG_CAD.md` says of Gen1,
> "Date range: 2021-2025 (exact build history not reconstructed)", the date is an inference
> and is marked *approximate*. None of these approximations should be cited as fact.

---

## Milestones

| Tag | Author date | Precision | What it marks |
|---|---|---|---|
| `v0.0-concept` | 2021-03-22 | **documented** | Concept, built around a coilgun. Presented at ARDE / INSARM 2021 |
| `v0.1-lsm` | 2025-07-01 | *approximate*, "mid-2025" | Coilgun to linear synchronous motor. The pivotal decision |
| `v0.2-gen1` | 2025-09-15 | *approximate*, see note | Gen1 CAD, 11 STEP files. The geometric ancestor of the parameter set |
| `v0.3-gen2` | 2026-02-15 | *approximate*, range 2025-2026-07 | Gen2 CAD, first structured revision |
| `v0.4-gen3` | 2026-07-23 | **documented** | Gen3 CAD build session; repository export |
| `v1.0` | 2026-07-29 | exact | Current published state |

### Note on Gen1's placement

`cad/CHANGELOG_CAD.md` gives Gen1 a range of 2021-2025 and states its build history was never
reconstructed. It is placed here **after** the mid-2025 motor decision rather than earlier in
that range, because of what the files contain: `EMOCD_Stator_Gen1.step` and a Halbach-array
sled are linear-motor geometry. A coilgun design has no stator. The placement is therefore
**inferred from the artifacts, not read from a record**, if the true date is earlier, this
file is wrong and the CAD changelog's range is the authority.

---

## The narrative

**2021, origin.** Watching a Rocket Lab Photon deploy CubeSats raised the question the
project has pursued since: rideshare secondaries inherit the primary customer's orbit, and a
1-2 m/s spring cannot change that. The first architecture was a coilgun.

**2023, host reframed.** From a dedicated free-flyer to a spent upper stage. This is what
made the concept a payload rather than a mission, and it is why the interface is now specified
generically against any restartable stage.

**mid-2025, the pivotal change.** Coilgun to linear synchronous motor. A coilgun cannot
deliver a programmable exit velocity at the dispersion this application needs; a synchronous
machine commands current against measured position. Everything downstream, the Halbach array,
the reusable sled, the eddy brake, the supercapacitor bank, follows from this one decision.
Recorded in `docs/DECISION_LOG.md`, and the reason I actually dropped the coilgun is below.

**2025-2026, three CAD generations.** Gen1 established the geometry. Gen2 was the first
structured revision. Gen3 rebuilt the parameter set from the actual geometry and is current.
Each generation's defects are audited in `cad/CHANGELOG_CAD.md`, including the twelve carried
by Gen3.

**2026-07, published, and the numbers moved.** The repository was made public, the paper's
analysis was rebuilt from scratch and four errors found, an independent propagator falsified a
claim in the paper's own abstract, and the sled mass measured from CAD moved the headline exit
velocity from 20.37 to 16.54 m/s. All of it is in `CHANGELOG.md` and `OPEN_PROBLEMS.md`.

---

## Why the coilgun was actually dropped

**Added 2026-08-05, from my 2021-2025 notebooks.** The reason on record until now has been
incomplete. `docs/DECISION_LOG.md` and ADR-003 both explain the change through velocity
accuracy: a coilgun fires and commits, a synchronous machine commands current against a
measured position. That is true, and it is not what stopped me. The notebook chain is shorter
and it is about the payload:

> Coilgun. This can produce the velocity, but the acceleration is enormous and the EMI
> environment is awful.
>
> That defeats the whole point of supporting unmodified CubeSats.

Both objections land on the same requirement. A satellite nobody is allowed to modify turns up
with the qualification envelope it already has, and it turns up with its own electronics,
harness and radio. A launcher that shakes it past its structural qual, or floods it with
switching transients, has quietly taken the modification back out of the customer's hands and
put it into mine. That is the one thing this concept is not allowed to do.

So the motor was not chosen because it was elegant. It was chosen because one architecture
answered several constraints at once:

- lower peak acceleration
- a smoother force profile
- controllability, because thrust is commanded rather than timed
- a reusable carriage, so the magnets stay with the machine
- programmable exit velocity
- less EMI than a pulsed coilgun
- and, out of all of the above, a CubeSat that flies unmodified

### Which half of that is calculated, and which half is not

**The acceleration half is a number now.** ADR-003 carries it: Feng et al.'s on-orbit coilgun
runs 1352 g mean over a 3.9 m barrel against this design's 10.5 g peak, about a hundred times a
standard CubeSat's quasi-static qualification. That comparison was made in 2026 from published
work, five years after the decision. In 2021 it was a judgement call, and it happened to be the
right one.

**The EMI half had never been calculated, here or in the notebooks.** I went looking for the
working behind "the EMI environment is awful" and there was none. It was an instinct about
megaampere-class pulsed discharges sitting next to unshielded commercial electronics, and an
instinct is not evidence. The far half of the question was not written down anywhere until a
systems engineer asked me directly what the EMI does to the payload and to the launch vehicle's
communications. He had not read this file or the coilgun history, and the question still had no
answer in the repository.

**Computed 2026-08-05 as A14, nine years late, and the instinct was right.** A coilgun stage
discharging 392 kA induces **355.6 mV** in a 10 cm² unshielded loop at 0.3 m against VOLLEY's
0.534 mV at the same geometry — a ratio of **666×**, against a band declared at 100×. The
electromagnetic half of the 2025 decision holds.

**Being right is not the same as being justified**, and the record should not blur them. The
number arrived nine years after the decision it supports, and until it did, an architecture had
been rejected on grounds nobody in this project could have defended if asked. That is the part
worth keeping.

A14 also found the thing I was not looking for. **The dominant electromagnetic term in VOLLEY is
not the drive at all — it is the permanent magnets.** The payload's nearest face sits 6 mm behind
a Halbach array in a 61 mT field, 611× the full scale of the magnetometer a CubeSat carries, while
the entire switching transient produces 36 mV. That is **P34**, and it is a constraint on which
satellites can fly in the magazine, which is a more awkward finding than the one I set out to
check.

---

## Publishing the tags and releases

The reconstructed commits and **all six milestone tags are now on GitHub** (pushed
2026-07-29). What is still missing is the **Releases**: the GitHub REST API is intercepted in
the environment this was built in, so no Release can be created from there. That is a property
of that sandbox, not of the repository.

Two things remain:

- **`v0.1.0` still points at `cb6e8855`**, a tag object referencing a commit the history
  reconstruction removed. It needs a force-update to `62b0b2c`. `restore_tags.sh` prepares the
  corrected tag; pushing it needs a force-push, which that sandbox declines to perform.
- **Six Releases**, one per milestone tag.

The three companion repositories are **live** as of 2026-07-29, `VOLLEY-paper` (84 files),
`VOLLEY-thesis` (148) and `VOLLEY-lab` (3), all generated from flagship `c927df9`.

Everything needed is committed. From any machine with ordinary GitHub access:

```bash
git clone https://github.com/aaaaaaaaaaaavm/VOLLEY.git   # full clone, not --depth
cd VOLLEY
gh auth login              # once
./tools/publish_releases.sh
```

`publish_releases.sh` re-points `v0.1.0` and creates a Release for each tag, with notes taken
from the annotated tag message so the tag and the release cannot drift apart. Tags already
pushed are reported as such and left alone.

### Why a fresh clone needs `restore_tags.sh` first

**A clone does not fetch these tags.** The six were pushed as refs, but `v0.1.0` on GitHub is
still the stale object, and a clone made before the push has none of them. Checked by cloning
and looking: a fresh clone arrives with exactly one tag, `v0.1.0`, pointing at the wrong
commit.

`tools/restore_tags.sh` rebuilds all seven **annotated** tags, original message, original
tagger date, original tagger identity, from data embedded in the script plus the commits
already in the clone. Every tagged commit is an ancestor of the default branch, so a full clone
has everything needed. It was verified by cloning fresh, running it, and comparing: **all seven
tag objects reproduce bit-for-bit**, identical SHAs. `publish_releases.sh` calls it
automatically when the tags are missing.

Two things it has to get right, both found by testing rather than assumption: the tagger
identity must be **pinned** rather than inherited, or a clone whose git config names someone
else silently restamps every milestone; and `v0.1.0` must be **force-rewritten rather than
skipped**, or the re-point step pushes the stale pointer and changes nothing.

**One thing that cannot be backdated:** GitHub stamps its own creation date on a Release and
the API offers no way to set it. The *tag* dates carry the design periods; the Release
creation dates will all read whenever the script is run. Do not let the Release dates be read
as the work dates, that is what this file is for.

## Why the reconstruction is labelled

This repository's argument for being trusted is that its record can be audited, bands
declared before runs, defects published rather than quietly fixed, scripts authoritative over
the paper. A git history that silently implied five years of continuous commits would
contradict that on its own front page. The dates are real design periods; the commits are new;
both facts are stated here and visible in git's own metadata.
