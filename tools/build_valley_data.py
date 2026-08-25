#!/usr/bin/env python3
"""
Build the two-surface dataset for the Las Vegas valley 3D page.

  Surface 1: the ground you stand on   -- USGS 3DEP DEM
  Surface 2: the bedrock floor beneath -- ground elevation minus basin-fill
             thickness Zg, from USGS gravity analyses (Langenheim et al.
             1998, 2001) reached via Simpson & Louie 2020, CC-BY-4.0,
             doi:10.5281/zenodo.4408557

The volume between them is the sediment that amplifies earthquake shaking.

Zg is a GRAVITY MODEL, not a drilled depth. See data/nevada-vs30/ATTRIBUTION.md.
"""
import base64, json, sys
import numpy as np
from scipy.interpolate import griddata

DEM_NPZ = sys.argv[1] if len(sys.argv) > 1 else 'lv_dem.npz'
BASIN   = sys.argv[2] if len(sys.argv) > 2 else 'data/nevada-vs30/extracted/lv-langenheim-thick-zmod.txt'
OUT     = sys.argv[3] if len(sys.argv) > 3 else 'data/derived/las-vegas-valley.json'
NX, NY  = 300, 260          # mesh resolution sent to the browser

d = np.load(DEM_NPZ)
zs, xs, ys = d['z'], d['x'], d['y']
if ys[0] > ys[-1]:                      # make y ascend north
    ys, zs = ys[::-1], zs[::-1, :]

# regular target grid inside the DEM extent
gx = np.linspace(xs.min(), xs.max(), NX)
gy = np.linspace(ys.min(), ys.max(), NY)
GX, GY = np.meshgrid(gx, gy)

# ground surface: bilinear sample of the DEM
from scipy.interpolate import RegularGridInterpolator
ground = RegularGridInterpolator((ys, xs), zs, bounds_error=False,
                                 fill_value=None)((GY, GX))

# basin thickness: interpolate the scattered gravity points onto the same grid
b = np.loadtxt(BASIN, skiprows=1)
zg = griddata((b[:, 1], b[:, 0]), b[:, 2], (GX, GY), method='linear')
zg = np.nan_to_num(zg, nan=0.0) * 1000.0        # km -> m
zg = np.clip(zg, 0, None)

bedrock = ground - zg

print(f"grid {NY} x {NX}")
print(f"ground  {ground.min():8.1f} to {ground.max():8.1f} m")
print(f"fill    {zg.min():8.1f} to {zg.max():8.1f} m thick")
print(f"bedrock {bedrock.min():8.1f} to {bedrock.max():8.1f} m")
assert (bedrock <= ground + 1e-6).all(), "bedrock must never sit above the ground"

# quantise to int16 metres -- plenty of precision for a landscape, 2 bytes/vertex
def pack(a):
    q = np.rint(a).astype('>i2')
    return base64.b64encode(q.tobytes()).decode('ascii')

json.dump({
    'nx': NX, 'ny': NY,
    'west': float(gx.min()), 'east': float(gx.max()),
    'south': float(gy.min()), 'north': float(gy.max()),
    'ground_i16_be_b64': pack(ground),
    'bedrock_i16_be_b64': pack(bedrock),
    'source': ('Ground: USGS 3DEP. Basin thickness: USGS gravity analyses '
               '(Langenheim et al. 1998, 2001) via Simpson & Louie 2020, '
               'CC-BY-4.0, doi:10.5281/zenodo.4408557. Zg is a gravity model, '
               'not a drilled depth.'),
}, open(OUT, 'w'))
print(f"wrote {OUT}")
