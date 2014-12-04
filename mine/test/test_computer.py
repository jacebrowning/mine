"""Integration tests for the `mine` package."""
# pylint: disable=R0201

from unittest.mock import Mock, patch

from mine.computer import Computer, Computers


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
        assert 'my-sample' == computer.label
        assert 'Sample.local' == computer.hostname
        assert '1.2.3.4' == computer.address.external
        assert '5.6.7.8' == computer.address.internal

    def test_init_defaults(self):
        """Verify the correct computer information can be overridden."""
        computer = Computer('label', 'hostname', 'external', 'internal')
        assert 'label' == computer.label
        assert 'hostname' == computer.hostname
        assert 'external' == computer.address.external
        assert 'internal' == computer.address.internal

    def test_get_match_none(self):
        """Verify a computer is added when missing."""
        other = Computer('label', 'hostname', 'external', 'internal')
        computers = Computers([other])
        this = computers.get_current()
        assert 'sample' == this.label
        assert 'Sample.local' == this.hostname
        assert '1.2.3.4' == this.address.external
        assert '5.6.7.8' == this.address.internal
        assert 2 == len(computers)

    def test_get_match_all(self):
        """Verify a computer can be matched exactly."""
        other = Computer('all', 'Sample.local', '1.2.3.4', '5.6.7.8')
        computers = Computers([other])
        this = computers.get_current()
        assert 'all' == this.label
        assert 'Sample.local' == this.hostname
        assert '1.2.3.4' == this.address.external
        assert '5.6.7.8' == this.address.internal
        assert 1 == len(computers)

    def test_get_match_hostname_external(self):
        """Verify a computer can be matched by hostname and external."""
        other = Computer('external', 'Sample.local', '1.2.3.4', '9.9.9.9')
        computers = Computers([other])
        this = computers.get_current()
        assert 'external' == this.label
        assert 'Sample.local' == this.hostname
        assert '1.2.3.4' == this.address.external
        assert '5.6.7.8' == this.address.internal
        assert 1 == len(computers)

    def test_get_match_hostname_internal(self):
        """Verify a computer can be matched by hostname and internal."""
        other = Computer('internal', 'Sample.local', '9.9.9.9', '5.6.7.8')
        computers = Computers([other])
        this = computers.get_current()
        assert 'internal' == this.label
        assert 'Sample.local' == this.hostname
        assert '1.2.3.4' == this.address.external
        assert '5.6.7.8' == this.address.internal
        assert 1 == len(computers)

    def test_get_hostname_single(self):
        """Verify a computer can be matched by a single hostname."""
        others = [Computer('sample', 'Sample.local', '9.9.9.9', '9.9.9.9'),
                  Computer('another', 'Another.local', '9.9.9.9', '9.9.9.9')]
        computers = Computers(others)
        this = computers.get_current()
        assert 'sample' == this.label
        assert 'Sample.local' == this.hostname
        assert '1.2.3.4' == this.address.external
        assert '5.6.7.8' == this.address.internal
        assert 2 == len(computers)

    def test_get_hostname_multiple(self):
        """Verify a computer cannot be matched by multiple hostnames."""
        others = [Computer('sample', 'Sample.local', '9.9.9.9', '9.9.9.9'),
                  Computer('sample-2', 'Sample.local', '8.8.8.8', '8.8.8.8')]
        computers = Computers(others)
        this = computers.get_current()
        assert 'sample-3' == this.label
        assert 'Sample.local' == this.hostname
        assert '1.2.3.4' == this.address.external
        assert '5.6.7.8' == this.address.internal
        assert 3 == len(computers)

    def test_get_match_external_internal(self):
        """Verify a computer can be matched by external and internal."""
        other = Computer('another', 'Another.local', '1.2.3.4', '5.6.7.8')
        computers = Computers([other])
        this = computers.get_current()
        assert 'another' == this.label
        assert 'Sample.local' == this.hostname
        assert '1.2.3.4' == this.address.external
        assert '5.6.7.8' == this.address.internal
        assert 1 == len(computers)
