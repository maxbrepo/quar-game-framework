"""Minimal host-side QGF lifecycle prototype.

This Python bootstrap is not a Visual Quar runtime implementation.
It has no dependency on SDL, QRVM, or the game loop.
"""
from dataclasses import dataclass
from enum import Enum, auto


class CoreErrorCode(Enum):
    INVALID_TRANSITION = "invalid_transition"


class CoreError(RuntimeError):
    """Structured lifecycle error; failures never change the core state."""

    def __init__(self, code: CoreErrorCode, source: "CoreState", target: "CoreState") -> None:
        self.code = code
        self.source = source
        self.target = target
        super().__init__(f"{code.value}: {source.name} -> {target.name}")


class CoreState(Enum):
    CREATED = auto()
    INITIALIZED = auto()
    RUNNING = auto()
    STOPPED = auto()


@dataclass(frozen=True)
class CoreConfig:
    """Immutable configuration for one QGF core instance."""
    app_name: str = "QGF Application"

    def __post_init__(self) -> None:
        if not isinstance(self.app_name, str) or not self.app_name.strip():
            raise ValueError("app_name must be a non-empty string")


@dataclass(frozen=True)
class CoreStatus:
    """Read-only diagnostic snapshot of a core instance."""
    app_name: str
    state: CoreState
    is_active: bool
    last_error: CoreErrorCode | None


class QGFCore:
    """State-only bootstrap core; no rendering, input or scheduling."""

    def __init__(self, config: CoreConfig | None = None) -> None:
        if config is not None and not isinstance(config, CoreConfig):
            raise TypeError("config must be CoreConfig or None")
        self._config = config if config is not None else CoreConfig()
        self._state = CoreState.CREATED
        self._last_error: CoreErrorCode | None = None

    @property
    def config(self) -> CoreConfig:
        """Return the immutable core configuration."""
        return self._config

    @property
    def state(self) -> CoreState:
        """Return the current lifecycle state."""
        return self._state

    def status(self) -> CoreStatus:
        """Return a snapshot without changing lifecycle state."""
        return CoreStatus(
            app_name=self._config.app_name,
            state=self._state,
            is_active=self._state is CoreState.RUNNING,
            last_error=self._last_error,
        )

    def initialize(self) -> None:
        """Move CREATED to INITIALIZED; reject other states."""
        self._transition(CoreState.CREATED, CoreState.INITIALIZED)

    def start(self) -> None:
        """Move INITIALIZED to RUNNING; no game loop is started."""
        self._transition(CoreState.INITIALIZED, CoreState.RUNNING)

    def stop(self) -> None:
        """Move INITIALIZED or RUNNING to STOPPED, once only."""
        if self._state not in (CoreState.INITIALIZED, CoreState.RUNNING):
            self._reject(CoreState.STOPPED)
        self._state = CoreState.STOPPED

    def _transition(self, source: CoreState, target: CoreState) -> None:
        """Change state only if the expected source state matches."""
        if self._state is not source:
            self._reject(target)
        self._state = target

    def _reject(self, target: CoreState) -> None:
        """Record a stable error code and raise without changing lifecycle state."""
        self._last_error = CoreErrorCode.INVALID_TRANSITION
        raise CoreError(self._last_error, self._state, target)
