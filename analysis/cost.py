"""
EMOCD | Recurring hardware cost, parametric.

WHY THIS EXISTS: the paper asserts that "unit cost is comparable to a small-satellite
reaction-wheel assembly and far below a propulsive stage" with nothing behind it. That is
exactly the kind of unsupported claim this repository flags everywhere else, and it had
never been checked. This script checks it.

>>> READ THIS BEFORE QUOTING ANY NUMBER FROM THIS FILE <<<

EVERY PRICE HERE IS AN ASSUMPTION. No vendor quote exists for any line item, and none was
obtainable -- the working environment has no route to a distributor. These are order-of-
magnitude figures for space-grade or near-space-grade parts in single-unit quantity, and a
real quotation could move any of them by a factor of two or more. NdFeB and titanium in
particular are commodity-priced and volatile.

What this script is FOR: the *structure* of the cost -- which line items dominate, and how
hard the total moves when a price assumption is wrong. That conclusion is robust to the
price errors in a way the absolute total is not. The sensitivity table at the bottom is the
actual deliverable.

Masses are IMPORTED from mass_properties.py, never re-entered. That module is authoritative
for mass; duplicating its numbers here is how the operating point forked once already
(see sizing.py's _check_operating_point).

Marked unverified under OPEN_PROBLEMS.md E16 (reference hygiene).

Reproduces:
    recurring hardware cost, single unit, order of magnitude only
    dominant line items and their share
    sensitivity of the total to each price assumption
"""
import json
import os

import mass_properties

# --- assumed unit prices ------------------------------------------------------
# UNVERIFIED. Single-unit, space-grade or near-space-grade, INR. No quotations.
# The `basis` string records what each figure is a guess AT, so a reader can judge it.
MATERIAL_INR_PER_KG = {
    'NdFeB':     {'price': 12000, 'basis': 'N45SH sintered blocks, machined, coated, small qty'},
    'Ti-6Al-4V': {'price':  4500, 'basis': 'plate stock, grade 5, before machining'},
    'Copper':    {'price':  1200, 'basis': 'oxygen-free bar and strip'},
    'Aluminium': {'price':   600, 'basis': '7075-T6 plate and box section'},
    'PEEK':      {'price':  9000, 'basis': 'unfilled rod and plate stock'},
    'Steel':     {'price':   900, 'basis': '440C and mild, mixed'},
}

# Machining multiplier: what the finished part costs relative to its raw material.
# Titanium is the expensive one to cut; aluminium is not.
MACHINING_FACTOR = {
    'NdFeB': 1.0,       # bought finished, price above already includes it
    'Ti-6Al-4V': 4.0,
    'Copper': 2.5,
    'Aluminium': 3.0,
    'PEEK': 3.0,
    'Steel': 2.0,
}

# Bought-in assemblies, priced per unit rather than per kg. UNVERIFIED.
BOUGHT_IN_INR = {
    'Supercapacitor cells (32 series, 190 F)': {'price': 240000, 'basis': '32 cells, space-screened, plus balancing'},
    'SiC bridge + gate drive':                 {'price': 180000, 'basis': '1200 V modules, drivers, busbar, filters'},
    'Avionics, sequencer, IMU':                {'price': 320000, 'basis': 'rad-tolerant SBC class, single unit'},
    'Position sensing (encoder + photogates)': {'price':  90000, 'basis': 'the dispersion claim depends on this chain'},
    'Hybrid ceramic bearings and rails':       {'price':  70000, 'basis': '440C/Si3N4, vacuum-rated'},
    'Harness, connectors, EMC':                {'price':  60000, 'basis': 'space-grade wiring and backshells'},
    'Thermal (radiator, MLI, pipes)':          {'price':  80000, 'basis': 'passive only'},
    'Fasteners, A-286 pins, misc':             {'price':  40000, 'basis': 'aerospace-grade hardware'},
}

# Which material each mass_properties part is made of, keyed by name prefix.
PART_MATERIAL = [
    ('Track longerons',        'Aluminium'),
    ('Stator copper',          'Copper'),
    ('Stator formers',         'PEEK'),
    ('Sled Halbach magnets',   'NdFeB'),
    ('Sled Ti chassis',        'Ti-6Al-4V'),
    ('Sled rollers',           'Steel'),
    ('Sled CAD reconciliation', 'Ti-6Al-4V'),
    ('Eddy brake magnets',     'NdFeB'),
    ('Brake Cu fin',           'Copper'),
    ('Cassette shells',        'Aluminium'),
    ('Followers, gates',       'Steel'),
    ('ESPA bracket',           'Aluminium'),
    ('Panels / closeouts',     'Aluminium'),
]

# Parts whose cost is carried by BOUGHT_IN_INR instead of by material mass, so that
# they are not counted twice.
BOUGHT_IN_PARTS = ('Supercapacitor', 'PPU', 'Battery + avionics', 'Harness', 'Thermal')


def material_for(part_name):
    for prefix, mat in PART_MATERIAL:
        if part_name.startswith(prefix):
            return mat
    return None


def fabricated_cost():
    """Cost of parts made from stock, driven by mass_properties' own part list."""
    mass_properties.build()                     # populates mass_properties.parts
    rows, total = [], 0.0
    for name, kg, _cg in mass_properties.parts:
        if any(name.startswith(p) for p in BOUGHT_IN_PARTS):
            continue
        mat = material_for(name)
        if mat is None:
            continue
        raw = kg * MATERIAL_INR_PER_KG[mat]['price']
        cost = raw * MACHINING_FACTOR[mat]
        rows.append(dict(part=name, material=mat, kg=round(kg, 3),
                         raw_INR=round(raw), finished_INR=round(cost)))
        total += cost
    return rows, total


def sensitivity(base_total, fab_rows):
    """How far does the total move if one price assumption is wrong by 2x?

    This is the part of the analysis that survives the price uncertainty: a line item
    whose doubling moves the total by 1 % does not need a quotation, and one that moves
    it by 20 % does.
    """
    out = []
    by_mat = {}
    for r in fab_rows:
        by_mat[r['material']] = by_mat.get(r['material'], 0) + r['finished_INR']
    for mat, amount in by_mat.items():
        out.append(dict(item=f"{mat} (material + machining)", share_pct=round(100 * amount / base_total, 1),
                        total_if_2x_pct=round(100 * (base_total + amount) / base_total - 100, 1)))
    for name, d in BOUGHT_IN_INR.items():
        out.append(dict(item=name, share_pct=round(100 * d['price'] / base_total, 1),
                        total_if_2x_pct=round(100 * (base_total + d['price']) / base_total - 100, 1)))
    return sorted(out, key=lambda r: -r['share_pct'])


def main():
    fab_rows, fab_total = fabricated_cost()
    bought_total = sum(d['price'] for d in BOUGHT_IN_INR.values())
    total = fab_total + bought_total

    print("EMOCD recurring hardware cost -- ALL PRICES ASSUMED, NO QUOTATIONS\n")
    print(f"{'part':42s} {'material':12s} {'kg':>7s} {'INR':>12s}")
    for r in sorted(fab_rows, key=lambda x: -x['finished_INR']):
        print(f"{r['part']:42s} {r['material']:12s} {r['kg']:7.2f} {r['finished_INR']:12,.0f}")
    print(f"{'FABRICATED SUBTOTAL':42s} {'':12s} {'':7s} {fab_total:12,.0f}\n")

    for name, d in sorted(BOUGHT_IN_INR.items(), key=lambda x: -x[1]['price']):
        print(f"{name:42s} {'bought-in':12s} {'':7s} {d['price']:12,.0f}")
    print(f"{'BOUGHT-IN SUBTOTAL':42s} {'':12s} {'':7s} {bought_total:12,.0f}\n")
    print(f"{'RECURRING TOTAL, ONE UNIT':42s} {'':12s} {'':7s} {total:12,.0f}")
    print(f"{'  per 3U satellite (12 per unit)':42s} {'':12s} {'':7s} {total/12:12,.0f}\n")

    sens = sensitivity(total, fab_rows)
    print("Sensitivity -- what a 2x price error does to the total:\n")
    print(f"{'line item':44s} {'share':>7s} {'total moves':>12s}")
    for r in sens:
        print(f"{r['item']:44s} {r['share_pct']:6.1f}% {r['total_if_2x_pct']:11.1f}%")

    res = dict(
        WARNING="ALL PRICES ARE ASSUMPTIONS. No vendor quotation exists for any line item. "
                "Use the structure and the sensitivity, not the absolute total. See E16.",
        currency="INR", quantity="single unit, recurring hardware only",
        excludes=["non-recurring engineering", "qualification test campaign",
                  "launch", "ground support equipment", "labour"],
        fabricated=fab_rows,
        fabricated_subtotal_INR=round(fab_total),
        bought_in={k: v['price'] for k, v in BOUGHT_IN_INR.items()},
        bought_in_subtotal_INR=bought_total,
        total_INR=round(total),
        per_satellite_INR=round(total / 12),
        sensitivity=sens,
        price_basis={**{k: v['basis'] for k, v in MATERIAL_INR_PER_KG.items()},
                     **{k: v['basis'] for k, v in BOUGHT_IN_INR.items()}},
        machining_factors=MACHINING_FACTOR,
    )
    os.makedirs('results', exist_ok=True)
    json.dump(res, open('results/cost.json', 'w'), indent=2)
    print("\n-> results/cost.json")


if __name__ == '__main__':
    main()
