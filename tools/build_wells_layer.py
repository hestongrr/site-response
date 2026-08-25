#!/usr/bin/env python3
"""
Prepare NDWR well logs for the 3D valley model.

Wells are rendered as what they are -- individual boreholes at real locations --
NOT interpolated into a smooth water-table surface. The records span 1935-2026
and the well population changes character over that time (median static water
level is 68 ft in pre-1995 records and 18 ft in 2010+ records), so a single
continuous groundwater surface fitted through all of them would depict something
that never existed at any one moment.

Quality filters applied, and reported so they are not silent:
  - static water level deeper than the drilled hole  (physically impossible)
  - drilled depth over 2000 ft                       (implausible for these logs)
  - drilled depth under 10 ft
  - missing completion year
"""
import json, sys
import numpy as np

src = sys.argv[1] if len(sys.argv) > 1 else 'data/derived/las-vegas-wells.json'
dem = sys.argv[2] if len(sys.argv) > 2 else '/tmp/claude-1000/-home-heston/adf1a36e-ea43-4232-b436-f84cab7b660f/scratchpad/lv_dem.npz'
out = sys.argv[3] if len(sys.argv) > 3 else 'data/derived/las-vegas-wells-layer.json'

d = json.load(open(src))
w = np.array(d['wells'], dtype=float)
n0 = len(w)

lon, lat, dep, swl, yr = w[:, 0], w[:, 1], w[:, 2], w[:, 3], w[:, 4]
reasons = {
    'water level deeper than the hole': swl > dep,
    'drilled depth over 2000 ft':       dep > 2000,
    'drilled depth under 10 ft':        dep < 10,
    'no completion year':               yr <= 0,
}
bad = np.zeros(n0, bool)
print(f"raw records: {n0}")
for label, mask in reasons.items():
    print(f"  dropped {int((mask & ~bad).sum()):5d}  {label}")
    bad |= mask
keep = ~bad
w = w[keep]
print(f"kept: {len(w)}  ({100*len(w)/n0:.1f}%)")

# ground elevation at each well, sampled from the DEM
D = np.load(dem)
xs, ys, zs = D['x'], D['y'], D['z']
if ys[0] > ys[-1]:
    ys, zs = ys[::-1], zs[::-1, :]
from scipy.interpolate import RegularGridInterpolator
g = RegularGridInterpolator((ys, xs), zs, bounds_error=False, fill_value=None)
ground = g((w[:, 1], w[:, 0]))

FT = 0.3048
rows = np.column_stack([
    w[:, 0], w[:, 1],
    np.rint(ground),                    # ground elevation, m
    np.rint(w[:, 2] * FT),              # drilled depth, m
    np.rint(w[:, 3] * FT),              # static water level below ground, m
    w[:, 4],                            # completion year
])
print(f"\ndrilled depth  m: median {np.median(rows[:,3]):.0f}  p99 {np.percentile(rows[:,3],99):.0f}  max {rows[:,3].max():.0f}")
print(f"water level    m: median {np.median(rows[:,4]):.0f}  p99 {np.percentile(rows[:,4],99):.0f}  max {rows[:,4].max():.0f}")
print(f"years           : {int(rows[:,5].min())} to {int(rows[:,5].max())}")

json.dump({
    'fields': ['lon', 'lat', 'ground_m', 'drilled_m', 'water_below_ground_m', 'year'],
    'count': len(rows),
    'raw_count': n0,
    'dropped': {k: int(v.sum()) for k, v in reasons.items()},
    'source': ('Nevada Division of Water Resources, Well Driller Reports (public '
               'record). Owner, address, parcel and contractor fields deliberately '
               'excluded. Ground elevation sampled from USGS 3DEP.'),
    'caveat': ('Records span 1935-2026. The well population changes character over '
               'that period, so these are shown as individual boreholes and are NOT '
               'interpolated into a groundwater surface.'),
    'wells': [[round(r[0], 5), round(r[1], 5), int(r[2]), int(r[3]), int(r[4]), int(r[5])]
              for r in rows],
}, open(out, 'w'))
print(f"wrote {out}")
