#!/usr/bin/python

from functools import total_ordering

@total_ordering
class Event:
    """The class defining an event."""
    LEFT = 0   # BentleyOttmann, ShamosHoey
    CROSSING = 1   # BentleyOttmann
    RIGHT = 2   # BentleyOttmann, ShamosHoey
    HORIZONTAL = 3   #  HorizontalVertical
    VERTICAL = 4   #  HorizontalVertical
    BOTTOM = 5   #  HorizontalVertical
    TOP = 6   #  HorizontalVertical

    def __init__(self, point, event_type, *sequence):
        self.point = point
        self.type = event_type
        if self.type == Event.CROSSING:
            self.segment_above = sequence[0]
            self.segment_below = sequence[1]
        else:
            self.segment = sequence[0]

    def __str__(self):
        return "Event({}, {})".format(self.point, self.type)

    def __eq__(self, other):
        """Comparison of events (event1 == event2)."""
        return self.point == other.point

    def __ne__(self, other):
        """Comparison of events (event1 != event2)."""
        return self.point != other.point

    def __lt__(self, other):
        """Comparison of events (event1 < event2)."""
        return (self.point.x, self.point.y) < (other.point.x, other.point.y)

    def __hash__(self):
        """Hashable events."""
        return hash((self.point.x, self.point.y, self.type))   # hash based on tuple
