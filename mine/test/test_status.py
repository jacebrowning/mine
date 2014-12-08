"""Unit tests for the `status` module."""
# pylint: disable=R0201

import pytest

from mine.status import Timestamps


class TestTimestamps:

    """Unit tests for the timestamps class."""

    none = Timestamps()
    started_only = Timestamps(started=42)
    stopped_only = Timestamps(stopped=42)
    started_after_stopped = Timestamps(2, 1)
    stopped_after_started = Timestamps(3, 4)

    active_timestamps = [
        (False, none),
        (True, started_only),
        (False, stopped_only),
        (True, started_after_stopped),
        (False, stopped_after_started),
    ]

    @pytest.mark.parametrize("active,timestamps", active_timestamps)
    def test_running(self, active, timestamps):
        """Verify started/stopped counters determine activity."""
        assert active == timestamps.active
