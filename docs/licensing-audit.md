# Licensing audit

Everything this project uses, and whether we are actually allowed to use it.
Reviewed 2026-08-24. Re-run this before anything new gets added.

Short version: **we are clear on everything currently in the repo**, with one
item that needs a human decision (naming living people — see the last section).

---

## 1. What we redistribute

Redistribution is where licences actually bite. Only two things here qualify.

**Nevada basin-depth dataset — Simpson & Louie (2020), Zenodo 4408557.**
Licence **CC-BY-4.0**. Redistribution is explicitly permitted, on condition of
attribution. ✅ Compliant: `data/nevada-vs30/ATTRIBUTION.md` carries the required
credit, and `fetch.sh` re-downloads from the source rather than vendoring 24 MB
of someone else's work into git. Any figure or page built from it must carry the
attribution too — the licence follows the data.

**Site chrome CSS — resolved, and the answer is no.** The thebigpicture.tech
design is **not public**. Its shell and stylesheet were removed from this repo
and from its git history, and now live outside it in
`~/private/site-response-site-build/`. `build.js` produces the site page only
when that private directory is present, so a clone builds the standalone page
and nothing else. ✅ Do not reintroduce them.

**Our own code and writing.** MIT, ours, no issue.

---

## 2. What we cite but must NOT reproduce

Facts, findings, and physical equations are not copyrightable. The expression of
them is. We state findings and cite the source; we do not host the papers.

| Source | Status | Rule |
|---|---|---|
| Kramer, *Geotechnical Earthquake Engineering* (1996) | Copyrighted textbook | Physics used; derivation written in our own words. Cite. Never reproduce text or figures. |
| Scott et al. (2006), BSSA 96(3) | © Seismological Society of America | State findings + cite DOI. **Do not host the PDF.** |
| UNLV AGC 3-D Vs model (2008), *The Leading Edge* | © SEG | Cite only. |
| *J. Earth Science* 3-D Vs model; *Soil Dynamics & Earthquake Engineering* paper | Publisher copyright | Cite only. |

✅ Currently compliant — we reproduce none of these.

---

## 3. Federal government works — the most reusable material available

Works produced by US federal employees in the course of their duties are
generally **public domain**. This makes federal sources the best-licensed
material in this whole space, and we should lean on them deliberately:

- **USGS Earthquake Hazards Program** — https://earthquake.usgs.gov/
  National Seismic Hazard Model, ShakeMap, the **Quaternary Fault and Fold
  Database**, Vs30 models. This is the backbone for any hazard-map work.
- **FEMA / Ready.gov** — https://www.ready.gov/earthquakes
  Also FEMA's technical series, notably **FEMA E-74, *Reducing the Risks of
  Nonstructural Earthquake Damage*** — which is precisely the "secure the water
  heater and the bookcases" material our safety section covers, from the
  authoritative source.
- **NEHRP** (National Earthquake Hazards Reduction Program) — provisions and
  guidance documents.
- **ANSS strong-motion data** — the network Woody Savage managed at USGS.
- **NOAA/NCEI** — historical earthquake and tsunami databases.
- **Congressional testimony** — public domain (e.g. Savage's, cited in
  `references-nevada.md`).

⚠️ Two standard caveats: material inside a federal publication that was produced
by a **contractor** or licensed from a third party can still be copyrighted, and
**agency logos and seals are restricted** regardless of the text's status. Check
per document; do not assume the whole PDF is free because the cover is federal.

---

## 4. State and university works — link, do not rehost

**NBMG, Nevada Seismological Laboratory, Nevada Earthquake Safety Council, UNLV.**
State-government and university works are **not** automatically public domain the
way federal works are. ✅ We only link to them and paraphrase facts, which needs
no permission. ⚠️ Do not mirror their PDFs into this repo without either a stated
licence or asking them. Asking is cheap and they are likely to say yes — their
mission is dissemination.

---

## 5. Outbound links

Linking needs no permission. Two things to stay careful about:

⚠️ **Do not imply endorsement.** The page links Build Change, World Housing
Encyclopedia, GEM, NBMG, ShakeOut, USGS and others. They must read as *"these
people do this work, go to them"* — never as partners, sponsors, or reviewers of
this page. Current wording is fine; keep it that way.

⚠️ **No logos, no hotlinked images.** Text links only. Organisation names and
logos are trademarks even when their content is free.

---

## 6. The item that needs a human decision: naming living people

Citing published work by its authors is standard scholarly practice and needs no
permission. Papers are cited here by first author and DOI.

**Standing instruction: do not name the Applied Geophysics Center's director
anywhere in this project** — not in the pages, not in the docs, not in commit
messages. Her published work may be cited in the normal "first author et al. +
DOI" form; her name does not appear.

⚠️ **Attributing personal advice or quotations to a named living person on a
public page is different.** Putting a specific researcher's name behind advice on
a public website puts words in a real person's mouth without their knowledge,
even when the advice is correct and they may well have said it many times.

Current handling: the water guidance stands on its own merits and names no one.

If any individual researcher is ever to be credited personally, the answer is to
**ask them first**. Until then, guidance stands on its own merits and on the
institutional and government sources cited.

---

## 7. Not applicable / clean

- **No web fonts, no CDNs, no external assets** — the pages are self-contained
  and load nothing from anyone else's server, so there is no third-party asset
  licensing question at all.
- **No client data.** Nothing from any Angle Engineering or GeoTek project, no
  job numbers, no boring logs. Everything here comes from published or openly
  licensed sources. This is a hard line and it must stay one.
