#!/usr/bin/env python3
"""
Build the ep 3 (rain / flash-flooding) drainage dataset.

Public domain (USGS federal work). Routes D8 on the native 30 m USGS 3DEP DEM
(whose extent is the actual valley, with semi-natural mountain/Lake-Mead edges
rather than a synthetic rectangle), then aggregates flow accumulation onto the
SAME 300x260 grid the ep 2 valley model renders so the wash lines drape on the
block the viewer already knows.

Output (data/derived/rain-drainage.json):
  * acc_u16_be_b64 -- D8 flow accumulation (upstream 30m cell count) per display
    cell, quantised 0..65535, for draping as line brightness.
  * acc_max_cells  -- raw max (the Las Vegas Wash / Lake Mead outlet).

Method:
  * internal routing grid ~90 m (1 in 3 of the 30 m cells) so the priority-flood
    sink fill is tractable;
  * sink fill (priority flood) so pits don't trap flow;
  * D8 steepest-descent direction;
  * accumulate by descending filled-elevation order (each cell's runoff added to
    its downhill neighbour once);
  * map each routing cell's accumulation onto the display grid via nearest output
    cell, summed.

Flow accumulation = upstream 30 m cell count = proxy for upstream area. Shows
WHERE water runs, not HOW MUCH (that needs Atlas-14 rainfall depth).
"""
import argparse, base64, heapq, json, os, sys
import numpy as np
import rasterio

DEFAULT_DEM = "/home/heston/geo-ref/05_Maps_Data/LasVegas_WaterTable/lv_dem30.tif"
DEFAULT_OUT = "/home/heston/repos/site-response/data/derived/rain-drainage.json"
NX, NY = 300, 260
STRIDE = 3                      # ~90 m routing grid from the 30 m DEM

DR = [0, -1, -1, -1, 0, 1, 1, 1]
DC = [1, 1, 0, -1, -1, -1, 0, 1]
WLEN = [1.0, np.sqrt(2), 1.0, np.sqrt(2), 1.0, np.sqrt(2), 1.0, np.sqrt(2)]



def main(argv=None):
    ap = argparse.ArgumentParser(description="Build the ep 3 drainage dataset.")
    ap.add_argument("out", nargs="?", default=DEFAULT_OUT, help="output .json")
    ap.add_argument("--dem", default=DEFAULT_DEM, help="USGS 3DEP 30 m DEM GeoTIFF")
    a = ap.parse_args(argv)
    if not os.path.isfile(a.dem):
        sys.exit(f"error: DEM not found: {a.dem} (use --dem)")
    with rasterio.open(a.dem) as src:
        big = src.read(1).astype('float64')
        big[big < -1000] = np.nan
        if src.nodata is not None:
            big[big == src.nodata] = np.nan
        xs = src.bounds.left  + (np.arange(src.width)  + 0.5) * abs(src.transform.a)
        ys = src.bounds.top   - (np.arange(src.height) + 0.5) * abs(src.transform.e)

    # ---- routing grid -----------------------------------------------------------
    R0 = big[::STRIDE, ::STRIDE]
    rx = xs[::STRIDE]; ry = ys[::STRIDE]
    R = R0.copy(); valid = np.isfinite(R)
    R = np.where(valid, R, 0.0)
    NR, NC = R.shape
    print(f"routing grid {NR}x{NC}")

    # ---- 1. sink fill (priority flood boundary) --------------------------------
    H = R.copy()
    PRI = []
    done = np.zeros((NR, NC), bool)
    for i in range(NR):
        for j in [0, NC - 1]:
            heapq.heappush(PRI, (H[i, j], i, j))
    for j in range(NC):
        for i in [0, NR - 1]:
            heapq.heappush(PRI, (H[i, j], i, j))
    while PRI:
        h, i, j = heapq.heappop(PRI)
        if done[i, j]:
            continue
        done[i, j] = True
        for k in range(8):
            ni, nj = i + DR[k], j + DC[k]
            if ni < 0 or ni >= NR or nj < 0 or nj >= NC or done[ni, nj]:
                continue
            if H[ni, nj] < h:
                H[ni, nj] = h
            heapq.heappush(PRI, (H[ni, nj], ni, nj))

    # ---- 2. D8 direction (vectorised) ------------------------------------------
    HI = np.full((NR, NC), -1, dtype=np.int8)
    BEST = np.zeros((NR, NC), dtype=np.float32) - 1
    for k in range(8):
        dr, dc = DR[k], DC[k]
        up = np.roll(np.roll(H, -dr, axis=0), -dc, axis=1)
        if dr == 1:  up[-1, :] = np.nan
        if dr == -1: up[0, :]  = np.nan
        if dc == 1:  up[:, -1] = np.nan
        if dc == -1: up[:, 0]  = np.nan
        slope = (H - up) / WLEN[k]
        better = (slope > BEST) & np.isfinite(slope)
        BEST = np.where(better, slope, BEST)
        HI = np.where(better, k, HI)
    HI[HI < 0] = 8
    HI[~valid] = 8

    # ---- 3. accumulation --------------------------------------------------------
    acc = np.where(valid, 1.0, 0.0)
    order = np.argsort(-H, axis=None)
    for idx in order:
        i, j = np.unravel_index(idx, H.shape)
        if HI[i, j] == 8:
            continue
        ni, nj = i + DR[HI[i, j]], j + DC[HI[i, j]]
        if 0 <= ni < NR and 0 <= nj < NC:
            acc[ni, nj] += acc[i, j]

    # ---- 4. map accumulation onto the display grid ------------------------------
    WEST, EAST = -115.46327162051541, -114.83116603429595
    SOUTH, NORTH = 35.93421707955155, 36.48630930042678
    dgx = (EAST - WEST) / (NX - 1); dgy = (NORTH - SOUTH) / (NY - 1)
    out = np.zeros((NY, NX), dtype=np.float64)
    cnt = np.zeros((NY, NX), dtype=np.float64)
    for i in range(NR):
        for j in range(NC):
            if not valid[i, j]:
                continue
            ix = int(round((rx[j] - WEST) / dgx))
            iy = int(round((ry[i] - SOUTH) / dgy))
            if 0 <= ix < NX and 0 <= iy < NY:
                out[iy, ix] += acc[i, j]
                cnt[iy, ix] += 1
    mean = np.where(cnt > 0, out / np.maximum(cnt, 1), 0.0)

    qmax = float(mean.max()) if mean.size else 0.0
    if qmax <= 0:
        sys.exit('error: no flow accumulation computed (DEM empty or all nodata?)')
    q = (np.clip(mean / qmax, 0, 1) * 65535).astype('>u2')
    payload = {
        'nx': NX, 'ny': NY,
        'west': WEST, 'east': EAST, 'south': SOUTH, 'north': NORTH,
        'acc_u16_be_b64': base64.b64encode(q.tobytes()).decode('ascii'),
        'acc_max_cells': round(qmax, 1),
        'method': ('D8 flow accumulation of the sink-filled USGS 3DEP 30m DEM '
                   '(routed ~90m), aggregated to the 300x260 display grid, in '
                   'upstream-cell count. Shows where water runs, not how much '
                   '(volume needs Atlas-14 rainfall depth).'),
        'source': 'USGS 3DEP (public domain).',
    }
    json.dump(payload, open(a.out, 'w'))
    print(f"wrote {a.out}  acc max {qmax:.0f} 30m cells")


if __name__ == "__main__":
    main()
