"""Integration tests for the `mine` package."""

from unittest.mock import Mock, patch

from mine.computer import Computer


class MockSocket(Mock):

    """A mock socket connection for testing."""

    connect = Mock()
    close = Mock()
    getsockname = lambda _: ['5.6.7.8']


@patch('socket.gethostname', Mock(return_value='Sample-Computer.local'))
@patch('ipgetter.myip', Mock(return_value='1.2.3.4'))
@patch('socket.socket', MockSocket)
def test_init():
    """Verify the correct computer information is loaded."""
    computer = Computer('sample')
    assert 'sample' == computer.label
    assert 'Sample-Computer.local' == computer.hostname
    assert '1.2.3.4' == computer.address.external
    assert '5.6.7.8' == computer.address.internal


def test_init_defaults():
    """Verify the correct computer information can be overridden."""
    computer = Computer('label', 'hostname', 'external', 'internal')
    assert 'label' == computer.label
    assert 'hostname' == computer.hostname
    assert 'external' == computer.address.external
    assert 'internal' == computer.address.internal
