#!/usr/bin/python

from functools import total_ordering

@total_ordering
class Event:
    """The class defining an event."""
    LEFT = 0
    CROSSING = 1
    RIGHT = 2
    HORIZONTAL = 3
    VERTICAL = 4
    BOTTOM = 5
    TOP = 6

    def __init__(self, pt, event_type, *sequence):
        self.pt = pt
        self.type = event_type
        if len(sequence) == 1:
            self.segment = sequence[0]
        elif len(sequence) == 2:
            self.segment_above = sequence[0]
            self.segment_below = sequence[1]

    def __str__(self):
        return "Event({}, {})".format(self.pt, self.type)

    def __eq__(self, other):
        """Comparison of events (event1 == event2)."""
        return self.pt == other.pt

    def __ne__(self, other):
        """Comparison of events (event1 != event2)."""
        return self.pt != other.pt

    def __lt__(self, other):
        """Comparison of events (event1 < event2)."""
        return (self.pt.x, self.pt.y) < (other.pt.x, other.pt.y)

    def __hash__(self):
        """Hashable events."""
        return hash((self.pt.x, self.pt.y, self.type))   # hash based on tuple
