# /// script
# requires-python = ">=3.11,<3.13"
# dependencies = []
# ///
"""validate_batch refuses malformed hen-cap-batch/1 files, never crashes.

    uv run --python 3.12 test_cap_batch_validate.py

Deep copies of fixtures/batch_sample.json, one mutation each: a malformed
batch must come back with an error listing it, never with a traceback and
never with a silent []. Imports no build123d (validate_batch and
load_catalog are plain-stdlib modules), unlike test_cap_batch.py.
"""
import copy
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FIX = HERE / "fixtures" / "batch_sample.json"
PASS, FAIL = 0, []

sys.path.insert(0, str(HERE))
from cap_batch import validate_batch  # noqa: E402
from cap_design import load_catalog  # noqa: E402

CAT = load_catalog()


def check(cond, label, detail=""):
    global PASS
    PASS += bool(cond)
    FAIL.extend([] if cond else [label])
    print(f"  [{'PASS' if cond else 'FAIL'}] {label}  {detail}")


def run(mutate):
    """(errors, exception) for one mutated deep copy of the fixture."""
    b = copy.deepcopy(json.loads(FIX.read_text()))
    mutate(b)
    try:
        return validate_batch(b, CAT), None
    except Exception as e:  # the contract is to refuse, not to crash
        return [], e


def refused(label, mutate, needle):
    errs, exc = run(mutate)
    check(exc is None and any(needle in e for e in errs), f"refuse {label}",
          f"raised {type(exc).__name__}: {exc}" if exc else str(errs))


def caps_object(b):
    b["caps"] = {"a": 1}


def cap_string(b):
    b["caps"][1] = "x"


def colours_string(b):
    b["caps"][0]["colours"] = "base"


def serial_list(b):
    b["caps"][0]["serial"] = [1]


def duplicate_serial(b):
    b["caps"][1]["serial"] = 67


print("=== fixture ===")
errs, exc = run(lambda b: None)
check(exc is None and errs == [], "unchanged fixture validates", str(errs))

print("=== batch_id ===")
for label, mutate in [
    ("missing", lambda b: b.pop("batch_id")),
    ("parent path", lambda b: b.update(batch_id="../x")),
    ("slash", lambda b: b.update(batch_id="a/b")),
    ("xml specials", lambda b: b.update(batch_id="a&b<c")),
    ("empty", lambda b: b.update(batch_id="")),
    ("number", lambda b: b.update(batch_id=123)),
]:
    refused(f"batch_id {label}", mutate, "batch_id")

print("=== caps ===")
errs, exc = run(caps_object)
check(exc is None and errs == ["caps must be a list"],
      "caps object gives exactly one error", str(errs))

print("=== cap items ===")
refused("a cap that is not an object", cap_string, "must be an object")

print("=== cap fields ===")
refused("colours as a string", colours_string, "colours must be an object")
refused("serial as a list", serial_list, "serial must be an integer")

print("=== regression ===")
refused("duplicate serial", duplicate_serial, "duplicate serial")

print(f"{PASS} passed, {len(FAIL)} failed" + (f": {FAIL}" if FAIL else ""))
sys.exit(1 if FAIL else 0)
