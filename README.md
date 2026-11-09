# Cajuí Hardware

English | [Português brasileiro](README.pt-BR.md)

**3D-printable enclosures for Cajuí sensor transmitters, modelled as parametric FreeCAD
scripts.**

This repository is the hardware layer of [Cajuí](https://github.com/cajui/docs). The
transmitter firmware lives in [cajui-firmware](https://github.com/cajui/cajui-firmware).

| Enclosure | Board | Battery | Revision | Status |
| --- | --- | --- | --- | --- |
| [Wide](enclosures/wide/README.md) | Heltec Wireless Stick Lite V3 | One protected 18650 cell | `wide-r05` | Physical test pending |

**Experimental designs.** Each revision is checked in the model (closed meshes, no collisions
between the assembled parts), but fit is only known after printing. Water resistance has not
been tested: use the enclosures under cover.

## Layout

Each enclosure has its own folder:

- **`model.py`:** the parametric model, with every dimension in one dictionary.
- **`export.py`:** writes the STLs, already oriented for printing, and `verification.json`.
- **`render.py`:** writes the preview image; it needs the FreeCAD GUI.
- **`print/`:** the STLs to print and the preview image.
- **`revision.json`:** the revision, the SHA-256 of each STL and the known limits.
- **`README.md`:** what to print, the hardware, assembly and what to check.

STL file names are stable across revisions. Each revision is tagged as `<enclosure>-rNN`, for
example `wide-r05`.

## Requirements

[FreeCAD](https://www.freecad.org/) 1.1 to regenerate the parts. Tested with 1.1.4. Printing only
needs the STLs.

## License

[Apache License 2.0](LICENSE).
