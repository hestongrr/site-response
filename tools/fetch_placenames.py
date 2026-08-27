#!/usr/bin/env python3
"""
Pull official place names for the Las Vegas valley from USGS GNIS.

Source: USGS The National Map, Geographic Names Information System (GNIS) —
  https://carto.nationalmap.gov/arcgis/rest/services/geonames/MapServer
GNIS is the Federal standard for geographic nomenclature, maintained by the
U.S. Board on Geographic Names. As a US federal work it is PUBLIC DOMAIN, so
the names may be used freely, including commercially. Credit is courtesy, not
obligation -- we give it anyway.

Note: this map service carries Landforms and Populated Places but NOT parks;
its "Cultural Points" group contains only Crossings. Park names would need the
full GNIS staged download or a local open-data source.
"""
import json, urllib.parse, urllib.request, sys

BASE = "https://carto.nationalmap.gov/arcgis/rest/services/geonames/MapServer"
BBOX = {"xmin": -115.464, "ymin": 35.934, "xmax": -114.831, "ymax": 36.487,
        "spatialReference": {"wkid": 4326}}
WANT = {5: ("Summit", "Range", "Ridge", "Gap"), 3: ("Populated Place",)}

def fetch(layer):
    q = urllib.parse.urlencode({
        "geometry": json.dumps(BBOX), "geometryType": "esriGeometryEnvelope",
        "inSR": "4326", "outSR": "4326", "spatialRel": "esriSpatialRelIntersects",
        "where": "1=1", "outFields": "gaz_name,gaz_featureclass",
        "returnGeometry": "true", "resultRecordCount": 1000, "f": "json"})
    with urllib.request.urlopen(f"{BASE}/{layer}/query?{q}", timeout=90) as r:
        return json.load(r)

out = []
for layer, classes in WANT.items():
    d = fetch(layer)
    for f in d.get("features", []):
        a = f["attributes"]
        cls = a.get("gaz_featureclass")
        if cls not in classes:
            continue
        pts = (f.get("geometry") or {}).get("points") or []
        if not pts:
            continue
        lon, lat = pts[0][0], pts[0][1]          # multipoint geometry
        out.append({"name": a["gaz_name"], "class": cls,
                    "lat": round(lat, 5), "lon": round(lon, 5)})

out.sort(key=lambda r: (r["class"], r["name"]))
dest = sys.argv[1] if len(sys.argv) > 1 else "data/derived/las-vegas-placenames.json"
json.dump({"source": ("USGS Geographic Names Information System (GNIS), "
                      "The National Map. US federal work — public domain."),
           "retrieved": "2026-08-26", "count": len(out), "places": out},
          open(dest, "w"), indent=1)
print(f"wrote {dest}: {len(out)} names")
from collections import Counter
for k, v in Counter(r["class"] for r in out).items():
    print(f"  {k}: {v}")
