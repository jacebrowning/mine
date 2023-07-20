from unittest.mock import Mock, patch

import pytest

from mine.models import Application, Computer, ProgramConfig


@patch("uuid.getnode", Mock(return_value=0))
@patch("socket.gethostname", Mock(return_value="Sample.local"))
class TestProgramConfig:
    """Unit tests for the program configuration class."""

    config = ProgramConfig(
        applications=[Application("iTunes"), Application("HipChat")],
        computers=[
            Computer("abc", "s1", "1:1", "abc.local"),
            Computer("def", "s2", "2:2", "def.local"),
            Computer("My iMac", "s3", "3:3", "imac.local"),
            Computer("My Mac", "s4", "4:4", "mac.local"),
        ],
    )

    def test_init(self):
        """Verify a new program configuration is blank."""
        config = ProgramConfig()
        assert not config.applications
        assert not config.computers

    def test_get_application(self):
        """Verify an application can be found in a list."""
        app = self.config.get_application("itunes")
        assert "iTunes" == app.name

    def test_get_application_missing(self):
        """Verify an invalid names raise an assertion."""
        with pytest.raises(AssertionError):
            self.config.get_application("fake")

    def test_get_computer(self):
        """Verify a computer can be found in a list."""
        computer = self.config.get_computer("ABC")
        assert "abc" == computer.name

    def test_get_computer_missing(self):
        """Verify an invalid names raise an assertion."""
        with pytest.raises(AssertionError):
            self.config.get_computer("fake")

    def test_match_computer(self):
        """Verify a similar computer can be found."""
        computer = self.config.match_computer("AB")
        assert "abc" == computer.name

    def test_match_computer_partial(self):
        """Verify an exact match is preferred over partial."""
        computer = self.config.match_computer("mac")
        assert "My Mac" == computer.name

    def test_generate_name(self):
        """Verify a computer name is generated correctly."""
        config = ProgramConfig()
        computer = Computer("", hostname="Jaces-iMac.local")
        name = config.generate_computer_name(computer)
        assert "jaces-imac" == name

    def test_generate_name_duplicates(self):
        """Verify a computer name is generated correctly with duplicates."""
        config = ProgramConfig(computers=[Computer("jaces-imac")])
        computer = Computer("", "s", hostname="Jaces-iMac.local")
        name = config.generate_computer_name(computer)
        assert "jaces-imac-2" == name

    def test_get_current_computer_by_matching_address(self):
        config = ProgramConfig(
            computers=[Computer("abc", "s", "00:00:00:00:00:00", "foobar")]
        )
        computer = config.get_current_computer()
        assert "abc" == computer.name

    def test_get_current_computer_by_matching_hostname(self):
        config = ProgramConfig(computers=[Computer("abc", "s", "a:", "Sample.local")])
        computer = config.get_current_computer()
        assert "abc" == computer.name
