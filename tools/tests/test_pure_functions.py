"""Tests for the pure helpers in tools/. Run: python -m pytest tools/tests"""
import calendar
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import mine_caliche_wells as mcw  # noqa: E402

OCR = [
    "WELL LOG 99001",
    "Depth  Material",
    "0-3    asphalt fill",
    "3-7.5  Caliche, hard",
    "7.5-20 silty sand w/ gravel",
    "CALICHE again at 18",
]


def test_find_mentions_is_case_insensitive_and_reports_line_and_column():
    assert mcw.find_mentions(OCR) == [(3, 7), (5, 0)]


def test_find_mentions_counts_repeats_on_one_line():
    assert mcw.find_mentions(["caliche over caliche"]) == [(0, 0), (0, 13)]


def test_find_mentions_none():
    assert mcw.find_mentions(["clay", "sand"]) == []


def test_depth_candidates_use_row_plus_minus_one_line_with_decimals():
    # line 3 +/- 1 -> lines 2..4
    assert mcw.depth_candidates(OCR, 3) == [0.0, 3.0, 3.0, 7.5, 7.5, 20.0]


def test_depth_candidates_clamp_at_start_and_end_of_file():
    assert mcw.depth_candidates(["caliche 5", "x 9"], 0) == [5.0, 9.0]
    assert mcw.depth_candidates(OCR, 5) == [7.5, 20.0, 18.0]


def test_depth_candidates_empty_when_no_numbers():
    assert mcw.depth_candidates(["caliche"], 0) == []


def test_mention_evidence_strips_and_drops_blank_context_lines():
    lines = ["  ", "a", "", "caliche 12", "  ", "b"]
    ev = mcw.mention_evidence(lines, 3, ctx=1)
    assert ev["context"] == ["caliche 12"]
    assert ev["depth_candidates_ft"] == [12.0]
    wide = mcw.mention_evidence(lines, 3, ctx=3)
    assert wide["context"] == ["a", "caliche 12", "b"]


def test_finish_year_from_epoch_ms_utc():
    ms = calendar.timegm((2021, 6, 15, 0, 0, 0)) * 1000
    assert mcw.finish_year(ms) == 2021
    # just before / after the UTC new-year boundary
    assert mcw.finish_year(calendar.timegm((2020, 12, 31, 23, 59, 59)) * 1000) == 2020
    assert mcw.finish_year(calendar.timegm((2021, 1, 1, 0, 0, 0)) * 1000) == 2021


@pytest.mark.parametrize("bad", [None, "", "n/a", float("nan"), 10**30])
def test_finish_year_bad_input_is_none(bad):
    assert mcw.finish_year(bad) is None


def test_main_end_to_end_on_tiny_fixture(tmp_path):
    ocr = tmp_path / "ocr"
    ocr.mkdir()
    (ocr / "1.txt").write_text("0-2 fill\n2-5 caliche\n")
    (ocr / "2.txt").write_text("0-9 sand\n")                # no mention
    (ocr / "3.txt").write_text("caliche 4\n")               # mention, no coords
    meta = tmp_path / "m.json"
    meta.write_text('{"1": {"latitude": 36.1, "longitude": -115.2, '
                    '"DepthDrilled": 30, "StaticWaterLevel": 12, '
                    '"ParcelNumber": "SECRET"}, "3": {}}')
    dest = tmp_path / "out" / "c.json"
    mcw.main([str(dest), "--ocr-dir", str(ocr), "--meta", str(meta)])
    import json
    out = json.loads(dest.read_text())
    assert out["summary"]["logs_scanned"] == 3
    assert out["summary"]["logs_with_caliche"] == 2
    assert out["summary"]["wells_geocoded"] == 1
    props = out["features"][0]["properties"]
    assert props["log"] == "1" and props["depth_drilled_ft"] == 30
    assert "SECRET" not in dest.read_text()                 # privacy rule
    assert dest.with_suffix(".geojson").exists()


def test_main_missing_inputs_exit_cleanly(tmp_path):
    with pytest.raises(SystemExit) as e:
        mcw.main([str(tmp_path / "o.json"), "--ocr-dir", str(tmp_path / "nope")])
    assert "OCR directory not found" in str(e.value)


# ---- build_rain_washes.simplify (needs numpy + rasterio at import) ----------
washes = pytest.importorskip("build_rain_washes")


def test_simplify_keeps_only_corners():
    pts = [(0, 0), (1, 0), (2, 0), (3, 0), (3, 1), (3, 2)]
    assert washes.simplify(pts) == [(0, 0), (3, 0), (3, 2)]


def test_simplify_short_inputs_unchanged():
    assert washes.simplify([(0, 0)]) == [(0, 0)]
    assert washes.simplify([(0, 0), (1, 1)]) == [(0, 0), (1, 1)]


def test_simplify_does_not_collapse_small_degree_steps():
    # regression: old tolerance (|dx*dy| < 2.5 deg^2) dropped every interior point
    pts = [(-115.2, 36.1), (-115.199, 36.1), (-115.199, 36.101)]
    assert washes.simplify(pts) == pts
