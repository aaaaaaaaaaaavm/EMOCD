# Smaller payloads, and what they actually change

VOLLEY is designed around a 3U CubeSat. This file asks what happens if it carries something else:
PocketQubes, TubeSats, 1U, or non-standard containerised smallsats.

**The answer is the opposite of the intuition, and it matters.** Smaller payloads do not make the
machine faster. They make it economically viable, which is the more urgent problem.

---

## The velocity question, settled first

A lighter payload should mean more acceleration for the same force. It does not, because **the
sled is most of the moving mass**:

| Payload | Payload mass | Moving mass with the 9.445 kg sled | Acceleration | Exit velocity |
|---|---|---|---|---|
| 3U CubeSat | 4.00 kg | 13.45 kg | 10.7 g | **16.5 m/s** |
| 1U | 1.33 kg | 10.78 kg | 13.4 g | 18.5 m/s |
| PocketQube 1P | 0.25 kg | 9.70 kg | 14.9 g | 19.5 m/s |
| TubeSat/chipsat | 0.05 kg | 9.50 kg | 15.2 g | 19.7 m/s |

Removing 99 % of the payload buys 19 % more velocity.

**And scaling the sled down does not help either**, because array length sets thrust and sled
mass together. A shorter array is a lighter sled *and* a weaker motor:

| Array length | K_t | Sled mass | Force | Acceleration, 3U | Exit velocity |
|---|---|---|---|---|---|
| 340 mm, as built | 11.22 | 9.45 kg | 1413 N | 10.7 g | 16.5 m/s |
| 240 mm | 7.92 | 7.18 kg | 998 N | 9.1 g | 15.2 m/s |
| 150 mm | 4.95 | 5.15 kg | 624 N | 7.0 g | 13.3 m/s |

Pairing a light sled with a light payload recovers most of it and no more: a 150 mm sled with a
PocketQube gives **11.8 g and 17.3 m/s**. Around a tonne of algebra to gain 0.8 m/s.

> **The velocity ceiling is a payload qualification property, not a mass property.** It stays at
> 25.3 m/s over the 1.30 m zone for every class here, and reaching it needs the same levers
> regardless of what is being launched. See [`VELOCITY_CEILING.md`](VELOCITY_CEILING.md).

**The sled mass scaling above is crude**: it assumes chassis mass scales with array length plus a
fixed overhead, which is the current chassis geometry rather than a redesign. A genuinely minimal
sled for a 0.25 kg payload has not been designed and would not look like a scaled copy of this
one.

---

## What smaller payloads actually change

The deployer's mass is fixed. The number of customers it carries is not, and
[`KILL_CRITERIA.md`](KILL_CRITERIA.md) threat 1 is the one that decides whether VOLLEY has a
reason to exist:

| Payload | Form factor | Typical mass | Fits the magazine | Deployer kg per satellite |
|---|---|---|---|---|
| 3U CubeSat | 340 × 100 × 100 mm | 4 kg | 12 | **6.41** |
| 1U | 100 × 100 × 100 mm | 1.33 kg | 36 | 2.14 |
| TubeSat | Ø88 × 127 mm | 0.75 kg | 40 | 1.92 |
| **PocketQube 1P** | 50 × 50 × 50 mm | 0.25 kg | ~546 | **0.14** |

Against a cold-gas module at 0.5 to 1.2 kg giving the same 16.5 m/s, the 3U configuration loses
by about 8x and the PocketQube configuration **wins by about 6x**. That is the entire commercial
argument, and it turns on payload class rather than on any machine parameter.

### Four things that must be read with those numbers

**1. The packing counts are volumetric bounds.** They divide cassette volume by payload volume
and ignore septa, follower plates, the escapement and the drive bay. Realistic packing is likely
40 to 60 %. At 40 %, PocketQube gives **0.35 kg per satellite**, which still clears the threshold
by 5x. No cassette layout for a small-payload variant exists.

**2. 546 shots is a different machine from 12.** The campaign thermal case (28.0 kJ over twelve
shots), the bank recharge duty, and the escapement cycle life were all sized for twelve. A
magazine of hundreds needs those re-derived, not scaled. The bank is already the binding problem
at twelve shots (P26).

**3. The feed mechanism is built around CubeSat corner rails.** The cradle, the escapement and
the retention gate all engage the CDS rail interface. PocketQubes and TubeSats have different
interfaces, so a smaller class needs its own cassette, cradle and gate. **That is real mechanical
design, not a parameter change.**

**4. Qualification loads for the small classes are not established here.** The 25 g cap comes
from the CubeSat Design Specification and GEVS. PocketQube and TubeSat standards are less mature
and their qualification environments have not been checked against any published document for
this file. **Until they are, assume the same limits**: smaller structures often survive more, but
"often" is not a number.

---

## What this implies for the programme

**A small-payload variant attacks the only threat that is currently crossed**, and it does so
without touching the velocity, the field model or the control loop, all of which are the
best-validated parts of the design.

It is also honest about what it does not do. It does not make the machine faster, it does not fix
the envelope (P9), and it does not fix the bank (P26). It changes who the machine is for.

**Not adopted, and not costed as a design.** This file establishes that the payload class is the
dominant term in the mass-per-satellite argument. Turning that into a variant means a cassette,
a cradle, a gate, and a re-derived thermal and power case for hundreds of shots. That is a
programme decision, and the numbers above exist so it can be made against evidence.

---

## Sources

- Form factors: PocketQube and CubeSat Design Specification published dimensions; TubeSat from
  the published kit specification
- Cassette volume: `cad/parameters.json`, `groups.magazine`
- Sled mass, thrust constant and exit velocity: `analysis/motor_model.py`
- Deployer dry mass: `analysis/mass_properties.py`, **which excludes enclosure, radiator and
  avionics** (P10), so every kg-per-satellite figure here is optimistic
- Cold-gas module masses: published COTS ranges, not a quotation
