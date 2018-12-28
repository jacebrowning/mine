# pylint: disable=misplaced-comparison-constant,no-self-use

from unittest.mock import Mock, patch

import pytest

from mine.models import Computer, ProgramConfig

from .test_models_application import TestApplication


class TestProgramConfig:
    """Unit tests for the program configuration class."""

    def test_init(self):
        """Verify a new program configuration is blank."""
        config = ProgramConfig()
        assert not config.applications
        assert not config.computers


@patch('uuid.getnode', Mock(return_value=0))
@patch('socket.gethostname', Mock(return_value='Sample.local'))
class TestComputers:
    """Unit tests for lists of computers."""

    config = ProgramConfig(
        computers=[Computer('abc', 'abc.local', 1), Computer('def', 'def.local', 2)]
    )

    def test_get(self):
        """Verify a computer can be found in a list."""
        computer = self.config.get_computer('ABC')
        assert 'abc' == computer.name

    def test_get_missing(self):
        """Verify an invalid names raise an assertion."""
        with pytest.raises(AssertionError):
            self.config.get_computer('fake')

    def test_match(self):
        """Verify a similar computer can be found."""
        computer = self.config.match_computer('AB')
        assert 'abc' == computer.name

    def test_generate_name(self):
        """Verify a computer name is generated correctly."""
        computer = Computer(None, hostname='Jaces-iMac.local')
        name = self.config.generate_computer_name(computer)
        assert 'jaces-imac' == name

    def test_generate_name_duplicates(self):
        """Verify a computer name is generated correctly with duplicates."""
        config = ProgramConfig(computers=[Computer('jaces-imac')])
        computer = Computer(None, hostname='Jaces-iMac.local')
        name = config.generate_computer_name(computer)
        assert 'jaces-imac-2' == name

    def test_get_current_by_matching_address(self):
        config = ProgramConfig(
            computers=[Computer('abc', 'foobar', '00:00:00:00:00:00')]
        )
        computer = config.get_current_computer()
        assert 'abc' == computer.name

    def test_get_current_by_matching_hostname(self):
        config = ProgramConfig(computers=[Computer('abc', 'Sample.local', 'foobar')])
        computer = config.get_current_computer()
        assert 'abc' == computer.name


class TestApplications:
    """Unit tests for lists of applications."""

    config = ProgramConfig(applications=[TestApplication.app1, TestApplication.app2])

    def test_get(self):
        """Verify an application can be found in a list."""
        app = self.config.get_application('itunes')
        assert 'iTunes' == app.name

    def test_get_missing(self):
        """Verify an invalid names raise an assertion."""
        with pytest.raises(AssertionError):
            self.config.get_application('fake')
