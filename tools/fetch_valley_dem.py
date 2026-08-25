#!/usr/bin/env python3
"""
Fetch the USGS 3DEP elevation model for the Las Vegas valley.

Public domain (USGS federal work). 90 m resolution is deliberate: this is a
57 x 61 km valley, and finer data would be gigabytes for no visible gain at
the scale the model is viewed.
"""
import numpy as np, py3dep, sys
from shapely.geometry import box

W, S, E, N = -115.464, 35.934, -114.831, 36.487   # matches the basin-depth grid
out = sys.argv[1] if len(sys.argv) > 1 else 'lv_dem.npz'

dem = py3dep.get_map("DEM", box(W, S, E, N), resolution=90, crs="EPSG:4326")
a = dem.to_numpy()
print(f"{a.shape}  elevation {np.nanmin(a):.0f} to {np.nanmax(a):.0f} m, {np.isnan(a).sum()} gaps")
np.savez_compressed(out, z=a.astype('float32'),
                    x=dem.x.to_numpy(), y=dem.y.to_numpy())
print("wrote", out)
