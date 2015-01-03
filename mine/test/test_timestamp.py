"""Unit tests for the `timestamp` module."""
# pylint: disable=R0201

import pytest

from mine.timestamp import Timestamp


class TestTimestamp:

    """Unit tests for the timestamp class."""

    none = Timestamp()
    started_only = Timestamp(started=42)
    stopped_only = Timestamp(stopped=42)
    started_after_stopped = Timestamp(2, 1)
    stopped_after_started = Timestamp(3, 4)

    active_timestamp = [
        (False, none),
        (True, started_only),
        (False, stopped_only),
        (True, started_after_stopped),
        (False, stopped_after_started),
    ]

    repr_timestamp = [
        ("<timestamp 0>", none),
        ("<timestamp 42>", started_only),
        ("<timestamp 42>", stopped_only),
        ("<timestamp 2>", started_after_stopped),
        ("<timestamp 4>", stopped_after_started),
    ]

    @pytest.mark.parametrize("representation,timestamp", repr_timestamp)
    def test_repr(self, representation, timestamp):
        """Verify timestamps can represented as strings."""
        assert representation == repr(timestamp)

    def test_eq(self):
        """Verify timestamps can be equated."""
        assert Timestamp(1, 1) == Timestamp(1, 1)
        assert Timestamp(1, 2) == Timestamp(1, 2)
        assert Timestamp(1, 2) != Timestamp(1, 3)
        assert Timestamp(4, 2) == Timestamp(4, 3)

    def test_lt(self):
        """Verify timestamps can be sorted."""
        assert Timestamp(1, 2) < Timestamp(1, 3)
        assert Timestamp(1, 4) > Timestamp(1, 3)
        assert Timestamp(4, 2) < Timestamp(5, 3)
        assert Timestamp(3, 2) < Timestamp(4, 3)

    @pytest.mark.parametrize("active,timestamp", active_timestamp)
    def test_active(self, active, timestamp):
        """Verify started/stopped counters determine activity."""
        assert active == timestamp.active
