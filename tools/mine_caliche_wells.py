#!/usr/bin/env python3
"""
Mine NDWR scanned well-log OCR for caliche mentions -> valley map layer.

PRIVACY -- READ BEFORE CHANGING OUTPUT:
well_metadata.json also carries ParcelNumber, ContractorName and address-ish
fields. Those are private. This script emits ONLY: caliche mention evidence,
log number, lat/lon, DepthDrilled, StaticWaterLevel, and finish year. Do not
add parcel/contractor/owner fields to any output.

OCR HONESTY -- the scanned well logs are printed forms with HANDWRITTEN
lithology, and Tesseract mangles handwriting silently (verified: log 67084's
caliche was missed entirely by OCR). Consequences:
  * a log that mentions caliche is a POSITIVE signal, and its depth is usually
    readable off the same page;
  * a log that does NOT mention caliche proves nothing -- absence of OCR text
    is not absence of caliche. Only report positives, and never claim a
    negative.
Depth numbers near a "caliche" token are stored as *candidates* for human
review (the same row can be a casing-schedule column, not lithology depth).
"""
import json, re, sys
from pathlib import Path

OCR_DIR = Path("/home/heston/geo-ref/05_Maps_Data/NDWR_WellLogs/scanned_logs/ocr_text")
META = Path("/home/heston/geo-ref/05_Maps_Data/NDWR_WellLogs/scanned_logs/well_metadata.json")
DEST = (Path(sys.argv[1]) if len(sys.argv) > 1
        else Path("/home/heston/repos/site-response/data/derived/"
                  "caliche-well-mentions.json"))
GEOJSON = DEST.with_suffix(".geojson")

meta = json.load(open(META))
WORD = re.compile(r"caliche", re.I)
NUM = re.compile(r"\d+(?:\.\d+)?")
CTX = 3                                  # context lines carried per mention

features, summary = [], {"logs_scanned": 0, "logs_with_caliche": 0, "mentions": 0}
for f in sorted(OCR_DIR.glob("*.txt")):
    summary["logs_scanned"] += 1
    log = f.stem
    text = f.read_text(errors="replace").splitlines()
    hits = [(i, m.start()) for i, l in enumerate(text) for m in WORD.finditer(l)]
    if not hits:
        continue
    summary["logs_with_caliche"] += 1
    ev = []
    for i, col in hits:
        summary["mentions"] += 1
        lo, hi = max(0, i - CTX), min(len(text), i + CTX + 1)
        ctx = [l.strip() for l in text[lo:hi] if l.strip()]
        row_nums = NUM.findall(" ".join(text[max(0, i - 1): i + 2]))
        ev.append({"context": ctx, "depth_candidates_ft": [float(n) for n in row_nums]})
    m = meta.get(log, {})
    lat, lon = m.get("latitude"), m.get("longitude")
    if lat is None or lon is None:
        continue
    features.append({
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [round(lon, 6), round(lat, 6)]},
        "properties": {
            "log": log,
            "caliche_mentions": len(ev),
            "evidence": ev,
            "depth_drilled_ft": m.get("DepthDrilled"),
            "static_water_level_ft": m.get("StaticWaterLevel"),
            "finish_year": None if not m.get("WellFinishDate") else
                __import__("time").gmtime(m["WellFinishDate"] / 1000).tm_year,
        },
    })

out = {
    "type": "FeatureCollection",
    "name": "caliche-well-mentions",
    "summary": {
        **summary,
        "wells_geocoded": len(features),
        "note": ("OCR of handwritten geology is unreliable: POSITIVE matches "
                 "indicate caliche, ABSENCE of a match proves nothing. Depth "
                 "candidates are for human review, not final numbers."),
    },
    "source": ("Nevada Division of Water Resources scanned well-driller reports "
               "(public record) + well_metadata.json. Private fields excluded."),
    "features": features,
}

DEST.parent.mkdir(parents=True, exist_ok=True)
json.dump(out, open(DEST, "w"), indent=1)
json.dump(out, open(GEOJSON, "w"), indent=1)
s = summary
print(f"logs scanned       : {s['logs_scanned']}")
print(f"logs w/ caliche    : {s['logs_with_caliche']}")
print(f"caliche mentions   : {s['mentions']}")
print(f"wells geocoded     : {len(features)}")
print(f"wrote {DEST}  (+ .geojson)")