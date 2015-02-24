"""Unit tests for the `computer` module."""
# pylint: disable=R0201

from unittest.mock import Mock, patch

from mine.computer import Computer, ComputerList


@patch('uuid.getnode', Mock(return_value=0))
@patch('socket.gethostname', Mock(return_value='Sample.local'))
class TestComputer:

    """Unit tests for the computer classes."""

    def test_init(self):
        """Verify the correct computer information is loaded."""
        computer = Computer('my-sample')
        assert 'my-sample' == computer.name
        assert '00:00:00:00:00:00' == computer.address
        assert 'Sample.local' == computer.hostname

    def test_init_defaults(self):
        """Verify the correct computer information can be overridden."""
        computer = Computer('name', 'hostname', 'address')
        assert 'name' == computer.name
        assert 'address' == computer.address
        assert 'hostname' == computer.hostname

    def test_eq(self):
        """Verify computers and strings can be equated."""
        assert Computer('mac1') == Computer('mac1')
        assert Computer('mac1') != Computer('mac2')
        assert Computer('mac1') == 'mac1'
        assert 'mac1' != Computer('mac2')

    def test_lt(self):
        """Verify computers can be sorted."""
        assert Computer('mac1') < Computer('mac2')
        assert Computer('def') > Computer('ABC')

    def test_get_match_none(self):
        """Verify a computer is added when missing."""
        other = Computer('name', 'hostname', 'address')
        computers = ComputerList([other])
        this = computers.get_current()
        assert 'sample' == this.name
        assert '00:00:00:00:00:00' == this.address
        assert 'Sample.local' == this.hostname
        assert 2 == len(computers)

    def test_get_match_all(self):
        """Verify a computer can be matched exactly."""
        other = Computer('all', 'Sample.local', '00:00:00:00:00:00')
        computers = ComputerList([other])
        this = computers.get_current()
        assert 'all' == this.name
        assert '00:00:00:00:00:00' == this.address
        assert 'Sample.local' == this.hostname
        assert 1 == len(computers)


@patch('uuid.getnode', Mock(return_value=0))
@patch('socket.gethostname', Mock(return_value='Sample.local'))
class TestComputerList:

    """Unit tests for lists of computers."""

    def test_generate_name(self):
        """Verify a computer name is generated correctly."""
        computers = ComputerList()
        computer = Computer(None, hostname='Jaces-iMac.local')
        name = computers.generate_name(computer)
        assert 'jaces-imac' == name

    def test_generate_name_duplicates(self):
        """Verify a computer name is generated correctly with duplicates."""
        computers = ComputerList([Computer('jaces-imac')])
        computer = Computer(None, hostname='Jaces-iMac.local')
        name = computers.generate_name(computer)
        assert 'jaces-imac-2' == name
