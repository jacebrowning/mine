"""Data structures for timestamp information."""

from dataclasses import dataclass


@dataclass
class Timestamp:
    """Dictionary of last start and stop times."""

    started: int = 0
    stopped: int = 0

    def __repr__(self):
        return "<timestamp {}>".format(self.latest)

    def __eq__(self, other):
        return self.latest == other.latest

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        return self.latest < other.latest

    @property
    def latest(self):
        """Get the latest timestamp."""
        return max((self.started, self.stopped))

    @property
    def active(self):
        """Determine if the timestamps indicate current activity."""
        if not self.started:
            return False

        if not self.stopped:
            return True

        return self.started > self.stopped
