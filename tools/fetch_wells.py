#!/usr/bin/env python3
"""
Fetch NDWR Well Driller Report points for the Las Vegas valley.

Source: Nevada Division of Water Resources, Well Driller Reports
  https://arcgis.water.nv.gov/arcgis/rest/services/NDWR/Well_Driller_Reports/FeatureServer/0
Nevada requires drillers to file a log for every well. Public record.

PRIVACY -- READ BEFORE CHANGING outFields:
The source layer also carries OwnerCurrent, OwnerAddress, ParcelNumber,
ContractorName and ContractorAddress. Those are private individuals' names and
home addresses. We deliberately request ONLY the geotechnical columns. Do not
add owner, address, parcel, or contractor fields to this request -- being public
record does not make it appropriate to republish a homeowner's name and address
on a public map.
"""
import json, time, sys, urllib.parse, urllib.request

URL = ("https://arcgis.water.nv.gov/arcgis/rest/services/NDWR/"
       "Well_Driller_Reports/FeatureServer/0/query")
BBOX = {"xmin": -115.464, "ymin": 35.934, "xmax": -114.831, "ymax": 36.487,
        "spatialReference": {"wkid": 4326}}
FIELDS = "DepthDrilled,StaticWaterLevel"     # geotechnical only -- see note above
PAGE = 2000

def page(offset):
    q = urllib.parse.urlencode({
        "geometry": json.dumps(BBOX), "geometryType": "esriGeometryEnvelope",
        "inSR": "4326", "outSR": "4326", "spatialRel": "esriSpatialRelIntersects",
        "where": "DepthDrilled>0 AND StaticWaterLevel>0",
        "outFields": FIELDS, "returnGeometry": "true",
        "resultOffset": offset, "resultRecordCount": PAGE, "f": "json"})
    with urllib.request.urlopen(URL + "?" + q, timeout=90) as r:
        return json.load(r)

out, offset = [], 0
while True:
    d = page(offset)
    feats = d.get("features", [])
    if not feats:
        break
    for f in feats:
        g, a = f.get("geometry"), f["attributes"]
        if not g or g.get("x") is None:
            continue
        out.append([round(g["x"], 6), round(g["y"], 6),
                    a["DepthDrilled"], a["StaticWaterLevel"]])
    print(f"  {len(out):6d} wells", flush=True)
    if not d.get("exceededTransferLimit"):
        break
    offset += PAGE
    time.sleep(0.4)                      # be polite to a state agency's server

dest = sys.argv[1] if len(sys.argv) > 1 else "data/derived/las-vegas-wells.json"
json.dump({"fields": ["lon", "lat", "depth_drilled_ft", "static_water_level_ft"],
           "count": len(out),
           "source": ("Nevada Division of Water Resources, Well Driller Reports. "
                      "Public record. Owner/address/parcel/contractor fields "
                      "deliberately excluded."),
           "wells": out}, open(dest, "w"))
print(f"wrote {dest}: {len(out)} wells")
