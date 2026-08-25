# References — Nevada and Las Vegas seismic hazard

Sources for anything this project says about Nevada. House rule: cite where it
came from, and flag what is paywalled or unavailable.

Last updated 2026-08-24.

---

## The people doing this work locally

**UNLV Applied Geophysics Center** — the group that actually measured the ground
under Las Vegas.

- **Dr. Wanda Taylor** — Professor, Department of Geoscience. Structural geology,
  tectonics, neotectonics; currently working on Las Vegas Valley sediments and
  their relationship to southern Nevada faults.
  Profile: https://geoscience.unlv.edu/people/department-faculty/wanda-j-taylor/
- **Dr. Aly Said** — Civil & Environmental Engineering and Construction;
  co-investigator on the DOE "Earthquakes in Southern Nevada" study.
- **Dr. William U. "Woody" Savage** — Adjunct Professor with the Applied
  Geophysics Center. **USGS Emeritus Seismologist**; managed the ANSS
  Strong-Motion Program at Menlo Park 2001–2008, then Seismotectonics Senior
  Scientist / USGS Science Advisor on the Yucca Mountain Project in Las Vegas
  until 2010. Board member of the Seismological Society of America and co-chair
  of its Government Relations Committee; chaired the Bruce Bolt Panel. Since 2010
  the **Southern Nevada Geosciences representative on the Nevada Earthquake
  Safety Council**, and works to improve earthquake monitoring in the Las Vegas
  valley. Congressional testimony (public domain, US House):
  https://democrats-science.house.gov/imo/media/doc/Savage%20Testimony.pdf

The Applied Geophysics Center is explicitly interdisciplinary — a joint venture
of UNLV's Department of Civil & Environmental Engineering and its Department of
Geoscience, which is why the engineering and geology sides appear together on
this work.

**Nevada Seismological Laboratory (UNR)** — https://www.seismo.unr.edu/
Operates the state seismic network. **Dr. John N. Louie** there developed the
refraction microtremor (ReMi) method used for much of the Las Vegas Vs work, and
co-authored the key papers below.

**Nevada Earthquake Safety Council (NESC)** — https://nbmg.unr.edu/nesc/
(also listed via Nevada Division of Emergency Management, https://dem.nv.gov/Boards/nesc/)
Its stated mission is to give decision makers and the public information and
actions that reduce earthquake losses and speed recovery. This is the state-level
body for exactly the thing this project is trying to help with.

**Nevada Bureau of Mines and Geology (NBMG)** —
https://nbmg.unr.edu/Geohazards/Earthquakes/EarthquakeResources.html
Quaternary fault maps, hazard publications, and public preparedness guidance
(including Spanish-language material).

---

## Key publications

**Scott, J. B., et al. (2006).** "Shallow shear velocity and seismic microzonation of the
urban Las Vegas, Nevada, basin." *Bulletin of the Seismological Society of
America*, 96(3), 1068–1077. **DOI: 10.1785/0120050044**

The anchor reference for Las Vegas site conditions. A 13-km transect parallel to
Las Vegas Blvd. (the Strip) plus borehole and surface-wave measurements at 30
further sites — Vs-vs-depth profiles at **49 locations**, mostly by refraction
microtremor.

Findings that matter to this project:
- **Caliche raises Vs30 along the Strip to roughly 500–600 m/s — NEHRP site
  class C.** Calcite-cemented alluvium is stiffer than the loose sediment people
  assume is under a desert city.
- **The lowest velocities (NEHRP D) sit near intrabasin faults**, around
  Interstate 15 and Lake Mead Blvd.
- **Geologic map units predict measured Vs poorly.** You cannot infer the site
  class from surface geology here. This is a caution, not a detail — see below.

**UNLV Applied Geophysics Center (2008).** Three-dimensional shallow shear-wave
velocity model for the Las Vegas Valley. Reported in *The Leading Edge* (Society
of Exploration Geophysicists), November 2008.

Built from **230 shear-wave velocity measurements**, **160+ seismic site
classifications** from local agencies, and interpretation of **nearly 1,600
geologic well logs**, to depths of hundreds of feet. Funded by a multi-year U.S.
Department of Energy grant, "Earthquakes in Southern Nevada." UNLV summary:
https://www.unlv.edu/news/release/unlv-research-team-completes-3-d-model-depicting-how-valley-soils-could-react-during

**Three-Dimensional Modeling of Shallow Shear-Wave Velocities for Las Vegas,
Nevada, Using Sediment Type.** *Journal of Earth Science*.
DOI: 10.1007/s12583-009-0046-8

**Shallow-to-deep shear wave velocity profiling by surface waves in complex
ground for enhanced seismic microzonation of Las Vegas, Nevada.** *Soil Dynamics
and Earthquake Engineering*.
https://www.sciencedirect.com/science/article/abs/pii/S026772611200214X

---

## Open data we can actually redistribute

**Simpson, A. R., and J. N. Louie (2020).** "Measurements and Predictions of
Vs30, Z1.0, and Z2.5 in Nevada." Nevada Seismological Laboratory, UNR.
**Zenodo record 4408557 — https://zenodo.org/records/4408557**

**License: CC-BY-4.0.** Redistributable with attribution, which makes it the one
dataset here we can ship rather than merely link.

Contains Vs30, Z1.0 (depth to Vs = 1.0 km/s) and Z2.5 measurements and
predictions. 170 sites in the Reno basin plus others statewide, and
**49 measurements along Las Vegas Boulevard with Z1.0 from 0.05 to 0.68 km**.
Ships as text data, a PDF report, maps, and **KML for Google Earth** — which
drops straight into the existing `gis-maps` workflow.

Independently reaches the same conclusion as Scott et al. (2006): there appear to
be no geological or soil-mapping criteria able to predict Vs30 in Nevada.

### Basin depth under Las Vegas — actual numbers from the open dataset

Computed from `lv-langenheim-thick-zmod.txt` (22,022 grid points):

| | min | median | max |
|---|---|---|---|
| Zg — basin depth from gravity | 0.00 km | 0.13 km | **4.90 km** |
| Z1.0 — depth to Vs = 1.0 km/s | 0.14 km | 0.15 km | 2.07 km |
| Z2.5 — depth to Vs = 2.5 km/s | 0.30 km | 0.33 km | 4.45 km |

| Place | Zg | Z1.0 (range) | Z2.5 (range) |
|---|---|---|---|
| The Strip | 0.43 km | 0.18 (0.13–0.24) | 0.38 (0.29–0.50) |
| Downtown | **1.66 km** | 0.35 (0.18–0.67) | 0.75 (0.42–1.31) |
| NW valley / Centennial Hills | 0.94 km | 0.24 (0.15–0.37) | 0.51 (0.34–0.75) |
| Henderson | 0.62 km | 0.20 (0.13–0.28) | 0.43 (0.30–0.58) |

Median stated uncertainty is **21% on Z1.0 and 19% on Z2.5**, and the bounds are
wide. Anything we publish from this shows the range.

Note the contrast worth explaining to the public: the Strip sits on relatively
shallow, caliche-stiffened ground (Vs30 500–600 m/s, site class C) while
downtown has kilometres of basin fill beneath it. Same city, very different
ground.

---

## The finding we must not paper over

**Two independent studies, fourteen years apart, both concluded you cannot
predict Vs30 in Nevada from geologic or soil maps.**

That is a hard constraint on any "type your address and see your site class"
feature. The honest version of such a tool interpolates *measured* points and
says plainly how far the nearest measurement is. Anything that infers a site
class from mapped geology would be contradicting the two best local studies while
citing them, which is worse than not building it.

---

## Statewide hazard context

Nevada is the **third most seismically active state** in the US, after Alaska and
California.

- Magnitude 6 or greater: roughly every 10 years
- Magnitude 7 or greater: roughly every 27 years
- 63 earthquakes of M5.5+ since the 1850s
- The state sits in the **Basin and Range** — actively extending crust, hence the
  density of faults
- The **Walker Lane**, ~600 miles along the Nevada–California border, is the most
  seismically active part of the state

Source: Nevada Seismological Laboratory (John Anderson, former director); NBMG,
"An Introduction to Nevada's Earthquake Hazards,"
https://nbmg.unr.edu/_docs/Newsletters/nl2.htm

**Las Vegas Valley faults:** Wanda Taylor has stated that at least **11 faults**
crossing the valley floor or lying just outside it are capable of a substantial
earthquake. Named intrabasin faults commonly cited include Frenchman Mountain,
Eglington, Decatur, Valley View, and Cashman Field. *Individual fault parameters
still need to be pulled from the NBMG/USGS Quaternary fault database before we
publish any of them.*

---

## Public safety guidance

- **NBMG Earthquake Preparedness** —
  https://nbmg.unr.edu/geohazards/earthquakes/Preparedness.html
  Six steps; explicitly says drop/cover/hold and **do not run outside**.
  Publications, with series numbers:
  - *Living With Earthquakes in Nevada* — Special Publication 27
  - *Earthquakes in Nevada and How to Survive Them* — Educational Series 16
  - *Terremotos en Nevada y Cómo Sobrevivirlos* — Educational Series 27 (Spanish)
- **Nevada Seismological Laboratory preparedness guide**, "Put the odds in your
  favor!" — https://www.seismo.unr.edu/Files/Preparedness/nvguide_2010.pdf
- **The Great Nevada ShakeOut** — https://www.shakeout.org/nevada/resources/
- NBMG earthquake presentations —
  https://nbmg.unr.edu/geohazards/Earthquakes/EarthquakePresentations.html
- **Great ShakeOut** — https://www.shakeout.org/
- **Ready.gov earthquakes** (FEMA) — https://www.ready.gov/earthquakes
- **Earthquake Country Alliance**, Seven Steps to Earthquake Safety —
  https://www.earthquakecountry.org/
- **USGS Earthquake Hazards Program** — https://earthquake.usgs.gov/
- UNLV, "5 Common Earthquake Myths" —
  https://www.unlv.edu/news/article/5-common-earthquake-myths
- UNLV, "Earthquakes in Southern Nevada: Knowing the Risk and How to Prepare" —
  https://www.unlv.edu/news/release/earthquakes-southern-nevada-knowing-risk-and-how-prepare

---

## Still to chase

- Whether the 2008 3-D Vs model itself is publicly obtainable, or only described
  in the papers. The UNLV release does not say where to get it.
- NBMG/USGS Quaternary fault database entries for the named Las Vegas faults —
  slip rates and recurrence, properly cited, before any of it is published.
- Full text of Scott et al. (2006); GeoScienceWorld returns 403 and the BSSA
  abstract page is the accessible route.
- Whether the Applied Geophysics Center publishes profile data directly. The
  old directory URL (`unlv.edu/engineering/agcd`) now 404s.

---

## Source documents held locally

Downloaded to `refs/` (gitignored — these are large, and freely available from
the links below rather than needing to be vendored here).

**USGS, public domain — the actual origin of the basin-thickness data:**
- Langenheim and others, **OF-98-576**, *Thickness of Cenozoic deposits and
  location and geometry of the Las Vegas Valley shear zone, Nevada* —
  https://pubs.usgs.gov/of/1998/0576/report.pdf
- Langenheim and others, **OF-97-441**, *Preliminary location and geometry of the
  Las Vegas Valley shear zone based on gravity and aeromagnetic data* —
  https://pubs.usgs.gov/of/1997/0441/report.pdf
- Langenheim and others, **OF-96-259**, *Thickness of Cenozoic deposits and
  groundwater storage capacity, westernmost Las Vegas Valley* —
  https://pubs.usgs.gov/of/1996/0259/report.pdf
- **OF-99-435**, *Principal facts for gravity stations, Lake Mead 30' x 60'
  quadrangle* — https://pubs.usgs.gov/of/1999/0435/pdf/of99-435.pdf

**Paywalled — cite, do not redistribute:**
- Langenheim and others (2001), *Geophysical constraints on the location and
  geometry of the Las Vegas Valley shear zone*, **Tectonics** 20(2), 189–209,
  doi:10.1029/1999TC001159. Wiley returns 403.
- Scott and others (2006), BSSA 96(3), doi:10.1785/0120050044.

### What the authors themselves say about the uncertainty

From OF-98-576, on the seismic interval velocities used to convert to depth:

> It is difficult to assess the uncertainties in these interval velocities
> because of the lack of well logs and check shots. The error is probably +/- 10%,
> but could be as high as +/- 20%. Velocities are poorly constrained beneath
> 2.0 s (approximately 3 km).

**This matters directly.** The deepest part of the valley in our model is 4.9 km
— below the depth the authors describe as poorly constrained. The headline number
is the least certain one, and any public presentation must say so.

Gravity station elevation uncertainty is given as <0.3 m (<0.06 mGal); terrain
correction error is put at up to 3.3 mGal worst case, averaging far less.

### Independent agreement

Published work reports the deepest subbasin at roughly **5 km, about 5 km west of
Frenchman Mountain**. Our build, from the derived grid, puts it at **4.90 km,
6.2 km west** of the DEM-verified Frenchman crest. Depth agrees within 0.1 km and
direction agrees. That is reassuring, not proof.

---

## Nevada Division of Water Resources — well driller reports

https://arcgis.water.nv.gov/arcgis/rest/services/NDWR/Well_Driller_Reports/FeatureServer/0
145,746 records statewide; **41,996 inside the Las Vegas valley bounding box**.
Nevada requires a filed log for every well, so this is public record.

Populated fields, within the valley:

| Field | Records | Usable? |
|---|---|---|
| DepthDrilled | 40,506 | yes |
| StaticWaterLevel | 31,643 | yes |
| both together | 31,610 | yes |
| **DepthBedrock** | **3** | **no — effectively empty** |

**The bedrock-validation idea does not work.** Only three wells in the entire
valley report a depth to bedrock, so the gravity model cannot be checked against
drilled rock depth using this dataset. Recording that here so it is not
re-attempted.

**Privacy — binding constraint.** The layer also carries `OwnerCurrent`,
`OwnerAddress`, `ParcelNumber`, `ContractorName` and `ContractorAddress`. Those
are private individuals' names and home addresses. `tools/fetch_wells.py`
requests **only** `DepthDrilled` and `StaticWaterLevel`, and the stored file was
audited to confirm it contains nothing but four numbers per row. Do not add
owner, address, parcel, or contractor fields: public record status does not make
it appropriate to republish someone's name and home address on a map.

**Known data-quality problems** in the raw records, to be filtered before use:
33 wells report a static water level deeper than the hole was drilled
(impossible), 7 exceed 2,000 ft with one implausible 15,000 ft entry, and the
depth distribution is heavily skewed (median 50 ft, p99 922 ft).
