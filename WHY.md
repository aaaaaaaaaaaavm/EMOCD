# Why I'm doing this

*Adityavardhan Mishra — 2026-07-29. The reasoning behind the structure of this programme,
in my own words. Everything else in this repository is engineering; this is the part that
explains what the engineering is for.*

---

I'm not doing this because I believe I've already invented the perfect CubeSat deployer. I'm
doing it because I want to become the kind of engineer who can take an idea from first
principles to a rigorously validated aerospace system.

EMOCD is the vehicle I've chosen for that journey. It forces me to learn and apply orbital
mechanics, electromagnetics, mechanical design, manufacturing, systems engineering, controls,
testing, technical writing, and engineering decision-making within one coherent project. More
than the deployer itself, I'm interested in becoming capable of solving complex engineering
problems through disciplined, evidence-based reasoning.

I'm not emotionally attached to any specific architecture or mechanism. If evidence shows that
part of the design is wrong or that a fundamentally better approach exists, I want to
understand why and improve it. The engineering process matters more to me than proving my
original idea was correct.

At the same time, I've learned something important about how I work. I have a tendency to
continually question my own foundations, redesign systems from scratch, and spiral into endless
iterations in pursuit of something better. While that mindset is valuable during research, it
can also prevent me from ever finishing meaningful work.

To address that, I've intentionally separated the programme into two parts.

The **Engineering Programme** remains a living research effort where every assumption may be
questioned and every subsystem is open to revision as new evidence emerges.

The **Phase I deliverables**, however, are intentionally developed against a stable engineering
baseline. Their purpose is to produce tangible outcomes without becoming trapped in perpetual
redesign.

Those deliverables are:

1. A flagship engineering repository that demonstrates my engineering process and serves as my
   portfolio for aerospace companies.
2. An IEEE paper that communicates the work in a rigorous, reproducible form.
3. My final-year thesis, completed to the standards required by my university.
4. A continuing research programme where I remain free to question assumptions, explore new
   ideas, redesign architectures, and pursue future versions of EMOCD without disrupting the
   completed deliverables.

This separation is deliberate. It allows me to satisfy two goals that would otherwise compete
with each other: finishing high-quality engineering work today while preserving the freedom to
continue learning and evolving the programme tomorrow.

Ultimately, I'm doing this because I want to build a body of work that demonstrates how I think
as an engineer. If EMOCD eventually leads to a practical technology, that would be immensely
rewarding. But even if it doesn't, I want this programme to have made me a better engineer,
taught me how to approach difficult problems with discipline, and produced work that is
genuinely useful to others.

---

## What this means in practice

Each of the four deliverables above has a repository, and the structure is a control against
the failure mode named above rather than an organisational preference:

| | |
|---|---|
| [`PROGRAMME.md`](PROGRAMME.md) | The four repositories and how they relate |
| [`BASELINE.md`](BASELINE.md) | What is frozen for Phase I, and the rule for what may move it |
| [`docs/PHASE_II.md`](docs/PHASE_II.md) | Where redesign goes, and how it gets back |
| [`docs/programme/`](docs/programme/) | The governing dossier, adopted verbatim |

The honest test of all this is not whether the structure is elegant. It is whether the thesis
gets submitted and the paper gets published while the research track stays alive. If Phase I
ships and Phase II is empty, the freeze was too tight. If Phase II fills and Phase I slips,
the freeze failed.
