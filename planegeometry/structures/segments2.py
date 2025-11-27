#!/usr/bin/env python3

from fractions import Fraction
from dataclasses import dataclass
from planegeometry.structures.points2 import Point
from planegeometry.algorithms.geomtools import orientation

@dataclass(frozen=True,order=True,repr=False)
class Segment:   # odcinek skierowany
    pt1: Point
    pt2: Point

    def __post_init__(self):
        if not isinstance(self.pt1, Point):
            raise ValueError("not a Point")
        if not isinstance(self.pt2, Point):
            raise ValueError("not a Point")
        if self.pt1 == self.pt2:
            raise ValueError("equal points")

    def __repr__(self):
        """String representation of a segment."""
        return "Segment({0!r}, {1!r})".format(self.pt1, self.pt2)

    @property
    def source(self):
        """I'm the 'source' property."""
        return self.pt1

    @property
    def target(self):
        """I'm the 'target' property."""
        return self.pt2

    @property
    def weight(self):
        """I'm the 'weight' property."""
        return (self.pt2 - self.pt1).length()

    def copy(self):   # zwraca nowa instancje
        """Return a copy of a segment."""
        return self

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
            return Segment(Point(x1, y1), Point(x2, y2))
        elif len(arguments) == 2:
            x, y = arguments
            x1 = self.pt1.x + x
            y1 = self.pt1.y + y
            x2 = self.pt2.x + x
            y2 = self.pt2.y + y
            return Segment(Point(x1, y1), Point(x2, y2))
        else:
            raise ValueError("bad arguments")

    def __invert__(self):
        """Return the segment with the opposite direction."""
        return Segment(self.pt2, self.pt1)

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
        elif isinstance(other, Segment):
            return other.pt1 in self and other.pt2 in self
        else:
            raise ValueError()

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
        """Return the intersection point of two segments (not parallel)."""
        if self.intersect(other):
            if self.parallel(other):
                # o--o----o is forbidden.
                raise ValueError("segments are parallel")
            x1, y1, x2, y2 = self.pt1.x, self.pt1.y, self.pt2.x, self.pt2.y
            x3, y3, x4, y4 = other.pt1.x, other.pt1.y, other.pt2.x, other.pt2.y
            if x1 == x2:
                assert x3 != x4   # if x3==x4 then the segments are parallel
                x5 = x1
                if isinstance((x1+x3+x4), float):
                    y5 = y3 + (y4 - y3) * (x1 - x3) / float(x4 - x3)
                else:
                    y5 = y3 + (y4 - y3) * Fraction(x1 - x3, x4 - x3)
            elif x3 == x4:
                assert x1 != x2   # if x1==x2 then the segments are parallel
                x5 = x3
                if isinstance((x1+x3+x2), float):
                    y5 = y1 + (y2 - y1) * (x3 - x1) / float(x2 - x1)
                else:
                    y5 = y1 + (y2 - y1) * Fraction(x3 - x1, x2 - x1)
            else:
                B = (y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1)
                assert B != 0   # if B==0 then the segments are parallel
                A = (x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)
                if isinstance((A*B), float):
                    x5 = x1 + (A / B) * (x2 - x1)
                    y5 = y1 + (A / B) * (y2 - y1)
                else:
                    x5 = x1 + Fraction(A, B) * (x2 - x1)
                    y5 = y1 + Fraction(A, B) * (y2 - y1)
            return Point(x5, y5)
        else:
            return None

    def parallel(self, other):
        """Test if two segments are parallel."""
        return (self.pt2 - self.pt1).cross(other.pt2 - other.pt1) == 0

    def perpendicular(self, other):
        """Test if two segments are perpendicular."""
        return (self.pt2 - self.pt1) * (other.pt2 - other.pt1) == 0

    def calculate_y(self, x):
        """Calculate y for a given x in the segment."""
        # Is x between x1 and x2? Yes for a sweep line.
        x1 = self.pt1.x
        y1 = self.pt1.y
        x2 = self.pt2.x
        y2 = self.pt2.y
        if isinstance((y2 - y1) * (x2 - x1), float):
            return y1 + (x - x1) * (y2 - y1) / float(x2 - x1)
        else:
            return y1 + (x - x1) * Fraction(y2 - y1, x2 - x1)

    def calculate_x(self, y):
        """Calculate x for a given y in the segment."""
        # Is y between y1 and y2? Yes for a sweep line.
        x1 = self.pt1.x
        y1 = self.pt1.y
        x2 = self.pt2.x
        y2 = self.pt2.y
        if isinstance((x2 - x1) * (y2 - y1), float):
            return x1 + (y - y1) * (x2 - x1) / float(y2 - y1)
        else:
            return x1 + (y - y1) * Fraction(x2 - x1, y2 - y1)

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
