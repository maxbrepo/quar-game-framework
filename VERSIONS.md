# QGF — Version History

## 0.0.2-dev — 17 November 2026

**Type:** Development prerelease (not an official stable release).

### Development scope

- Ongoing Marathon 2 native SDL3 integration and Game Loop work.
- Versioned graphical demos, runner improvements, and structural regression tests are present in the development tree.
- Chapter 2 Pass B has received positive user test feedback for its latest checkpoint; this does not certify the entire repository or all demos.
- Numeric interoperability issues and advanced event handling remain subject to further SDK integration and validation.

### Repository status and boundaries

- The working tree includes numerous uncommitted and untracked changes relative to the 0.0.1 Git baseline. Their authorship and correctness cannot be established from Git status alone.
- The Visual Quar SDK is an external dependency; QGF does not modify its sources as part of this version update.
- This prerelease version label does not imply a complete code audit or full native SDL3 regression pass.

## 0.0.1 — 05 November 2026

**Type:** Initial experimental milestone / symbolic first release.

### Confirmed accomplishments

- Marathon A established the first 11 logical chapters and 275 numbered Visual Quar examples, previously tested on the user's PC.
- A Main Runner was developed to execute examples and select graphical demos.
- Marathon B began native SDL3 support through the Visual Quar ABI/FFI mechanism.
- The first graphical demo, `d001_hello_pixels`, was confirmed successful by the user: an SDL3 window renders a line and a point.
- SDL3 was built and installed on the user's Ubuntu 24.04 machine; its shared library is detected by the system.

### Current boundaries

- The graphical demo is an initial proof of execution, not a complete rendering backend.
- More SDL3 features, game interaction, sprite handling and integration remain future work.
- QGF must not patch or silently fork Visual Quar SDK; required language/runtime features belong in the SDK project.
