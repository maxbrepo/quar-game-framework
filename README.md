# Quar Game Framework (QGF)

**Version 0.0.1 — 05 November 2026**  
Experimental 2D game framework developed primarily in **Visual Quar**.

QGF is a separate project from the Visual Quar / Quar SDK toolchain. Its goal is to build a lightweight game framework while using the SDK's execution and native interoperability capabilities, without modifying SDK sources from QGF.

## Milestone 0.0.1

- **275 numbered examples** across the 11 chapters of Marathon A (logical foundations), previously validated on the user's PC.
- **Main Runner** for example execution and graphical demo selection.
- **First native SDL3 demo, D001 Hello Pixels**, confirmed working on the user's PC: a window, a line and a point drawn via Visual Quar ABI/FFI.
- Marathon B underway to integrate additional native SDL3 capabilities.

**Important:** 0.0.1 is a symbolic early milestone, not a stable engine release. A working SDL3 demo does not imply that every logical subsystem has a complete native implementation.

## Requirements

- A compatible external Visual Quar SDK, including QRVM and ABI/FFI support.
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
- `VERSION.md` — current version and scope.
- `VERSIONS.md` — dated version history.
- `SCHEMATICS.md` — architecture and boundaries.

## Development policy

Visual Quar remains the primary implementation language; the SDK is a separately maintained dependency. New native integrations must preserve earlier functionality, avoid unapproved workarounds and distinguish candidate work from user-validated results.
