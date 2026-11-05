# QGF — Architecture Schematics (0.0.1)

## 1. Component boundaries

```text
QGF application / example / demo (Visual Quar)
                 |
                 v
      QGF core modules and APIs
                 |
                 v
        Visual Quar / QRVM
        (external Quar SDK)
                 |
          ABI / FFI boundary
                 |
                 v
        SDL3 shared library
                 |
                 v
     OS / display / input devices
```

The diagram shows the **intended layering**. In 0.0.1, D001 calls SDL3 functions directly through Visual Quar FFI; it does not yet demonstrate a fully abstracted QGF rendering API.

## 2. Repository responsibilities

| Area | Responsibility | State in 0.0.1 |
| --- | --- | --- |
| `core/` | Logical modules for framework systems | Experimental foundation |
| `examples/` | Numbered functional Visual Quar examples | 275 examples from Marathon A |
| `demos/` | Native graphical demonstration programs | D001 SDL3 Hello Pixels |
| `tests/` | Regression and smoke-test harnesses | Experimental tooling |
| `main.py` | Main Runner / selection and execution | Implemented for examples and demos |
| `docs/` | Notes, specifications and decisions | Evolving |
| Quar SDK | Compiler/frontend, QRVM and native FFI | **External dependency** |
| SDL3 | Native platform/rendering library | Initial direct FFI demonstration |

## 3. Marathon structure

**Marathon A — logical foundations:**

1. Core
2. Game Loop
3. Platform Layer
4. Window Manager
5. Input System
6. Math Library
7. Rendering 2D
8. Resource Manager
9. Scene System
10. Entity System
11. Collision 2D

**Marathon B — native SDL3 integration:** revisit chapters 1–10 to incrementally add real windows, graphics, input, sprites and interactive demos, without breaking the previously validated examples.

## 4. Graphical demo execution

```text
Main Runner
  |-- interactive: one demo -> continuous frame loop -> close/key exit
  `-- smoke: one/chapter/all demos -> bounded frames -> PASS/FAIL/SKIP
                                             |
                                             `-- SDL3 unavailable => SKIP
```

The D001 implementation currently exits on **any key**, including Escape, rather than exclusively on Escape. Smoke PASS means process-level success, not verified rendered pixels. SDL3 is required; there is no SDL2 fallback.

## 5. Architectural constraints

- Visual Quar is the primary source language.
- Keep SDK development and QGF development separate.
- Prefer canonical SDK ABI/FFI improvements to ad hoc QGF bridges.
- SDL3 is the chosen native backend, not the public game API.
- Preserve existing working examples and add features incrementally.
- Distinguish implemented, user-validated, and planned features.
