# Attribution — required by the licence

The data in this directory is **not ours**. It is redistributed here under
CC-BY-4.0, which permits redistribution **on condition of attribution**. If you
reuse it, carry this attribution with it.

> Simpson, Alexander R., and John N. Louie (2020). *Measurements and Predictions
> of Vs30, Z1.0, and Z2.5 in Nevada.* Nevada Seismological Laboratory, University
> of Nevada, Reno. DOI: [10.5281/zenodo.4408557](https://doi.org/10.5281/zenodo.4408557)
> Licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/).

Source record: https://zenodo.org/records/4408557

## What is here

Retrieved 2026-08-24 by `fetch.sh`, which re-downloads it from Zenodo.

| File | What it is |
|---|---|
| `lv-langenheim-thick-zmod.txt` | Las Vegas valley grid, 22,022 points. Basin depth from gravity (Zg) plus Z1.0 and Z2.5 with min/max bounds and percent error. |
| `jachens-basindepth-zmod.txt` | Same fields, statewide Nevada grid, 218,210 points. |
| `Nevada Z1.0 Z2.5.kml` | Google Earth overlay of the model areas and source-study extents. |
| `*.png`, `*.jpg` | Rendered basin-depth maps for Nevada, Las Vegas, and Reno. |
| `Nevada-Z1.0-Z2.5-report1231.pdf` | The full report. Read this before using the numbers. |

Columns in the `.txt` grids:
`lat long Zg Z1.0min Z1.0 Z1.0max Z2.5min Z2.5 Z2.5max Z1.0error Z2.5error`
— depths in km, errors in percent.

## What it says about Las Vegas

Computed from `lv-langenheim-thick-zmod.txt` (22,022 grid points spanning
35.93–36.49 N, 115.46–114.83 W):

| | min | median | max |
|---|---|---|---|
| Zg — basin depth from gravity | 0.00 km | 0.13 km | **4.90 km** |
| Z1.0 — depth to Vs = 1.0 km/s | 0.14 km | 0.15 km | 2.07 km |
| Z2.5 — depth to Vs = 2.5 km/s | 0.30 km | 0.33 km | 4.45 km |

Nearest grid point to some recognisable places:

| Place | Zg | Z1.0 (range) | Z2.5 (range) |
|---|---|---|---|
| The Strip | 0.43 km | 0.18 (0.13–0.24) | 0.38 (0.29–0.50) |
| Downtown | **1.66 km** | 0.35 (0.18–0.67) | 0.75 (0.42–1.31) |
| NW valley / Centennial Hills | 0.94 km | 0.24 (0.15–0.37) | 0.51 (0.34–0.75) |
| Henderson | 0.62 km | 0.20 (0.13–0.28) | 0.43 (0.30–0.58) |

**Carry the uncertainty.** Median stated error is **21% on Z1.0 and 19% on
Z2.5**, and the min/max columns are wide — downtown Z2.5 spans 0.42 to 1.31 km.
Any figure or tool built on this must show the range, not just the middle number.
Quoting a single value as if it were measured at that spot misrepresents the
source.
