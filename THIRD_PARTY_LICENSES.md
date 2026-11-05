# Third-Party Licenses — Quar Game Framework (QGF)

This document records the main external dependencies identified in the QGF 0.0.1 README. It is a preliminary inventory, **not** a complete audit of all repository files, transitive dependencies, or packaged binaries.

QGF's original project code is licensed under Apache License 2.0; see `LICENSE`. Third-party components retain their own licenses.

| Component | License | Role in QGF | Distribution status |
| --- | --- | --- | --- |
| Visual Quar / Quar SDK | Apache License 2.0 (project's stated licensing policy; verify the SDK release used) | Separate external toolchain, QRVM and ABI/FFI support | External dependency; the README says SDK sources are not modified by QGF |
| Python 3 (CPython) | Python Software Foundation License (PSF License), with historical notices as applicable | Runs `main.py` and bootstrap tooling | Required interpreter; whether bundled in release packages is not yet verified |
| SDL3 | zlib License | Shared library for native graphical demos | External shared library according to README; bundling not verified |

## Official license information

- Visual Quar / Quar SDK: consult the exact `LICENSE` and third-party notices of the SDK version distributed or required.
- Python: https://docs.python.org/3/license.html
- SDL3: https://github.com/libsdl-org/SDL/blob/main/LICENSE.txt

## Distribution and compliance notes

1. Invoking or depending on an external tool does not, by itself, make that tool's license the license of QGF.
2. If a release bundles Python, SDL3, SDK files, or any other third-party material, preserve the required copyright notices, license texts, and any applicable attribution files in that distribution.
3. Inspect actual source imports, vendored files, binary packages, build scripts, and transitive dependencies before declaring this inventory complete.
4. QGF-generated games may use author-chosen licenses, but any runtime code or third-party assets actually included in those games must be reviewed separately.
5. GTK, PyGObject, GCC, and Clang are **not** listed as direct QGF requirements because the supplied QGF README does not establish that they are direct dependencies of QGF. They may be used by the separate SDK or development environment.

This file is informational and does not replace the official license text of any third-party component.
