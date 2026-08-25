# The Las Vegas valley two-surface model

Two surfaces, and the sediment between them:

- **Ground surface** — USGS 3DEP elevation, 90 m. Public domain.
- **Bedrock floor** — ground elevation minus basin-fill thickness Zg, from USGS
  gravity analyses (Langenheim et al. 1998, 2001), reached via Simpson & Louie
  2020, CC-BY-4.0, doi:10.5281/zenodo.4408557.

## Build

    python3 tools/fetch_valley_dem.py lv_dem.npz
    python3 tools/build_valley_data.py lv_dem.npz

Output: `data/derived/las-vegas-valley.json` — a 300 x 260 mesh, both surfaces
quantised to int16 metres and base64'd, about 400 KB.

## Verification

The build asserts bedrock never sits above the ground surface. The DEM
orientation was checked against known points rather than assumed:

| Check | Model | Reality |
|---|---|---|
| Highest point in bbox | 2465 m at 36.213 N, 115.460 W | Spring Mountains, west edge ✓ |
| Lowest point in bbox | 318 m at 36.116 N, 114.831 W | Lake Mead / Las Vegas Wash, east edge ✓ |
| Frenchman Mtn ridge crest | 1221 m | summit ~1235 m ✓ (~1% at 90 m) |
| Sunrise Mtn | 954 m | ~950 m ✓ |
| Valley floor near I-15 | 625 m | ~610 m ✓ |
| Frenchman Mtn basin fill | 0.00 km | bedrock outcrop, correct ✓ |

West high, east low — the orientation is right. An earlier apparent error turned
out to be badly chosen test coordinates (Mt Charleston is at 115.69 W, outside
this bounding box entirely), not a data fault.

## Numbers it produces

| | |
|---|---|
| Ground surface | 318 – 2424 m |
| Basin fill thickness | 0 – 4882 m |
| Bedrock elevation | −4330 – 2424 m |
| Under downtown | 1.69 km of fill |
| Under the Strip | 0.44 km of fill |
| Valley extent | 57 × 61 km |

## What this is not

Zg is a **gravity model**, not drilling. Basin fill is less dense than bedrock
and weakens the local gravity field; inverting that anomaly gives thickness. It
carries real uncertainty and the source report says so. Any public rendering
must state that, and must state its vertical exaggeration.
