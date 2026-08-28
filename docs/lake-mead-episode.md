# Episode plan — Lake Mead: the number that actually matters

Status: **researched and verified, not built.** Ranked behind ep 3 (rain).

## The idea

The public argument is about *how empty Lake Mead will get*. Making another
forecast adds noise. The gap is that **"percent full" and "feet of elevation"
are not proportional, and nobody says so** — and that the threshold that
actually matters to Las Vegas is not a percentage at all. It is whether the
water is above the straw.

**Hook:** Everyone argues about how empty Lake Mead will get. The number that
matters isn't a percentage — it's whether the water is above your intake. Las
Vegas worked that out, spent $1.5 billion, and built a straw that reaches below
the point where the dam itself stops working.

## The numbers (all verified 2026-08-26)

| | |
|---|---|
| Today | **1,039.05 ft · 6.91 maf** |
| Record high | **1,225.83 ft · 24 July 1983** |
| Capacity at full pool (1,229 ft) | 162,916 acres · ~26 maf usable |
| Fraction of usable storage remaining | **~26%** |

### Elevations that matter
| Mark | ft | Today |
|---|---|---|
| Full pool | 1,229 | 190 ft above water |
| **Intake No. 1** (1970s) | **1,050** | **11 ft above water — DRY** |
| Intake No. 2 | 1,000 | 39 ft below water |
| Minimum power pool | 950 | Hoover stops generating |
| **Dead pool** | **895** | capacity table reads **zero** |
| **Low Lake Level Pumping Stn** | **875** | **20 ft BELOW dead pool** |

### The non-linearity — the actual teaching point
The reservoir is a canyon, not a bathtub. Surface area at 1,229 ft is roughly
**1.9x** the area near 1,082 ft, so **the same one foot of drop is worth about
1.8x more water at the top than near the bottom**. That is why "it dropped 30
feet" and "it lost X percent" describe one event and sound like two.

## Verification — the DEM matches the official bathymetry

Computed a hypsometric curve from USGS 3DEP terrain alone, then compared it to
USBR's area-capacity tables (2001 multibeam survey):

| Elev ft | USBR km² | DEM km² | Diff |
|---|---|---|---|
| 1,093 | 352 | 355 | +0.8% |
| 1,150 | 454 | 456 | +0.3% |
| **1,157** | **470** | **470** | **exact** |
| 1,206 | 604 | 606 | +0.3% |
| 1,218 | 634 | 636 | +0.4% |

Ten of thirteen elevations agree to better than 1%.

Two independent USBR datasets also agree with each other: at 1,039 ft the table
gives 6.909 maf, the daily series 6.912 maf — 0.05% apart.

**The NHD waterbody polygon (541 km² at a stated 1,157 ft) is the outlier**, not
the DEM. Its ELEVATION attribute does not mean the water surface. Do not
"correct" a good computation toward a bad reference.

## Data — all US federal, public domain

`tools/fetch_lake_mead.py` pulls everything.

| Layer | Source | File |
|---|---|---|
| Terrain above waterline | USGS 3DEP, 90 m, bbox −114.98/35.90/−113.55/36.65 | fetch on demand |
| Bathymetry (area + capacity per 0.1 ft) | USBR 2009 tables, 2001 multibeam survey | `lake-mead-area-capacity.json` |
| Daily elevation + storage 1935→now | USBR Lower Colorado | `lake-mead-daily.json` (33,444 records) |
| Intake elevations | SNWA published pages | `lake-mead-intakes.json` |
| Lake polygon | USGS NHD | use with caution, see above |

**A DEM has no bathymetry.** ~36% of cells below 400 m sit in one flat bin at the
survey-date water plane (1,082 ft in the current tile). Terrain gives the exposed
shell; the USBR tables give everything below. You need both.

## Supporting thread — quagga mussels

Present since 2007, never eradicated. **But it is a managed cost, not a crisis** —
Lake Mead is nutrient-poor so growth is slow, and Intake No. 3 is 24 ft in
diameter, which defeats fouling by sheer scale. SNWA budgets >$500k/yr,
Reclamation ~$1M/yr at Hoover.

Control is **chloramine, dosed in the intake process and never into the lake**.
Say chloramine, not chlorine. Worth about 20 seconds, not a pillar.

Heston's UNLV senior design project was a chlorine-dosing scheme for mussels at
an intake. **A class project** — one honest sentence explaining why he knows the
problem exists, carrying no other weight.

## Guardrails

- **Do not forecast.** Show the shape of the container and where the marks sit.
  Forecasting is the crowded, contested part.
- **Surviving below dead pool solves Las Vegas's straw, not the region's water.**
  Hoover's power and downstream deliveries still stop. If the video implies Vegas
  is fine, a knowledgeable commenter will correctly object.
- Avoid Colorado River allocation politics entirely. This is an engineering
  story about geometry and thresholds.
- Zebra mussels were recently found in the upper Colorado for the first time.
  Nevada is still clear. A watch-item, not a current problem.
