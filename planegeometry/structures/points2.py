#!/usr/bin/env python3

import math
from dataclasses import dataclass
from numbers import Real
from fractions import Fraction

@dataclass(repr=False,frozen=True,order=True)
class Point:
    x: Real = 0
    y: Real = 0

    def __repr__(self):
        """String representation of a point."""
        return "Point({0!r}, {1!r})".format(self.x, self.y)

    def __add__(self, other):            # point1 + point2
        """p + q, addition of points."""
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):           # point1 - point2
        """p - q, substraction of points."""
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        """The scalar product of two 2D vectors or number * point."""
        if isinstance(other, Point):      # point1 * point2 to iloczyn skalarny
            return (self.x * other.x + self.y * other.y)
        else:   # mnozenie przez liczbe (int, float, Fraction)
            return Point(self.x * other, self.y * other)

    __rmul__ = __mul__

    def copy(self):
        """Return a copy of a point."""
        return self     # points are immutable

    def cross(self, other):    # point1 x point2, iloczyn wektorowy 2D
        """The cross product of two 2D vectors, p.cross(q)."""
        return (self.x * other.y - self.y * other.x)

    # operatory jednoargumentowe
    def __pos__(self):  # +point
        """+point is the same point."""
        return self

    def __neg__(self):  # -point=(-1)*point
        """-point is (-1) * point."""
        return Point(-self.x, -self.y)

    def length(self):
        """The length of a point (2D vector)."""
        #return math.sqrt(self * self)
        return math.hypot(self.x, self.y)

    def __abs__(self):
        """abs(point), the length of a point (2D vector)."""
        return math.hypot(self.x, self.y)

    def alpha(self):
        """Funkcja monotoniczna wzgledem kata nachylenia.
        
        http://www.algorytm.org/geometria-obliczeniowa/porzadkowanie-wierzcholkow-wg-rosnacych-katow-nachylenia-ich-wektorow-wodzacych.html
        """
        if self.x == 0 and self.y == 0:
            #raise ValueError("alpha() not defined")
            return 0   # wygodna konwencja
        distance = abs(self.x) + abs(self.y)
        if isinstance(distance, float):
            if self.x >= 0 and self.y >= 0:  # I cwiartka
                return self.y / distance
            elif self.x < 0 and self.y >= 0:  # II cwiartka
                return 2.0 - (self.y / distance)
            elif self.x < 0 and self.y < 0:  # III cwiartka
                return 2.0 + (-self.y / distance)
            elif self.x >= 0 and self.y < 0:  # IV cwiartka
                return 4.0 - (-self.y / distance)
        else:
            if self.x >= 0 and self.y >= 0:  # I cwiartka
                return Fraction(self.y, distance)
            elif self.x < 0 and self.y >= 0:  # II cwiartka
                return 2 - Fraction(self.y, distance)
            elif self.x < 0 and self.y < 0:  # III cwiartka
                return 2 + Fraction(-self.y, distance)
            elif self.x >= 0 and self.y < 0:  # IV cwiartka
                return 4 - Fraction(-self.y, distance)

    def gnu(self):
        """Return a string for Gnuplot."""
        return 'set label "" at {},{} point pt 7 ps 0.5\n'.format(
            float(self.x), float(self.y))

# EOF
