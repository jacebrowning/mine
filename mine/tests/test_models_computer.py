from unittest.mock import Mock, patch

from mine.models import Computer, ProgramConfig


@patch("uuid.getnode", Mock(return_value=0))
@patch("socket.gethostname", Mock(return_value="Sample.local"))
class TestComputer:
    """Unit tests for the computer classes."""

    def test_init(self):
        """Verify the correct computer information is loaded."""
        computer = Computer("my-sample")
        assert "my-sample" == computer.name
        assert "00:00:00:00:00:00" == computer.address
        assert "Sample.local" == computer.hostname

    def test_init_defaults(self):
        """Verify the correct computer information can be overridden."""
        computer = Computer("name", "serial", "address:", "hostname")
        assert "name" == computer.name
        assert "address:" == computer.address
        assert "hostname" == computer.hostname
        assert "serial" == computer.serial

    def test_eq(self):
        """Verify computers and strings can be equated."""
        assert Computer("mac1") == Computer("mac1")
        assert Computer("mac1") != Computer("mac2")
        assert Computer("mac1") == "mac1"
        assert "mac1" != Computer("mac2")

    def test_lt(self):
        """Verify computers can be sorted."""
        assert Computer("mac1") < Computer("mac2")
        assert Computer("def") > Computer("ABC")

    # TODO: move these to test_models_config.py

    def test_get_match_none(self):
        """Verify a computer is added when missing."""
        other = Computer("name", "serial", "address:", "hostname")
        config = ProgramConfig(computers=[other])
        this = config.get_current_computer()
        assert "sample" == this.name
        assert "00:00:00:00:00:00" == this.address
        assert "Sample.local" == this.hostname
        assert 2 == len(config.computers)

    def test_get_match_all(self):
        """Verify a computer can be matched exactly."""
        other = Computer("all", "serial", "00:00:00:00:00:00", "Sample.local")
        config = ProgramConfig(computers=[other])
        this = config.get_current_computer()
        assert "all" == this.name
        assert "00:00:00:00:00:00" == this.address
        assert "Sample.local" == this.hostname
        assert 1 == len(config.computers)
