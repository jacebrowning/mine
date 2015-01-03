"""Unit tests for the `config` module."""
# pylint: disable=R0201,W0201,W0613

from mine.config import ProgramConfig


class TestProgramConfig:

    """Unit tests for the program configuration class."""

    def test_init(self):
        """Verify a new program configuration is blank."""
        config = ProgramConfig()
        assert not config.applications
        assert not config.computers
