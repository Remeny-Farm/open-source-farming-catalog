# /// script
# requires-python = ">=3.11,<3.13"
# dependencies = ["build123d"]
# ///
"""The slicer-log error filter: real errors fail, known notes do not.

    uv run --python 3.12 test_slicer_error_lines.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from slice_check import KNOWN_SLICER_NOTES, slicer_error_lines  # noqa: E402

PASS, FAIL = 0, []


def check(cond, label):
    global PASS
    PASS += bool(cond)
    FAIL.extend([] if cond else [label])
    print(f"  [{'PASS' if cond else 'FAIL'}] {label}")


# A real slice of cap serial 543 (batch 2026-11-01-eggshell-02) logged the
# note at [error] level between ordinary debug lines and still wrote the
# G-code; that plate is the reason the whitelist exists.
SAMPLE_NOTE = ("[2026-11-01 13:47:13.405484] [0x000000016cb93000] [error]   "
               "Reversing even wall line causes it to be printed CCW instead of CW!")

check(len(slicer_error_lines("")) == 0, "an empty log has no errors")
check(slicer_error_lines("[info] Generating walls...") == [], "info lines pass")
check(slicer_error_lines(SAMPLE_NOTE) == [], "the known Arachne wall note passes")
check(len(slicer_error_lines("[error]   Some other failure")) == 1,
      "an unknown [error] line fails")
check(len(slicer_error_lines("CRITICAL: something")) == 1, "CRITICAL fails")
check(len(slicer_error_lines("floating cantilever detected")) == 1,
      "a floating cantilever fails")
check(slicer_error_lines("[WARNING] no filament colors") == [],
      "the pre-existing [WARNING]/no-filament exclusions stay")
check(any("Reversing even wall line" in n for n in KNOWN_SLICER_NOTES),
      "the note text stays anchored in KNOWN_SLICER_NOTES")

print(f"\n{PASS} passed, {len(FAIL)} failed")
sys.exit(1 if FAIL else 0)
