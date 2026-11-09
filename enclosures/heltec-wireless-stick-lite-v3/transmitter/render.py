"""Renders print/preview.png: the assembled enclosure without the lid, with ghost parts.

Needs the FreeCAD GUI (freecadcmd cannot render). Usage, from the repository root:
    FreeCAD enclosures/heltec-wireless-stick-lite-v3/transmitter/render.py

On macOS, FreeCAD is at /Applications/FreeCAD.app/Contents/MacOS/FreeCAD. The window
closes by itself once the image is saved.
"""

import os
import sys
import time

import FreeCAD as App
import FreeCADGui as Gui

HERE = next(
    (os.path.dirname(os.path.abspath(a)) for a in sys.argv if a.endswith("render.py")),
    os.path.dirname(os.path.abspath(globals().get("__file__", "."))),
)
sys.path.insert(0, HERE)
import model  # noqa: E402  (needs the path above)



def settle(seconds=1.0):
    # Camera changes may be animated: let the GUI run them to the end before the next step
    end = time.monotonic() + seconds
    while time.monotonic() < end:
        Gui.updateGui()
        time.sleep(0.02)


doc, _ = model.build()
for name in ("Lid", "Usb_cover"):
    doc.getObject(name).ViewObject.Visibility = False
settle()
view = Gui.activeDocument().activeView()
view.viewIsometric()
settle()
view.fitAll()
settle()
view.saveImage(os.path.join(HERE, "print", "preview.png"), 1400, 1000, "#f7f7f7")
App.closeDocument(doc.Name)
# Leave without the save prompts of a regular GUI exit
os._exit(0)
