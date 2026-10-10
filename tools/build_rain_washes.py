#!/usr/bin/env python3
"""
Build the ep 3 wash-network polylines (rain / flash-flooding).

Public domain (USGS federal work). Routes D8 on the same ~90 m routing grid as
build_rain_drainage.py (sink-filled 30 m USGS 3DEP DEM), then extracts the
channel network as connected polylines by walking STEEPEST-DESCENT down each
channel headwater. A cell used by an earlier polyline stops the walk, so
branches stitch onto shared trunks instead of duplicating them -- the output is
a connected river network, not a pile of fragments.

Output (data/derived/rain-washes.json):
  * washes: [{path:[[lon,lat],...], strength}] -- strength = acc/accmax so the
    capstone's brightness/width scales with upstream area.

Run:  python3 build_rain_washes.py [OUT.json] [THR]
  THR = channel-cell accumulator threshold in upstream ~90 m cells
        (default ~1.2 % of the maximum upstream count).
"""
import argparse, heapq, json, os, sys
import numpy as np
import rasterio

DEFAULT_DEM = "/home/heston/geo-ref/05_Maps_Data/LasVegas_WaterTable/lv_dem30.tif"
DEFAULT_OUT = "/home/heston/repos/site-response/data/derived/rain-washes.json"
NX, NY = 300, 260
STRIDE = 3

DR = [0, -1, -1, -1, 0, 1, 1, 1]
DC = [1, 1, 0, -1, -1, -1, 0, 1]
WLEN = [1.0, np.sqrt(2), 1.0, np.sqrt(2), 1.0, np.sqrt(2), 1.0, np.sqrt(2)]


def simplify(pts):
    """Drop interior points that are exactly colinear with their neighbours.

    pts are (x, y) pairs on a regular grid (any consistent unit); a point is
    kept only where the walk changes direction.
    """
    if len(pts) < 3:
        return list(pts)
    out = [pts[0]]
    for prev, p, nxt in zip(pts, pts[1:], pts[2:]):
        cross = (p[0] - prev[0]) * (nxt[1] - p[1]) - (p[1] - prev[1]) * (nxt[0] - p[0])
        if abs(cross) > 1e-9 * max(1.0, abs(p[0]) * abs(p[1])):
            out.append(p)
    out.append(pts[-1])
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description="Build the ep 3 wash polylines.")
    ap.add_argument("out", nargs="?", default=DEFAULT_OUT, help="output .json")
    ap.add_argument("thr", nargs="?", type=float, default=None,
                    help="channel threshold in upstream ~90 m cells (default: 99.5th pct)")
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

    R0 = big[::STRIDE, ::STRIDE]
    rx = xs[::STRIDE]; ry = ys[::STRIDE]
    R = R0.copy(); valid = np.isfinite(R)
    R = np.where(valid, R, 0.0)
    NR, NC = R.shape
    print(f"routing grid {NR}x{NC}")

    # ---- sink fill (priority flood) --------------------------------------------
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

    # ---- D8 steepest descent + accumulation ------------------------------------
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

    acc = np.where(valid, 1.0, 0.0)
    order = np.argsort(-H, axis=None)
    for idx in order:
        i, j = np.unravel_index(idx, H.shape)
        if HI[i, j] == 8:
            continue
        ni, nj = i + DR[HI[i, j]], j + DC[HI[i, j]]
        if 0 <= ni < NR and 0 <= nj < NC:
            acc[ni, nj] += acc[i, j]
    accmax = float(acc.max())
    q = np.quantile(acc[acc >= 1], [0.9, 0.95, 0.99, 0.995, 0.999])
    print(f"acc max {accmax:.0f}  (~90 m upstream cells)")
    print("acc quantiles (>=1):", {f"{x:g}%": int(v) for x, v in zip([90,95,99,99.5,99.9], q)})

    THR = a.thr if a.thr is not None else float(np.quantile(acc[acc >= 1], 0.995))
    print(f"channel threshold THR = {THR:.0f}")

    # ---- channel cells ----------------------------------------------------------
    chan = acc >= THR
    nchan = int(chan.sum())
    print(f"channel cells {nchan} ({100*nchan/(NR*NC):.2f}% of grid)")

    def drain(i, j):
        k = HI[i, j]
        if k == 8:
            return None
        ni, nj = i + DR[k], j + DC[k]
        if 0 <= ni < NR and 0 <= nj < NC:
            return ni, nj
        return None

    # ---- walk downstream from every channel headwater ---------------------------
    # headwater = a channel cell that NO channel cell drains INTO (true top of a
    # branch). Walk steepest descent from each until hitting used ground, claiming
    # the whole branch, so later tributaries stitch onto the shared trunk.
    rev_needed = {}
    for i in range(NR):
        for j in range(NC):
            if not chan[i, j] or HI[i, j] == 8:
                continue
            ni, nj = i + DR[HI[i, j]], j + DC[HI[i, j]]
            if 0 <= ni < NR and 0 <= nj < NC:
                rev_needed.setdefault((i, j), []).append((ni, nj))  # (i,j) pours into ni,nj
    fed_into = {}
    for (i, j), outs in rev_needed.items():
        for (ni, nj) in outs:
            fed_into.setdefault((ni, nj), []).append((i, j))        # what pours into (ni,nj)

    used = np.zeros_like(chan)
    lines = []
    cellbuf = []
    # seed by acc so the main trunks get walked first and longest
    for order_idx in np.argsort(-acc, axis=None):
        i, j = np.unravel_index(order_idx, acc.shape)
        if not chan[i, j] or used[i, j]:
            continue
        if fed_into.get((i, j)):                 # something pours in: not a headwater
            continue
        cellbuf.clear()
        seen = set()                         # guard against routing cycles
        ci, cj = i, j
        while chan[ci, cj] and not used[ci, cj] and (ci, cj) not in seen:
            seen.add((ci, cj))
            cellbuf.append((ci, cj))
            d = drain(ci, cj)
            if d is None:
                break
            ci, cj = d
        if not cellbuf:
            continue
        for (ci2, cj2) in cellbuf:
            used[ci2, cj2] = True
        lines.append(cellbuf.copy())

    # ---- prune stub branches under MIN_LEN channel cells -----------------------
    MIN_LEN = 8
    kept = [L for L in lines if len(L) >= MIN_LEN]
    print(f"lines total {len(lines)} -> kept {len(kept)} (>= {MIN_LEN} cells)")

    # ---- simplify (drop colinear points) + emit lon/lat -------------------------

    WEST, EAST = -115.46327162051541, -114.83116603429595
    SOUTH, NORTH = 35.93421707955155, 36.48630930042678


    washes = []
    for L in sorted(kept, key=lambda L: -max(acc[i, j] for i, j in L)):
        s = max(acc[i, j] for i, j in L) / accmax
        path = simplify([(rx[j], ry[i]) for i, j in L])
        washes.append({'path': [[round(lon, 6), round(lat, 6)] for lon, lat in path],
                       'strength': round(float(s), 3)})

    json.dump({'count': len(washes), 'washes': washes, 'threshold_cells': THR,
               'source': 'USGS 3DEP, public domain. D8 steepest-descent '
                         'downstream walk on the sink-filled ~90 m routing grid.',
               'method': 'branching network, branches stitched onto shared trunks'},
              open(a.out, 'w'))
    print(f"wrote {a.out}: {len(washes)} washes, "
          f"max strength {max((w['strength'] for w in washes), default=0):.3f}")

    # ---- ASCII map of the network for a quick eyeball ---------------------------
    if os.environ.get('RAIN_ASCII'):
        on = {}
        for w in washes:
            for lon, lat in w['path']:
                ix = int((lon - WEST)/(EAST - WEST)*(NX-1))
                iy = int((lat - SOUTH)/(NORTH - SOUTH)*(NY-1))
                on[(ix, iy)] = on.get((ix, iy), 0) + 1
        rows, cols = 60, 120
        for rr in range(rows):
            row = []
            for cc in range(cols):
                ix = cc*(NX-1)//(cols-1); iy = rr*(NY-1)//(rows-1)
                c = on.get((ix, iy), 0)
                row.append('#' if c >= 3 else '+' if c == 2 else
                           '.' if c == 1 else ' ')
            print(''.join(row))


if __name__ == "__main__":
    main()
