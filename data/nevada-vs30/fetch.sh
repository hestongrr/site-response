#!/usr/bin/env bash
# Re-download the CC-BY-4.0 Nevada basin-depth dataset from Zenodo.
# Kept as a script rather than committing 24 MB of someone else's data.
# See ATTRIBUTION.md -- the licence requires attribution on any reuse.
set -euo pipefail
cd "$(dirname "$0")"
BASE="https://zenodo.org/api/records/4408557/files"
curl -sL -o Nevada-Z1.0-Z2.5-models.zip   "$BASE/Nevada-Z1.0-Z2.5-models.zip/content"
curl -sL -o Nevada-Z1.0-Z2.5-report1231.pdf "$BASE/Nevada-Z1.0-Z2.5-report1231.pdf/content"
rm -rf extracted && unzip -oq Nevada-Z1.0-Z2.5-models.zip -d extracted && rm -rf extracted/__MACOSX
echo "Simpson & Louie (2020), DOI 10.5281/zenodo.4408557, CC-BY-4.0 -- attribution required."
