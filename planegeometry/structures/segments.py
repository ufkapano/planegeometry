#!/usr/bin/python

from fractions import Fraction
from functools import total_ordering
from planegeometry.structures.points import Point
from planegeometry.algorithms.geomtools import orientation

@total_ordering
class Segment:   # odcinek skierowany
    """The class defining a segment (a bounded interval on a line)."""

    def __init__(self, *arguments):
        """Make a segment in the plane."""
        if len(arguments) == 2:
            if not all(isinstance(pt, Point) for pt in arguments):
                raise ValueError("arguments are not points")
            self.pt1, self.pt2 = arguments
        elif len(arguments) == 4:
            x1, y1, x2, y2 = arguments
            self.pt1 = Point(x1, y1)
            self.pt2 = Point(x2, y2)
        else:
            raise ValueError("bad number of arguments")

    def __repr__(self):
        """String representation of a segment."""
        return "Segment({0!r}, {1!r}, {2!r}, {3!r})".format(
            self.pt1.x, self.pt1.y, self.pt2.x, self.pt2.y)

    def __eq__(self, other):
        """Comparison of segments (s1 == s2)."""
        return other.pt1 == self.pt1 and other.pt2 == self.pt2

    def __ne__(self, other):
        """Comparison of segments (s1 != s2)."""
        return not self == other

    def __lt__(self, other):
        """Comparison of segments (s1 < s2)."""
        return (self.pt1.x, self.pt1.y, self.pt2.x, self.pt2.y) < (
            other.pt1.x, other.pt1.y, other.pt2.x, other.pt2.y)

    def copy(self):   # zwraca nowa instancje
        """Return a copy of a segment."""
        return Segment(self.pt1, self.pt2)

    def center(self):
        """Return the center of a segment."""
        return (self.pt1 + self.pt2) * Fraction(1, 2)

    def length(self):
        """Return the segment length."""
        return (self.pt2 - self.pt1).length()

    def move(self, *arguments):   # przesuniecie o (x, y)
        """Return a new moved segment."""
        if len(arguments) == 1 and isinstance(arguments[0], Point):
            pt = arguments[0]
            x1 = self.pt1.x + pt.x
            y1 = self.pt1.y + pt.y
            x2 = self.pt2.x + pt.x
            y2 = self.pt2.y + pt.y
            return Segment(x1, y1, x2, y2)
        elif len(arguments) == 2:
            x, y = arguments
            x1 = self.pt1.x + x
            y1 = self.pt1.y + y
            x2 = self.pt2.x + x
            y2 = self.pt2.y + y
            return Segment(x1, y1, x2, y2)
        else:
            raise ValueError("bad arguments")

    def __contains__(self, other):
        """Test if a point is in a segment."""
        if isinstance(other, Point):
            if orientation(self.pt1, self.pt2, other) != 0:
                return False   # not collinear
            if (other.x <= max(self.pt1.x, self.pt2.x) and
                other.x >= min(self.pt1.x, self.pt2.x) and
                other.y <= max(self.pt1.y, self.pt2.y) and
                other.y >= min(self.pt1.y, self.pt2.y)):
                return True
            else:
                return False
        else:
            raise ValueError("not a point")

    def intersect(self, other):
        """Test if two segments intersect."""
        # https://www.geeksforgeeks.org/check-if-two-given-line-segments-intersect/
        o1 = orientation(self.pt1, self.pt2, other.pt1)
        o2 = orientation(self.pt1, self.pt2, other.pt2)
        o3 = orientation(other.pt1, other.pt2, self.pt1)
        o4 = orientation(other.pt1, other.pt2, self.pt2)
        # General case.
        if (o1 != o2) and (o3 != o4):
            return True
        # Special cases.
        if o1 == 0 and other.pt1 in self:
            return True
        if o2 == 0 and other.pt2 in self:
            return True
        if o3 == 0 and self.pt1 in other:
            return True
        if o4 == 0 and self.pt2 in other:
            return True
        return False

    def intersection_point(self, other):
        """Return the intersection point of two segments."""
        if self.intersect(other):
            x1, y1, x2, y2 = self.pt1.x, self.pt1.y, self.pt2.x, self.pt2.y
            x3, y3, x4, y4 = other.pt1.x, other.pt1.y, other.pt2.x, other.pt2.y
            if x1 == x2:
                assert x3 != x4
                x5 = x1
                y5 = y3 + Fraction(x1 - x3, x4 - x3) * (y4 - y3)
            elif x3 == x4:
                assert x1 != x2
                x5 = x3
                y5 = y1 + Fraction(x3 - x1, x2 - x1) * (y2 - y1)
            else:
                B = (y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1)
                assert B != 0   # inaczej odcinki rownolegle
                A = (x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)
                x5 = x1 + Fraction(A, B) * (x2 - x1)
                y5 = y1 + Fraction(A, B) * (y2 - y1)
            return Point(x5, y5)
        else:
            return None

    def calculate_y(self, x):
        """Calculate y for a given x in the segment."""
        x1 = self.pt1.x
        y1 = self.pt1.y
        x2 = self.pt2.x
        y2 = self.pt2.y
        return y1 + Fraction(y2 - y1, x2 - x1) * (x - x1)

    def calculate_x(self, y):
        """Calculate x for a given y in the segment."""
        x1 = self.pt1.x
        y1 = self.pt1.y
        x2 = self.pt2.x
        y2 = self.pt2.y
        return x1 + Fraction(x2 - x1, y2 - y1) * (y - y1)

    def __hash__(self):
        """Hashable segments."""
        #return hash((self.pt1.x, self.pt1.y, self.pt2.x, self.pt2.y))
        return hash((self.pt1, self.pt2))

    def gnu(self, visible=False):
        """String for Gnuplot."""
        L = []
        if visible:
            L.append(self.pt1.gnu())
            L.append(self.pt2.gnu())
        L.append('set arrow from {0},{1} to {2},{3} nohead\n'.format(
            float(self.pt1.x), float(self.pt1.y),
            float(self.pt2.x), float(self.pt2.y)))
        return "".join(L)

# EOF
