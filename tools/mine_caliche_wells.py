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
import argparse, json, re, sys, time
from pathlib import Path

DEFAULT_OCR_DIR = "/home/heston/geo-ref/05_Maps_Data/NDWR_WellLogs/scanned_logs/ocr_text"
DEFAULT_META = "/home/heston/geo-ref/05_Maps_Data/NDWR_WellLogs/scanned_logs/well_metadata.json"
DEFAULT_DEST = ("/home/heston/repos/site-response/data/derived/"
                "caliche-well-mentions.json")

WORD = re.compile(r"caliche", re.I)
NUM = re.compile(r"\d+(?:\.\d+)?")
CTX = 3                                  # context lines carried per mention


def find_mentions(lines):
    """(line_index, column) of every 'caliche' token in OCR lines."""
    return [(i, m.start()) for i, l in enumerate(lines) for m in WORD.finditer(l)]


def depth_candidates(lines, i):
    """Every number on lines i-1..i+1 (the mention row +/- one), as floats."""
    return [float(n) for n in NUM.findall(" ".join(lines[max(0, i - 1): i + 2]))]


def mention_evidence(lines, i, ctx=CTX):
    lo, hi = max(0, i - ctx), min(len(lines), i + ctx + 1)
    return {"context": [l.strip() for l in lines[lo:hi] if l.strip()],
            "depth_candidates_ft": depth_candidates(lines, i)}


def finish_year(ms):
    """WellFinishDate (ms since the Unix epoch, UTC) -> year, or None."""
    if ms in (None, ""):
        return None
    try:
        return time.gmtime(float(ms) / 1000).tm_year
    except (TypeError, ValueError, OverflowError, OSError):
        return None


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("dest", nargs="?", default=DEFAULT_DEST,
                    help="output .json (a .geojson twin is written alongside)")
    ap.add_argument("--ocr-dir", default=DEFAULT_OCR_DIR)
    ap.add_argument("--meta", default=DEFAULT_META)
    a = ap.parse_args(argv)
    ocr_dir, dest = Path(a.ocr_dir), Path(a.dest)
    geojson = dest.with_suffix(".geojson")

    if not ocr_dir.is_dir():
        sys.exit(f"error: OCR directory not found: {ocr_dir} (use --ocr-dir)")
    if not Path(a.meta).is_file():
        sys.exit(f"error: well metadata not found: {a.meta} (use --meta)")
    with open(a.meta) as fh:
        meta = json.load(fh)

    features, summary = [], {"logs_scanned": 0, "logs_with_caliche": 0, "mentions": 0}
    no_coords = []
    for f in sorted(ocr_dir.glob("*.txt")):
        summary["logs_scanned"] += 1
        log = f.stem
        text = f.read_text(errors="replace").splitlines()
        hits = find_mentions(text)
        if not hits:
            continue
        summary["logs_with_caliche"] += 1
        ev = []
        for i, _col in hits:
            summary["mentions"] += 1
            ev.append(mention_evidence(text, i))
        m = meta.get(log, {})
        lat, lon = m.get("latitude"), m.get("longitude")
        if lat is None or lon is None:
            no_coords.append(log)
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
                "finish_year": finish_year(m.get("WellFinishDate")),
            },
        })

    if summary["logs_scanned"] == 0:
        sys.exit(f"error: no *.txt OCR files in {ocr_dir}")

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

    dest.parent.mkdir(parents=True, exist_ok=True)
    for path in (dest, geojson):
        with open(path, "w") as fh:
            json.dump(out, fh, indent=1)
    s = summary
    print(f"logs scanned       : {s['logs_scanned']}")
    print(f"logs w/ caliche    : {s['logs_with_caliche']}")
    print(f"caliche mentions   : {s['mentions']}")
    print(f"wells geocoded     : {len(features)}")
    if no_coords:
        print(f"WARNING: {len(no_coords)} caliche log(s) dropped, no lat/lon in "
              f"metadata: {', '.join(no_coords[:10])}"
              f"{' ...' if len(no_coords) > 10 else ''}", file=sys.stderr)
    print(f"wrote {dest}  (+ .geojson)")


if __name__ == "__main__":
    main()
