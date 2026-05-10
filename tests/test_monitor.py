import pytest
from make_ci_green_again import monitor

@pytest.mark.parametrize(
    ("status", "expected"),
    [
        (
            monitor.BuildStatus.IDLE,
            monitor.DeviceState(
                led="off",
                display="Ready to trigger CI",
                should_buzz=False,
            ),
        ),
        (
            monitor.BuildStatus.QUEUED,
            monitor.DeviceState(led="yellow", display="CI queued", should_buzz=False),
        ),
        (
            monitor.BuildStatus.RUNNING,
            monitor.DeviceState(led="yellow", display="CI running", should_buzz=False),
        ),
        (
            monitor.BuildStatus.PASSED,
            monitor.DeviceState(led="green", display="CI passed", should_buzz=False),
        ),
        (
            monitor.BuildStatus.FAILED,
            monitor.DeviceState(led="red", display="CI failed", should_buzz=True),
        ),
    ],
)
def test_describe_build_maps_status_to_device_state(status, expected):
    assert monitor.describe_build(status) == expected


def test_describe_build_accepts_status_strings():
    assert monitor.describe_build("passed") == monitor.DeviceState(
        led="green",
        display="CI passed",
        should_buzz=False,
    )


def test_describe_build_rejects_unknown_status():
    with pytest.raises(ValueError, match="'unknown' is not a valid BuildStatus"):
        monitor.describe_build("unknown")
