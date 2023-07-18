import pytest

from mine.models import Application


class TestApplication:
    """Unit tests for the application class."""

    app1 = Application("iTunes")
    app1.versions.mac = "iTunes.app"
    app2 = Application("HipChat")
    app3 = Application("Sublime Text")
    app3.versions.linux = "sublime_text"
    app4 = Application("hipchat")

    str_application = [
        ("iTunes", app1),
        ("HipChat", app2),
        ("Sublime Text", app3),
        ("hipchat", app4),
    ]

    @pytest.mark.parametrize("string,application", str_application)
    def test_str(self, string, application):
        """Verify applications can be converted to strings."""
        assert string == str(application)

    def test_eq(self):
        """Verify applications can be equated."""
        assert self.app2 == self.app4
        assert self.app1 != self.app3

    def test_lt(self):
        """Verify applications can be sorted."""
        assert self.app2 < self.app1
        assert self.app3 > self.app2
