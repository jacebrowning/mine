"""Unit tests for the `computer` module."""
# pylint: disable=R0201

from unittest.mock import Mock, patch

from mine.computer import Computer, ComputerList


class MockSocket(Mock):

    """A mock socket connection for testing."""

    connect = Mock()
    close = Mock()
    getsockname = lambda _: ['5.6.7.8']


@patch('socket.gethostname', Mock(return_value='Sample.local'))
@patch('ipgetter.myip', Mock(return_value='1.2.3.4'))
@patch('socket.socket', MockSocket)
class TestComputer:

    """Unit tests for the computer classes."""

    def test_init(self):
        """Verify the correct computer information is loaded."""
        computer = Computer('my-sample')
        assert 'my-sample' == computer.name
        assert 'Sample.local' == computer.hostname
        assert '1.2.3.4' == computer.address.external
        assert '5.6.7.8' == computer.address.internal

    def test_init_defaults(self):
        """Verify the correct computer information can be overridden."""
        computer = Computer('name', 'hostname', 'external', 'internal')
        assert 'name' == computer.name
        assert 'hostname' == computer.hostname
        assert 'external' == computer.address.external
        assert 'internal' == computer.address.internal

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
        other = Computer('name', 'hostname', 'external', 'internal')
        computers = ComputerList([other])
        this = computers.get_current()
        assert 'sample' == this.name
        assert 'Sample.local' == this.hostname
        assert '1.2.3.4' == this.address.external
        assert '5.6.7.8' == this.address.internal
        assert 2 == len(computers)

    def test_get_match_all(self):
        """Verify a computer can be matched exactly."""
        other = Computer('all', 'Sample.local', '1.2.3.4', '5.6.7.8')
        computers = ComputerList([other])
        this = computers.get_current()
        assert 'all' == this.name
        assert 'Sample.local' == this.hostname
        assert '1.2.3.4' == this.address.external
        assert '5.6.7.8' == this.address.internal
        assert 1 == len(computers)

    def test_get_match_hostname_external(self):
        """Verify a computer can be matched by hostname and external."""
        other = Computer('external', 'Sample.local', '1.2.3.4', '9.9.9.9')
        computers = ComputerList([other])
        this = computers.get_current()
        assert 'external' == this.name
        assert 'Sample.local' == this.hostname
        assert '1.2.3.4' == this.address.external
        assert '5.6.7.8' == this.address.internal
        assert 1 == len(computers)

    def test_get_match_hostname_internal(self):
        """Verify a computer can be matched by hostname and internal."""
        other = Computer('internal', 'Sample.local', '9.9.9.9', '5.6.7.8')
        computers = ComputerList([other])
        this = computers.get_current()
        assert 'internal' == this.name
        assert 'Sample.local' == this.hostname
        assert '1.2.3.4' == this.address.external
        assert '5.6.7.8' == this.address.internal
        assert 1 == len(computers)

    def test_get_hostname_single(self):
        """Verify a computer can be matched by a single hostname."""
        others = [Computer('sample', 'Sample.local', '9.9.9.9', '9.9.9.9'),
                  Computer('another', 'Another.local', '9.9.9.9', '9.9.9.9')]
        computers = ComputerList(others)
        this = computers.get_current()
        assert 'sample' == this.name
        assert 'Sample.local' == this.hostname
        assert '1.2.3.4' == this.address.external
        assert '5.6.7.8' == this.address.internal
        assert 2 == len(computers)

    def test_get_hostname_multiple(self):
        """Verify a computer cannot be matched by multiple hostnames."""
        others = [Computer('sample', 'Sample.local', '9.9.9.9', '9.9.9.9'),
                  Computer('sample-2', 'Sample.local', '8.8.8.8', '8.8.8.8')]
        computers = ComputerList(others)
        this = computers.get_current()
        assert 'sample-3' == this.name
        assert 'Sample.local' == this.hostname
        assert '1.2.3.4' == this.address.external
        assert '5.6.7.8' == this.address.internal
        assert 3 == len(computers)

    def test_get_match_external_internal(self):
        """Verify a computer can be matched by external and internal."""
        other = Computer('another', 'Another.local', '1.2.3.4', '5.6.7.8')
        computers = ComputerList([other])
        this = computers.get_current()
        assert 'another' == this.name
        assert 'Sample.local' == this.hostname
        assert '1.2.3.4' == this.address.external
        assert '5.6.7.8' == this.address.internal
        assert 1 == len(computers)


@patch('socket.gethostname', Mock(return_value='Sample.local'))
@patch('ipgetter.myip', Mock(return_value='1.2.3.4'))
@patch('socket.socket', MockSocket)
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
