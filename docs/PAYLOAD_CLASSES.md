# Smaller payloads, and what they actually change

VOLLEY is designed around a 3U CubeSat. This file asks what happens if it carries something else:
chipsats, PocketQubes, ThinSats, TubeSats, 1U, or the larger CubeSat classes.

**The answer is the opposite of the intuition, and it matters.** Smaller payloads do not make the
machine faster. They make it economically viable, which is the more urgent problem.

> **Generated.** The tables below are written by `analysis/payload_family.py` from
> `analysis/results/payload_family.json`. Do not hand-edit them; change the script and re-run it.
> They were typed by hand until 2026-07-31, and the packing counts were wrong.

---

## The velocity question, settled first

A lighter payload should mean more acceleration for the same force. It does not, because **the
sled is most of the moving mass**. And scaling the sled down does not help either, because array
length sets thrust and sled mass together: a shorter array is a lighter sled *and* a weaker motor.

<!-- PAYLOAD-TABLES-START -->

### Velocity, which barely moves

| Payload | Mass | Moving mass with the 9.445 kg sled | Acceleration | Exit velocity |
|---|---|---|---|---|
| ChipSat / femtosat | 0.005 kg | 9.45 kg | 15.2 g | 19.7 m/s |
| PocketQube 1P | 0.250 kg | 9.70 kg | 14.9 g | 19.5 m/s |
| ThinSat | 0.280 kg | 9.72 kg | 14.8 g | 19.4 m/s |
| PocketQube 3P | 0.750 kg | 10.20 kg | 14.1 g | 19.0 m/s |
| TubeSat | 0.750 kg | 10.20 kg | 14.1 g | 19.0 m/s |
| 1U CubeSat | 1.330 kg | 10.78 kg | 13.4 g | 18.5 m/s |
| 3U CubeSat | 4.000 kg | 13.45 kg | 10.7 g | 16.5 m/s |
| 6U CubeSat | 8.000 kg | 17.45 kg | 8.3 g | 14.5 m/s |
| 12U CubeSat | 12.000 kg | 21.45 kg | 6.7 g | 13.1 m/s |

### Deployer mass per customer, which moves by a factor of thirty

| Payload | Envelope, mm | Per load | Deployer kg per satellite | |
|---|---|---|---|---|
| ChipSat / femtosat | 35 x 35 x 2.5 | 13322 | **0.006** | **beyond the mechanism** |
| PocketQube 1P | 50 x 50 x 50 | 326 | **0.236** | **beyond the mechanism** |
| ThinSat | 114 x 114 x 25.4 | 123 | **0.625** |  |
| PocketQube 3P | 50 x 50 x 150 | 108 | **0.712** |  |
| TubeSat | 88 x 88 x 127 | 41 | **1.876** |  |
| 1U CubeSat | 100 x 100 x 100 | 40 | **1.923** |  |
| 3U CubeSat | 340 x 100 x 100 | 12 | **6.408** |  |
| 6U CubeSat | 340 x 200 x 100 | 6 | **12.817** |  |
| 12U CubeSat | 340 x 200 x 200 | 3 | **25.633** |  |

### Shortening the magnet array, which buys nothing

| Array length | K<sub>t</sub> | Sled mass | Force | Acceleration, 3U | Exit velocity |
|---|---|---|---|---|---|
| 340 mm | 11.22 | 9.45 kg | 1413 N | 10.7 g | 16.5 m/s |
| 240 mm | 7.92 | 7.18 kg | 998 N | 9.1 g | 15.2 m/s |
| 150 mm | 4.95 | 5.15 kg | 624 N | 7.0 g | 13.3 m/s |

<!-- PAYLOAD-TABLES-END -->

Removing 99.9 % of the payload buys **19 % more velocity**. Pairing a light sled with a light
payload recovers most of that and no more: a 150 mm sled with a PocketQube gives about 11.8 g and
17.3 m/s. A great deal of algebra for 0.8 m/s.

> **The velocity ceiling is a payload qualification property, not a mass property.** It stays at
> 25.3 m/s over the 1.30 m zone for every class here, and reaching it needs the same levers
> regardless of what is being launched. See [`VELOCITY_CEILING.md`](VELOCITY_CEILING.md).

**The sled mass scaling is crude**: it assumes chassis mass scales with array length plus a fixed
end-structure overhead, which describes the current chassis rather than a redesign. A genuinely
minimal sled for a 0.25 kg payload has not been designed and would not look like a scaled copy of
this one.

---

## What smaller payloads actually change

The deployer's mass is fixed. The number of customers it carries is not, and
[`KILL_CRITERIA.md`](KILL_CRITERIA.md) threat 1 is the one that decides whether VOLLEY has a
reason to exist. Against a cold-gas module at 0.5 to 1.2 kg giving the same 16.5 m/s, the **3U
configuration loses by about 8x** at 6.41 kg per satellite, and the **PocketQube configuration
wins by 2 to 5x** at 0.236 kg. That is the entire commercial argument, and it turns on payload
class rather than on any machine parameter.

### How the packing counts are computed, because they used to be wrong

A raw volume ratio says the magazine holds **21** 3U satellites. It holds **12**. The difference
is septa, follower plates, the escapement, the gate and the drive bay, none of which a volume
ratio knows about.

So the model is calibrated instead of asserted: packing efficiency is set so the **3U case
returns the twelve the machine is actually laid out for**, and the same 56.2 % is applied to every
other class. This file previously carried a raw volumetric bound with a note that "realistic
packing is likely 40 to 60 %", and then quoted the unadjusted numbers anyway. **PocketQube 1P was
published here as 546 per load and 0.14 kg per satellite; calibrated, it is 326 and 0.236 kg.**
The conclusion survives — it still beats the cold-gas comparator — but the margin is 2 to 5x
rather than 6x, and the old figure should not be quoted.

### Four things that must be read with those numbers

**1. They are still volumetric.** Calibration fixes the average, not the geometry. **No cassette
layout exists for any class except 3U.**

**2. Hundreds of satellites is a different machine from twelve.** The campaign thermal case
(24.4 kJ over twelve shots), the bank recharge duty, and the escapement cycle life were all sized
for twelve. A magazine of hundreds needs those re-derived, not scaled. The bank is already the
binding problem at twelve shots (P26). Classes exceeding 200 per load are flagged in the table for
exactly this reason, and the chipsat row is a volumetric statement rather than a proposal.

**3. The feed mechanism is built around CubeSat corner rails.** The cradle, the escapement and
the retention gate all engage the CDS rail interface. PocketQubes, ThinSats and TubeSats have
different interfaces, so a smaller class needs its own cassette, cradle and gate. **That is real
mechanical design, not a parameter change.**

**4. Qualification loads for the small classes are not established here.** The 25 g cap comes
from the CubeSat Design Specification and GEVS. PocketQube, ThinSat and TubeSat standards are less
mature and their qualification environments have not been checked against any published document
for this file. **Until they are, assume the same limits**: smaller structures often survive more,
but "often" is not a number.

---

## What this implies for the programme

**A small-payload variant attacks the only threat that is currently crossed**, and it does so
without touching the velocity, the field model or the control loop, all of which are the
best-validated parts of the design.

It is also honest about what it does not do. It does not make the machine faster, it does not fix
the envelope (P9), and it does not fix the bank (P26). It changes who the machine is for.

**Not adopted, and not costed as a design.** This file establishes that payload class is the
dominant term in the mass-per-satellite argument. Turning that into a variant means a cassette, a
cradle, a gate, and a re-derived thermal and power case for hundreds of shots. That is a
programme decision, and the numbers above exist so it can be made against evidence.

---

## Sources

- Form factors: PocketQube and CubeSat Design Specification published dimensions; TubeSat from
  the published kit specification; ThinSat from its published envelope; chipsat masses from the
  Sprite class
- Payload masses are **typical flight masses, not qualification maxima** — the CDS allows 2 kg
  for a 1U and 12 kg for a 6U, and using those would make the ladder look worse, not better
- Cassette geometry: `cad/parameters.json`, `groups.magazine`
- Sled mass, thrust constant and exit velocity: `analysis/motor_model.py`
- Deployer dry mass: `analysis/mass_properties.py`, **which excludes enclosure, radiator and
  avionics** (P10), so every kg-per-satellite figure here is optimistic
- Cold-gas module masses: published COTS ranges, not a quotation
