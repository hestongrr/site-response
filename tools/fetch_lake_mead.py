#!/usr/bin/env python3
"""
Fetch every Lake Mead dataset needed for the reservoir episode.

All sources are US federal works — public domain, free for any use.

  USGS 3DEP          terrain ABOVE the waterline
  USBR 2009 tables   area + capacity at every tenth of a foot (the bathymetry)
  USBR daily series  pool elevation and storage, 1935 -> present
  SNWA               intake elevations (verified from published pages)

Why both terrain and tables: a DEM shows the WATER SURFACE where the lake
currently is, not the bottom. Roughly 36% of cells below 400 m sit in one flat
bin at the survey-date water plane. Terrain gives the exposed shell; the USBR
tables give everything below.
"""
import csv, io, json, re, subprocess, sys, urllib.request

OUT = "data/derived"
AC2KM2 = 0.00404686

def get(url, timeout=120):
    return urllib.request.urlopen(url, timeout=timeout).read()

# ---- 1. daily elevation + storage, 1935 -> present ------------------------
def daily():
    series = {}
    for pid, name in ((49, "pool_elevation_ft"), (17, "storage_af")):
        raw = get(f"https://www.usbr.gov/uc/water/hydrodata/reservoir_data/921/csv/{pid}.csv")
        for row in csv.reader(io.StringIO(raw.decode())):
            if not row or not row[0][:1].isdigit():
                continue
            if len(row) < 2 or row[1] in ("", "NA"):
                continue
            series.setdefault(row[0], {})[name] = float(row[1])
    rows = [{"date": d, **v} for d, v in sorted(series.items())]
    json.dump({"source": "US Bureau of Reclamation, Lower Colorado. Public domain.",
               "count": len(rows), "rows": rows},
              open(f"{OUT}/lake-mead-daily.json", "w"))
    return rows

# ---- 2. area-capacity table (the bathymetry) ------------------------------
def area_capacity(pdf="refs/usbr-2009-lake-mead-area-capacity-tables.pdf"):
    txt = subprocess.run(["pdftotext", "-layout", pdf, "-"],
                         capture_output=True, text=True).stdout
    seen = {}
    for ln in txt.split("\n"):
        m = re.match(r"\s*(\d{3,4})\s+((?:[\d,]+\s+){9}[\d,]+)\s*$", ln)
        if not m:
            continue
        e = int(m.group(1))
        if not 600 <= e <= 1250:
            continue
        seen.setdefault(e, []).append(float(m.group(2).split()[0].replace(",", "")))
    # first table is area in HUNDREDS of acres, second is capacity in KAF
    rows = [{"elev_ft": e, "area_acres": v[0]*100, "area_km2": round(v[0]*100*AC2KM2, 2),
             "capacity_af": v[1]*1000}
            for e, v in sorted(seen.items()) if len(v) >= 2]
    json.dump({"source": ("US Bureau of Reclamation, Lake Mead Area and Capacity Tables, "
                          "Sept 2011, from the 2001 multibeam bathymetric survey. "
                          "Public domain."),
               "note": "capacity is zero at 895 ft (dead pool)",
               "count": len(rows), "rows": rows},
              open(f"{OUT}/lake-mead-area-capacity.json", "w"))
    return rows

INTAKES = [
    {"name": "Full pool",                  "elev_ft": 1229, "note": "USBR"},
    {"name": "Intake No. 1",               "elev_ft": 1050, "note": "SNWA, 1970s. Went dry 2022."},
    {"name": "Intake No. 2",               "elev_ft": 1000, "note": "SNWA"},
    {"name": "Minimum power pool",         "elev_ft":  950, "note": "Hoover Dam stops generating"},
    {"name": "Dead pool",                  "elev_ft":  895, "note": "no water passes Hoover Dam"},
    {"name": "Low Lake Level Pumping Stn", "elev_ft":  875, "note": "SNWA, online Apr 2022. Below dead pool."},
]

if __name__ == "__main__":
    d = daily(); print(f"daily series      {len(d):,} records  {d[0]['date']} -> {d[-1]['date']}")
    a = area_capacity(); print(f"area-capacity     {len(a):,} elevations {a[0]['elev_ft']}-{a[-1]['elev_ft']} ft")
    json.dump({"source": "SNWA published pages, verified 2026-08-26", "marks": INTAKES},
              open(f"{OUT}/lake-mead-intakes.json", "w"))
    print(f"intake marks      {len(INTAKES)}")
