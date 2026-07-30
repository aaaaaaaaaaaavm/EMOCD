## Adityavardhan Mishra

**Mechanical engineer. Powertrain, ECUs, CubeSat deployment. Asking spacecraft inconvenient questions.**

BTech Mechanical Engineering, Symbiosis Institute of Technology, Pune · 2023-2027

In 2021 I got stuck on a dumb question: why do we still deploy CubeSats with springs. I never
really got unstuck. That question is now **VOLLEY**: an electromagnetic deployer that ejects
unmodified 3U CubeSats at a programmable velocity, eight times what a spring gives you, from a
spent rideshare upper stage. I've presented it at DRDO ARDE and the India Science Festival.

Before that there was rocketry, where our payload took **2nd globally** at the SDL Payload
Challenge, IREC 2025 in Texas. Alongside it there are engines, I run Poona Motor Club, tune Royal
Enfield, KTM and Honda platforms, and when Powertronic's map files turned out to be an obfuscated
binary I reverse-engineered the format and built a dual-map editor so I could stop guessing. This
year I'm on powertrain for our Formula Student team.

Aerospace, telecom software, engines. I have a hunch they all come from the same place. Haven't
proven it yet.

---

### The thing I'd actually like you to look at

**[VOLLEY](https://github.com/aaaaaaaaaaaavm/VOLLEY)**, a magazine-fed ironless double-sided
Halbach linear synchronous motor that ejects unmodified CubeSats at 16.5 m/s, 10.7 g, on 2.88 kJ
a shot. TRL 2-3, nothing built.

**Open it for the defect record, not the numbers.** Every error I've found in my own work is
published and numbered, including the ones that damage the claims. An independent propagator
falsified a claim in my paper's own abstract; that's logged as P16 rather than quietly dropped. My
cost model contradicted my own paper about which parts dominate. A literature check found prior art
I'd missed and retracted two claims. Acceptance bands are written down *before* each analysis runs,
so a failure can't be rationalised afterwards.

That habit is the actual portfolio: **[skills, with the file that proves each one](https://github.com/aaaaaaaaaaaavm/VOLLEY/blob/main/docs/SKILLS.md)**

| | |
|---|---|
| 🛰 **[VOLLEY](https://github.com/aaaaaaaaaaaavm/VOLLEY)** | The engineering record. Start at `SUMMARY.md` |
| 📄 **[VOLLEY-paper](https://github.com/aaaaaaaaaaaavm/VOLLEY-paper)** | IEEE manuscript + reproducibility package. Reproduces from a clean clone |
| 🎓 **[VOLLEY-thesis](https://github.com/aaaaaaaaaaaavm/VOLLEY-thesis)** | Final-year submission |
| 🧪 **[VOLLEY-lab](https://github.com/aaaaaaaaaaaavm/VOLLEY-lab)** | Where I'm allowed to break things. Nothing here is citable |

---

### What I actually do

**Simulation**: scikit-fem, gmsh, GetDP, CalculiX, ngspice, GMAT, magpylib. I wrote a 2-D
magnetostatic FEM from the weak form to check my own thrust constant; it agreed to 0.07 %, which
was the first time that number rested on a PDE solve instead of superposition.

**CAD/CAE**: Fusion 360, SolidWorks, AutoCAD, ANSYS. Three CAD generations of the deployer, all
in the repo as STEP.

**Engines**: combustion airflow, head porting, camshaft profiling, ECU calibration. 46 to ~60 bhp
on an RE Super Meteor 650, dyno-validated across the band.

**Code**: Python for the numerics, MATLAB, C. Applied AI at work: I own AI systems architecture
and product design for a telecom CRM platform, which is not what I was hired to do.

<sub>Hindi and English native · Marathi, Maithili · Russian, French elementary. Friends call me AVM,
pronounced how it's spelled, *Aevium*. Recognised by the ISRO Chairman for aerospace STEM
outreach; member, Space Generation Advisory Council.</sub>

📫 [adityavardhanmishr@gmail.com](mailto:adityavardhanmishr@gmail.com) ·
[LinkedIn](https://www.linkedin.com/in/adityavardhanmishra/) · Pune, India
