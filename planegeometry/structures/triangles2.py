#!/usr/bin/env python3

from fractions import Fraction
from dataclasses import dataclass
from planegeometry.structures.points2 import Point
from planegeometry.structures.segments2 import Segment
from planegeometry.algorithms.geomtools import orientation

@dataclass(frozen=True,repr=False,eq=False)
class Triangle:
    pt1: Point
    pt2: Point
    pt3: Point

    def __post_init__(self):
        if not isinstance(self.pt1, Point):
            raise ValueError("not a Point")
        if not isinstance(self.pt2, Point):
            raise ValueError("not a Point")
        if not isinstance(self.pt3, Point):
            raise ValueError("not a Point")
        if (self.pt2 - self.pt1).cross(self.pt3 - self.pt1) == 0:
            raise ValueError("collinear points")

    def __repr__(self):
        """String representation of a triangle."""
        return "Triangle({0!r}, {1!r}, {2!r})".format(self.pt1, self.pt2, self.pt3)

    def copy(self):
        """Return a copy of a triangle."""
        return self

    def area(self):
        """Return the triangle area."""
        a = self.pt2 - self.pt1   # powstaja wektory
        b = self.pt3 - self.pt1
        return Fraction(1, 2) * abs(a.cross(b)) # iloczyn wektorowy

    def center(self):
        """Return the center of a triangle."""
        # Jakby szukanie srodka masy.
        return (self.pt1 + self.pt2 + self.pt3) * Fraction(1, 3)

    def make3(self):
        """Return three smaller triangles (division)."""
        pt4 = self.center()
        t1 = Triangle(self.pt1, self.pt2, pt4)
        t2 = Triangle(self.pt2, self.pt3, pt4)
        t3 = Triangle(self.pt3, self.pt1, pt4)
        return (t1, t2, t3)

    def make4(self):
        """Return four smaller triangles (division)."""
        pt4 = Fraction(1, 2) * (self.pt1 + self.pt2)
        pt5 = Fraction(1, 2) * (self.pt3 + self.pt2)
        pt6 = Fraction(1, 2) * (self.pt1 + self.pt3)
        t1 = Triangle(self.pt1, pt4, pt6)
        t2 = Triangle(self.pt2, pt5, pt4)
        t3 = Triangle(self.pt3, pt6, pt5)
        t4 = Triangle(pt4, pt5, pt6)
        return (t1, t2, t3, t4)

    def move(self, *arguments):   # przesuniecie o (x, y)
        """Return a new moved triangle."""
        if len(arguments) == 1 and isinstance(arguments[0], Point):
            pt1 = arguments[0]
            return Triangle(*((pt1 + pt2) for pt2 in (self.pt1, self.pt2, self.pt3)))
        elif len(arguments) == 2:
            pt1 = Point(*arguments)
            return Triangle(*((pt1 + pt2) for pt2 in (self.pt1, self.pt2, self.pt3)))
        else:
            raise ValueError("bad arguments")

    def __eq__(self, other):
        """Comparison of triangles (t1 == t2)."""
        return set([self.pt1, self.pt2, self.pt3]) == set([other.pt1, other.pt2, other.pt3])
        #return frozenset([self.pt1, self.pt2, self.pt3]) == frozenset([other.pt1, other.pt2, other.pt3])

    def __ne__(self, other):
        """Comparison of triangles (t1 != t2)."""
        return not self == other

    def __hash__(self):
        """Hashable triangles."""
        return hash(frozenset([self.pt1, self.pt2, self.pt3]))

    def __contains__(self, other):
        """Test if a figure is in a triangle."""
        if isinstance(other, Point):
            # Chyba wystarczy sprawdzic, czy punkt jest po tej samej
            # stronie boku, co przeciwlegly wierzcholek.
            # Trojkat jest domkniety, zawiera swoj brzeg.
            # Tu mozna tez uzyc oriented_area(), bo chodzi o znak.
            a12 = orientation(self.pt1, self.pt2, self.pt3)
            b12 = orientation(self.pt1, self.pt2, other)
            a23 = orientation(self.pt2, self.pt3, self.pt1)
            b23 = orientation(self.pt2, self.pt3, other)
            a31 = orientation(self.pt3, self.pt1, self.pt2)
            b31 = orientation(self.pt3, self.pt1, other)
            return (a12 * b12 >= 0) and (a23 * b23 >= 0) and (a31 * b31 >= 0)
        elif isinstance(other, Segment):
            return other.pt1 in self and other.pt2 in self
        else:
            raise ValueError()

    def orientation(self):
        """Triangle orientation."""
        return orientation(self.pt1, self.pt2, self.pt3)

    def gnu(self, visible=False):
        """Return a string for Gnuplot."""
        L = []
        if visible:
            L.append(self.pt1.gnu())
            L.append(self.pt2.gnu())
            L.append(self.pt3.gnu())
        L.append(Segment(self.pt1, self.pt2).gnu())
        L.append(Segment(self.pt1, self.pt3).gnu())
        L.append(Segment(self.pt2, self.pt3).gnu())
        return "".join(L)

    def common_segment(self, other):
        """Find the common segment of two triangles."""
        set1 = set([self.pt1, self.pt2, self.pt3])
        set2 = set([other.pt1, other.pt2, other.pt3])
        set3 = set1 & set2
        assert len(set3) == 2
        return Segment(set3.pop(), set3.pop())

    def third_node(self, pt1, pt2):
        """Find a third node of a triangle."""
        node_set = set([self.pt1, self.pt2, self.pt3])
        node_set.remove(pt1)
        node_set.remove(pt2)
        assert len(node_set) == 1
        return node_set.pop()

    def in_circumcircle(self, point):
        """Check if point is inside triangle circumcircle.
        
        Formula is taken from
        https://en.wikipedia.org/wiki/Delaunay_triangulation#Algorithms
        """
        # Preparing parameters for calculating det for 3x3 matrix.
        a = self.pt1 - point
        b = self.pt2 - point
        c = self.pt3 - point
        det = (a*a) * b.cross(c) - (b*b) * a.cross(c) + (c*c) * a.cross(b)
        if orientation(self.pt1, self.pt2, self.pt3) > 0:
            return det > 0
        else:
            return det < 0

    def circumcenter(self):
        """Return the circumcenter for the triangle.
        
        https://en.wikipedia.org/wiki/Circumscribed_circle#Circumcircle_equations
        """
        a, b, c = self.pt1, self.pt2, self.pt3
        #d = 2 * (b-a).cross(c-a)
        d = 2 * ( a.cross(b) - a.cross(c) + b.cross(c) )
        x = ((a*a)*(b.y - c.y) + (b*b)*(c.y - a.y) + (c*c)*(a.y - b.y))
        y = ((a*a)*(c.x - b.x) + (b*b)*(a.x - c.x) + (c*c)*(b.x - a.x))
        if isinstance((x+y+d), float):
            return Point(x / float(d), y / float(d))
        else:
            return Point(Fraction(x, d), Fraction(y, d))

    def iterpoints(self):
        """Generate all points on demand (counterclockwise)."""
        if orientation(self.pt1, self.pt2, self.pt3) > 0:
            yield self.pt1
            yield self.pt2
            yield self.pt3
        else:
            yield self.pt1
            yield self.pt3
            yield self.pt2

    def itersegments(self):
        """Generate all segments on demand (segment.pt1 < segment.pt2)."""
        if self.pt1 < self.pt2:
            yield Segment(self.pt1, self.pt2)
        else:
            yield Segment(self.pt2, self.pt1)
        if self.pt1 < self.pt3:
            yield Segment(self.pt1, self.pt3)
        else:
            yield Segment(self.pt3, self.pt1)
        if self.pt2 < self.pt3:
            yield Segment(self.pt2, self.pt3)
        else:
            yield Segment(self.pt3, self.pt2)

    def itersegments_oriented(self):
        """Generate oriented segments (the face is on the right)."""
        if orientation(self.pt1, self.pt2, self.pt3) > 0:
            yield Segment(self.pt1, self.pt3)
            yield Segment(self.pt3, self.pt2)
            yield Segment(self.pt2, self.pt1)
        else:
            yield Segment(self.pt1, self.pt2)
            yield Segment(self.pt2, self.pt3)
            yield Segment(self.pt3, self.pt1)

# EOF
