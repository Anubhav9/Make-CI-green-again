import pytest

from make_ci_green_again import BuildStatus, DeviceState, describe_build


@pytest.mark.parametrize(
    ("status", "expected"),
    [
        (
            BuildStatus.IDLE,
            DeviceState(
                led="off",
                display="Ready to trigger CI",
                should_buzz=False,
            ),
        ),
        (
            BuildStatus.QUEUED,
            DeviceState(led="yellow", display="CI queued", should_buzz=False),
        ),
        (
            BuildStatus.RUNNING,
            DeviceState(led="yellow", display="CI running", should_buzz=False),
        ),
        (
            BuildStatus.PASSED,
            DeviceState(led="green", display="CI passed", should_buzz=False),
        ),
        (
            BuildStatus.FAILED,
            DeviceState(led="red", display="CI failed", should_buzz=True),
        ),
    ],
)
def test_describe_build_maps_status_to_device_state(status, expected):
    assert describe_build(status) == expected


def test_describe_build_accepts_status_strings():
    assert describe_build("passed") == DeviceState(
        led="green",
        display="CI passed",
        should_buzz=False,
    )


def test_describe_build_rejects_unknown_status():
    with pytest.raises(ValueError, match="'unknown' is not a valid BuildStatus"):
        describe_build("unknown")
