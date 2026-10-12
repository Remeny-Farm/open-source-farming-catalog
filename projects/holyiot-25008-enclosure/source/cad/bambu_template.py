# /// script
# requires-python = ">=3.11,<3.13"
# dependencies = []
# ///
"""Regenerate bambu/project_settings.json from Bambu Studio's own profiles.

    uv run --python 3.12 bambu_template.py

The template is the project config the Bambu Studio CLI exports for the
farm's printer, process and filament -- P1S 0.4 nozzle, 0.16mm Optimal, Bambu
PETG Basic in all four AMS slots -- with nothing of ours in it. Every setting
the cap projects change is in bambu_project, so the two can be reviewed apart. Rerun after a Bambu Studio update and diff.

Bambu's system profiles inherit from and include each other. Handed a system
profile file, the CLI resolves neither and silently falls back to libslic3r
defaults: `G28` as the whole start G-code, no AMS filament change,
single_extruder_multi_material 0, a 100 mm build height. Every project written
here before 2026-10-04 carried those defaults
(docs/lab/2026-10-04-cap-face-first-layer.md). This script resolves the chain
itself and hands the CLI complete user presets that name their system parent,
which is what its printer/process compatibility check asks for.

The CLI writes the per-filament arrays once per nozzle variant (Standard,
High Flow) and a few of them one entry wide. Bambu Studio counts a project's
filaments from those arrays (docs/lab/2026-09-29-cap-plate-filament-slots.md),
so they are normalised to one entry per AMS slot for the Standard nozzle: the
shape Bambu Studio itself exports for a four-filament P1S project.
"""

import json
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from bambu_project import APP, BODIES, TEMPLATE  # noqa: E402

PROFILES = APP.parents[1] / "Resources" / "profiles" / "BBL"
MACHINE = "Bambu Lab P1S 0.4 nozzle"
PROCESS = "0.16mm Optimal @BBL X1C"
FILAMENT = "Bambu PETG Basic @BBL X1C"
NOZZLE = "Direct Drive Standard"
SAMPLE = HERE / "out" / "coupon_cap.stl"    # any model will do; only the settings are kept


def resolve(kind: str, name: str) -> dict:
    """A system profile with its inherits chain and includes merged in."""
    d = json.loads((PROFILES / kind / f"{name}.json").read_text())
    out = resolve(kind, d["inherits"]) if "inherits" in d else {}
    for inc in d.get("include", []):
        out.update(resolve(kind, inc))
    out.update(d)
    for key in ("include", "instantiation"):
        out.pop(key, None)
    return out


def user_preset(kind: str, name: str) -> dict:
    return {**resolve(kind, name), "name": f"{name} (resolved)", "inherits": name, "from": "User"}


def export(workdir: Path) -> dict:
    paths = {}
    for kind, name in (("machine", MACHINE), ("process", PROCESS), ("filament", FILAMENT)):
        paths[kind] = workdir / f"{kind}.json"
        paths[kind].write_text(json.dumps(user_preset(kind, name)))
    r = subprocess.run([str(APP), "--debug", "2", "--load-settings", f"{paths['machine']};{paths['process']}",
                        "--load-filaments", ";".join([str(paths["filament"])] * len(BODIES)),
                        "--outputdir", str(workdir), "--export-3mf", "template.3mf", str(SAMPLE)],
                       capture_output=True, text=True)
    project = workdir / "template.3mf"
    if r.returncode or not project.exists():
        errors = [ln for ln in (r.stdout + r.stderr).splitlines() if "[error]" in ln]
        raise SystemExit(f"Bambu Studio CLI export failed (exit {r.returncode}): {errors[-3:]}")
    return json.loads(zipfile.ZipFile(project).read("Metadata/project_settings.config"))


def normalise(cfg: dict) -> dict:
    n = len(BODIES)
    variants = cfg["filament_extruder_variant"]
    keep = [i for i, v in enumerate(variants) if v == NOZZLE]
    if len(keep) != n:
        raise SystemExit(f"expected {n} '{NOZZLE}' entries in filament_extruder_variant, got {variants}")
    for key, value in cfg.items():
        if key == "flush_volumes_vector":       # two per filament, not one per nozzle variant
            continue
        if isinstance(value, list) and len(value) == len(variants) != n:
            cfg[key] = [value[i] for i in keep]
        elif key.startswith("filament_") and isinstance(value, list) and len(value) == 1:
            cfg[key] = value * n
    cfg["printer_settings_id"], cfg["print_settings_id"] = MACHINE, PROCESS
    cfg["filament_settings_id"] = [FILAMENT] * n
    cfg["inherits_group"] = [""] * len(cfg["inherits_group"])
    return cfg


def main() -> int:
    if not APP.exists():
        print(f"Bambu Studio not found at {APP}")
        return 1
    with tempfile.TemporaryDirectory() as tmp:
        cfg = normalise(export(Path(tmp)))
    # The two values the libslic3r fallback gets wrong; refuse to write it.
    if cfg["single_extruder_multi_material"] != "1" or "M620" not in cfg["change_filament_gcode"]:
        raise SystemExit("the export fell back to libslic3r defaults (no AMS filament change)")
    TEMPLATE.write_text(json.dumps(cfg, indent=1, sort_keys=True) + "\n")
    print(f"wrote {TEMPLATE.relative_to(HERE)}: {len(cfg)} keys, {MACHINE} / {PROCESS} / "
          f"{len(BODIES)} x {FILAMENT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
