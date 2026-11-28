# QGF — Architecture Schematics (0.0.3-dev)

**Status:** Experimental development update

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

| Area | Responsibility | State in 0.0.3-dev |
| --- | --- | --- |
| `core/` | Logical modules for framework systems | Logical foundations and native session coordination |
| `examples/` | Numbered functional Visual Quar examples | 275 examples from Marathon A |
| `demos/` | Native graphical demonstration programs | D001 and expanded SDL3/game-loop demos |
| `tests/` | Regression and smoke-test harnesses | Experimental tooling |
| `main.py` | Main Runner / selection and execution | Implemented for examples and demos |
| `docs/` | Notes, specifications and decisions | Evolving |
| Quar SDK | Compiler/frontend, QRVM and native FFI | **External dependency** |
| SDL3 | Native platform/rendering library | Direct FFI demos and lifecycle probes |

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

## 6. Application and backend lifecycle

```text
Application
    |
Session coordination
    |
Platform / backend contract
    |
SDL3 session
    +-- Initialization
    +-- Execution
    +-- Shutdown
    +-- Error recovery / restart
```

Development probes cover guarded transitions, session coordination and native lifecycle boundaries. This is not a claim of complete public backend integration.

## 7. Game loop and timing

```text
Application session
    |
Game loop
    +-- Time measurement / delta time
    +-- Fixed timestep
    +-- Integer frame pacing
    +-- Scheduler and loop states
    +-- Update / render separation
```

Regression coverage includes pause handling, persistent sessions and scheduler transitions.

## 8. Window and input policies

```text
Platform abstraction (intended native integration)
    +-- Window manager
    |   +-- Configuration
    |   +-- State and lifecycle
    +-- Input system
        +-- Logical actions
        +-- Axes
        +-- Directional movement
```

Logical policies and examples have been extended. Complete public native window and input integration remains under development.

## 9. Development and validation boundaries

The 0.0.3-dev update expands core, game loop, platform, window and input development. Native demos may still call SDL3 directly through SDK FFI. Experimental probes and regression test inventories do not establish exhaustive user validation. Public rendering abstractions and further graphical systems require additional development.

Quar SDK remains external; missing SDK capabilities should be addressed in the SDK project rather than duplicated in QGF.
