# Project history

> ## This git history was reconstructed on 2026-07-29
>
> The project began on **22 March 2021**. It was not under version control until
> **23 July 2026**, when the working files were exported into this repository. The commits
> before that export date were created during the reconstruction and **their author dates are
> design-period markers, not original commit times** — there were no original commits to
> preserve.
>
> Git records this itself: every reconstructed commit carries an **author date** at its design
> period and a **committer date of 2026-07-29**. `git log --format='%ad | %cd'` shows both.
>
> **Four of the six milestones below are approximate.** Where the record fixes a date, it is
> marked *documented*. Where it only gives a range — `cad/CHANGELOG_CAD.md` says of Gen1,
> "Date range: 2021–2025 (exact build history not reconstructed)" — the date is an inference
> and is marked *approximate*. None of these approximations should be cited as fact.

---

## Milestones

| Tag | Author date | Precision | What it marks |
|---|---|---|---|
| `v0.0-concept` | 2021-03-22 | **documented** | Concept, built around a coilgun. Presented at ARDE / INSARM 2021 |
| `v0.1-lsm` | 2025-07-01 | *approximate* — "mid-2025" | Coilgun → linear synchronous motor. The pivotal decision |
| `v0.2-gen1` | 2025-09-15 | *approximate* — see note | Gen1 CAD, 11 STEP files. The geometric ancestor of the parameter set |
| `v0.3-gen2` | 2026-02-15 | *approximate* — range 2025–2026-07 | Gen2 CAD, first structured revision |
| `v0.4-gen3` | 2026-07-23 | **documented** | Gen3 CAD build session; repository export |
| `v1.0` | 2026-07-29 | exact | Current published state |

### Note on Gen1's placement

`cad/CHANGELOG_CAD.md` gives Gen1 a range of 2021–2025 and states its build history was never
reconstructed. It is placed here **after** the mid-2025 motor decision rather than earlier in
that range, because of what the files contain: `EMOCD_Stator_Gen1.step` and a Halbach-array
sled are linear-motor geometry. A coilgun design has no stator. The placement is therefore
**inferred from the artifacts, not read from a record** — if the true date is earlier, this
file is wrong and the CAD changelog's range is the authority.

---

## The narrative

**2021 — origin.** Watching a Rocket Lab Photon deploy CubeSats raised the question the
project has pursued since: rideshare secondaries inherit the primary customer's orbit, and a
1–2 m/s spring cannot change that. The first architecture was a coilgun.

**2023 — host reframed.** From a dedicated free-flyer to a spent upper stage. This is what
made the concept a payload rather than a mission, and it is why the interface is now specified
generically against any restartable stage.

**mid-2025 — the pivotal change.** Coilgun → linear synchronous motor. A coilgun cannot
deliver a programmable exit velocity at the dispersion this application needs; a synchronous
machine commands current against measured position. Everything downstream — the Halbach array,
the reusable sled, the eddy brake, the supercapacitor bank — follows from this one decision.
Recorded in `docs/DECISION_LOG.md`.

**2025–2026 — three CAD generations.** Gen1 established the geometry. Gen2 was the first
structured revision. Gen3 rebuilt the parameter set from the actual geometry and is current.
Each generation's defects are audited in `cad/CHANGELOG_CAD.md`, including the twelve carried
by Gen3.

**2026-07 — published, and the numbers moved.** The repository was made public, the paper's
analysis was rebuilt from scratch and four errors found, an independent propagator falsified a
claim in the paper's own abstract, and the sled mass measured from CAD moved the headline exit
velocity from 20.37 to 16.54 m/s. All of it is in `CHANGELOG.md` and `OPEN_PROBLEMS.md`.

---

## Publishing the tags and releases

The reconstructed commits are on GitHub. **The six milestone tags are not** — the environment
this was built in has a git proxy that permits pushes to `refs/heads/*` and returns 403 for
`refs/tags/*`, and its network policy intercepts the GitHub REST API. Neither is a property of
the repository; both are properties of that sandbox.

The same applies to the three companion repositories: they exist as of 2026-07-29 but are
still empty, because that sandbox serves only the flagship. `tools/bootstrap_repos.sh` fills
them.

Everything needed is committed. From any machine with ordinary GitHub access:

```bash
gh auth login          # once
./tools/publish_releases.sh
```

That pushes the six tags, re-points `v0.1.0` (whose existing GitHub release references a
commit the reconstruction removed), and creates a Release for each tag with notes taken from
the annotated tag message, so the tag and the release cannot drift apart.

**One thing that cannot be backdated:** GitHub stamps its own creation date on a Release and
the API offers no way to set it. The *tag* dates carry the design periods; the Release
creation dates will all read whenever the script is run. Do not let the Release dates be read
as the work dates — that is what this file is for.

## Why the reconstruction is labelled

This repository's argument for being trusted is that its record can be audited — bands
declared before runs, defects published rather than quietly fixed, scripts authoritative over
the paper. A git history that silently implied five years of continuous commits would
contradict that on its own front page. The dates are real design periods; the commits are new;
both facts are stated here and visible in git's own metadata.
