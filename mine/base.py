"""Shared base classes and mixins."""


class NameMixin:

    """Mixin class for objects identified by their name."""

    def __str__(self):
        return str(self.name)

    def __eq__(self, other):
        return str(self).lower() == str(other).lower()

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        return str(self).lower() < str(other).lower()
