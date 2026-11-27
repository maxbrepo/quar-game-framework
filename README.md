# Quar Game Framework (QGF)

**Current version: 0.0.2-alpha (alpha prerelease)**  
Experimental 2D game framework developed primarily in **Visual Quar**.

QGF is a separate project from the Visual Quar / Quar SDK toolchain. Its goal is to build a lightweight game framework while using the SDK's execution and native interoperability capabilities, without modifying SDK sources from QGF.

## Current version: 0.0.2-alpha (alpha prerelease)

**This README describes QGF 0.0.2-alpha.** This is the current alpha version, **not** the historical 0.0.1-alpha release and **not** a stable engine release.

### Current scope

- The logical framework foundation and numbered examples established during Marathon A remain part of the project.
- The Main Runner supports selecting and running examples and SDL3 graphical demos.
- Native SDL3 demonstrations use Visual Quar through the SDK's QRVM and ABI/FFI pipeline.
- Marathon 2, Pass B is integrating and validating native SDL3 behavior chapter by chapter. Chapter 2 (Game Loop) has undergone work on frame pacing, loop states, independent simulation/rendering and controlled termination.

### Validation and limitations

- Individual Chapter 2 demos and checkpoints have received positive tests on the user's PC; this does **not** establish a complete regression pass for all of QGF 0.0.2-alpha.
- FPS reporting and some numerical behavior remain subject to limitations in the current Visual Quar typed SDK.
- Advanced keyboard/event handling is deferred. Some native integrations remain experimental or incomplete.
- QGF depends on an external Visual Quar SDK and does not maintain a modified private SDK implementation.

## Requirements and SDK installation

- **Quar SDK 0.0.5-dev**: obtain it separately and place its contents in the project-root `sdk/` directory. Place the SDK files and directories directly inside `sdk/`, without an additional nested `quar-sdk/` directory.
- The SDK must include QRVM and ABI/FFI support. It is an external dependency and is **not distributed or tracked in the QGF repository**.
- Python 3 for the current Main Runner / SDK bootstrap tooling.
- SDL3 shared library for native graphical demos.
- A graphical desktop session to display windows.

SDL2 and SDL3 are separate libraries; graphical D001 requires SDL3.

## Usage

From the project root:

```bash
python3 main.py
```

Graphical demo commands (where supported by the current Main Runner):

```bash
python3 main.py --list-demos
python3 main.py --demo d001_hello_pixels
python3 main.py --demo-smoke d001_hello_pixels
python3 main.py --demo-chapter 1
python3 main.py --demo-all
```

If SDL3 is installed but not discovered automatically:

```bash
export QGF_SDL3_LIBRARY=/usr/local/lib/libSDL3.so.0
```

The D001 interactive demo currently exits when any key is pressed or the window is closed. The bounded smoke mode checks execution and completion, not the visual correctness of pixels.

## Project structure

- `core/` — logical framework modules.
- `examples/` — numbered Visual Quar examples.
- `demos/` — interactive and smoke-test graphical demos.
- `tests/` — regression tests and test utilities.
- `docs/` — development notes.
- `main.py` — Main Runner.
- `sdk/` — locally installed Quar SDK 0.0.5-dev (excluded from Git).
- `VERSION.md` — current version and scope.
- `VERSIONS.md` — dated version history.
- `SCHEMATICS.md` — architecture and boundaries.

## Version history

This README documents **only QGF 0.0.2-alpha**. See `VERSIONS.md` for historical releases, including 0.0.1-alpha, and `VERSION.md` for the current version declaration.

## Development policy

Visual Quar remains the primary implementation language; the SDK is a separately maintained dependency. New native integrations must preserve earlier functionality, avoid unapproved workarounds and distinguish candidate work from user-validated results.

## License

Quar Game Framework (QGF) is licensed under the **Apache License 2.0**. See [`LICENSE`](LICENSE) for the full license terms.

Third-party software, including Visual Quar / Quar SDK, Python, and SDL3, retains its own licensing terms. See [`THIRD_PARTY_LICENSES.md`](THIRD_PARTY_LICENSES.md) for dependency information.

Games and applications created using QGF may be distributed under licenses chosen by their authors, subject to any applicable third-party and runtime licensing requirements.
