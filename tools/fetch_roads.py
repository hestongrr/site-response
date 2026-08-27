#!/usr/bin/env python3
"""
Fetch the valley's freeway network from US Census TIGER/Line.

Source: US Census Bureau, TIGERweb Transportation
  https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/Transportation/MapServer
A US federal work -- PUBLIC DOMAIN, free for any use including commercial.

Only primary roads and US highways. Local streets exist in the same service but
there are tens of thousands of them; at valley scale they would be grey mush.
The freeway ring is what people actually recognise.
"""
import json, urllib.parse, urllib.request, sys

BASE = ("https://tigerweb.geo.census.gov/arcgis/rest/services/"
        "TIGERweb/Transportation/MapServer")
BBOX = {"xmin": -115.464, "ymin": 35.934, "xmax": -114.831, "ymax": 36.487,
        "spatialReference": {"wkid": 4326}}

def fetch(layer):
    q = urllib.parse.urlencode({
        "geometry": json.dumps(BBOX), "geometryType": "esriGeometryEnvelope",
        "inSR": "4326", "outSR": "4326", "spatialRel": "esriSpatialRelIntersects",
        "where": "1=1", "outFields": "NAME,MTFCC", "returnGeometry": "true",
        "resultRecordCount": 2000, "f": "json"})
    with urllib.request.urlopen(f"{BASE}/{layer}/query?{q}", timeout=90) as r:
        return json.load(r).get("features", [])

lines, names = [], {}
for layer, cls in ((2, "primary"), (3, "highway")):
    for f in fetch(layer):
        nm = (f["attributes"].get("NAME") or "").strip()
        for path in (f.get("geometry") or {}).get("paths", []):
            if len(path) < 2:
                continue
            lines.append({"cls": cls, "name": nm,
                          "pts": [[round(x, 5), round(y, 5)] for x, y in path]})
            names[nm] = names.get(nm, 0) + 1

dest = sys.argv[1] if len(sys.argv) > 1 else "data/derived/las-vegas-roads.json"
json.dump({"source": ("US Census Bureau TIGER/Line via TIGERweb. "
                      "US federal work - public domain."),
           "retrieved": "2026-08-26",
           "count": len(lines),
           "vertices": sum(len(l["pts"]) for l in lines),
           "roads": lines}, open(dest, "w"))
print(f"wrote {dest}: {len(lines)} segments, "
      f"{sum(len(l['pts']) for l in lines)} vertices")
for nm, c in sorted(names.items(), key=lambda kv: -kv[1])[:10]:
    print(f"  {nm or '(unnamed)':32s} {c}")
