# /// script
# requires-python = ">=3.11,<3.13"
# dependencies = []
# ///
"""Bambu Studio project (3MF) writer with no dependency on the Bambu CLI.

Mirrors the package the CLI writes (see out/cap_67_P1S.3mf): one assembly
object per cap in 3D/3dmodel.model, its mesh bodies (up to four) in
3D/Objects/object_<k>.model, per-part extruders in
Metadata/model_settings.config, and a full project_settings.config: Bambu's
own P1S 0.4 / 0.16mm Optimal / PETG Basic x 4 export from
bambu/project_settings.json (bambu_template.py regenerates it), the farm's
deviations in PRINT_SETTINGS, the scheme's colours in AMS slots 1-4, and the
purge volumes and first-layer colour order those colours call for.

Deterministic: fixed zip timestamps, uuid5 ids, sorted keys -- the same batch
produces a byte-identical plate.
"""

import colorsys
import json
import math
import re
import struct
import uuid
import zipfile
import zlib
from pathlib import Path

HERE = Path(__file__).parent
APP = Path("/Applications/BambuStudio.app/Contents/MacOS/BambuStudio")
TEMPLATE = HERE / "bambu" / "project_settings.json"
P1S_PRINTABLE_AREA = ["0x0", "256x0", "256x256", "0x256"]
P1S_EXCLUDE = ["0x0", "18x0", "18x28", "0x28"]
PLATE_MAX = 36
GRID_ORIGIN = 38.0      # first cap centre, both axes: clear of the 18 x 28 exclusion
GRID_PITCH = 36.0       # 31.94 mm cap + 4 mm
GRID_COLS = 6
STAMP = (2026, 1, 1, 0, 0, 0)
NS = uuid.UUID("6f1c2b7e-9c1e-4b2a-8f0e-2d5f7a1c3e44")
XML_HEAD = '<?xml version="1.0" encoding="UTF-8"?>\n'
MODEL_NS = ('xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02" '
            'xmlns:BambuStudio="http://schemas.bambulab.com/package/2021" '
            'xmlns:p="http://schemas.microsoft.com/3dmanufacturing/production/2015/06" '
            'requiredextensions="p"')
# AMS slots: 1 base colour (the shell), 2 clear (the LED window), 3 and 4 the
# scheme's two free colours; a cap without a colour simply omits that body.
BODY_EXTRUDER = {"shell": 1, "window": 2, "a": 3, "b": 4}
BODIES = tuple(BODY_EXTRUDER)
# Bambu Studio decides whether a package is its own project from this
# metadata. Anything else is loaded as a "3mf from other vendor": project
# settings are ignored, the plate defaults to 200 x 200 and every cap beyond
# that is silently dropped (observed: 26 of 36 sliced). The version is the
# one the settings template in bambu/ was exported from.
BAMBU_APPLICATION = "BambuStudio-02.08.02.60"
# Where this generator departs from Bambu's profiles, and the few Bambu values
# the cap face depends on, pinned so a template refresh cannot move them. A
# list-valued setting takes the value for every entry.
PRINT_SETTINGS = {
    # the bayonet (DESIGN.md)
    "wall_loops": "3", "wall_generator": "arachne", "reduce_crossing_wall": "1",
    # Textured PEI: the P1S start G-code lowers the nozzle 0.04 mm for it,
    # which fuses the face's short wall loops, and the texture gives an even
    # matte face. The smooth Engineering Plate printed them rope-like
    # (docs/lab/2026-10-12-cap-plate-engineering-plate.md).
    "curr_bed_type": "Textured PEI Plate",
    # The design face is the first layer and prints against the textured
    # plate (docs/lab/2026-10-04-cap-face-first-layer.md).
    "initial_layer_print_height": "0.2",    # pinned; the GUI print ran 0.12
    "initial_layer_line_width": "0.5",      # pinned
    "initial_layer_flow_ratio": "1.05",     # PETG Basic's 0.95 back to 1.0 on the face
    "initial_layer_speed": "30",
    "initial_layer_infill_speed": "35",
    "bottom_surface_pattern": "monotonic",  # pinned
    "elefant_foot_compensation": "0.15",    # pinned
    "brim_type": "no_brim",                 # a brim would bond to the face's edge
    # Prime tower in the 22 mm strip right of the grid (the last column of
    # caps ends at x 233.97): 14 mm plus a 1 mm brim keeps every tower line
    # inside x 236-253. Colour changes stop at the top of the 1.1 mm top
    # plate, so the tower is about seven layers tall.
    "enable_prime_tower": "1", "prime_tower_width": "14", "prime_tower_brim_width": "1",
    "prime_tower_rib_wall": "0", "wipe_tower_x": "237.5", "wipe_tower_y": "60",
}
# Bambu Studio's cap on a single purge, mm3 (libslic3r/FlushVolCalc.cpp).
FLUSH_MAX = 900


def grid_positions(n: int) -> list[tuple[float, float]]:
    """Row-major centres for n caps, front row first."""
    if not 1 <= n <= PLATE_MAX:
        raise SystemExit(f"a plate holds 1..{PLATE_MAX} caps, got {n}")
    return [(GRID_ORIGIN + GRID_PITCH * (i % GRID_COLS), GRID_ORIGIN + GRID_PITCH * (i // GRID_COLS))
            for i in range(n)]


def grid_label(pos: tuple[float, float]) -> str:
    """'1A'..'6F': column number, row letter, for the manifest."""
    col = int(round((pos[0] - GRID_ORIGIN) / GRID_PITCH)) + 1
    row = int(round((pos[1] - GRID_ORIGIN) / GRID_PITCH))
    return f"{col}{chr(65 + row)}"


def filaments_used(result_json: Path) -> set[int]:
    """Slots the Bambu CLI actually extruded from, read from the result.json
    it writes next to the G-code. A plate whose parts all collapsed to slot 1
    slices without a warning; this is the only place that shows it."""
    if not result_json.exists():
        return set()
    plates = json.loads(result_json.read_text()).get("sliced_plates") or [{}]
    return {int(f["id"]) for f in plates[0].get("filaments", []) if f.get("total_used_g", 0) > 0}


def assigned_slots(plate: Path) -> set[int]:
    """Slots the plate's parts are assigned to in model_settings.config."""
    with zipfile.ZipFile(plate) as z:
        settings = z.read("Metadata/model_settings.config").decode()
    return {int(s) for s in re.findall(r'<metadata key="extruder" value="(\d+)"/>', settings)}


def project_settings(scheme: dict, window: dict) -> dict:
    """The project_settings.config for a cap project: the template with the
    P1S bed, the scheme's colours in AMS slots 1-4 (base, clear, a, b),
    PRINT_SETTINGS, and the purge volumes and first-layer order for those
    colours. Shared by the batch plate and the single-cap project so both
    open with four filaments."""
    cfg = json.loads(TEMPLATE.read_text())
    cfg["printable_area"], cfg["bed_exclude_area"] = P1S_PRINTABLE_AREA, P1S_EXCLUDE
    # Bambu Studio counts the project's filaments from the per-filament
    # arrays, not from filament_settings_id. With one filament_colour entry
    # it loads a single filament and moves every part to slot 1, in the GUI
    # and the CLI alike, whatever model_settings says. The template therefore
    # carries every per-filament array four entries wide (widening only some
    # of them is what broke the CLI export on 2026-09-14); only the colours
    # change per scheme. See docs/lab/2026-09-29-cap-plate-filament-slots.md.
    colours = [scheme["base"]["hex"], window["hex"], scheme["a"]["hex"], scheme["b"]["hex"]]
    for key, value in cfg.items():
        if key.startswith("filament_") and isinstance(value, list) and len(value) != len(BODIES):
            raise SystemExit(f"template {TEMPLATE.name}: {key} has {len(value)} entries, "
                             f"expected {len(BODIES)}")
    cfg["filament_colour"] = colours
    for key, value in PRINT_SETTINGS.items():
        if key not in cfg:
            raise SystemExit(f"template {TEMPLATE.name} has no setting {key!r}")
        cfg[key] = [value] * len(cfg[key]) if isinstance(cfg[key], list) else value
    cfg["flush_volumes_matrix"] = [str(v) for row in flush_matrix(colours, cfg) for v in row]
    cfg["first_layer_print_sequence"] = [str(s) for s in first_layer_order(colours)]
    return cfg


def _luminance(rgb: tuple[float, float, float]) -> float:
    r, g, b = rgb
    return r * 0.3 + g * 0.59 + b * 0.11


def _rgb(hex_colour: str) -> tuple[float, float, float]:
    h = hex_colour.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def flush_floor(cfg: dict, slot: int) -> int:
    """The smallest purge Bambu Studio allows after `slot` (0-based), mm3: the
    nozzle volume less the filament the cutter retraction already pulled out
    (Plater.cpp get_min_flush_volumes). 107 - 18 mm of 1.75 mm filament = 63
    for PETG Basic on the P1S."""
    level = int(cfg["enable_long_retraction_when_cut"])        # 2 = per filament
    retract = 0
    if level and cfg["long_retractions_when_cut"][0] == "1":
        retract = int(float(cfg["retraction_distances_when_cut"][0]))
    if cfg["filament_long_retractions_when_cut"][slot] == "0":
        retract = 0
    elif level == 2:
        retract = int(float(cfg["filament_retraction_distances_when_cut"][slot]))
    return int(int(float(cfg["nozzle_volume"][0])) - math.pi * 1.75 * 1.75 / 4 * retract)


def flush_volume(src: str, dst: str, floor: int) -> int:
    """Purge for a change from colour src to dst, mm3, as Bambu Studio 02.08
    computes it from the two colours (libslic3r/FlushVolCalc.cpp): hue and
    saturation distance and the luminance step, a step towards light costing
    far more than one towards dark, plus the floor. It reproduces every pair
    Bambu Studio recalculated for the 2026-09-29 plate."""
    s, d = _rgb(src), _rgb(dst)
    (h1, s1, v1), (h2, s2, v2) = colorsys.rgb_to_hsv(*s), colorsys.rgb_to_hsv(*d)
    h1, h2 = 2 * math.pi * h1, 2 * math.pi * h2
    hs = min(1.2, math.hypot(math.cos(h1) * s1 * v1 - math.cos(h2) * s2 * v2,
                             math.sin(h1) * s1 * v1 - math.sin(h2) * s2 * v2))
    l_src, l_dst = _luminance(s), _luminance(d)
    if l_dst >= l_src:
        lumi = (l_dst - l_src) ** 0.7 * 560
    else:
        lumi = (l_src - l_dst) * 80
        hs = min(0.67 * v2 + 0.33 * v1, hs)
    a, b = 230 * hs, lumi
    predicted = max(math.sqrt(a * a + b * b + a * b), 60.0)     # third side, 120 deg apart
    return min(int(int(predicted) + floor), FLUSH_MAX)


def flush_matrix(colours: list[str], cfg: dict) -> list[list[int]]:
    """Row = from slot, column = to slot, as Bambu stores flush_volumes_matrix."""
    return [[0 if i == j else flush_volume(a, b, flush_floor(cfg, i)) for j, b in enumerate(colours)]
            for i, a in enumerate(colours)]


def first_layer_order(colours: list[str]) -> list[int]:
    """AMS slots (1-based) for the first layer, the design face: the clear
    window first, then lightest to darkest, so no change on the face goes from
    a dark colour to a lighter one."""
    clear = BODY_EXTRUDER["window"] - 1
    rest = sorted((i for i in range(len(colours)) if i != clear),
                  key=lambda i: (-_luminance(_rgb(colours[i])), i))
    return [clear + 1] + [i + 1 for i in rest]


def _uid(*parts: str) -> str:
    return str(uuid.uuid5(NS, ":".join(parts)))


def _png_1x1() -> bytes:
    def chunk(tag: bytes, data: bytes) -> bytes:
        return (struct.pack(">I", len(data)) + tag + data
                + struct.pack(">I", zlib.crc32(tag + data) & 0xffffffff))
    return (b"\x89PNG\r\n\x1a\n"
            + chunk(b"IHDR", struct.pack(">IIBBBBB", 1, 1, 8, 2, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(b"\x00\xe9\xee\xf2"))
            + chunk(b"IEND", b""))


def _mesh_xml(oid: int, name: str, verts, tris) -> str:
    vx = "".join(f'<vertex x="{x:.4f}" y="{y:.4f}" z="{z:.4f}"/>' for x, y, z in verts)
    tx = "".join(f'<triangle v1="{a}" v2="{b}" v3="{c}"/>' for a, b, c in tris)
    return (f'<object id="{oid}" p:UUID="{_uid("mesh", name)}" type="model">'
            f'<mesh><vertices>{vx}</vertices><triangles>{tx}</triangles></mesh></object>')


def write_plate(path: Path, caps: list[dict], scheme: dict, window: dict, batch_id: str) -> None:
    """caps: [{"name", "position": (x, y), "bodies": {"shell"|"window"|"a"|"b": (verts, tris)}}]
    (a and b may be absent when a design leaves that colour unused)
    scheme: the catalog scheme ({"base"|"a"|"b": {"hex"}}); window: the
    catalog's clear filament ({"hex"}). Their colours go to AMS slots 1-4.
    Meshes are in world coordinates: cap bottom at z 0, centred on the xy
    origin, already in print orientation; the build item moves each cap to
    its plate position."""
    if len(caps) > PLATE_MAX:
        raise SystemExit(f"{len(caps)} caps exceed the plate ({PLATE_MAX})")
    # Every cap must stand on the bed on its own. Bambu Studio drops each
    # object to the bed, which hides a sunken cap until the plate is sliced
    # as one object; then the other caps start in the air (2026-09-30).
    for cap in caps:
        low = min(v[2] for verts, _ in cap["bodies"].values() for v in verts)
        if abs(low) > 1e-6:
            raise SystemExit(f"{cap['name']}: lowest point at z {low:.3f} mm, not on the bed")
    entries: list[tuple[str, bytes]] = []
    assemblies, items, settings_objects, instances = [], [], [], []
    for k, cap in enumerate(caps):
        base = 5 * k
        meshes, comps, parts = [], [], []
        for bi, body in enumerate(BODIES):
            if body not in cap["bodies"]:
                continue
            oid = base + 1 + bi
            verts, tris = cap["bodies"][body]
            meshes.append(_mesh_xml(oid, f'{cap["name"]}:{body}', verts, tris))
            comps.append(f'<component p:path="/3D/Objects/object_{k + 1}.model" objectid="{oid}" '
                         f'p:UUID="{_uid("comp", cap["name"], body)}" transform="1 0 0 0 1 0 0 0 1 0 0 0"/>')
            parts.append(f'<part id="{oid}" subtype="normal_part" uuid="{_uid("part", cap["name"], body)}">'
                         f'<metadata key="name" value="{cap["name"]}_{body}"/>'
                         f'<metadata key="matrix" value="1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1"/>'
                         f'<metadata key="extruder" value="{BODY_EXTRUDER[body]}"/></part>')
        entries.append((f"3D/Objects/object_{k + 1}.model",
                        (XML_HEAD + f'<model unit="millimeter" xml:lang="en-US" {MODEL_NS}>'
                         '<metadata name="BambuStudio:3mfVersion">1</metadata>'
                         f'<resources>{"".join(meshes)}</resources><build/></model>').encode()))
        aid = base + 5
        x, y = cap["position"]
        assemblies.append(f'<object id="{aid}" p:UUID="{_uid("asm", cap["name"])}" type="model">'
                          f'<components>{"".join(comps)}</components></object>')
        items.append(f'<item objectid="{aid}" p:UUID="{_uid("item", cap["name"])}" '
                     f'transform="1 0 0 0 1 0 0 0 1 {x:g} {y:g} 0" printable="1"/>')
        settings_objects.append(f'<object id="{aid}"><metadata key="name" value="{cap["name"]}"/>'
                                f'{"".join(parts)}</object>')
        instances.append(f'<model_instance><metadata key="object_id" value="{aid}"/>'
                         f'<metadata key="instance_id" value="0"/>'
                         f'<metadata key="identify_id" value="{100 + k}"/></model_instance>')
    model = (XML_HEAD + f'<model unit="millimeter" xml:lang="en-US" {MODEL_NS}>'
             f'<metadata name="Application">{BAMBU_APPLICATION}</metadata>'
             '<metadata name="BambuStudio:3mfVersion">1</metadata>'
             f'<metadata name="Title">{batch_id}</metadata>'
             f'<resources>{"".join(assemblies)}</resources>'
             f'<build p:UUID="{_uid("build", batch_id)}">{"".join(items)}</build></model>')
    model_settings = (
        XML_HEAD + '<config>' + "".join(settings_objects)
        + '<plate><metadata key="plater_id" value="1"/><metadata key="plater_name" value=""/>'
        '<metadata key="locked" value="false"/><metadata key="filament_map_mode" value="Auto For Flush"/>'
        '<metadata key="gcode_file" value=""/><metadata key="thumbnail_file" value="Metadata/plate_1.png"/>'
        '<metadata key="thumbnail_no_light_file" value="Metadata/plate_no_light_1.png"/>'
        '<metadata key="top_file" value="Metadata/top_1.png"/><metadata key="pick_file" value="Metadata/pick_1.png"/>'
        + "".join(instances) + '</plate><assemble></assemble></config>')
    cfg = project_settings(scheme, window)
    ctypes = (XML_HEAD + '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
              '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
              '<Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/>'
              '<Default Extension="png" ContentType="image/png"/></Types>')
    rels = (XML_HEAD + '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Target="/3D/3dmodel.model" Id="rel-1" '
            'Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/>'
            '<Relationship Target="/Metadata/plate_1.png" Id="rel-2" '
            'Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/thumbnail"/>'
            '</Relationships>')
    model_rels = (XML_HEAD + '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                  + "".join(f'<Relationship Target="/3D/Objects/object_{k + 1}.model" Id="rel-{k + 1}" '
                            'Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/>'
                            for k in range(len(caps)))
                  + '</Relationships>')
    slice_info = (XML_HEAD + '<config><header><header_item key="X-BBL-Client-Type" value="slicer"/>'
                  '</header></config>')
    png = _png_1x1()
    head = [("[Content_Types].xml", ctypes.encode()), ("_rels/.rels", rels.encode()),
            ("3D/3dmodel.model", model.encode()), ("3D/_rels/3dmodel.model.rels", model_rels.encode())]
    tail = [("Metadata/project_settings.config", json.dumps(cfg, indent=4, sort_keys=True).encode()),
            ("Metadata/model_settings.config", model_settings.encode()),
            ("Metadata/slice_info.config", slice_info.encode()),
            ("Metadata/plate_1.png", png), ("Metadata/plate_no_light_1.png", png),
            ("Metadata/top_1.png", png), ("Metadata/pick_1.png", png)]
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for name, payload in head + entries + tail:
            info = zipfile.ZipInfo(name, date_time=STAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, payload)
