#!/usr/bin/python
#
# Polygon.orientation() based on the C++ code from
# http://geomalgorithms.com/a01-_area.html

try:
    integer_types = (int, long)
except NameError:   # Python 3
    integer_types = (int,)
    xrange = range

from planegeometry.structures.points import Point
from planegeometry.structures.segments import Segment
from planegeometry.algorithms.geomtools import orientation

class Polygon:
    """The class defining a polygon."""

    def __init__(self, *arguments):
        """Make a polygon in the plane."""
        if all(isinstance(pt, Point) for pt in arguments):
            if len(arguments) < 3:
                raise ValueError("less then 3 points")
            self.point_list = list(arguments) # bedziemy rozszerzac
        elif len(arguments) % 2 == 0 and len(arguments) >= 6:
            self.point_list = []
            i = 0
            while i < len(arguments):
                self.point_list.append(Point(arguments[i], arguments[i+1]))
                i += 2
        else:
            raise ValueError("bad arguments")
        if len(self.point_list) != len(set(self.point_list)):
            raise ValueError("repeated points")

    def __repr__(self):
        """String representation of a polygon."""
        return "Polygon({})".format(
        ", ".join(repr(pt) for pt in self.point_list))

    def __eq__(self, other):
        """Comparison of polygones (polygon1 == polygon2)."""
        return self.point_list == other.point_list

    def __ne__(self, other):
        """Comparison of polygones (polygon1 != polygon2)."""
        return not self == other

    def move(self, *arguments):   # przesuniecie o (x, y)
        """Return a new moved polygon."""
        if len(arguments) == 1 and isinstance(arguments[0], Point):
            pt1 = arguments[0]
            return Polygon(*((pt1 + pt2) for pt2 in self.point_list))
        elif len(arguments) == 2:
            pt1 = Point(*arguments)
            return Polygon(*((pt1 + pt2) for pt2 in self.point_list))
        else:
            raise ValueError("bad arguments")

    def copy(self):
        """Return a copy of a polygon."""
        return Polygon(*self.point_list)

    def orientation(self, test_is_simple=True):
        """Simple polygon orientation."""
        if test_is_simple:   # mozemy pominac test
            if not self.is_simple():
                # Nie mamy wersji dla wielokata zlozonego.
                raise ValueError("polygon is not simple")
        # First find rightmost lowest vertex of the polygon.
        rmin = 0
        xmin = self.point_list[0].x
        ymin = self.point_list[0].y
        for i in xrange(1, len(self.point_list)):
            if self.point_list[i].y > ymin:
                continue
            if self.point_list[i].y == ymin:
                if self.point_list[i].x < xmin:
                    continue
            rmin = i
            xmin = self.point_list[i].x
            ymin = self.point_list[i].y
        # Test orientation at the rmin vertex.
        if rmin == 0:
            return orientation(self.point_list[-1],
                               self.point_list[0],
                               self.point_list[1])
        elif rmin == len(self.point_list)-1:
            return orientation(self.point_list[-2],
                               self.point_list[-1],
                               self.point_list[0])
        else:
            return orientation(self.point_list[rmin-1],
                               self.point_list[rmin],
                               self.point_list[rmin+1])

    def __contains__(self, other):
        """Test if a point is in a polygon."""
        if isinstance(other, Point):
            # cn = crossing_number(self, other)
            # return cn % 2 != 0
            wn = winding_number(self, other)
            return wn != 0
        else:
            raise ValueError("not a point")

    def is_simple(self):
        """Test if a polygon is simple in O(n^2) time (slow)."""
        n = len(self.point_list)
        for i in xrange(n):
            for j in xrange(2, n-1): # krawedz niesasiednia
                k = (i+j) % n
                if k < i:   # bylo sprawdzone
                    continue
                segment1 = Segment(self.point_list[i], self.point_list[(i+1) % n])
                segment2 = Segment(self.point_list[k], self.point_list[(k+1) % n])
                if segment1.intersect(segment2):
                    return False
        return True

    def is_convex(self, test_is_simple=True):
        """Test if a polygon is convex."""
        if test_is_simple:   # mozemy pominac test
            if not self.is_simple():
                # Nie mamy wersji dla wielokata zlozonego.
                raise ValueError("polygon is not simple")
        # Obliczamy orientacje.
        orient = self.orientation()
        # Sprawdzamy katy wewnetrzne.
        n = len(self.point_list)
        for i in xrange(n):
            pt1 = self.point_list[i]
            pt2 = self.point_list[(i+1) % n]
            pt3 = self.point_list[(i+2) % n]
            if orientation(pt1, pt2, pt3) * orient < 0:
                return False
        return True

    def is_rhombus(self):
        """Test if a polygon is a rhombus."""
        raise NotImplementedError

    def is_rectangle(self):
        """Test if a polygon is a rectangle."""
        raise NotImplementedError

    def is_square(self):
        """Test if a polygon is a square."""
        return self.is_rhombus() and self.is_rectangle()

    def itersegments(self):
        """Generate all segments on demand (segment.pt1 < segment.pt2)."""
        n = len(self.point_list)
        for i in xrange(n):
            pt1 = self.point_list[i]
            pt2 = self.point_list[(i + 1) % n]
            if pt1 < pt2:
                yield Segment(pt1, pt2)
            else:
                yield Segment(pt2, pt1)

    def __hash__(self):
        """Hashable polygons."""
        return hash(frozenset(self.point_list))


def bounding_box(point_list):
    """Return the bounding box for a point set."""
    xmin = xmax = point_list[0].x
    ymin = ymax = point_list[0].y
    for point in point_list:
        xmin = min(point.x, xmin)
        xmax = max(point.x, xmax)
        ymin = min(point.y, ymin)
        ymax = max(point.y, ymax)
    # One can use a divide-and-conquer algorithm to find pairs
    # (xmin, xmax) and (ymin, ymax) at the same time.
    return Polygon(xmin, ymin, xmax, ymin, xmax, ymax, xmin, ymax)


def crossing_number(polygon, point):
    """Return the crossing number for a point."""
    cn = 0
    n = len(polygon.point_list)
    for i in xrange(n):
        a = polygon.point_list[i]
        b = polygon.point_list[(i+1) % n]
        if a.y <= point.y:
            if b.y > point.y and orientation(a, b, point) > 0:
                cn += 1   # upward edge
        else:   # a.y > point.y
            if b.y <= point.y and orientation(a, b, point) < 0:
                cn += 1   # downward edge
    return cn


def crossing_number2(polygon, point):
    """Return the crossing number for a point."""
    cn = 0
    n = len(polygon.point_list)
    for i in xrange(n):
        a = polygon.point_list[i]
        b = polygon.point_list[(i+1) % n]
        if ((a.y <= point.y and b.y > point.y) or 
            (a.y > point.y and b.y <= point.y)): # upward or downward edge
            vt = float(point.y - a.y) / (b.y - a.y)
            xmid = a.x + vt * (b.x - a.x)
            if point.x < xmid:
                cn += 1
    return cn


def winding_number(polygon, point):
    """Return the winding number for a point."""
    wn = 0
    n = len(polygon.point_list)
    for i in xrange(n):
        a = polygon.point_list[i]
        b = polygon.point_list[(i+1) % n]
        if a.y <= point.y:
            if b.y > point.y and orientation(a, b, point) > 0:
                wn += 1   # upward edge
        else:   # a.y > point.y
            if b.y <= point.y and orientation(a, b, point) < 0:
                wn -= 1   # downward edge
    return wn

# EOF
