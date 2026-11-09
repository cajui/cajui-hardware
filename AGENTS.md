# Development of Cajuí Hardware

- Keep code, comments, technical documentation and commit messages in English. Keep each
  `README.md` and its `README.pt-BR.md` equivalent; the latter uses Brazilian Portuguese.
- Change geometry only in `model.py`. STLs, `verification.json` and `preview.png` are
  generated: regenerate them with `export.py` and `render.py`, never edit them by hand.
- After exporting, every part must be a closed mesh, without non-manifold edges, in a single
  component, and `assembly_collisions` must be empty. Parts that did not change keep their
  SHA-256.
- Every geometry change is a new revision:
  - bump `REVISION` in `export.py`;
  - update `revision.json` (description, hashes, `same_as`, limits);
  - in both READMEs, update the revision history and the parts to reprint;
  - tag the commit `<enclosure>-rNN`.

  Never move an existing tag. Keep STL file names stable.
- Do not describe a fit as validated until a print has confirmed it. Mark estimates and
  unmeasured values in comments and in the `limits` of `revision.json`.
- Never commit personal data, device identifiers or local machine paths.
- Run `uvx ruff@0.16.10 check .` before submitting.
- Use conventional commits.
