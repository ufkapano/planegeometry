#!/usr/bin/env python3

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
    START_VERTEX = 7   # monotone partition
    END_VERTEX = 8   # monotone partition
    SPLIT_VERTEX = 9   # monotone partition
    MERGE_VERTEX = 10   # monotone partition
    REGULAR_VERTEX = 11   # monotone partition

    def __init__(self, point, event_type, *sequence):
        self.point = point
        self.type = event_type
        if (self.type == Event.CROSSING or
            self.type == Event.START_VERTEX or
            self.type == Event.END_VERTEX or
            self.type == Event.SPLIT_VERTEX or
            self.type == Event.MERGE_VERTEX or
            self.type == Event.REGULAR_VERTEX):
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
