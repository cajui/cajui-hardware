"""Exports the enclosure STLs, already oriented for printing, and the verification report.

Usage, from the repository root:
    freecadcmd enclosures/heltec-wifi-lora-32-v3/receiver/export.py

On macOS, freecadcmd is at /Applications/FreeCAD.app/Contents/Resources/bin/freecadcmd.
"""

import hashlib
import json
import os
import sys

import FreeCAD as App
import Mesh
import MeshPart

HERE = next(
    (os.path.dirname(os.path.abspath(a)) for a in sys.argv if a.endswith("export.py")),
    os.path.dirname(os.path.abspath(globals().get("__file__", "."))),
)
sys.path.insert(0, HERE)
import model  # noqa: E402  (needs the path above)

REVISION = "r01"
OUTPUT = os.path.join(HERE, "print")
# Print orientation (axis and rotation from the assembly): body and carrier with the base
# on the bed; lid upside down, with the outer face on the bed
PARTS = {
    "body.stl": ("Body", None),
    "lid.stl": ("Lid", (App.Vector(1, 0, 0), 180)),
    "board-carrier.stl": ("Board_carrier", None),
}

os.makedirs(OUTPUT, exist_ok=True)
shapes, dimensions = model.geometry()
report = {"revision": REVISION, "envelope_mm": [round(v, 2) for v in dimensions["outer"]], "parts": {}}
for filename, (name, rotation) in PARTS.items():
    shape = shapes[name].copy()
    if rotation:
        shape.rotate(App.Vector(0, 0, 0), *rotation)
    bounds = shape.BoundBox
    shape.translate(App.Vector(-bounds.XMin, -bounds.YMin, -bounds.ZMin))
    mesh = MeshPart.meshFromShape(Shape=shape, LinearDeflection=0.02, AngularDeflection=0.0873, Relative=False)
    path = os.path.join(OUTPUT, filename)
    mesh.write(path)
    written = Mesh.Mesh(path)
    report["parts"][filename] = {
        "sha256": hashlib.sha256(open(path, "rb").read()).hexdigest(),
        "dimensions_mm": [round(v, 2) for v in (written.BoundBox.XLength, written.BoundBox.YLength, written.BoundBox.ZLength)],
        "volume_cm3": round(shape.Volume / 1000, 2),
        "closed_mesh": written.isSolid(),
        "non_manifold": written.hasNonManifolds(),
        "components": written.countComponents(),
        "facets": written.CountFacets,
    }

collisions = []
names = list(shapes)
for i, a in enumerate(names):
    for b in names[i + 1 :]:
        volume = shapes[a].common(shapes[b]).Volume
        if volume > 1e-6:
            collisions.append([a, b, round(volume, 3)])
report["assembly_collisions"] = collisions
with open(os.path.join(HERE, "verification.json"), "w") as f:
    json.dump(report, f, ensure_ascii=False, indent=2)
print(json.dumps(report, ensure_ascii=False, indent=2))
