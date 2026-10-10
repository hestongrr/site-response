# Episode plan — Caliche: the rock Las Vegas sits on

Status: **researched and verified, not built.** Candidate for the "do caliche
next" slot in the Las Vegas geology series.

## The idea

Caliche is one of the things that makes engineering in Las Vegas what it is,
yet nobody talks about it: the valley floor is laced with carbonate-cemented
soil that refuses to be dug or drilled, and the same groundwater chemistry that
leaves scale on a kitchen sink is what put it there. The gap is that people
picture Nevada's ground as "just sand and rock." The story is that a huge
fraction of what the valley sits on is **cemented by the very water that made
it a desert settlement** — and it is both a homeowner's and an engineer's
problem once you try to cut into it.

**Hook:** "Hard water" isn't just your sink and showerhead. The same chemistry
that crusts a faucet is what cements large parts of the Las Vegas valley into
rock that stops drill rigs and bends excavator teeth.

## The numbers (all verified 2026-08-30)

| | |
|---|---|
| Caliche = | calcium-carbonate (CaCO3)-cemented soil; calcite cement bridging and filling pore space between grains |
| Depth of pedogenic (soil-formed) horizon | ~1–3 m in stable desert soils |
| Gile stages I–VI | filaments→nodules→continuous "plugged" cement (III+)→laminar cap→pisolites→massive hardpan |
| Drill response to Stage III+ | reads like weak rock, not sand; drills "4–6 blows" on the local in-house scale |
| LV calcium / hardness | avg **75 ppm Ca**, total hardness **280 ppm** (~16 gpg) — the "sink scale" identity |
| Wells mentioning caliche (NDWR logs) | **81 of 637** scanned, **141** total mentions, all geocoded |

### The two caliches — the actual teaching point
There are two ways caliche forms, and Las Vegas has both:
- **Pedogenic (soil-formed):** rain carries atmospheric/soil CO2 down as weak
  carbonic acid, dissolves carbonate dust/clasts, and the desert's
  evaporation front re-concentrates it at a fairly consistent shallow depth —
  a "K-horizon" that means the surface has been geologically stable for
  ~10^4–10^5 years.
- **Phreatic / groundwater:** carbonate-rich basin groundwater meets aeration
  and evaporates at or below the water table, precipitating thick, massive,
  deep calcrete — the "valley-scale" caliche under parts of Las Vegas.

The viewer take-home: *is this the shallow soil caliche, or the deep
groundwater caliche?* The drill/rig behavior — and what you can build — differs.

## Heston's telling — with the hokey-pokey caveat

Heston's simplified, teachable version (the one that field-tests in the
valley), attributed to Dr. Barbara Luke (UNLV) and made his own:

> In Las Vegas it rains once in a great while. When it rains on the mountains,
> the mountains are full of limestone, and the rain slowly dissolves it — that
> is how the caves in the mountains are formed. The same dissolved limestone
> runs down into the valley over time, carried by groundwater movement. That
> groundwater has dissolved limestone in it, and when it settles on the sand,
> gravel, clay, and silt across the valley, those materials solidify into
> caliche. Same as the white calcium buildup on any old sink — same process.

The story is the **delivery**; it is a deliberate simplification ("hokey pokey"
— facts folded into a memorable shape). What it downplays is the pedogenic /
dust-and-infiltration route at shallow depth. Both routes cleanly reconcile:
dust/infiltration makes the surface caliche; groundwater makes the deep,
massive calcrete. The episode should say both plainly, then let Heston's one-
breath version carry the audience.

## Hero object — the CCSD caliche specimen

A real caliche chunk from the **over-excavation for a CCSD school** — the deep
grading cut that removes the valley's expansive/collapsible soils — given to
Heston by **Robert at Angle Engineering**. Reportedly from **~15 ft below
grade** (memory-approx; treat as a soft clue, not a publishable number).
The hero detail: **one piece showing BOTH end-members on one surface** — the
dry (vadose) flat side versus the side that sat in groundwater with
**teardrop-shaped (stalactite-family) cementation**. Field rule that films
well: *which way the teardrops point tells which way the water went.*

- Field-library photo: `~/Pictures/field-library/geotech-reference/caliche/2022-03-16_las-vegas-ccsd_caliche-specimen.jpg` (GPS 36.0809, -115.2127)
- Second caliche photo: `2019-05-24_reference_caliche-specimen.jpg`
- Use: identification plate + photogrammetry / iPhone LiDAR capture.

## Verification — claims against sources

| Claim | Verdict | Source |
|---|---|---|
| Mountains around Vegas are carbonate | ✓ | USGS SIM 2814 (Page et al. 2005): ranges largely Paleozoic carbonate rock; Spring Mountains = major recharge site of Nevada's carbonate-rock aquifer province |
| Rain dissolves limestone → karst | ✓ mechanism | USGS Karst Aquifers (2021) |
| Valley groundwater is carbonate-rich | ✓ | USGS WRI 87-4007 (Dettinger 1987): LV groundwater dominated by Ca, Mg, bicarbonate |
| Valley fill derived from the mountains | ✓ | USGS WSP 2320-A: basin filled 3,000–5,000 ft; Spring Mountains + McCullough Range major clastic sources |
| Groundwater deposits CaCO3 → caliche | ✓✓ | Werle & Luke 2007 (ASCE GSP 162): CaCO3 precipitated where evapotranspiration exceeds precipitation; cemented zones impacted The Strip; excavated blocks reused as retaining-wall facings |
| Sink scale = same CaCO3 | ✓ | LVVWD Water Quality Summary: 75 ppm Ca, 280 ppm hardness |

## Data — public records

`tools/mine_caliche_wells.py` mines NDWR scanned well-driller reports.

| Layer | Source | File |
|---|---|---|
| Well logs mentioning caliche | NDWR scanned drillers' reports + `well_metadata.json` (OCR, public record) | `data/derived/caliche-well-mentions.json` / `.geojson` |
| Scope | 637 logs scanned · 81 with caliche · 141 mentions · 81 geocoded wells | — |

**OCR caveat (important):** handwritten geology on scanned drillers' logs is
unreliable. Positive caliche matches indicate caliche; the *absence* of a match
proves nothing. Any depth figure from a log is a **human-review candidate, not
a final number** — this is why the binder keeps the specimen's ~15 ft as a soft
clue and why a single well mention must not be quoted out of context.

Note the well-log caliche mentions are often **shallow** (just under pavement/
fill in short 20–23 ft logs in the NW valley) — a separate, and genuinely
useful, contrast to the deep phreatic calcrete. Use the map to show extent, not
to over-claim depth.

## What the records actually show (2026-08-30)

New stats computed from `caliche-well-mentions.json` — all guardrailed by the
OCR caveat above (treat as extent/typing, not as individual depths).

**Where it shows up:**
- 81 geocoded wells; cluster is **central / east-central Las Vegas valley**
  (centroid 36.1295, -115.1615; bounds lat 36.000–36.268, lon −115.304 to
  −115.051). This is the dense urban core, which is also where the short,
  modern wells get drilled.
- Grid bins: 36.1/−115.1 = 35 wells, 36.1/−115.2 = 29, 36.2/−115.1 = 7,
  36.0/−115.2 = 7, 36.3/−115.3 = 3. No caliche hits out in the far west
  valley/ranges of this sample.

**The Strip cluster — confirms the field experience.** A distinct group sits
right at the **southern Strip corridor** (~36.00, −115.165 to −115.171), the
deep old wells logs 57517/57518/57524/57526/57535/57542/57577 (1955–1980,
120–295 ft deep, static water 88–143 ft). These carry caliche depth-candidates
across **the whole range — shallow (6–20 ft) AND deep (114–295 ft)** on the
same logs, e.g. 57518 caliche at 210 & 295 ft, 57526 at 160 ft. Plus a 2023 trio
(141063/141064/141676) at 36.11, −115.20 (north Strip). This is exactly the
"caliche layers all over near the strip" Heston reports and matches the
published claim that **cemented zones impacted The Strip (Werle & Luke 2007)**.
It is the single most defensible on-map anchor for the episode.

**When it was logged:**
- **58 of 81 wells finished 2016–2023** (2021 alone = 23). Nearly all older
  caliche-bearing logs predate OCR readability — so the temporal pattern is a
  **record-format artifact**, not a claim that caliche is "newer." Say so if
  anyone reads recency into it. (1952–1980: 13 wells; 1993–2018: ~10.)

**How deep (median, not a single authoritative number):**
- Drilled depth: min 12 ft, **median 30 ft**, max 500 ft (n=81).
- Static water level where reported: min 6 ft, median ~18.6 ft, max 290 ft
  (n=64).
- Deepest caliche **depth-candidates** (human review, not final): logs 69836
  (500 ft), 57518 (295/210), 56569 (200/188), 57526 (160), 57524 (156) — the
  plausible deep/phreatic-calcrete end. The very shallow mentions (right under
  asphalt/fill in 20–23 ft logs) are the near-surface pedogenic end. Both are
  visible in the same dataset — a nice on-map version of the two-end-member
  teaching point.

**What it sits in:** calibrated lithology near caliche tokens is repeatedly
"silty/clayey sand w/ gravel," i.e., caliche is logged *inside the alluvial
sand-and-gravel valley fill* — consistent with carbonate cementing the fill,
not a bedrock horizon.

**Engineering tie-in (already citable):** caliche is why the Strip is stiffer
than the loose fill intuition suggests — **Scott et al. 2006** found calcite
cementation raises Vs30 along the Strip to ~500–600 m/s, **NEHRP site class C**,
and that geology maps cannot predict it. One YouTube-legal sentence pairing
"caliche stiffens the ground under the Strip" ties the home/well story to the
existing seismic-reference material without overclaiming.

## Supporting thread — the wild-west framing

Old Las Vegas was springs, ranches, and cowboys before the casinos; the desert-
geology field work Heston and Dr. Luke do is on their own terms. "Hokey pokey"
as a Wild West term and the two of them as "very wild west" is accepted for the
record. Keep it as a light, one-line color beat — not a pillar.

## Guardrails

- **Do not over-claim depth from OCR'd logs.** Show the map of where caliche
  shows up in the well records; treat any individual depth as a candidate.
- **Do not publish the ~15 ft as a hard number.** It is memory-approx and the
  exact figure was forgotten. Say "deep, hit a distinct buried bed" — that is
  the defensible fact.
- **Keep the two end-members explicit.** The "which way do the teardrops
  point" field rule is the filmable, true centerpiece; don't fold them back
  into one vague "cemented soil."
- **Sink-scale analogy is exact** (75 ppm Ca, 280 ppm) — use it, but pin it to
  LVVWD data and say "same CaCO3 chemistry," not "same exact water."
- Client-sensitive Red Rock signage photos (Crescente Bush) stay internal —
  do not use in the episode.
- A knowledgeable commenter will note pedogenic-vs-phreatic nuance; acknowledging
  both routes up front preempts that and matches Heston's field observation.

## Review notes (cloud, 2026-10-09)

Automated technical review. The original text above is untouched. House rule:
every technical fact names its source. Suggested sources are pointers to check,
not verified citations — confirm title/number/page before they go on screen.

### A. Claims that look wrong or contradict the data

1. **"Deepest caliche depth-candidates: 69836 (500 ft), 57518 (295), 56569 (200), 57524 (156)" — these equal each well's `depth_drilled_ft`**
   in `caliche-well-mentions.json` (500, 295, 200, 156). They are very likely
   the total-depth annotation on the form, not a caliche depth, so using them
   as the "deep/phreatic end" is circular. The candidate list also contains
   casing/bit sizes (5, 8, 12, 16.94 in. on 56569) and 0.0 values.
   *Suggested source:* read the original scanned log images for these logs
   (NDWR well-log database) before claiming any deep caliche depth.
2. **"58 of 81 wells finished 2016–2023"** — the JSON gives **56** (2021 = 23 is
   correct). **"1952–1980: 13 wells"** — the JSON gives **16** with
   `finish_year` ≤ 1980. *Source:* recompute from `caliche-well-mentions.json`.
3. **Specimen: "teardrop-shaped (stalactite-family) cementation" on the side that sat in groundwater.**
   Pendant/stalactitic (gravity) cement is conventionally a *vadose* feature
   (water draining under gravity), whereas phreatic cement is typically
   uniform/isopachous or meniscus-free. The two sides may be swapped, and
   "teardrops point the way the water went" holds for vadose drip only.
   *Suggested source:* Machette 1985, GSA Spec. Paper 203 (calcic soils of the
   SW US); Scholle & Ulmer-Scholle 2003, AAPG Memo 77 (cement fabrics).
4. **"Sink scale = same CaCO3" using LVVWD 75 ppm Ca / 280 ppm.** Valley tap
   water is mostly Colorado River (Lake Mead) supply, not the local
   groundwater that precipitated caliche; the analogy is about chemistry, not
   the same water (the Guardrails section half-says this). 280 ppm ≈ 16.4 gpg
   (÷17.1) is arithmetically fine. *Source:* LVVWD/SNWA annual water quality
   report (year and sampling point), plus a source for the groundwater
   chemistry (USGS WRI 87-4007 as cited).
5. **"Caliche is why the Strip is stiffer… Vs30 ~500–600 m/s, NEHRP class C."**
   Class C is 360–760 m/s (ASCE 7-16 Table 20.3-1), so consistent, but the
   causal claim "caliche raises Vs30" and "geology maps cannot predict it"
   need the exact statement. *Source:* Scott et al. 2006 — give the full
   citation (journal/report, page); ASCE 7-16 Table 20.3-1 for the class bounds.

### B. Claims with no named source

| Claim (section) | Suggested source |
|---|---|
| Pedogenic horizon "~1–3 m in stable desert soils" (Numbers) | Machette 1985, GSA SP 203; Gile, Peterson & Grossman 1966, Soil Sci. 101 |
| Gile stages I–VI list and mapping of "III+ = plugged", "laminar cap → pisolites → massive" (Numbers) | Machette 1985 (stages I–VI); Gile et al. 1966 defined only I–IV for gravelly soils — check the stage/feature order |
| "Drills 4–6 blows on the local in-house scale" (Numbers) | Name the scale; if not published, label it as anecdotal. For a citable proxy: ASTM D1586 (SPT) or ASTM D5878 / ASTM D6032 (rock/weathering classification) |
| K-horizon "means stable ~10^4–10^5 years" (Two caliches) | Machette 1985 (stage–age tables); Reheis 1999 or Gile et al. 1966 |
| Phreatic calcrete "thick, massive, deep… under parts of Las Vegas" (Two caliches) | Quade et al. 1995, GSA Bull. (Las Vegas valley spring/wetland deposits); Mann & Horwitz 1979 (groundwater calcrete); Werle & Luke 2007 |
| Pedogenic mechanism: CO2/carbonic acid, evaporation front at consistent depth (Two caliches) | Machette 1985; Birkeland 1999, *Soils and Geomorphology* |
| CCSD over-excavation "removes the valley's expansive/collapsible soils" (Hero object) | Clark County Building Code geotechnical/soils chapter (cite section); CCSD or project geotech report |
| Hero specimen "~15 ft" (Hero object) | Already flagged as soft; no number should be on screen without the project geotech report |
| Basin fill "3,000–5,000 ft" (Verification table) | Name the author: Plume 1989, USGS WSP 2320-A (Part 1); cite figure/page |
| USGS "WRI 87-4007 (Dettinger 1987)" (Verification table) | Confirm report number ↔ author/title pairing against the USGS Publications Warehouse before citing |
| "81 of 637 / 141 mentions" (Numbers, Data) | Reproducible from `tools/mine_caliche_wells.py` + NDWR scanned-log OCR; cite NDWR log database and date of pull |
| Strip-cluster ages, depths and static levels, centroid/bounds, grid bins (What the records show) | Match `caliche-well-mentions.json` (checked: centroid, bounds, grid bins and static-water median 18.6 ft match; see A.1–A.2 for mismatches) |
| "Mountains are full of limestone… caves" (Heston's telling) | USGS SIM 2814 as already cited; a cave/karst source for the Spring Mountains (e.g. USFS Spring Mountains NRA) |

### C. Interpretation cautions (not errors)

- The "OCR absence proves nothing" guardrail is correct, but the geocoded
  count (81/81) also depends on `well_metadata.json` coordinates; the tool now
  warns on stderr if a caliche log is dropped for lacking lat/lon.
- "Short, modern wells in the urban core" explains the spatial cluster; the
  2016–2023 skew is a record-format artifact, as the text already says.
- Strip "1955–1980" wells include ten-plus 1955 logs — most of that cluster is a
  single year, not a spread.
