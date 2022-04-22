#!/usr/bin/env python3

import math
from functools import total_ordering
from planegeometry.structures.points import Point

@total_ordering
class Circle:
    """The class defining a circle."""

    def __init__(self, *arguments):
        """Make a circle in the plane."""
        if len(arguments) == 0:
            self.pt = Point(0, 0)
            self.radius = 1
        elif len(arguments) == 2:
            self.pt, self.radius = arguments
            if not isinstance(self.pt, Point):
                raise ValueError("the first argument is not a point")
        elif len(arguments) == 3:
            x, y, self.radius = arguments
            self.pt = Point(x, y)
        else:
            raise ValueError("bad number of arguments")
        if self.radius < 0:
            raise ValueError("radius negative")

    def __repr__(self):
        """String representation of a circle."""
        return "Circle({0!r}, {1!r}, {2!r})".format(
            self.pt.x, self.pt.y, self.radius)

    def copy(self):
        """Return a copy of a circle."""
        return Circle(self.pt, self.radius)

    def center(self):
        """Return the center of a circle."""
        return self.pt

    def area(self):
        """Return the circle area."""
        return math.pi * self.radius * self.radius

    def move(self, *arguments):   # przesuniecie o (x, y)
        """Return a new moved circle."""
        if len(arguments) == 1 and isinstance(arguments[0], Point):
            pt = arguments[0]
            return Circle(self.pt.x + pt.x, self.pt.y + pt.y, self.radius)
        elif len(arguments) == 2:
            x, y = arguments
            return Circle(self.pt.x + x, self.pt.y + y, self.radius)
        else:
            raise ValueError("bad arguments")

    def __eq__(self, other):
        """Comparison of circles (c1 == c2)."""
        return self.pt == other.pt and self.radius == other.radius

    def __ne__(self, other):
        """Comparison of circles (c1 != c2)."""
        return not self == other

    def __lt__(self, other):
        """Comparison of circles (c1 < c2)."""
        return (self.pt.x, self.pt.y, self.radius) < (
            other.pt.x, other.pt.y, other.radius)

    def __hash__(self):
        """Hashable circles."""
        #return hash((self.pt, self.radius))
        return hash((self.pt.x, self.pt.y, self.radius))

    def cover(self, other):
        """Return the smallest circle covering given circles."""
        # Trzeba znalezc srodek i promien.
        if self.pt == other.pt:
            radius = max(self.radius, other.radius)
            return Circle(self.pt, radius)
            # return self if self.radius > other.radius else other
        if self.radius <= other.radius:   # c1 to mniejszy okrag
            c1, c2 = self, other
        else:
            c1, c2 = other, self
        # Teraz c1 to mniejszy okrag.
        distance = (c1.pt - c2.pt).length()
        if distance + c1.radius <= c2.radius: # c1 in c2
            return c2.copy()
        radius = 0.5 * (distance + c1.radius + c2.radius)
        # f(t) = c1.pt + (c2.pt - c1.pt) * t
        t = (radius - c1.radius) / distance
        #t = 0.5 + (c2.radius - c1.radius)/(2.0 * distance)
        pt = c1.pt + (c2.pt - c1.pt) * t
        return Circle(pt, radius)

    def __contains__(self, other):
        """Test if a point is in a circle."""
        if isinstance(other, Point):
            #distance = (self.pt - other).length()
            #return distance <= self.radius
            # Chce unikac pierwiastkowania i liczb float.
            vector = self.pt - other
            return vector * vector <= self.radius * self.radius
        else:
            raise ValueError()

    def gnu(self, visible=False):
        """Return a string for Gnuplot."""
        L = []
        if visible:
            L.append(self.pt.gnu())
        L.append('set object circle at {},{} size {} fc rgb "black" fs empty\n'.format(
            float(self.pt.x), float(self.pt.y), float(self.radius)))
        return "".join(L)

# EOF
