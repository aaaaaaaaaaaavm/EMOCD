# Where to submit, and what that choice implies

Not a decision. A record of what the prior-art review turned up about the venues, so the choice
is made against evidence rather than habit.

## The finding that matters

Both journals publishing work nearest to this one are publishing it **now**, and both are the
obvious places to send this paper:

| Venue | What it has published in this space |
|---|---|
| *International Journal of Aerospace Engineering* (Wiley) | Feng, Yang & Wu, on-orbit electromagnetic launcher for CubeSats, Nov 2025 |
| *Aerospace* (MDPI) | Xu et al. 2024 on in-orbit electromagnetic transfer; Zhao et al. 2025 on a measured CubeSat storage prototype |
| *Remote Sensing* (MDPI) | Zhao et al. 2022, the stacked-CubeSat deployer that starts the Harbin line |

That cuts two ways and both need stating.

**It locates the readership.** A paper on electromagnetic CubeSat deployment has a home, and these
are it. The reviewers will be people who work on this.

**It also locates the reviewers.** Those same people will know the prior art in
[`PRIOR_ART.md`](PRIOR_ART.md) without needing to look it up. An editor at *Aerospace* may well
send this to the Harbin group, and an editor at IJAE may send it to Feng's. The contribution claim
therefore has to survive a reader who has the comparison memorised, which is exactly the standard
the §I rewrite was aimed at.

## What has to be true before submitting anywhere

1. **The novelty claim must hold against Feng et al. as written.** It now reads as a programmable
   velocity delivered to an unmodified satellite inside its own qualification envelope, which is
   narrower than the original and defensible. P22 records the retraction that got it there.
2. **Two bibliography author lists were incomplete and are now verified.** Both were completed from
   the PDFs rather than guessed. Nothing else in the reference list rests on a search result.
3. **`docs/LITERATURE.md` must not be cited.** It is a reading list with provenance, not a review,
   and none of its 136 entries has been read. `RELATED_WORK.md` sets that rule and it applies here.
4. **A8's stale band should be re-run first.** P24 leaves a recorded pass sitting against a
   superseded operating point. A reviewer who checks the validation table will find it, and it is
   better found by the author.

## The honest weakness, stated before a reviewer states it

Every comparable paper in this space has either hardware or a longer measurement record. Zhao et
al. 2025 built a prototype and measured it. Einat and Orbach measured a launcher. This work has
measured nothing, and its two strongest results are cross-checks between models.

That is not fatal for a design study, and the paper says so plainly rather than burying it. But
**B-1 costs about the price of two magnets and a Hall probe**, and one measured number would change
what kind of paper this is. See [`BENCHTOP_TESTS.md`](BENCHTOP_TESTS.md).

## Not evaluated here

Open-access fees, review timelines, indexing, and whether a conference paper or a journal article
is the better first publication. Those are the author's call and depend on the thesis timetable
more than on anything in this repository.
