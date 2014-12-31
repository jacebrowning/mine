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

    def test_eq(self):
        """Verify timestamps can be equated."""
        assert Timestamps(1, 1) == Timestamps(1, 1)
        assert Timestamps(1, 2) == Timestamps(1, 2)
        assert Timestamps(1, 2) != Timestamps(1, 3)
        assert Timestamps(4, 2) == Timestamps(4, 3)

    def test_lt(self):
        """Verify timestamps can be sorted."""
        assert Timestamps(1, 2) < Timestamps(1, 3)
        assert Timestamps(1, 4) > Timestamps(1, 3)
        assert Timestamps(4, 2) < Timestamps(5, 3)
        assert Timestamps(3, 2) < Timestamps(4, 3)
