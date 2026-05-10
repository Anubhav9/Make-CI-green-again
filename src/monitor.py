"""Small domain model for a physical GitHub Actions monitor."""

from dataclasses import dataclass
from enum import Enum


class BuildStatus(str, Enum):
    """Workflow states the device cares about."""

    IDLE = "idle"
    QUEUED = "queued"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"


@dataclass(frozen=True)
class DeviceState:
    """What the ESP32 should show for a workflow state."""

    led: str
    display: str
    should_buzz: bool


def describe_build(status: BuildStatus | str) -> DeviceState:
    """Convert a workflow status into LED, OLED, and buzzer behavior."""

    normalized_status = BuildStatus(status)

    match normalized_status:
        case BuildStatus.IDLE:
            return DeviceState(
                led="off",
                display="Ready to trigger CI",
                should_buzz=False,
            )
        case BuildStatus.QUEUED:
            return DeviceState(
                led="yellow",
                display="CI queued",
                should_buzz=False,
            )
        case BuildStatus.RUNNING:
            return DeviceState(
                led="yellow",
                display="CI running",
                should_buzz=False,
            )
        case BuildStatus.PASSED:
            return DeviceState(
                led="green",
                display="CI passed",
                should_buzz=False,
            )
        case BuildStatus.FAILED:
            return DeviceState(
                led="red",
                display="CI failed",
                should_buzz=True,
            )
