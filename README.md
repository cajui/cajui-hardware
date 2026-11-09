# Cajuí Hardware

English | [Português brasileiro](README.pt-BR.md)

**3D-printable enclosures for Cajuí sensor transmitters, modelled as parametric FreeCAD
scripts.**

This repository is the hardware layer of [Cajuí](https://github.com/cajui/docs). The
transmitter firmware lives in [cajui-firmware](https://github.com/cajui/cajui-firmware).

| Board | Function | Battery | Revision | Status |
| --- | --- | --- | --- | --- |
| Heltec Wireless Stick Lite V3 | [Transmitter](enclosures/heltec-wireless-stick-lite-v3/transmitter/README.md) | One protected 18650 cell | `r05` | Physical test pending |

**Experimental designs.** Each revision is checked in the model (closed meshes, no collisions
between the assembled parts), but fit is only known after printing. Water resistance has not
been tested: use the enclosures under cover.

## Layout

Enclosures are organised by board, then by function: `enclosures/<board>/<function>/`. Board
folder names match the board profiles of cajui-firmware, with hyphens instead of underscores.
Each enclosure folder holds:

- **`model.py`:** the parametric model, with every dimension in one dictionary.
- **`export.py`:** writes the STLs, already oriented for printing, and `verification.json`.
- **`render.py`:** writes the preview image; it needs the FreeCAD GUI.
- **`print/`:** the STLs to print and the preview image.
- **`revision.json`:** the revision, the SHA-256 of each STL and the known limits.
- **`README.md`:** what to print, the hardware, assembly and what to check.

STL file names are stable across revisions. Each revision is tagged as
`<board>/<function>/rNN`, for example `heltec-wireless-stick-lite-v3/transmitter/r05`.

## Requirements

[FreeCAD](https://www.freecad.org/) 1.1 to regenerate the parts. Tested with 1.1.4. Printing only
needs the STLs.

## License

[Apache License 2.0](LICENSE).
