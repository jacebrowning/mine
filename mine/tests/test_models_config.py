from mine.models import ProgramConfig


class TestProgramConfig:
    """Unit tests for the program configuration class."""

    def test_init(self):
        """Verify a new program configuration is blank."""
        config = ProgramConfig()
        assert not config.applications
        assert not config.computers
