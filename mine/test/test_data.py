"""Unit tests for the `data` module."""
# pylint: disable=R0201,W0201,W0613

from mine.data import Data


class TestData:

    """Unit tests for the program data class."""

    def test_repr(self):
        """Verify program configuration can represented as a string."""
        assert "settings" == repr(Data())
