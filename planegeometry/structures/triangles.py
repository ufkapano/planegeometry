#!/usr/bin/python

from fractions import Fraction
from planegeometry.structures.points import Point
from planegeometry.structures.segments import Segment
from planegeometry.algorithms.geomtools import orientation

class Triangle:
    """The class defining a triangle."""

    def __init__(self, *arguments):
        """Make a triangle in the plane."""
        if len(arguments) == 0:
            self.pt1 = Point(0, 0)
            self.pt2 = Point(1, 0)
            self.pt3 = Point(0, 1)
        elif len(arguments) == 3:
            if not all(isinstance(pt, Point) for pt in arguments):
                raise ValueError("arguments are not points")
            self.pt1, self.pt2, self.pt3 = arguments
        elif len(arguments) == 6:
            x1, y1, x2, y2, x3, y3 = arguments
            self.pt1 = Point(x1, y1)
            self.pt2 = Point(x2, y2)
            self.pt3 = Point(x3, y3)
        else:
            raise ValueError("bad number of arguments")
        if (self.pt2 - self.pt1).cross(self.pt3 - self.pt1) == 0:
            raise ValueError("collinear points")

    def __repr__(self):
        """String representation of a triangle."""
        return "Triangle({0!r}, {1!r}, {2!r}, {3!r}, {4!r}, {5!r})".format(
            self.pt1.x, self.pt1.y, 
            self.pt2.x, self.pt2.y, 
            self.pt3.x, self.pt3.y)

    def copy(self):
        """Return a copy of a triangle."""
        return Triangle(self.pt1, self.pt2, self.pt3)

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
        """Test if a point is in a triangle."""
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
        else:
            raise ValueError("not a point")

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

# EOF
