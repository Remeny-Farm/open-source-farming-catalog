# /// script
# requires-python = ">=3.11,<3.13"
# dependencies = []
# ///
"""The plate writer: structure, determinism, and (when Bambu Studio is
installed) a real slice of a two-cube plate.

    uv run --python 3.12 test_bambu_project.py
"""
import hashlib
import json
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent   # the Bambu CLI needs an absolute --outputdir
sys.path.insert(0, str(HERE))
from bambu_project import (APP, filaments_used, first_layer_order, flush_floor, flush_volume,  # noqa: E402
                           grid_label, grid_positions, project_settings, write_plate)

PASS, FAIL = 0, []


def check(cond, label, detail=""):
    global PASS
    PASS += bool(cond)
    FAIL.extend([] if cond else [label])
    print(f"  [{'PASS' if cond else 'FAIL'}] {label}  {detail}")


def cube(s: float, z0: float = 0.0, x0: float = 0.0, y0: float = 0.0):
    v = [(x0 + x, y0 + y, z) for z in (z0, z0 + s) for y in (-s / 2, s / 2) for x in (-s / 2, s / 2)]
    t = [(0, 2, 1), (1, 2, 3), (4, 5, 6), (5, 7, 6), (0, 1, 4), (1, 5, 4),
         (2, 6, 3), (3, 6, 7), (0, 4, 2), (2, 4, 6), (1, 3, 5), (3, 7, 5)]
    return v, t


scheme = {"id": "classic", "base": {"hex": "#FFFFFF"}, "a": {"hex": "#4F2C1D"}, "b": {"hex": "#DBC8B6"}}
window = {"hex": "#E6EDF1"}
caps = [{"name": f"cap_{n}", "position": pos,
         "bodies": {"shell": cube(10.0), "window": cube(4.0, 0.0, 9.0), "a": cube(2.0, 0.0, -9.0),
                    "b": cube(1.5, 0.0, 0.0, 9.0)}}   # all four on the first layer, like a design face
        for n, pos in zip((1, 2), grid_positions(2))]
caps[1]["bodies"].pop("b")     # a design that leaves colour b unused
out = HERE / "out" / "test_plate.3mf"
write_plate(out, caps, scheme, window, "test-batch")
z = zipfile.ZipFile(out)
names = z.namelist()
check("3D/3dmodel.model" in names and "Metadata/model_settings.config" in names
      and "Metadata/project_settings.config" in names and "3D/Objects/object_2.model" in names,
      "package structure")
model = z.read("3D/3dmodel.model").decode()
check(model.count("<item ") == 2 and 'transform="1 0 0 0 1 0 0 0 1 38 38 0"' in model
      and 'transform="1 0 0 0 1 0 0 0 1 74 38 0"' in model, "two items on the grid")
ms = z.read("Metadata/model_settings.config").decode()
check(ms.count('<metadata key="extruder" value="1"/>') == 2
      and ms.count('<metadata key="extruder" value="2"/>') == 2
      and ms.count('<metadata key="extruder" value="3"/>') == 2
      and ms.count('<metadata key="extruder" value="4"/>') == 1, "extruders 1/2/3/4 per body, b optional")
cfg = json.loads(z.read("Metadata/project_settings.config"))
check(cfg["wall_loops"] == "3" and cfg["reduce_crossing_wall"] == "1" and cfg["wall_generator"] == "arachne"
      and len(cfg["filament_settings_id"]) == 4
      and cfg["printable_area"][2] == "256x256", "settings, four filaments, plate area")
# One entry per filament in every per-filament array, or Bambu Studio loads a
# single filament and prints every part from slot 1.
check(cfg["filament_colour"] == ["#FFFFFF", "#E6EDF1", "#4F2C1D", "#DBC8B6"]
      and cfg["filament_type"] == ["PETG"] * 4
      and all(len(v) == 4 for k, v in cfg.items() if k.startswith("filament_") and isinstance(v, list)),
      "scheme colours in slots 1-4, every per-filament array four wide")
check(cfg["curr_bed_type"] == "Textured PEI Plate" and cfg["layer_height"] == "0.16",
      "PETG-capable plate, 0.16 mm layers")
# The template is Bambu's own P1S, not libslic3r's default printer: that one
# starts with a bare G28 and never changes filament (2026-10-04).
check(cfg["single_extruder_multi_material"] == "1" and "M620" in cfg["change_filament_gcode"]
      and cfg["printable_height"] == "250" and cfg["printer_settings_id"] == "Bambu Lab P1S 0.4 nozzle",
      "the P1S machine profile, AMS filament change included")
check(len(cfg["flush_volumes_vector"]) == 8, "flush_volumes_vector two entries per filament",
      str(len(cfg["flush_volumes_vector"])))
check(cfg["initial_layer_print_height"] == "0.2" and cfg["initial_layer_line_width"] == "0.5"
      and cfg["initial_layer_flow_ratio"] == "1.05" and cfg["initial_layer_infill_speed"] == ["35", "35"]
      and cfg["bottom_surface_pattern"] == "monotonic" and cfg["elefant_foot_compensation"] == "0.15"
      and cfg["brim_type"] == "no_brim", "first-layer settings for the design face")
check(cfg["enable_prime_tower"] == "1" and cfg["wipe_tower_x"] == ["237.5"] and cfg["prime_tower_width"] == "14",
      "prime tower in the strip right of the grid")
# Bambu Studio's own purge volumes for the 2026-09-29 plate's colours (its
# G-code, every pair the GUI recalculated). The clear slot ran Generic PETG
# there, whose floor has no cutter retraction in it: 107 instead of 63.
gui = ["#FFFFFF", "#77EDD7", "#4F2C1D", "#DBC8B6"]
seen = {(0, 1): 179, (0, 2): 157, (0, 3): 123, (1, 0): 370, (1, 2): 253, (1, 3): 260,
        (2, 0): 563, (2, 1): 533, (3, 0): 263, (3, 1): 197}
got = {k: flush_volume(gui[k[0]], gui[k[1]], 107 if k[0] == 1 else 63) for k in seen}
check(got == seen, "purge volumes match Bambu Studio", "" if got == seen else str(got))
check([flush_floor(cfg, i) for i in range(4)] == [63] * 4, "purge floor 63 mm3 (PETG Basic, cutter retraction)")
m = [int(v) for v in cfg["flush_volumes_matrix"]]
check(m[2 * 4 + 0] == flush_volume("#4F2C1D", "#FFFFFF", 63) == 563 and m[0] == 0,
      "scheme colours drive the plate's purge matrix", f"brown -> white {m[8]} mm3")
check(cfg["first_layer_print_sequence"] == ["2", "1", "4", "3"]
      and first_layer_order(["#101010", "#E6EDF1", "#F5F5F5", "#808080"]) == [2, 3, 4, 1],
      "first layer: clear, then light to dark", str(cfg["first_layer_print_sequence"]))
h1 = hashlib.sha256(out.read_bytes()).hexdigest()
write_plate(out, caps, scheme, window, "test-batch")
check(hashlib.sha256(out.read_bytes()).hexdigest() == h1, "byte-identical on rerun", h1[:12])
check(grid_positions(36)[-1] == (218.0, 218.0) and len(grid_positions(36)) == 36, "36-cap grid")
check(grid_label((38.0, 38.0)) == "1A" and grid_label((218.0, 218.0)) == "6F", "grid labels 1A..6F")
sunk = [{**caps[0], "bodies": {**caps[0]["bodies"], "window": cube(4.0, -1.1)}}]
try:
    write_plate(HERE / "out" / "test_sunk.3mf", sunk, scheme, window, "test-batch")
    check(False, "a cap below the bed refused")
except SystemExit as e:
    check("not on the bed" in str(e), "a cap below the bed refused", str(e))
try:
    grid_positions(37)
    check(False, "37 caps refused")
except SystemExit:
    check(True, "37 caps refused")
if APP.exists():
    work = HERE / "out" / "slice_test"
    shutil.rmtree(work, ignore_errors=True)
    r = subprocess.run([str(APP), "--debug", "2", "--slice", "0", "--outputdir", str(work), str(out)],
                       capture_output=True, text=True)
    g = work / "plate_1.gcode"
    log = r.stdout + r.stderr
    ids = set(re.findall(r"; OBJECT_ID: (\d+)", g.read_text(errors="replace"))) if g.exists() else set()
    # "[error] [WARNING]: the parent path ... is not there, create it!" is
    # the CLI creating the output directory; every other [error] is real.
    errors = [ln for ln in log.splitlines() if "[error]" in ln and "[WARNING]" not in ln]
    check(g.exists() and not errors and len(ids) == 2,
          "Bambu Studio slices the plate with 2 objects",
          f"{len(ids)} object ids" if g.exists() and not errors else (errors[-1:] or [log[-300:]])[0][-200:])
    used = filaments_used(work / "result.json")
    check(used == {1, 2, 3, 4}, "every part prints from its own slot", f"filaments used: {sorted(used)}")
    text = g.read_text(errors="replace") if g.exists() else ""
    first = text.split("; CHANGE_LAYER")[1] if text.count("; CHANGE_LAYER") > 1 else ""
    loads = [int(n) + 1 for n in re.findall(r"^M620 S(\d+)A", text.split("; CHANGE_LAYER")[0] + first, re.M)]
    check(loads[:4] == [2, 1, 4, 3], "the AMS loads clear, white, beige, brown for the first layer", str(loads))
    # Tower lines: inside the tower block, outside the filament change it
    # wraps (M620 ... M621 purges into the chute and wipes off the plate).
    tower, x, y, in_tower, changing = [], 0.0, 0.0, False, False
    for ln in text.splitlines():
        if ln.startswith(("; WIPE_TOWER_START", "; WIPE_TOWER_END")):
            in_tower = ln.startswith("; WIPE_TOWER_START")
        elif ln.startswith(("M620 S", "M621 S")):
            changing = ln.startswith("M620")
        elif ln.startswith("G1 ") and not changing:
            mx, my, me = (re.search(rf"{a}([-\d.]+)", ln) for a in "XYE")
            nx, ny = float(mx.group(1)) if mx else x, float(my.group(1)) if my else y
            if in_tower and me and float(me.group(1)) > 0:
                tower += [(x, y), (nx, ny)]
            x, y = nx, ny
    xs, ys = [p[0] for p in tower], [p[1] for p in tower]
    check(tower and 234.5 < min(xs) and max(xs) < 254.5 and 0 < min(ys) and max(ys) < 256,
          "prime tower between the grid and the plate edge",
          f"x {min(xs):.1f}-{max(xs):.1f}, y {min(ys):.1f}-{max(ys):.1f}" if tower else "no tower")
    shutil.rmtree(work, ignore_errors=True)
else:
    print("  (Bambu Studio not installed; slice step skipped)")
out.unlink(missing_ok=True)
print(f"{PASS} passed, {len(FAIL)} failed" + (f": {FAIL}" if FAIL else ""))
sys.exit(1 if FAIL else 0)
