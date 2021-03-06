"""Data structures for timestamp information."""

import yorm


@yorm.attr(started=yorm.types.Integer)
@yorm.attr(stopped=yorm.types.Integer)
class Timestamp(yorm.types.AttributeDictionary):
    """Dictionary of last start and stop times."""

    def __init__(self, started=0, stopped=0):
        super().__init__()
        self.started = started
        self.stopped = stopped

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
