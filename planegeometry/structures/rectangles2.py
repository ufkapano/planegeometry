#!/usr/bin/env python3

from fractions import Fraction
from dataclasses import dataclass
from planegeometry.structures.points2 import Point
from planegeometry.structures.segments2 import Segment
from planegeometry.structures.circles import Circle

@dataclass(frozen=True,order=True,repr=False)
class Rectangle:
    pt1: Point
    pt2: Point

    def __post_init__(self):
        if not isinstance(self.pt1, Point):
            raise ValueError("not a Point")
        if not isinstance(self.pt2, Point):
            raise ValueError("not a Point")
        # Nie chcemy prostokatow o polu zerowym.
        if self.pt1.x >= self.pt2.x:
            raise ValueError("x1 >= x2")
        if self.pt1.y >= self.pt2.y:
            raise ValueError("y1 >= y2")

    def __repr__(self):
        """String representation of a rectangle."""
        return "Rectangle({0!r}, {1!r})".format(self.pt1, self.pt2)

    def copy(self):   # zwraca nowa instancje
        """Return a copy of a rectangle."""
        return self

    def center(self):
        """Return the center of a rectangle."""
        return (self.pt1 + self.pt2) * Fraction(1, 2)

    def area(self):
        """Return the rectangle area."""
        return abs((self.pt2.y - self.pt1.y) * (self.pt2.x - self.pt1.x))

    def make4(self):
        """Return four smaller rectangles (division)."""
        pt3 = self.center()
        tl = Rectangle(Point(self.pt1.x, pt3.y), Point(pt3.x, self.pt2.y)) # top left
        tr = Rectangle(pt3, self.pt2) # top right
        bl = Rectangle(self.pt1, pt3) # bottom left
        br = Rectangle(Point(pt3.x, self.pt1.y), Point(self.pt2.x, pt3.y)) # bottom right
        # Kolejnosc dopasowana do QuadTree.
        return (tl, tr, bl, br)

    def cover(self, other):
        """Return the smallest rectangle covering given rectangles."""
        x1 = min(self.pt1.x, other.pt1.x)
        y1 = min(self.pt1.y, other.pt1.y)
        x2 = max(self.pt2.x, other.pt2.x)
        y2 = max(self.pt2.y, other.pt2.y)
        return Rectangle(Point(x1, y1), Point(x2, y2))

    def intersection(self, other):
        """Return the intersection of given rectangles."""
        x1 = max(self.pt1.x, other.pt1.x)
        y1 = max(self.pt1.y, other.pt1.y)
        x2 = min(self.pt2.x, other.pt2.x)
        y2 = min(self.pt2.y, other.pt2.y)
        return Rectangle(Point(x1, y1), Point(x2, y2))

    def move(self, *arguments):   # przesuniecie o (x, y)
        """Return a new moved rectangle."""
        if len(arguments) == 1 and isinstance(arguments[0], Point):
            pt = arguments[0]
            x1 = self.pt1.x + pt.x
            y1 = self.pt1.y + pt.y
            x2 = self.pt2.x + pt.x
            y2 = self.pt2.y + pt.y
            return Rectangle(Point(x1, y1), Point(x2, y2))
        elif len(arguments) == 2:
            x, y = arguments
            x1 = self.pt1.x + x
            y1 = self.pt1.y + y
            x2 = self.pt2.x + x
            y2 = self.pt2.y + y
            return Rectangle(Point(x1, y1), Point(x2, y2))
        else:
            raise ValueError("bad arguments")

    def __contains__(self, other):
        """Test if a point is in a rectangle."""
        if isinstance(other, Point):
            in_x = self.pt1.x <= other.x <= self.pt2.x
            in_y = self.pt1.y <= other.y <= self.pt2.y
            return in_x and in_y
        elif isinstance(other, Segment):
            return other.pt1 in self and other.pt2 in self
        elif isinstance(other, Circle):
            in1 = self.pt1.x + other.radius <= other.pt.x
            in2 = other.pt.x + other.radius <= self.pt2.x
            in3 = self.pt1.y + other.radius <= other.pt.y
            in4 = other.pt.y + other.radius <= self.pt2.y
            return in1 and in2 and in3 and in4
        else:
            raise ValueError()

    def is_square(self):
        """Test if a rectangle is a square."""
        return (self.pt2.x - self.pt1.x) == (self.pt2.y - self.pt1.y)

    def iterpoints(self):
        """Generate all points on demand (counterclockwise)."""
        yield self.pt1                        # bottom left
        yield Point(self.pt2.x, self.pt1.y)   # bottom right
        yield self.pt2                        # top right
        yield Point(self.pt1.x, self.pt2.y)   # top left

    def itersegments(self):
        """Generate all segments on demand (segment.pt1 < segment.pt2)."""
        yield Segment(self.pt1, Point(self.pt2.x, self.pt1.y)) # bottom
        yield Segment(self.pt1, Point(self.pt1.x, self.pt2.y)) # left
        yield Segment(Point(self.pt1.x, self.pt2.y), self.pt2) # top
        yield Segment(Point(self.pt2.x, self.pt1.y), self.pt2) # right

    def itersegments_oriented(self):
        """Generate oriented segments (the face is on the right)."""
        yield Segment(self.pt1, Point(self.pt1.x, self.pt2.y)) # left
        yield Segment(Point(self.pt1.x, self.pt2.y), self.pt2) # top
        yield Segment(self.pt2, Point(self.pt2.x, self.pt1.y)) # right
        yield Segment(Point(self.pt2.x, self.pt1.y), self.pt1) # bottom

    def gnu(self, visible=False):
        """Return a string for Gnuplot."""
        L = []
        if visible:
            pt3 = Point(self.pt1.x, self.pt2.y)   # top left
            pt4 = Point(self.pt2.x, self.pt1.y)   # bottom right
            L.append(self.pt1.gnu())
            L.append(self.pt2.gnu())
            L.append(pt3.gnu())
            L.append(pt4.gnu())
        L.append('set object rectangle from {},{} to {},{} fs empty\n'.format(
            float(self.pt1.x), float(self.pt1.y),
            float(self.pt2.x), float(self.pt2.y)))
        return "".join(L)


def bounding_box(point_list):
    """Return the bounding box for a point set."""
    xmin = xmax = point_list[0].x
    ymin = ymax = point_list[0].y
    for point in point_list:   # single loop over points
        xmin = min(point.x, xmin)
        xmax = max(point.x, xmax)
        ymin = min(point.y, ymin)
        ymax = max(point.y, ymax)
    # One can use a divide-and-conquer algorithm to find pairs
    # (xmin, xmax) and (ymin, ymax) at the same time.
    return Rectangle(Point(xmin, ymin), Point(xmax, ymax))

# EOF
