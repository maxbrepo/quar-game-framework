# Quar Game Framework (QGF)

**Version 0.0.3-dev — Development Update | Experimental Channel**
Experimental 2D game framework developed primarily in **Visual Quar**.

QGF is a lightweight, modular 2D game framework using the external Visual Quar SDK and SDL3 for execution and native interoperability.

## Current development milestone: 0.0.3-dev

- Application/backend session coordination and native SDL3 lifecycle probes.
- Timing, integer pacing, scheduler and loop-state regression coverage.
- Configuration, window-state and logical input policies, including directional movement examples.
- Existing SDL3 graphical demos from earlier alpha milestones.

This is an experimental prerelease, not a stable engine. Native window and input integration remain incomplete at the public core level. See [version history](VERSIONS.md) for earlier milestones.

## Release channels

| Branch | Release stage |
| --- | --- |
| `experimental` | Development (`-dev`) |
| `unstable` | Alpha (`-alpha`) |
| `testing` | Beta / release candidate (`-beta`, `-rc`) |
| `stable` | Stable releases |

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

D001 exits on any key or window close. Smoke tests check execution, not visual correctness.

## Project structure

- `core/` — logical framework modules.
- `examples/` — numbered Visual Quar examples.
- `demos/` — interactive and smoke-test graphical demos.
- `tests/` — regression tests and test utilities.
- `experimental/` — development probes.
- `sdk/` — local external SDK dependency (not distributed with QGF).
- `main.py` — Main Runner.
- `VERSION.md` — current version and scope.
- `VERSIONS.md` — dated version history.
- `SCHEMATICS.md` — architecture and boundaries.

## Development policy

Visual Quar remains the primary implementation language; the SDK is a separately maintained dependency. New native integrations must preserve earlier functionality, avoid unapproved workarounds and distinguish candidate work from user-validated results.

## License

Quar Game Framework (QGF) is licensed under the **Apache License 2.0**. See [`LICENSE`](LICENSE) for the full license terms.

Third-party software, including Visual Quar / Quar SDK, Python, and SDL3, retains its own licensing terms. See [`THIRD_PARTY_LICENSES.md`](THIRD_PARTY_LICENSES.md) for dependency information.

Games and applications created using QGF may be distributed under licenses chosen by their authors, subject to any applicable third-party and runtime licensing requirements.
